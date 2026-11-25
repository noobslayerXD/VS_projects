"""Test double for the emodeconnection package. It is NOT EMode and NOT a mode solver.

It accepts exactly the keyword arguments that the EMode 1.0.8 documentation lists
(unknown keywords raise, as EMode does since 1.0.7) and applies the documented
conventions, so that the Python of solver_emode.py and adc_study.py can be run
without an EMode licence. The numbers it returns come from the made-up coupled-mode
model below: smooth, phase-matchable and self-consistent, but not physical results.
None of the study's results come from it.

Documented conventions it enforces:
  - origin at the horizontal centre of the bottom wall; x in [-W/2, W/2], y in [0, H]
  - windows a whole even number of cells (EMode would grow them and warn)
  - 'TE' fold dropped (BC falls back to '00') unless the structure is centred on y = H/2
  - bend_radius measured at x = 0 and larger than W/2; n_eff and loss_dB_per_m
    referenced to that radius
  - reset(kind) only 'shapes', 'settings' or 'all'; settings persist between solves
  - after a straight solve, get_grid() gives a Grid (x centred, y from the bottom wall,
    cell centres) and get_fields(key) a Field: an array [field, mode, x, y] with
    field_names, modes in the same order as get('effective_index'), each mode scaled
    to carry 1 W: (1/2) Re sum of (E x H*).z over the cells = 1. Reading x, y or a
    field through get() raises, as those keys are deprecated in EMode.

Made-up model (only for testing):
  - a strip of width W has guided modes p = 0, 1, 2, ... of each polarization with
        n_p^2 = n_slab^2 - ((p + 1) lambda / (2 (W + D)))^2,   D = 100 nm,
    n_slab = n_clad + 0.69 (n_core - n_clad) for TE and + 0.27 (n_core - n_clad) for TM,
    kept while n_p > n_clad;
  - its field is a Hermite-Gaussian with p nodes across x (sigma = (W + D)/3) and a
    Gaussian across y (sigma = 150 nm), along x for TE and along y for TM, with
    H = n_eff z x E, so that every mode carries positive power (scaled to 1 W);
  - modes of the same polarization in two strips couple with strength
        c = 0.02 exp(-(g - 200 nm) / 100 nm)
    (g the gap), signed like the product of the two fields in the middle of the gap,
    and the supermodes are the eigenvectors of diag(n) + C;
  - unguided "box" modes with zero fields fill the list up to num_modes.
"""
import math

import numpy as np

CONSTRUCTOR = {"simulation_name", "license_type", "clear", "save_path", "verbose", "roaming",
               "open_existing", "new_name", "priority", "emode_cmd", "force_open", "save"}
SETTINGS_DEFAULTS = {
    "profile": "_default", "wavelength": 1550, "frequency": None, "excitation": None, "simulation_name": "emode",
    "propagation_resolution": None, "window_width": None, "window_height": None,
    "x_resolution": "auto", "y_resolution": "auto", "boundary_condition": "auto",
    "pml_NSEW_bool": [0, 0, 0, 0], "num_pml_layers": None, "pml_thickness": 0, "pml_order": 3,
    "pml_reflection": 1e-8, "pml_kappa_max": 7, "pml_alpha_max": 0, "remove_pml_modes_bool": False,
    "pml_seed_bool": False, "num_modes": 1, "max_effective_index": 0, "tolerance": 1e-12, "field_to_solve": "Et",
    "solver": "default", "solver_threads": 0, "solve_workers": "auto", "sparse_solver": "auto",
    "bend_radius": 0, "bend_method": "cylindrical", "background_material": "Vacuum",
    "expansion_resolution": 20, "expansion_size": 0, "subpixel_avg": True, "subpixel_tensor": "auto",
    "generate_chi2": False, "include_heat": True, "include_scattering": False, "error_reporting": True,
    "fem_order": 2, "fem_points_per_wavelength": 3, "fem_min_angle": 30, "fem_smooth_passes": 3,
    "fem_refine_fraction": 0.5, "fem_max_refinements": 3, "fem_neff_tolerance": 1e-6, "fem_max_dofs": 2000000,
    "fem_mesh_wavelength": 0}
