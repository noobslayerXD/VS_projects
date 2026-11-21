"""Checks solver_emode.py against a test double of emodeconnection that accepts only
the keyword arguments in the EMode 1.0.8 documentation. Tests the Python, not EMode.

    python tests/test_solver_emode.py
"""
import os, sys
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
study = next(p for p in (os.path.join(here, ".."), os.path.join(here, "..", "adc-emode-study"))
             if os.path.exists(os.path.join(p, "solver_emode.py")))   # tests/ inside or beside the study
sys.path.insert(0, os.path.join(here, "mock_emode")); sys.path.insert(0, os.path.abspath(study))
import emodeconnection as emc
from solver_emode import EModeSolver
from solver_empy import EMpySolver

for res in (10, 20, 40):
    s = EModeSolver(resolution=res)
    # straight: single strip and asymmetric pair
    n1, t1 = s.modes([(0.0, 400.0)], 1550, 4)
    n2, t2 = s.modes([(0.0, 400.0), (400/2 + 200 + 827.3/2, 827.3)], 1550, 6)
    assert all(n1[:-1] >= n1[1:]) and all(n2[:-1] >= n2[1:]), "not sorted"
    print(f"res {res}: single TE0 {n1[0]:.4f} (TE {t1[0]:.2f}); pair top {n2[:3].round(4)}; last {s.last}")
    # bend: rescaling back to the core radius must recover the mock's 'true' values
    for R in (3000, 5000, 10000):
        n0 = n1[0]
        nb, lb = s.bend_loss(400, R, 1550, n_guess=n0)
        tr = s.em.truth
        assert abs(nb - tr["n_core"]) < 1e-9 and abs(lb - tr["loss_core"]) < 1e-6, (nb, lb, tr)
        print(f"   bend R={R}: n_core {nb:.4f}, loss {lb:.4g} dB/m, W={s.last['window_width']}, "
              f"x_off={s.last['x_off']}, caustic={s.last['caustic_nm']:.0f}, BC={s.last['boundary_condition']}")
    # bend without n_guess
    s.bend_loss(400, 3000, 1550)
    # fixed indices (Dai benchmark path) gives the same as the EMpy backend with fixed indices
    s.fixed_indices = (3.455, 1.445)
    nf, _ = s.modes([(0.0, 400.0)], 1500, 4)
    e = EMpySolver(resolution=res, side_margin=1000, vert_margin=800); e.fixed_indices = (3.455, 1.445)
    ne, _ = e.modes([(0.0, 400.0)], 1500, 4)
    assert abs(nf[0] - ne[0]) < 1e-6, (nf[0], ne[0])
    s.fixed_indices = None
    print(s.describe()[:40]); s.close()

# settings must not leak from a bend solve into the next straight solve
s = EModeSolver(resolution=20); s.bend_loss(400, 3000, 1550, n_guess=2.2); s.modes([(0.0, 400.0)], 1550, 4)
print("no settings leak; all solver_emode checks passed")

# a bend mode far above the straight index: the first solve finds nothing, the seeded retry must recover it
emc.SHIFT = 0.5
s = EModeSolver(resolution=20)
nb, lb = s.bend_loss(400, 3000, 1550, n_guess=2.2)
assert s.last["pml_seeded"] and abs(nb - s.em.truth["n_core"]) < 1e-9
print("seeded fallback works:", round(nb, 4))
emc.SHIFT = 0.05


# mode_fields: fields in the caller's coordinates, sorted like modes(), whatever the array layout
def centre(f, k=0):
    e = np.abs(f["Ex"][k]) ** 2
    return (e.sum(1) * f["x"]).sum() / e.sum(), (e.sum(0) * f["y"]).sum() / e.sum()

pair = [(0.0, 400.0), (400 / 2 + 200 + 840 / 2, 840.0)]
for layout in ("xy", "yx"):
    emc.FIELD_LAYOUT = layout
    s = EModeSolver(resolution=20)
    n1, t1, f1 = s.mode_fields(pair[:1], 1550, 4)
    assert np.allclose(n1, s.modes(pair[:1], 1550, 4)[0]), "mode_fields and modes disagree"
    assert f1["Ex"].shape == (4, f1["x"].size, f1["y"].size) and {"Hx", "Hy"} <= set(f1)
    xc, yc = centre(f1)
    assert abs(xc) < 2 and abs(yc) < 2, ("TE0 not centred on the strip", xc, yc)
    nc, tc, fc = s.mode_fields(pair, 1550, 6)
    nb_, tb_, fb_ = s.mode_fields(pair[1:], 1550, 6, frame=pair)    # bus alone, on the coupler's grid
    assert np.array_equal(fc["x"], fb_["x"]) and np.array_equal(fc["y"], fb_["y"]), "frame grid differs"
    assert abs(centre(fb_)[0] - pair[1][0]) < 5, "bus mode not on the bus strip"
    assert all(nc[:-1] >= nc[1:]), "not sorted"
    print(f"fields ({layout}): grid {fc['x'].size} x {fc['y'].size}, TE0 centre ({xc:.1f}, {yc:.1f}) nm, "
          f"bus TE0 centre {centre(fb_)[0]:.0f} nm (strip at {pair[1][0]:.0f})")
    s.close()
emc.FIELD_LAYOUT = "xy"

emc.GIVE_H = False                                   # EMode without H fields: E only, and it says so
s = EModeSolver(resolution=20)
_, _, f = s.mode_fields(pair[:1], 1550, 4)
assert "Hx" not in f and s.last["fields_missing"] == ["Hx", "Hy"]
emc.GIVE_H = True
print("mode_fields checks passed")
