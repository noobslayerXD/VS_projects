"""
EMode2D backend. This is the only file that talks to EMode.

Every call here is an EMode2D function (no EME, no FEM, nothing that needs an
EMode3D licence). Two kinds of finite-difference mode (FDM) solve are used:

    modes()        straight cross-section with one or two silicon strips
    mode_fields()  the same solve, also returning the mode fields (x, y, Ex, Ey, Hx, Hy)
    bend_loss()    one strip in a bend (cylindrical bend solver with a PML)

The calls follow the EMode documentation, checked page by page (version 1.0.8):

  Python interface    EMode(simulation_name=..., license_type='2d', save_path=...)
  Simulation setup    settings(), shape(), reset(kind='all')
  Solver analysis     FDM(verbose=False), refractive_index()
  File management     get('effective_index' | 'TE_fraction' | 'loss_dB_per_m' |
                      'BC' | 'PML_indices' | 'emode_version'), close()
  Fields              get('x' | 'y' | 'Ex' | 'Ey' | 'Hx' | 'Hy'): x and y as in
                      SiN_width_sweep.py, which reads them from EMode the same way;
                      Hx and Hy are optional (the field keys stored in .eph files)
  Examples            'Straight Waveguide Convergence' (straight solves, '00' walls),
                      'Bend Mode Solvers', 'Bending: SiN' and 'Ring Resonator Design'
                      (bends), 'Scattering loss: Laser' (MaterialProperties)

Conventions taken from the docs
-------------------------------
- All lengths are in nm.
- The origin is at the horizontal centre of the bottom wall: x runs from
  -window_width/2 to +window_width/2 and y from 0 to window_height. A shape's
  `position` is its centre. Giving y explicitly stops EMode stacking the shape
  as a substrate, so each silicon strip floats in the oxide background.
- The window is grown by EMode to a whole, even number of cells (extra cells at
  the top). Here the window is rounded up beforehand, so the geometry is exactly
  what is asked for and the core sits on the mirror plane needed by the 'TE' fold.
- Since 1.0.8 the defaults are boundary_condition='auto' and resolution='auto'
  (the solver may grow the window or add PML by itself). Both are set explicitly
  here, so the mesh and window convergence checks in adc_study.py control them.
- Settings stay on the profile between solves. reset(kind='all') returns the
  profile to its defaults and removes the shapes, so no setting from a bend solve
  (PML, bend radius, eigen-solver shift) leaks into the next straight solve.
- In a bend, bend_radius is measured at the window centre (x = 0), and the
  effective index and loss_dB_per_m are referenced to that radius. bend_loss()
  rescales both to the radius of the core.

Status: checked against the documentation and the official examples, but not yet
run against a licensed EMode installation. Run
    python adc_study.py --backend emode --steps check
first: it does one single-waveguide solve and prints the result and the
boundary condition EMode actually used.
"""
import math

import numpy as np
import emodeconnection as emc


