"""
Open-source cross-check solver (no EMode licence needed).

Same interface as solver_emode.EModeSolver, but built on the free finite-difference
mode solver in the EMpy package:

    pip install electromagneticpython scipy numpy

Why it exists
-------------
1. The analysis in adc_study.py can be run and tested without EMode.
2. It gives an independent check of the EMode2D numbers. Two different solvers
   that agree are stronger evidence than one solver alone.

Differences from the EMode backend
----------------------------------
- Material indices come from the Sellmeier fits below (silicon: Salzberg & Villa
  form; silica: Malitson), not from EMode's material database.
- The grid is "conformal": every silicon wall lies exactly on a grid line, so a
  1 nm width change is resolved even on a 10 or 20 nm grid. There is no sub-pixel
  averaging, so n_eff converges slowly with grid step (about 0.01 too high at 10 nm).
- Metal walls on all four sides and no PML, so there is no bend solver here:
  bend_loss() returns NaN.

All lengths at the interface are in nm, as in EMode.
"""
import numpy as np
from scipy.sparse import linalg
from EMpy.modesolvers.FD import VFDModeSolver, FDMode


def n_si(wl_nm):
    """Refractive index of crystalline silicon (Sellmeier fit, near-infrared)."""
    L2 = (wl_nm * 1e-3) ** 2
    return np.sqrt(11.6858 + 0.939816 / L2 + 0.00810461 * 1.1071**2 / (L2 - 1.1071**2))


def n_sio2(wl_nm):
    """Refractive index of fused silica (Malitson)."""
    L2 = (wl_nm * 1e-3) ** 2
    return np.sqrt(1 + 0.6961663 * L2 / (L2 - 0.0684043**2)
                   + 0.4079426 * L2 / (L2 - 0.1162414**2)
                   + 0.8974794 * L2 / (L2 - 9.896161**2))


def _segment(a, b, step):
    """Grid lines from a to b with a whole number of cells of about `step`."""
    n = max(1, int(round((b - a) / step)))
    return np.linspace(a, b, n + 1)


class EMpySolver:
    name = "empy"

    def __init__(self, resolution=20, h_si=220, side_margin=1000, vert_margin=800):
        self.resolution = resolution      # nm, target grid step in x and y
        self.h_si = h_si                  # nm, silicon thickness
        self.side_margin = side_margin    # nm, cladding left/right of the outermost core
        self.vert_margin = vert_margin    # nm, cladding above/below the silicon
        self.fixed_indices = None         # (n_core, n_clad) to override the Sellmeier fits

    def indices(self, wavelength):
        if self.fixed_indices:
            return self.fixed_indices
        return float(n_si(wavelength)), float(n_sio2(wavelength))

    def _grid(self, cores):
        """Grid lines in um with every silicon wall on a grid line."""
        d, h = self.resolution * 1e-3, self.h_si * 1e-3
        xe = sorted({round(e * 1e-3, 9) for c, w in cores for e in (c - w / 2, c + w / 2)})
        xe = [xe[0] - self.side_margin * 1e-3] + xe + [xe[-1] + self.side_margin * 1e-3]
        ye = [-h / 2 - self.vert_margin * 1e-3, -h / 2, h / 2, h / 2 + self.vert_margin * 1e-3]
        x = np.concatenate([_segment(a, b, d)[:-1] for a, b in zip(xe, xe[1:])] + [[xe[-1]]])
        y = np.concatenate([_segment(a, b, d)[:-1] for a, b in zip(ye, ye[1:])] + [[ye[-1]]])
        return x, y

    def modes(self, cores, wavelength, num_modes=8):
        """Solve one straight cross-section.

        cores      : list of (x_centre_nm, width_nm) silicon strips, all h_si thick
        wavelength : nm
        Returns (n_eff, TE_fraction) as arrays sorted by decreasing n_eff.
        """
        n_core, n_clad = self.indices(wavelength)
        wl, h = wavelength * 1e-3, self.h_si * 1e-3
        x, y = self._grid(cores)

        def eps(xc, yc):
            X, Y = np.meshgrid(xc, yc, indexing="ij")
            e = np.full(X.shape, n_clad**2)
            for c, w in cores:
                e[(np.abs(X - c * 1e-3) < w * 1e-3 / 2) & (np.abs(Y) < h / 2)] = n_core**2
            return e

        fd = VFDModeSolver(wl, x, y, eps, "0000")
        A = fd.build_matrix()
        k0 = 2 * np.pi / wl
        # Shift-invert at the core index: returns the num_modes highest-index modes.
        vals, vecs = linalg.eigs(A, k=num_modes, sigma=(n_core * k0) ** 2, which="LM", tol=1e-9)
        neff = wl * np.sqrt(vals) / (2 * np.pi)
        order = np.flipud(np.argsort(neff.real))
        neff, nx, ny = neff[order], fd.nx, fd.ny
        Hx = [vecs[:nx * ny, i].reshape(nx, ny) for i in order]
        Hy = [vecs[nx * ny:, i].reshape(nx, ny) for i in order]
        Hz, Ex, Ey, Ez = fd.compute_other_fields(neff, Hx, Hy)
        te = [FDMode(wl, x, y, n, ex, ey, ez, hx, hy, hz).normalize().TEfrac()
              for n, ex, ey, ez, hx, hy, hz in zip(neff, Ex, Ey, Ez, Hx, Hy, Hz)]
        return np.real(neff).astype(float), np.real(np.array(te)).astype(float)

    def bend_loss(self, width, radius, wavelength, n_guess=None):
        """No bend solver in this backend."""
        return float("nan"), float("nan")

    def close(self):
        pass
