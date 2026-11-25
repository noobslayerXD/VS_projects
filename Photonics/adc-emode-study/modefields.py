"""
Mode fields of the couplers: the checks done on them and the saved files.

Pure numpy, so the checks can be redone on files saved earlier.

A saved set, modes/TE0-TE<m>_wa<access>_dw<error>.npz, holds four modes of one
coupler geometry, all on the same grid (x along the chip, y up, nm; the silicon
from -h_si/2 to +h_si/2, the access strip centred on x = 0):

    access   the access strip alone (TE0), solved in the coupler's window
    bus      the bus strip alone (TE1 or TE2), solved in the coupler's window
    upper    the coupler supermode with the higher effective index
    lower    the coupler supermode with the lower effective index

Each mode is stored as its transverse electric field Ex, Ey, multiplied by a phase so
that it is real (lossless modes are real up to one phase factor):
    access   Ex > 0 at the centre of the access strip
    bus      Ex > 0 in the bus lobe next to the gap
    upper, lower  their access-mode part in phase with the stored access mode, so
             the sign of the bus lobe next to the gap shows whether the two strips
             oscillate in phase (+) or in anti-phase (-)
The files keep `crop` nm of cladding around the strips; the checks below are done
on the full window before cropping.

    data = modefields.load("results_emode/modes/TE0-TE1_wa320_dw+0.npz")
    data["x"], data["y"], data["modes"]["upper"]["Ex"], data["meta"]
"""
import json

import numpy as np

NAMES = ("access", "bus", "upper", "lower")


# ----------------------------------------------------------------- integrals
def cell_sizes(v):
    """Width of the grid cell around each point of a 1D axis (nm)."""
    v = np.asarray(v, dtype=float)
    if v.size < 2:
        return np.ones_like(v)
    edges = np.concatenate(([1.5 * v[0] - 0.5 * v[1]], (v[:-1] + v[1:]) / 2,
                            [1.5 * v[-1] - 0.5 * v[-2]]))
    return np.diff(edges)


def weights(x, y):
    """Area of the grid cell around each point (nm^2), shape (x, y)."""
    return np.outer(cell_sizes(x), cell_sizes(y))


def power(f, w):
    """Power carried along z, 1/2 Re integral of (E x H*).z, in solver units.
    Without H fields: the field norm, the integral of |Ex|^2 + |Ey|^2."""
    if "Hx" in f and "Hy" in f:
        s = f["Ex"] * np.conj(f["Hy"]) - f["Ey"] * np.conj(f["Hx"])
        return 0.5 * float(np.real(np.sum(s * w)))
    return float(np.sum((np.abs(f["Ex"]) ** 2 + np.abs(f["Ey"]) ** 2) * w))


def normalised(f, w):
    """The mode scaled to unit power (unit field norm without H)."""
    p = power(f, w)
    if p == 0:
        raise ValueError("mode with zero power")
    return {k: v / np.sqrt(abs(p)) for k, v in f.items()}


def inner(f, g, w):
    """<f, g>: the integral of conj(E_f) . E_g over the transverse electric field."""
    return complex(np.sum((np.conj(f["Ex"]) * g["Ex"] + np.conj(f["Ey"]) * g["Ey"]) * w))


def decompose(s, a, b, w):
    """Fit a supermode with the two strip modes: s ~ alpha a + beta b.

    Least squares on the transverse electric field, with a and b at unit power.
    Returns (alpha, beta, share, residual):
        share     |alpha|^2 / (|alpha|^2 + |beta|^2), the supermode's share of power
                  in the a-mode (0.5: an even mixture, as at phase matching)
        residual  the fraction of the supermode's field that a and b do not explain
                  (0 for a pure two-mode mixture)
    """
    gram = np.array([[inner(a, a, w), inner(a, b, w)], [inner(b, a, w), inner(b, b, w)]])
    rhs = np.array([inner(a, s, w), inner(b, s, w)])
    alpha, beta = np.linalg.solve(gram, rhs)
    d = {k: s[k] - alpha * a[k] - beta * b[k] for k in ("Ex", "Ey")}
    residual = inner(d, d, w).real / inner(s, s, w).real
    share = abs(alpha) ** 2 / (abs(alpha) ** 2 + abs(beta) ** 2)
    return complex(alpha), complex(beta), float(share), float(residual)


# -------------------------------------------------------------------- checks
def phase_at(f, x, y, point):
    """Phase factor that makes Ex real and positive at the grid point nearest `point`."""
    i = int(np.argmin(np.abs(x - point[0])))
    j = int(np.argmin(np.abs(y - point[1])))
    v = f["Ex"][i, j]
    return np.conj(v) / abs(v) if abs(v) > 0 else 1.0


def rotated(f, phase):
    return {k: v * phase for k, v in f.items()}


def imaginary_fraction(f, w):
    """Share of the transverse field in its imaginary part (about 0 once aligned)."""
    e = (np.abs(f["Ex"]) ** 2 + np.abs(f["Ey"]) ** 2) * w
    im = (np.imag(f["Ex"]) ** 2 + np.imag(f["Ey"]) ** 2) * w
    return float(im.sum() / e.sum())


def mid_cut(f, y, comp="Ex"):
    """|comp|^2 along x through the middle of the silicon (y nearest 0), peak = 1."""
    j = int(np.argmin(np.abs(y)))
    v = np.abs(f[comp][:, j]) ** 2
    return v / v.max()


def level_dB(f, x, y, x0):
    """|Ex|^2 at x0 on the mid-plane, relative to the peak on that line (dB)."""
    return float(10 * np.log10(max(np.interp(x0, x, mid_cut(f, y)), 1e-30)))


def edge_fraction(f, x, y, w, depth=300.0):
    """Share of |E_t|^2 within `depth` nm of the window walls. It should be tiny:
    otherwise the walls of the simulation window are distorting the mode."""
    e = (np.abs(f["Ex"]) ** 2 + np.abs(f["Ey"]) ** 2) * w
    keep = np.outer((x > x.min() + depth) & (x < x.max() - depth),
                    (y > y.min() + depth) & (y < y.max() - depth))
    return float(1 - e[keep].sum() / e.sum())


# --------------------------------------------------------------------- files
def save(path, x, y, modes, meta, xlim, ylim):
    """Save the four modes of one geometry, cropped to xlim, ylim (nm).

    modes : {name: dict(Ex=..., Ey=...)} on the grid x, y, already phase aligned.
    meta  : JSON-serialisable dictionary stored with them.
    """
    ix = (x >= xlim[0]) & (x <= xlim[1])
    iy = (y >= ylim[0]) & (y <= ylim[1])
    arrays = {"x": x[ix].astype(np.float32), "y": y[iy].astype(np.float32)}
    for name, f in modes.items():
        for comp in ("Ex", "Ey"):
            v = f[comp][np.ix_(ix, iy)]
            real = np.abs(np.imag(v)).max() <= 1e-3 * np.abs(v).max()
            arrays[f"{name}_{comp}"] = np.real(v).astype(np.float32) if real else v.astype(np.complex64)
    arrays["meta"] = np.array(json.dumps(meta))
    np.savez_compressed(path, **arrays)


def load(path):
    """Read a saved set: dict(x, y, meta, modes={name: dict(Ex, Ey, neff, te)})."""
    with np.load(path) as z:
        meta = json.loads(str(z["meta"]))
        modes = {n: dict(Ex=z[f"{n}_Ex"], Ey=z[f"{n}_Ey"], **meta["modes"][n])
                 for n in meta["modes"]}
        return {"x": z["x"].astype(float), "y": z["y"].astype(float), "meta": meta, "modes": modes}
