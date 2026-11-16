"""
EMode2D backend. This is the only file that talks to EMode.

It uses three kinds of EMode2D calculation, all finite-difference mode (FDM) solves
of a 2D cross-section:

    modes()      straight cross-section with one or two silicon strips
    bend_loss()  one strip in a bend (cylindrical bend solver + PML)

EMode function calls follow the EMode documentation (docs.emodephotonix.com):
settings(), shape(), reset(), FDM(), get(), close(). All lengths are in nm.

NOTE: this file was written from the documentation and has not been run against
a licensed EMode installation. If a call fails, compare it with the 'Basic: SOI',
'Bend Mode Solvers' and 'Straight Waveguide Convergence' examples in the docs.
Run `python adc_study.py --backend emode --steps check` first: it does one
single-waveguide solve and prints the result.
"""
import numpy as np
import emodeconnection as emc


class EModeSolver:
    name = "emode"

    def __init__(self, resolution=10, h_si=220, side_margin=1500, vert_margin=1000,
                 core="Si", clad="SiO2", simulation_name="adc_study"):
        self.resolution = resolution      # nm, grid step in x and y
        self.h_si = h_si                  # nm, silicon thickness
        self.side_margin = side_margin    # nm, cladding left/right of the outermost core
        self.vert_margin = vert_margin    # nm, cladding above/below the silicon
        self.core, self.clad = core, clad # names from EMode's material database
        self.fixed_indices = None         # not used: EMode takes indices from its database
        self.simulation_name = simulation_name
        self.em = emc.EMode(simulation_name=simulation_name)

    # ------------------------------------------------------------------ helpers
    def _clear_shapes(self):
        """Remove all shapes so the next cross-section starts empty."""
        try:
            self.em.reset(kind="shapes")
        except Exception:
            # Older EMode versions may not have reset(): restart the session instead.
            self.em.close()
            self.em = emc.EMode(simulation_name=self.simulation_name)

    def _read(self, key):
        """Read a per-mode result from EMode as a 1D real numpy array."""
        return np.real(np.atleast_1d(np.asarray(self.em.get(key)))).astype(float).ravel()

    # ---------------------------------------------------------------- interface
    def modes(self, cores, wavelength, num_modes=8):
        """Solve one straight cross-section.

        cores      : list of (x_centre_nm, width_nm) silicon strips, all h_si thick
        wavelength : nm
        Returns (n_eff, TE_fraction) as arrays sorted by decreasing n_eff.
        """
        em = self.em
        x_min = min(c - w / 2 for c, w in cores)
        x_max = max(c + w / 2 for c, w in cores)
        shift = -(x_min + x_max) / 2                      # centre the structure in the window
        window_width = (x_max - x_min) + 2 * self.side_margin
        window_height = self.h_si + 2 * self.vert_margin

        self._clear_shapes()
        em.settings(
            wavelength=wavelength,
            x_resolution=self.resolution, y_resolution=self.resolution,
            window_width=window_width, window_height=window_height,
            num_modes=num_modes,
            boundary_condition="00",                      # metal walls, full window (no symmetry)
            background_material=self.clad,                # oxide below, beside and above the silicon
            bend_radius=0, pml_NSEW_bool=[0, 0, 0, 0], max_effective_index=0)
        for i, (c, w) in enumerate(cores):
            em.shape(name=f"core{i}", material=self.core, width=w, height=self.h_si,
                     position=[c + shift, window_height / 2])
        em.FDM()

        neff = self._read("effective_index")
        te = self._read("TE_fraction")
        if te.max() > 1.5:                                # in case it is reported in percent
            te = te / 100.0
        order = np.argsort(-neff)
        return neff[order], te[order]

    def bend_loss(self, width, radius, wavelength, n_guess=None):
        """Fundamental TE mode of one strip in a bend of the given radius.

        Follows the 'Bend Mode Solvers' example: the centre of curvature is on the
        west side, so the field leaks east. PMLs sit on the north, south and east
        walls, and the core is shifted west to leave room for the leaking field.
        Returns (n_eff, loss_dB_per_m).
        """
        em = self.em
        x_off = 500                                       # nm, core shift towards the bend centre
        window_width = width + 2 * (self.side_margin + x_off)
        window_height = self.h_si + 2 * self.vert_margin
        pml = 1000                                        # nm, PML thickness

        self._clear_shapes()
        em.settings(
            wavelength=wavelength,
            x_resolution=self.resolution, y_resolution=self.resolution,
            window_width=window_width, window_height=window_height,
            num_modes=1, boundary_condition="TE",
            background_material=self.clad,
            bend_radius=radius + x_off,                   # so the radius is measured at the core
            pml_NSEW_bool=[1, 1, 1, 0], pml_thickness=[pml, pml, pml, 0], pml_kappa_max=1,
            # Aim the eigen-solver just above the straight-waveguide index so it
            # returns the guided mode and not a PML mode.
            max_effective_index=(n_guess + 0.05) if n_guess else 0)
        em.shape(name="core0", material=self.core, width=width, height=self.h_si,
                 position=[-x_off, window_height / 2])
        em.FDM()
        neff = float(self._read("effective_index")[0])
        loss = float(self._read("loss_dB_per_m")[0])
        return neff, loss

    def close(self):
        self.em.close()