SHAPE = {"profile", "name", "material", "fill_material", "loss_dB_per_m", "shape_type", "vertices",
         "width", "height", "position", "sidewall_angle", "mask", "mask_offset", "tone", "etch_depth",
         "correlation_length", "roughness_rms", "roughness_field_side", "priority", "fem_resolution",
         "current", "voltage", "heat_only"}
FDM_ARGS = {"profile", "section", "propagation_distance", "mode_filter", "fLanczos", "solve_type",
            "include_heat", "include_static", "scattering", "verbose", "simulation_name"}
BOUNDARY = {"auto", "TE", "TM", "TE-h", "TM-h", "TE-v", "TM-v"} | {a + b for a in "0SA" for b in "0SA"}
DEPRECATED = {"x", "y", "Ex", "Ey", "Ez", "Hx", "Hy", "Hz", "Sx", "Sy", "Sz"}
GRID_ARGS = {"include_expand", "include_pml", "unfold", "profile", "simulation_name"}

CALLS = []                 # log of calls, for the test scripts
SHIFT = 0.05               # bend: made-up outward shift of the mode; a test raises it

N_SI = 3.476               # made-up silicon index (database name 'Si')
D_PEN = 100.0              # nm, made-up penetration added to the strip width
SIGMA_Y = 150.0            # nm, vertical width of the made-up fields
C0, G0, L_GAP = 0.02, 200.0, 100.0   # coupling c = C0 exp(-(g - G0) / L_GAP), index units


def n_sio2(wl_nm):
    """Fused silica (Malitson Sellmeier fit)."""
    L2 = (wl_nm * 1e-3) ** 2
    return math.sqrt(1 + 0.6961663 * L2 / (L2 - 0.0684043**2) + 0.4079426 * L2 / (L2 - 0.1162414**2)
                     + 0.8974794 * L2 / (L2 - 9.896161**2))


def strip_modes(width, n_core, n_clad, wl):
    """Guided modes of one strip in the made-up model: list of (n_eff, polarization, order)."""
    out = []
    for pol, frac in (("TE", 0.69), ("TM", 0.27)):
        n_slab = n_clad + frac * (n_core - n_clad)
        p = 0
        while True:
            n2 = n_slab**2 - ((p + 1) * wl / (2 * (width + D_PEN)))**2
            if n2 <= n_clad**2:
                break
            out.append((math.sqrt(n2), pol, p))
            p += 1
    return out


def _profile(x, y, xc, width, order):
    """Hermite-Gaussian with `order` nodes across x, Gaussian across y; unit L2 norm."""
    u = (x - xc) / ((width + D_PEN) / 3)
    fx = np.polynomial.hermite.hermval(u, [0] * order + [1]) * np.exp(-u**2 / 2)
    f = np.outer(fx, np.exp(-(y / SIGMA_Y)**2 / 2))
    return f / np.sqrt((f**2).sum())


def _check(kw, allowed, fn):
    bad = set(kw) - allowed
    if bad:
        raise TypeError(f"{fn}() got unknown keyword arguments {sorted(bad)}")


class MaterialProperties:
    def __init__(self, n=1.0, mu=1.0):
        self.n, self.mu = n, mu


class Grid:
    """As EMode's Grid: the cell-centre x and y of the last solve."""
    def __init__(self, x, y, is_pml=False, is_expanded=False, is_bc=True):
        self.x, self.y, self.is_pml, self.is_expanded, self.is_bc = x, y, is_pml, is_expanded, is_bc