class EModeSolver:
    name = "emode"

    def __init__(self, resolution=10, h_si=220, side_margin=1500, vert_margin=1000,
                 core="Si", clad="SiO2", simulation_name="adc_study", save_path=".",
                 license_type="2d", verbose=False):
        self.resolution = resolution      # nm, grid step in x and y
        self.h_si = h_si                  # nm, silicon thickness
        self.side_margin = side_margin    # nm, cladding left/right of the outermost core
        self.vert_margin = vert_margin    # nm, cladding above/below the silicon
        self.core, self.clad = core, clad # names from EMode's material database
        self.fixed_indices = None         # (n_core, n_clad): constant indices instead of the database
        self.verbose = verbose            # True prints EMode's own output for every solve
        # Bend solver (values from the 'Bend Mode Solvers' and 'Ring Resonator Design' examples)
        self.pml_side = 1500              # nm, PML on the outer (east) wall of the bend
        self.pml_vertical = 1000          # nm, PML on the top and bottom walls of the bend
        self.caustic_clearance = 500      # nm, oxide between the radiation caustic and the PML
        self.last = {}                    # details of the last solve, for checking
        # license_type='2d' checks out the EMode2D licence directly ('default' tries 3D first).
        self.em = emc.EMode(simulation_name=simulation_name, save_path=save_path,
                            license_type=license_type)

    # ------------------------------------------------------------------ helpers
    def _even(self, length):
        """Round a window length up to a whole, even number of grid cells."""
        cells = 2 * math.ceil(length / (2 * self.resolution) - 1e-9)
        return cells * self.resolution

    def _snap(self, length):
        """Round a length up to a whole number of grid cells."""
        return self.resolution * math.ceil(length / self.resolution - 1e-9)

    def _materials(self):
        """Core and cladding materials: database names, or constant indices."""
        if self.fixed_indices:
            n_core, n_clad = self.fixed_indices
            return emc.MaterialProperties(n=n_core), emc.MaterialProperties(n=n_clad)
        return self.core, self.clad

    def _clad_index(self, wavelength):
        """Cladding index, used only to place the bend window past the radiation caustic."""
        if self.fixed_indices:
            return float(self.fixed_indices[1])
        try:
            return float(np.real(np.ravel(self.em.refractive_index(
                material=self.clad, wavelength=wavelength))[0]))
        except Exception:
            return 1.444                                  # SiO2 near 1550 nm

    def _read(self, key):
        """Read a per-mode result from EMode as a 1D real numpy array."""
        return np.real(np.atleast_1d(np.asarray(self.em.get(key)))).astype(float).ravel()

    def _read_optional(self, key, default=None):
        try:
            return self.em.get(key)
        except Exception:
            return default

    def _te_fraction(self):
        te = self._read("TE_fraction")                    # documented as a fraction (0..1)
        return te / 100.0 if te.size and te.max() > 1.5 else te

    @staticmethod
    def _axis(values):
        """A grid axis read from EMode ('x' or 'y') as a 1D float array in nm."""
        a = np.real(np.asarray(values, dtype=complex)).astype(float)
        if a.ndim > 1 and min(a.shape) > 1:              # a meshgrid: keep the distinct values
            return np.unique(a.round(6))
        return a.ravel()

    @staticmethod
    def _stack(raw, n_modes, nx, ny):
        """One field component of every mode as an array (mode, x, y).

        EMode returns a field as (mode, x, y) or (mode, y, x); a single mode may come
        without the mode axis. The x and y lengths tell the layouts apart (the window
        is never square here)."""
        a = np.squeeze(np.asarray(raw))
        if a.ndim == 2:
            a = a[None]
        if a.ndim != 3:
            raise ValueError(f"field array of shape {np.shape(raw)}")
        if a.shape[0] != n_modes and a.shape[-1] == n_modes:
            a = np.moveaxis(a, -1, 0)
        if a.shape[0] != n_modes:
            raise ValueError(f"field array of shape {np.shape(raw)} for {n_modes} modes")
        if a.shape[1:] == (nx, ny):
            return a
        if a.shape[1:] == (ny, nx):
            return a.transpose(0, 2, 1)
        raise ValueError(f"field array of shape {np.shape(raw)} on a {nx} x {ny} grid")

    # ---------------------------------------------------------------- interface
    def modes(self, cores, wavelength, num_modes=8, frame=None):
        """Solve one straight cross-section.

        cores      : list of (x_centre_nm, width_nm) silicon strips, all h_si thick
        wavelength : nm
        frame      : strips that set the window (default: cores). Giving a coupler's two
                     strips here while solving only one of them puts that strip on the
                     coupler's grid, so their fields can be compared point by point.
        Returns (n_eff, TE_fraction) as arrays sorted by decreasing n_eff.
        """
        neff, te, order, _, _ = self._straight(cores, wavelength, num_modes, frame)
        return neff[order], te[order]

    def mode_fields(self, cores, wavelength, num_modes=8, frame=None):
        """Like modes(), and also returns the mode fields.

        Returns (n_eff, TE_fraction, fields), sorted by decreasing n_eff. `fields` holds
        x and y (1D, nm, in the caller's coordinates: the strips at their given x, the
        silicon from -h_si/2 to +h_si/2) and Ex, Ey, Hx, Hy as arrays (mode, x, y) in
        EMode's units. Hx and Hy are left out if EMode does not return them.
        Reads get('x'), get('y') and get('Ex' | 'Ey' | 'Hx' | 'Hy'), the calls that
        SiN_width_sweep.py already uses with EMode.
        """
        neff, te, order, shift, window_height = self._straight(cores, wavelength, num_modes, frame)
        x = self._axis(self.em.get("x")) - shift
        y = self._axis(self.em.get("y")) - window_height / 2
        fields, missing = dict(x=x, y=y), []
        for comp in ("Ex", "Ey", "Hx", "Hy"):
            try:
                fields[comp] = self._stack(self.em.get(comp), len(neff), x.size, y.size)[order]
            except Exception as err:
                if comp in ("Ex", "Ey"):
                    raise RuntimeError(f"could not read {comp} from EMode: {err}") from err
                missing.append(comp)
        self.last["fields_missing"] = missing
        return neff[order], te[order], fields

    def _straight(self, cores, wavelength, num_modes, frame=None):
        """Set up and solve one straight cross-section (see modes()).

        Returns the raw EMode results (n_eff, TE_fraction), the order that sorts them
        by decreasing n_eff, and the shift and window height that map EMode's
        coordinates to the caller's: x_caller = x - shift, y_caller = y - height/2.
        """
        em, res = self.em, self.resolution
        frame = frame or cores
        x_min = min(c - w / 2 for c, w in frame)
        x_max = max(c + w / 2 for c, w in frame)
        # Centre the structure on x = 0. The shift is a whole number of cells, so
        # walls that lie on the grid in the caller's coordinates stay on the grid.
        shift = -res * round((x_min + x_max) / 2 / res)
        half = max(abs(x_min + shift), abs(x_max + shift)) + self._snap(self.side_margin)
        window_width = self._even(2 * half)
        window_height = self._even(self.h_si + 2 * self._snap(self.vert_margin))
        core_mat, clad_mat = self._materials()

        em.reset(kind="all")
        em.settings(
            wavelength=wavelength,
            x_resolution=res, y_resolution=res,
            window_width=window_width, window_height=window_height,
            num_modes=num_modes,
            # Metal walls on all four sides, full window. No symmetry fold: the
            # asymmetric coupler has no vertical mirror plane, and the TM modes are
            # needed for the TM benchmark. Setting it also switches off 'auto'.
            boundary_condition="00",
            background_material=clad_mat,                 # oxide below, beside and above the silicon
            max_effective_index=0)                        # 0: highest index in the window
        for i, (c, w) in enumerate(cores):
            em.shape(name=f"core{i}", material=core_mat, width=w, height=self.h_si,
                     position=[c + shift, window_height / 2])
        em.FDM(verbose=self.verbose)

        neff = self._read("effective_index")
        te = self._te_fraction()
        self.last = dict(kind="straight", window_width=window_width, window_height=window_height,
                         boundary_condition=self._read_optional("BC"), modes_found=len(neff))
        return neff, te, np.argsort(-neff), shift, window_height

    def bend_loss(self, width, radius, wavelength, n_guess=None):
        """Fundamental TE mode of one strip bent to `radius` (nm, at the core centre).

        Set up as in the 'Ring Resonator Design' and 'Bend Mode Solvers' examples:
          - the centre of curvature is to the west, so the bend radiates east;
          - the core is moved x_off to the west of the window centre and
            bend_radius = radius + x_off, so the radius is measured at the core;
          - the window reaches past the radiation caustic, about
            radius * (n_eff / n_clad - 1) outside the core, before the east PML;
          - PMLs on the north, south and east walls, with pml_kappa_max = 1;
          - boundary_condition 'TE' folds the window about its horizontal mirror plane.

        Returns (n_eff, loss_dB_per_m), both referenced to the core radius, so the
        loss of a 90 degree bend is loss_dB_per_m * (pi/2) * radius.
        """
        em = self.em
        if n_guess is None or not np.isfinite(n_guess):   # straight-waveguide TE0 index
            neff, te = self.modes([(0.0, float(width))], wavelength, 4)
            n_guess = float(neff[te > 0.5][0])

        caustic = radius * (n_guess / self._clad_index(wavelength) - 1)
        d_west = width / 2 + self._snap(self.side_margin)
        d_east = max(width / 2 + self._snap(self.side_margin), caustic + self.caustic_clearance)
        d_east += self.pml_side
        window_width = self._even(d_west + d_east)
        x_off = window_width / 2 - d_west                 # core centre sits at x = -x_off
        v = self._snap(self.vert_margin) + self.pml_vertical
        window_height = self._even(self.h_si + 2 * v)
        bend_radius = radius + x_off                      # EMode measures it at x = 0
        if bend_radius <= window_width / 2:
            raise ValueError("bend radius must exceed half the window width "
                             f"({bend_radius:.0f} nm vs {window_width / 2:.0f} nm)")
        scale = bend_radius / radius                      # window-centre -> core-centre reference
        core_mat, clad_mat = self._materials()

        def solve(seed):
            em.reset(kind="all")
            em.settings(
                wavelength=wavelength,
                x_resolution=self.resolution, y_resolution=self.resolution,
                window_width=window_width, window_height=window_height,
                num_modes=2, boundary_condition="TE",
                background_material=clad_mat,
                bend_radius=bend_radius, bend_method="cylindrical",
                pml_NSEW_bool=[1, 1, 1, 0],
                pml_thickness=[self.pml_vertical, self.pml_vertical, self.pml_side, 0],
                pml_kappa_max=1,
                # First try: eigen-solver limit just above the guided mode, referenced
                # to the window centre as in the 'Ring Resonator Design' example (margin
                # 0.05 rather than 0.01, since the mode moves outward in tight bends).
                # Fallback: pml_seed_bool lets EMode take the shift from the same
                # structure solved without PML, so no guess is needed.
                max_effective_index=0 if seed else (n_guess + 0.05) / scale,
                pml_seed_bool=seed)
            em.shape(name="core0", material=core_mat, width=width, height=self.h_si,
                     position=[-x_off, window_height / 2])
            em.FDM(verbose=self.verbose)
            neff = self._read("effective_index")
            pml = set(np.atleast_1d(self._read_optional("PML_indices", [])).astype(int).tolist())
            te = self._te_fraction()
            ok = [i for i in range(len(neff)) if i not in pml and te[i] > 0.5]
            return neff, te, pml, ok

        try:
            neff, te, pml_modes, ok = solve(seed=False)
        except Exception:
            ok = []
        seeded = not ok
        if seeded:
            neff, te, pml_modes, ok = solve(seed=True)
        loss = self._read("loss_dB_per_m")
        self.last = dict(kind="bend", window_width=window_width, window_height=window_height,
                         x_off=x_off, bend_radius_setting=bend_radius, caustic_nm=caustic,
                         boundary_condition=self._read_optional("BC"), modes_found=len(neff),
                         pml_modes=sorted(pml_modes), pml_seeded=seeded)
        if not ok:
            raise RuntimeError(f"no guided TE mode found in the bend (W = {width}, R = {radius})")
        i = max(ok, key=lambda k: neff[k])
        if loss[i] < 0:
            print(f"  warning: negative loss {loss[i]:.3g} dB/m (PML truncation error) "
                  f"for W = {width}, R = {radius}")
        return float(neff[i] * scale), float(loss[i] * scale)

    def describe(self):
        """One line on the EMode session and the last solve, for the 'check' step."""
        version = self._read_optional("emode_version", "unknown")
        return f"EMode version {version}; last solve: {self.last}"

    def close(self):
        self.em.close()                                   # saves <simulation_name>.eph in save_path
