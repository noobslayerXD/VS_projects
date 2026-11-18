"""Test double for the emodeconnection package (NOT EMode).

It accepts exactly the keyword arguments that the EMode 1.0.8 documentation lists
(unknown keywords raise, as EMode does since 1.0.7), applies the documented
conventions, and answers straight solves with the open-source EMpy solver. It lets
the Python logic of solver_emode.py be exercised without an EMode licence. It says
nothing about EMode's numerical accuracy.

Documented conventions it enforces:
  - origin at the horizontal centre of the bottom wall; x in [-W/2, W/2], y in [0, H]
  - windows a whole even number of cells (EMode would grow them and warn)
  - 'TE' fold dropped (BC falls back to '00') unless the structure is centred on y = H/2
  - bend_radius measured at x = 0 and larger than W/2; n_eff and loss_dB_per_m
    referenced to that radius
  - reset(kind) only 'shapes', 'settings' or 'all'; settings persist between solves
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from solver_empy import EMpySolver, n_sio2  # noqa: E402

CONSTRUCTOR = {"simulation_name", "license_type", "clear", "save_path", "verbose", "roaming",
               "open_existing", "new_name", "priority", "emode_cmd", "force_open", "save"}
SETTINGS_DEFAULTS = dict(
    profile="_default", wavelength=1550, frequency=None, excitation=None, simulation_name="emode",
    propagation_resolution=None, window_width=None, window_height=None,
    x_resolution="auto", y_resolution="auto", boundary_condition="auto",
    pml_NSEW_bool=[0, 0, 0, 0], num_pml_layers=None, pml_thickness=0, pml_order=3,
    pml_reflection=1e-8, pml_kappa_max=7, pml_alpha_max=0, remove_pml_modes_bool=False,
    pml_seed_bool=False, num_modes=1, max_effective_index=0, tolerance=1e-12, field_to_solve="Et",
    solver="default", solver_threads=0, solve_workers="auto", sparse_solver="auto",
    bend_radius=0, bend_method="cylindrical", background_material="Vacuum",
    expansion_resolution=20, expansion_size=0, subpixel_avg=True, subpixel_tensor="auto",
    generate_chi2=False, include_heat=True, include_scattering=False, error_reporting=True,
    fem_order=2, fem_points_per_wavelength=3, fem_min_angle=30, fem_smooth_passes=3,
    fem_refine_fraction=0.5, fem_max_refinements=3, fem_neff_tolerance=1e-6, fem_max_dofs=2000000,
    fem_mesh_wavelength=0)
SHAPE = {"profile", "name", "material", "fill_material", "loss_dB_per_m", "shape_type", "vertices",
         "width", "height", "position", "sidewall_angle", "mask", "mask_offset", "tone", "etch_depth",
         "correlation_length", "roughness_rms", "roughness_field_side", "priority", "fem_resolution",
         "current", "voltage", "heat_only"}
FDM_ARGS = {"profile", "section", "propagation_distance", "mode_filter", "fLanczos", "solve_type",
            "include_heat", "include_static", "scattering", "verbose", "simulation_name"}
BOUNDARY = {"auto", "TE", "TM", "TE-h", "TM-h", "TE-v", "TM-v"} | {a + b for a in "0SA" for b in "0SA"}
CALLS = []                                         # log of calls, for the test script
SHIFT = 0.05                                       # bend shift factor; the test raises it


def _check(kw, allowed, fn):
    bad = set(kw) - allowed
    if bad:
        raise TypeError(f"{fn}() got unknown keyword arguments {sorted(bad)}")


class MaterialProperties:
    def __init__(self, n=1.0, mu=1.0):
        self.n, self.mu = n, mu


class EMode:
    def __init__(self, **kw):
        _check(kw, CONSTRUCTOR, "EMode")
        assert kw.get("license_type", "default") in ("2d", "3d", "default")
        self.s, self.shapes, self.out = dict(SETTINGS_DEFAULTS), {}, {}
        CALLS.append(("EMode", kw))

    def settings(self, **kw):
        _check(kw, set(SETTINGS_DEFAULTS), "settings")
        if "boundary_condition" in kw:
            assert kw["boundary_condition"] in BOUNDARY, kw["boundary_condition"]
        self.s.update(kw)
        CALLS.append(("settings", kw))

    def shape(self, **kw):
        _check(kw, SHAPE, "shape")
        self.shapes.setdefault(kw.get("name", f"shape{len(self.shapes)}"), {}).update(kw)

    def reset(self, kind="shapes", profile="_default", simulation_name="emode"):
        if kind not in ("shapes", "settings", "all"):
            raise ValueError(f"unknown kind {kind!r}")
        self.shapes = {}
        if kind in ("settings", "all"):
            self.s = dict(SETTINGS_DEFAULTS)
        self.out = {}

    def refractive_index(self, material, wavelength=1550, reference=False):
        n = material.n if isinstance(material, MaterialProperties) else {"SiO2": float(n_sio2(wavelength))}[material]
        return [n, n, n]

    def FDM(self, **kw):
        _check(kw, FDM_ARGS, "FDM")
        s, res = self.s, self.s["x_resolution"]
        W, H = s["window_width"], s["window_height"]
        assert isinstance(res, (int, float)) and s["boundary_condition"] != "auto"
        for L in (W, H):                                  # whole even number of cells
            assert abs(L / res / 2 - round(L / res / 2)) < 1e-9, f"window {L} not an even cell count at {res}"
        cores, h = [], None
        for v in self.shapes.values():
            x, y = v["position"]
            assert -W / 2 <= x - v["width"] / 2 and x + v["width"] / 2 <= W / 2, "core outside window in x"
            assert 0 <= y - v["height"] / 2 and y + v["height"] / 2 <= H, "core outside window in y"
            cores.append((x, v["width"]))
            h = v["height"]
        centred = all(abs(v["position"][1] - H / 2) < 1e-9 for v in self.shapes.values())
        bc = s["boundary_condition"]
        self.out["BC"] = bc if (bc not in ("TE", "TM") or centred) else "00"

        mat = next(iter(self.shapes.values()))["material"]
        clad = s["background_material"]
        fixed = (mat.n, clad.n) if isinstance(mat, MaterialProperties) else None
        side = min(1000, W / 2 - max(abs(c) + w / 2 for c, w in cores))
        solver = EMpySolver(resolution=res, h_si=h, side_margin=side, vert_margin=min(800, (H - h) / 2))
        solver.fixed_indices = fixed

        if s["bend_radius"]:
            R_set = s["bend_radius"]
            assert R_set > W / 2, "bend_radius must exceed window_width/2"
            assert s["pml_NSEW_bool"][2] == 1, "the outer (east) wall needs a PML"
            (xc, w), = cores
            R_core = R_set + xc                           # xc < 0: core west of the window centre
            neff, te = solver.modes([(0.0, w)], s["wavelength"], 2)
            n_straight = float(neff[te > 0.5][0])
            n_true = n_straight * (1 + SHIFT * w / R_core)  # made-up outward shift of the mode
            loss_true = 1e3 * math.exp(-R_core / 2000.0)  # made-up bend loss, dB/m along the core
            n_win, loss_win = n_true * R_core / R_set, loss_true * R_core / R_set
            if not s["pml_seed_bool"] and s["max_effective_index"] and s["max_effective_index"] < n_win:
                raise RuntimeError("max_effective_index below the guided mode: no mode found")
            # A PML mode first, to test that the caller skips it.
            self.out.update(effective_index=[1.30, n_win], TE_fraction=[0.6, 0.98],
                            loss_dB_per_m=[5e6, loss_win], PML_indices=[0])
            self.truth = dict(n_core=n_true, loss_core=loss_true)
        else:
            assert s["pml_NSEW_bool"] == [0, 0, 0, 0] and s["max_effective_index"] == 0
            neff, te = solver.modes(cores, s["wavelength"], s["num_modes"])
            self.out.update(effective_index=list(neff[::-1]), TE_fraction=list(te[::-1]),
                            loss_dB_per_m=[0.0] * len(neff))   # unsorted on purpose
        CALLS.append(("FDM", dict(BC=self.out["BC"], W=W, H=H, res=res)))
        return {"n_eff_tilde": self.out["effective_index"], "TE_fraction": self.out["TE_fraction"]}

    def get(self, key, profile="_default", simulation_name="emode"):
        if key == "emode_version":
            return "mock"
        return self.out[key]

    def close(self, save=True, save_all_fields=False, file_type="eph", simulation_name="emode"):
        CALLS.append(("close", {}))