class Field:
    """As EMode's Field: an array [field, mode, x, y], its field names, the number of modes
    and the grid."""
    def __init__(self, field, field_names, num_modes, grid):
        self.field, self.field_names, self.num_modes, self.grid = field, field_names, num_modes, grid


def _index(material, wl):
    if isinstance(material, MaterialProperties):
        return float(material.n)
    return {"Si": N_SI, "SiO2": n_sio2(wl)}[material]


class EMode:
    def __init__(self, **kw):
        _check(kw, CONSTRUCTOR, "EMode")
        assert kw.get("license_type", "default") in ("2d", "3d", "default")
        self.s, self.shapes, self.out, self.fields = dict(SETTINGS_DEFAULTS), {}, {}, {}
        self.materials = None
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
        self.out, self.fields = {}, {}

    def refractive_index(self, material, wavelength=1550, reference=False):
        n = _index(material, wavelength)
        return [n, n, n]

    def FDM(self, **kw):
        _check(kw, FDM_ARGS, "FDM")
        s, res = self.s, self.s["x_resolution"]
        W, H, wl = s["window_width"], s["window_height"], s["wavelength"]
        assert isinstance(res, (int, float)) and s["boundary_condition"] != "auto"
        for L in (W, H):                                  # whole even number of cells
            assert abs(L / res / 2 - round(L / res / 2)) < 1e-9, f"window {L} not an even cell count at {res}"
        cores = []
        for v in self.shapes.values():
            x, y = v["position"]
            assert -W / 2 <= x - v["width"] / 2 and x + v["width"] / 2 <= W / 2, "core outside window in x"
            assert 0 <= y - v["height"] / 2 and y + v["height"] / 2 <= H, "core outside window in y"
            cores.append((x, v["width"]))
        centred = all(abs(v["position"][1] - H / 2) < 1e-9 for v in self.shapes.values())
        bc = s["boundary_condition"]
        self.out["BC"] = bc if (bc not in ("TE", "TM") or centred) else "00"
        n_core = _index(next(iter(self.shapes.values()))["material"], wl)
        n_clad = _index(s["background_material"], wl)
        self.materials = (n_core, n_clad)

        if s["bend_radius"]:
            R_set = s["bend_radius"]
            assert R_set > W / 2, "bend_radius must exceed window_width/2"
            assert s["pml_NSEW_bool"][2] == 1, "the outer (east) wall needs a PML"
            (xc, w), = cores
            R_core = R_set + xc                           # xc < 0: core west of the window centre
            n_straight = strip_modes(w, n_core, n_clad, wl)[0][0]
            n_true = n_straight * (1 + SHIFT * w / R_core)  # made-up outward shift of the mode
            loss_true = 1e3 * math.exp(-R_core / 2000.0)  # made-up bend loss, dB/m along the core
            n_win, loss_win = n_true * R_core / R_set, loss_true * R_core / R_set
            if not s["pml_seed_bool"] and s["max_effective_index"] and s["max_effective_index"] < n_win:
                raise RuntimeError("max_effective_index below the guided mode: no mode found")
            # A PML mode first, to test that the caller skips it.
            self.out.update(effective_index=[1.30, n_win], TE_fraction=[0.6, 0.98],
                            loss_dB_per_m=[5e6, loss_win], PML_indices=[0])
            self.truth = {"n_core": n_true, "loss_core": loss_true}
        else:
            assert s["pml_NSEW_bool"] == [0, 0, 0, 0] and s["max_effective_index"] == 0
            y_core = next(iter(self.shapes.values()))["position"][1]
            self._straight(cores, n_core, n_clad, wl, W, H, res, y_core, s["num_modes"])
        CALLS.append(("FDM", {"BC": self.out["BC"], "W": W, "H": H, "res": res}))
        return {"n_eff_tilde": self.out["effective_index"], "TE_fraction": self.out["TE_fraction"]}

    def _straight(self, cores, n_core, n_clad, wl, W, H, res, y_core, num_modes):
        """Supermodes of the made-up model on the window's cell centres."""
        xe = np.arange(-W / 2 + res / 2, W / 2, res)
        ye = np.arange(res / 2, H, res)
        basis = []                                        # (n, polarization, field, strip)
        for k, (xc, w) in enumerate(sorted(cores)):
            for n, pol, p in strip_modes(w, n_core, n_clad, wl):
                basis.append((n, pol, _profile(xe, ye - y_core, xc, w, p), k))
        ham = np.diag([b[0] for b in basis])
        if len(cores) == 2:
            (x1, w1), (x2, w2) = sorted(cores)
            gap = (x2 - w2 / 2) - (x1 + w1 / 2)
            c = C0 * math.exp(-(gap - G0) / L_GAP)
            ig = int(np.argmin(np.abs(xe - (x1 + w1 / 2 + gap / 2))))
            jg = int(np.argmin(np.abs(ye - y_core)))
            for i, bi in enumerate(basis):
                for j, bj in enumerate(basis):
                    if bi[3] == 0 and bj[3] == 1 and bi[1] == bj[1]:
                        sign = np.sign(bi[2][ig, jg] * bj[2][ig, jg]) or 1.0
                        ham[i, j] = ham[j, i] = c * sign
        vals, vecs = np.linalg.eigh(ham)
        modes = []
        for k in np.argsort(-vals)[:num_modes]:
            ex, ey = np.zeros((xe.size, ye.size)), np.zeros((xe.size, ye.size))
            for i, b in enumerate(basis):                 # TE strip modes make Ex, TM ones Ey
                if b[1] == "TE":
                    ex = ex + vecs[i, k] * b[2]
                elif b[1] == "TM":
                    ey = ey + vecs[i, k] * b[2]
            te = float((ex**2).sum() / ((ex**2).sum() + (ey**2).sum()))
            # Scaled to 1 W as EMode does: with H = n z x E, (1/2) Re (E x H*).z = (n/2)|E|^2.
            scale = 1 / math.sqrt(0.5 * vals[k] * ((ex**2).sum() + (ey**2).sum()) * res**2)
            modes.append((float(vals[k]), te, ex * scale, ey * scale))
        while len(modes) < num_modes:                     # unguided box modes
            z = np.zeros((xe.size, ye.size))
            modes.append((n_clad - 0.01 * (len(modes) + 1), 0.5, z, z))
        modes = modes[::-1]                               # unsorted on purpose
        self.out.update(effective_index=[m[0] for m in modes], TE_fraction=[m[1] for m in modes],
                        loss_dB_per_m=[0.0] * len(modes))

        self.fields = {
            "x": xe, "y": ye,
            "Ex": np.array([m[2] for m in modes]).astype(complex),
            "Ey": np.array([m[3] for m in modes]).astype(complex),
            "Hx": np.array([-m[0] * m[3] for m in modes]).astype(complex),
            "Hy": np.array([m[0] * m[2] for m in modes]).astype(complex)}

    def get(self, key, profile="_default", simulation_name="emode"):
        if key in DEPRECATED:
            raise RuntimeError(f"get('{key}') is deprecated: use get_grid() or get_fields()")
        if key == "emode_version":
            return "test double"
        return self.out[key]

    def get_grid(self, **kw):
        _check(kw, GRID_ARGS, "get_grid")
        return Grid(self.fields["x"], self.fields["y"])

    def get_fields(self, key=None, **kw):
        _check(kw, GRID_ARGS, "get_fields")
        names = ["Ex", "Ey", "Hx", "Hy"] if key is None else ([key] if isinstance(key, str) else list(key))
        f = self.fields
        return Field(np.array([f[n] for n in names]), names, f["Ex"].shape[0], self.get_grid())

    def close(self, save=True, save_all_fields=False, file_type="eph", simulation_name="emode"):
        CALLS.append(("close", {}))
