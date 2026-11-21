"""The 'modes' step through the EMode code path (test double of emodeconnection), and the
helpers in modefields.py. Tests the Python, not EMode's numbers.

    python tests/test_modes_step.py
"""
import os
import sys
import tempfile

import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
study = next(p for p in (os.path.join(here, ".."), os.path.join(here, "..", "adc-emode-study"))
             if os.path.exists(os.path.join(p, "adc_study.py")))
sys.path.insert(0, os.path.join(here, "mock_emode"))
sys.path.insert(0, os.path.abspath(study))
import adc_study  # noqa: E402
import modefields as mf  # noqa: E402
import plots  # noqa: E402
from solver_emode import EModeSolver  # noqa: E402
from solver_empy import EMpySolver  # noqa: E402

# 1. Helpers. Cell sizes add up to the span of the grid, uniform or not.
for x in (np.arange(5.0, 100, 10), np.array([0.0, 10, 30, 35, 60])):
    assert abs(mf.cell_sizes(x).sum() - (x[-1] - x[0] + (x[1] - x[0]) / 2 + (x[-1] - x[-2]) / 2)) < 1e-9

# 2. A symmetric coupler's supermodes are exactly even mixtures of the two strip modes.
s = EMpySolver(resolution=20)
pair = [(0.0, 400.0), (600.0, 400.0)]
nc, tc, fc = s.mode_fields(pair, 1550, 6)
na, ta, fa = s.mode_fields(pair[:1], 1550, 6, frame=pair)
nb, tb, fb = s.mode_fields(pair[1:], 1550, 6, frame=pair)
w = mf.weights(fc["x"], fc["y"])
pick = lambda f, i: mf.normalised({c: f[c][i] for c in ("Ex", "Ey", "Hx", "Hy")}, w)
A, B = pick(fa, 0), pick(fb, 0)
for i in (0, 1):
    _, _, share, residual = mf.decompose(pick(fc, i), A, B, w)
    assert abs(share - 0.5) < 2e-3 and residual < 0.02, (i, share, residual)
print("symmetric coupler: both supermodes are 50/50 mixtures")

# 3. Unit power and phase alignment.
assert abs(mf.power(A, w) - 1) < 1e-9
Ar = mf.rotated(A, mf.phase_at(A, fc["x"], fc["y"], (0.0, 0.0)))
assert mf.imaginary_fraction(Ar, w) < 1e-6 and np.real(Ar["Ex"][np.argmin(abs(fc["x"])), np.argmin(abs(fc["y"]))]) > 0

# 4. The whole step through the EMode code path, on a small coarse study.
cfg = dict(adc_study.CFG, **adc_study.QUICK)
cfg.update(resolution=40, couplers=[1], access_widths=[400], mode_errors=[-10, 0, 10])
out = tempfile.mkdtemp()
st = adc_study.Study(EModeSolver(resolution=40, save_path=out), cfg, out)
for step in ("design", "tolerance", "modes"):
    getattr(st, f"step_{step}")()
rows = st.res["modes"]
assert [r["dw"] for r in rows] == [-10, 0, 10]
for r in rows:
    assert r["residual_upper"] < 0.05 and r["residual_lower"] < 0.05, r
    assert r["bus_sign_upper"] > 0 > r["bus_sign_lower"], "upper not in phase or lower not in anti-phase"
    assert abs(r["dn_s"] - r["dn_s_model"]) / r["dn_s_model"] < 0.05, (r["dn_s"], r["dn_s_model"])
    assert r["edge_fraction"] < 1e-2 and r["te_upper"] > 0.8
up = [r["share_upper"] for r in rows]
assert up[0] < up[1] < up[2], f"access share should grow with dW (access index grows faster): {up}"
data = mf.load(os.path.join(out, rows[1]["file"]))
assert set(data["modes"]) == set(mf.NAMES) and data["modes"]["upper"]["Ex"].shape == (data["x"].size, data["y"].size)
assert data["meta"]["norm"] == "power"
print("modes step through the EMode code path: shares", [round(u, 3) for u in up])

# 5. A rerun reuses the saved fields; a changed grid does not.
st2 = adc_study.Study(EModeSolver(resolution=40, save_path=out), cfg, out)
st2.step_modes()
assert st2.n_new == 0, st2.n_new

# 6. The figures render from the saved results.
plots.make_all(st.res, cfg, out, "emode")
for name in ("fig8_modes_TE0-TE1", "fig10_supermodes_width_error", "fig11_mode_checks", "fig12_tolerance_fields"):
    assert os.path.exists(os.path.join(out, name + ".png")), name
print("all modes-step checks passed; output in", out)
