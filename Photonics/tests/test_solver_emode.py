"""Checks solver_emode.py against a test double of emodeconnection that accepts only
the keyword arguments in the EMode 1.0.8 documentation. Tests the Python, not EMode.

    python tests/test_solver_emode.py
"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "mock_emode")); sys.path.insert(0, os.path.join(here, ".."))
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
