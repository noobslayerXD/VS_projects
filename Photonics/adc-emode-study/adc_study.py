#!/usr/bin/env python3
"""
Does a narrower access waveguide make a silicon asymmetric directional coupler
(ADC) more tolerant to fabrication width errors?

Two couplers are studied on 220 nm silicon-on-insulator with oxide cladding:
    coupler 1:  TE0 (access waveguide)  ->  TE1 (bus waveguide)
    coupler 2:  TE0 (access waveguide)  ->  TE2 (bus waveguide)

Method (2D cross-section mode solves only, so it runs in EMode2D)
-----------------------------------------------------------------
A coupler cross-section (access strip | gap | bus strip) has two "supermodes"
that share power between the two strips. Their index difference is dn_s.

1. Scan the bus width through the anticrossing and fit
        dn_s(W_bus)^2 = dn_min^2 + [c * (W_bus - W_star)]^2
   W_star is the bus width of minimum splitting, dn_min gives the coupling
   coefficient kappa = pi*dn_min/lambda and the coupling length
   L_c = lambda/(2*dn_min). Steps 2 and 3 treat W_star as the phase-matched width;
   the mode fields (step 4) show that it is wider than that when the coupling
   changes with the bus width.
2. For a coupler that is detuned (wrong width or wavelength) the converted power
   after a length L is (two-mode coupled-mode theory):
        eta = (dn_min/dn_s)^2 * sin^2(pi * dn_s * L / lambda)
   The first factor is the phase-matching penalty, the second the length penalty.
3. Fabrication tolerance: every waveguide is dW wider (dW < 0: narrower) while the
   centre lines stay where they are. So access -> W_a + dW, bus -> W_star + dW and
   gap -> gap - dW. The coupler length stays at the nominal L_c. The tolerance is
   the largest |dW| for which the unconverted power 1 - eta stays below -15 dB.
4. Mode fields ('modes' step): the supermodes and the two strip modes are solved
   on one grid and saved, and each supermode is fitted with the two strip modes.
   That checks the two-mode picture behind step 2 directly on the fields, and gives
   the bus width W_pm at which the supermodes are an even mixture (phase matching).
5. Phase-matched couplers ('matched' step): each coupler is rebuilt with its bus at
   W_pm and its tolerance is taken from the fields.

Usage
-----
    python adc_study.py --backend emode --steps check     # one solve, tests the EMode link
    python adc_study.py --backend emode --quick           # coarse first look (minutes)
    python adc_study.py --backend emode                   # full study
    python adc_study.py --backend emode --steps modes,plots   # add the mode fields to a finished run
    python adc_study.py --backend emode --steps matched,plots # tolerance with the bus at the phase-matched width
    python adc_study.py --backend emode --steps plots     # redraw figures from saved results

Steps: check, sweep, design, tolerance, wavelength, bend, validate, modes, matched, plots.
Every mode solve is done by EMode2D (solver_emode.py). Results go to
results_emode/ next to this script (or --out). Solved
cross-sections are cached in its cache.json, so a rerun only solves what is new.
Delete that file to force new solves. Saved mode fields (modes/*.npz) are reused
the same way.
"""
import argparse
import json
import math
import os
import time

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

import modefields

# ----------------------------------------------------------------------------
# Study parameters (all lengths in nm). Edit these.
# ----------------------------------------------------------------------------
CFG = dict(
    wavelength=1550,                      # design wavelength
    gap=200,                              # coupling gap = smallest feature allowed in this study
    access_widths=[320, 360, 400, 440, 480],   # access widths to compare
    baseline=400,                         # conventional access width used in the literature
    access_sweep=(280, 520, 20),          # isolated-strip sweep for TE0: start, stop, step
    bus_sweep=(600, 1700, 50),            # isolated-strip sweep for TE1, TE2: start, stop, step
    scan_half_range=30, scan_step=10,     # anticrossing scan of the bus width: +/- range, step
    width_errors=[-20, -10, 0, 10, 20],   # uniform width errors dW that are re-solved
    wavelengths=[1500, 1530, 1550, 1565, 1600],
    c_band=(1530, 1565),
    residual_limit_dB=-15.0,              # tolerance criterion on the unconverted power
    bend_radii=[3000, 5000, 10000],       # S-bend radii for the access waveguide
    resolution=10,                        # grid step
    convergence_resolutions=[40, 20, 10], # for the mesh-convergence check
    modes_single=10, modes_coupled=10,    # number of modes requested per solve
    couplers=[1, 2],                      # 1: TE0-TE1, 2: TE0-TE2
    mode_errors=[-10, 0, 10],             # width errors dW whose mode fields are saved ('modes' step)
    mode_crop=600,                        # cladding kept around the strips in the saved fields
    matched_errors=[-10, -5, 0, 5, 10],   # width errors for the couplers rebuilt at the phase-matched width
)
QUICK = dict(                             # coarse settings for a first look
    access_widths=[320, 400, 480], width_errors=[-10, 0, 10],
    wavelengths=[1530, 1550, 1565], bus_sweep=(600, 1700, 100),
    access_sweep=(280, 520, 40), scan_half_range=20,
    resolution=20, convergence_resolutions=[40, 20],
)
N_GUIDED = 1.46        # modes with n_eff below this are not guided in oxide cladding

# Published designs used as benchmarks in the 'validate' step
WANG_2022 = dict(access=400, gap=200, bus=820, Lc_um=17.0)               # TE0-TE1, 1550 nm; 820 nm is
                                                                         # the bus of its corrugated coupler
DAI_2013 = dict(access=400, gap=300, bus=1020, Lc_um=4.5, wavelength=1500,
                n_si=3.455, n_sio2=1.445)                                # TM0-TM1


# ----------------------------------------------------------------------------
# Physics helpers
# ----------------------------------------------------------------------------
def conversion(dn_min, dn_det, length, wavelength):
    """Converted power fraction of a detuned coupler (two-supermode model)."""
    dn_s = np.hypot(dn_min, dn_det)
    return (dn_min / dn_s) ** 2 * np.sin(np.pi * dn_s * length / wavelength) ** 2


def to_dB(x):
    return 10 * np.log10(np.maximum(x, 1e-6))


def width_at_index(w, n, n_target):
    """Width at which a sweep n(w), rising with w, reaches n_target, on the PCHIP curve
    through the sweep points. A straight line between the points would put the width up
    to about 1 nm too high here: n_eff(W) is concave, so the chord lies below the curve."""
    w, n = np.asarray(w, dtype=float), np.asarray(n, dtype=float)
    i = int(np.searchsorted(n, n_target))
    if not 0 < i < len(n):
        raise ValueError(f"n_eff = {n_target:.4f} is outside the sweep ({n[0]:.4f} to {n[-1]:.4f})")
    f = PchipInterpolator(w, n)
    return float(brentq(lambda x: float(f(x)) - n_target, w[i - 1], w[i]))


def symmetric_tolerance(dw, residual_dB, limit_dB):
    """Largest |dW| such that the residual stays below the limit for all smaller |dW|."""
    tol = 0.0
    for t in sorted(set(np.round(np.abs(dw), 6))):
        if (residual_dB[np.abs(dw) <= t + 1e-9] <= limit_dB).all():
            tol = float(t)
        else:
            break
    return tol


class Study:
    def __init__(self, solver, cfg, outdir):
        self.s, self.cfg, self.out = solver, cfg, outdir
        os.makedirs(outdir, exist_ok=True)
        self.cache_file = os.path.join(outdir, "cache.json")
        self.res_file = os.path.join(outdir, "results.json")
        self.cache = json.load(open(self.cache_file)) if os.path.exists(self.cache_file) else {}
        self.res = json.load(open(self.res_file)) if os.path.exists(self.res_file) else {}
        self.n_new = 0

    # ------------------------------------------------------------ solver access
    def solve(self, cores, wavelength, num_modes):
        """Cached mode solve. Returns (n_eff, TE_fraction) sorted by decreasing n_eff."""
        s = self.s
        key = "|".join(str(v) for v in (
            s.resolution, s.side_margin, s.vert_margin, s.h_si, wavelength, num_modes,
            s.fixed_indices, ";".join(f"{c:.2f},{w:.2f}" for c, w in cores)))
        if key not in self.cache:
            neff, te = s.modes(cores, wavelength, num_modes)
            self.cache[key] = [list(map(float, neff)), list(map(float, te))]
            self.n_new += 1
            if self.n_new % 10 == 0:
                self.save()
        neff, te = self.cache[key]
        return np.array(neff), np.array(te)

    def save(self):
        json.dump(self.cache, open(self.cache_file, "w"))
        json.dump(self.res, open(self.res_file, "w"), indent=1)

    def guided(self, cores, wavelength, pol, num_modes):
        """Guided modes of one polarisation ('TE' or 'TM'), highest index first."""
        neff, te = self.solve(cores, wavelength, num_modes)
        keep = (neff > N_GUIDED) & ((te > 0.5) if pol == "TE" else (te <= 0.5))
        return neff[keep]

    def n_iso(self, width, wavelength, order=0, pol="TE"):
        """Effective index of mode `order` of a single strip (NaN if not guided)."""
        n = self.guided([(0.0, float(width))], wavelength, pol, self.cfg["modes_single"])
        return float(n[order]) if len(n) > order else float("nan")

    def splitting(self, wa, gap, wb, wavelength, pol="TE"):
        """Index difference dn_s of the two supermodes built from the access
        fundamental mode and the bus mode it is (nearly) phase matched to."""
        cores = [(0.0, float(wa)), (wa / 2 + gap + wb / 2, float(wb))]
        n = self.guided(cores, wavelength, pol, self.cfg["modes_coupled"])
        if len(n) < 2:
            raise RuntimeError(f"fewer than two guided {pol} modes for {cores}")
        n_a = self.n_iso(wa, wavelength, 0, pol)
        mean = (n[:-1] + n[1:]) / 2                       # neighbouring pairs
        i = int(np.argmin(np.abs(mean - n_a)))            # the pair that sits around n_a
        return float(n[i] - n[i + 1])

    def anticrossing(self, wa, gap, wavelength, wb_guess, pol="TE"):
        """Scan the bus width and fit dn_s^2 = dn_min^2 + [c (W - W_star)]^2."""
        half, step = self.cfg["scan_half_range"], self.cfg["scan_step"]
        for _ in range(5):                                # re-centre until W_star is mid-scan
            centre = step * round(wb_guess / step)
            wb = np.arange(centre - half, centre + half + 1, step, dtype=float)
            dn = np.array([self.splitting(wa, gap, w, wavelength, pol) for w in wb])
            p2, p1, p0 = np.polyfit(wb - centre, dn**2, 2)
            if p2 <= 0:
                raise RuntimeError(f"no anticrossing found near W_bus = {centre} nm (W_a = {wa})")
            w_star = centre - p1 / (2 * p2)
            if abs(w_star - centre) <= step / 2 + 0.5:
                break
            wb_guess = centre + float(np.clip(w_star - centre, -2 * half, 2 * half))
        dn_min2 = p0 - p1**2 / (4 * p2)
        if dn_min2 <= 0:
            raise RuntimeError(f"anticrossing fit failed near W_bus = {centre} nm (W_a = {wa})")
        fit = np.sqrt(dn_min2 + p2 * (wb - w_star) ** 2)
        return dict(wb_star=float(w_star), dn_min=float(math.sqrt(dn_min2)), slope=float(math.sqrt(p2)),
                    scan_w=wb.tolist(), scan_dn=dn.tolist(),
                    fit_rms=float(np.sqrt(np.mean((fit - dn) ** 2))))

    # -------------------------------------------------------------------- steps
    def step_check(self):
        """One single-strip solve: use it to test the link to the solver."""
        wa, wl = self.cfg["baseline"], self.cfg["wavelength"]
        t = time.time()
        neff, te = self.s.modes([(0.0, float(wa))], wl, 4)
        print(f"\nSingle {wa} nm x {self.s.h_si} nm strip at {wl} nm ({time.time() - t:.1f} s):")
        for n, f in zip(neff, te):
            print(f"   n_eff = {n:.4f}   TE fraction = {f:.2f}")
        print("Expected: a TE0 mode with n_eff near 2.2 and TE fraction near 1, then a TM0 mode near 1.7.")
        if hasattr(self.s, "describe"):
            print(self.s.describe())
        if hasattr(self.s, "mode_fields"):                # the field reading used by the 'modes' step
            _, _, f = self.s.mode_fields([(0.0, float(wa))], wl, 4)
            x, y, e = f["x"], f["y"], np.abs(f["Ex"][0]) ** 2
            xc, yc = (round(float((e.sum(axis) * v).sum() / e.sum())) + 0 for axis, v in ((1, x), (0, y)))
            comps = [k for k in ("Ex", "Ey", "Hx", "Hy") if k in f]
            print(f"Fields: {x.size} x {y.size} points, x {x[0]:.0f} to {x[-1]:.0f} nm, "
                  f"y {y[0]:.0f} to {y[-1]:.0f} nm; components {', '.join(comps)}")
            print(f"  TE0 |Ex|^2 is centred at x = {xc:.0f} nm, y = {yc:.0f} nm "
                  "(expected 0, 0: the centre of the strip)")
            if "Hx" not in f:
                print("  No H field: the 'modes' step will weight the modes by their field norm, not by power.")

    def step_sweep(self):
        """Isolated strips: n_eff of TE0, TE1, TE2 against width, and the slopes dn/dW."""
        wl = self.cfg["wavelength"]
        a0, a1, da = self.cfg["access_sweep"]
        b0, b1, db = self.cfg["bus_sweep"]
        widths = sorted(set(np.arange(a0, a1 + 1, da).tolist() + np.arange(b0, b1 + 1, db).tolist()
                            + [float(w) for w in self.cfg["access_widths"]]))
        print(f"\n[sweep] {len(widths)} isolated strips, {widths[0]:.0f}-{widths[-1]:.0f} nm")
        table = {m: [self.n_iso(w, wl, m) for w in widths] for m in (0, 1, 2)}
        self.res["sweep"] = dict(width=widths, TE0=table[0], TE1=table[1], TE2=table[2])
        self.save()

    def _curves(self):
        """Interpolators n_eff(W) for the isolated TE0, TE1, TE2 modes."""
        if "sweep" not in self.res:
            self.step_sweep()
        sw = self.res["sweep"]
        w = np.array(sw["width"])
        out = {}
        for m in (0, 1, 2):
            n = np.array(sw[f"TE{m}"], dtype=float)
            ok = np.isfinite(n)
            out[m] = (w[ok], n[ok], PchipInterpolator(w[ok], n[ok]))
        return out

    def _phase_matched_width(self, n_target, m):
        """Width at which the isolated TEm mode has the index n_target (isolated phase matching)."""
        w, n, _ = self._curves()[m]
        if not (n.min() < n_target < n.max()):
            raise RuntimeError(f"TE{m} never reaches n_eff = {n_target:.3f}: widen bus_sweep")
        return width_at_index(w, n, n_target)

    def step_design(self):
        """Nominal design of both couplers for every access width."""
        cfg, wl, gap = self.cfg, self.cfg["wavelength"], self.cfg["gap"]
        curves = self._curves()
        rows = []
        print(f"\n[design] gap = {gap} nm, wavelength = {wl} nm")
        print("  coupler  W_a   W_bus(isolated)  W_bus(anticrossing)  dn_min    L_c(um)  S_a-S_b(1e-3/nm)")
        for m in cfg["couplers"]:
            for wa in cfg["access_widths"]:
                n_a = self.n_iso(wa, wl)
                wb_iso = self._phase_matched_width(n_a, m)
                s_a = float(curves[0][2].derivative()(wa))            # dn/dW of the access TE0
                s_b = float(curves[m][2].derivative()(wb_iso))        # dn/dW of the bus TEm
                ac = self.anticrossing(wa, gap, wl, wb_iso)
                lc = wl / (2 * ac["dn_min"])
                # First-order coupled-mode estimate: kappa fixed, detuning from the slopes only
                dw = np.arange(0, 40.01, 0.25)
                eta = conversion(ac["dn_min"], (s_a - s_b) * dw, lc, wl)
                tol_cmt = symmetric_tolerance(dw, to_dB(1 - eta), cfg["residual_limit_dB"])
                rows.append(dict(m=m, wa=wa, n_a=n_a, wb_iso=wb_iso, s_a=s_a, s_b=s_b, Lc=lc,
                                 kappa_per_um=math.pi * ac["dn_min"] / wl * 1e3,
                                 fom_nm=ac["dn_min"] / abs(s_a - s_b), tol_cmt=tol_cmt, **ac))
                print(f"  TE0-TE{m}  {wa:4.0f}  {wb_iso:12.1f}  {ac['wb_star']:17.1f}  "
                      f"{ac['dn_min']:9.4f}  {lc / 1e3:7.2f}  {(s_a - s_b) * 1e3:10.3f}")
        self.res["design"] = rows
        self.save()

    def _designs(self):
        if "design" not in self.res:
            self.step_design()
        return self.res["design"]

    def step_tolerance(self):
        """Re-solve each coupler with a uniform width error dW and get eta(dW)."""
        cfg, wl, gap = self.cfg, self.cfg["wavelength"], self.cfg["gap"]
        errors = sorted(cfg["width_errors"])
        fine = np.arange(errors[0], errors[-1] + 0.01, 0.25)
        out = []
        print(f"\n[tolerance] width errors {errors} nm, limit {cfg['residual_limit_dB']} dB")
        for d in self._designs():
            pts = []
            for dw in errors:
                if dw == 0:
                    ac = d
                else:   # every waveguide dW wider, centre lines fixed -> gap shrinks by dW
                    guess = d["wb_star"] + dw * d["s_a"] / d["s_b"]
                    ac = self.anticrossing(d["wa"] + dw, gap - dw, wl, guess)
                dn_det = ac["slope"] * ((d["wb_star"] + dw) - ac["wb_star"])
                pts.append(dict(dw=dw, dn_min=ac["dn_min"], dn_det=dn_det,
                                eta=float(conversion(ac["dn_min"], dn_det, d["Lc"], wl))))
            deg = min(2, len(errors) - 1)
            dn_min_f = np.polyval(np.polyfit(errors, [p["dn_min"] for p in pts], deg), fine)
            dn_det_f = np.polyval(np.polyfit(errors, [p["dn_det"] for p in pts], deg), fine)
            residual = to_dB(1 - conversion(dn_min_f, dn_det_f, d["Lc"], wl))
            tol = symmetric_tolerance(fine, residual, cfg["residual_limit_dB"])
            out.append(dict(m=d["m"], wa=d["wa"], points=pts, dw=fine.tolist(),
                            residual_dB=residual.tolist(), tol=tol,
                            tol_is_lower_bound=bool(tol >= min(-errors[0], errors[-1]) - 1e-9)))
            flag = ">=" if out[-1]["tol_is_lower_bound"] else "  "
            print(f"  TE0-TE{d['m']}  W_a = {d['wa']:4.0f} nm:  tolerance {flag}+/-{tol:4.1f} nm "
                  f"(first-order estimate +/-{d['tol_cmt']:.1f} nm)   "
                  + "  ".join(f"eta({p['dw']:+d})={p['eta']:.3f}" for p in pts))
        self.res["tolerance"] = out
        self.save()

    def step_wavelength(self):
        """Converted power against wavelength for the nominal couplers."""
        cfg, wl0, gap = self.cfg, self.cfg["wavelength"], self.cfg["gap"]
        wls = sorted(cfg["wavelengths"])
        fine = np.arange(wls[0], wls[-1] + 0.01, 1.0)
        band = (fine >= cfg["c_band"][0]) & (fine <= cfg["c_band"][1])
        out = []
        print(f"\n[wavelength] {wls} nm")
        for d in self._designs():
            pts = []
            for wl in wls:
                ac = d if wl == wl0 else self.anticrossing(d["wa"], gap, wl, d["wb_star"])
                dn_det = ac["slope"] * (d["wb_star"] - ac["wb_star"])
                pts.append(dict(wl=wl, dn_min=ac["dn_min"], dn_det=dn_det,
                                eta=float(conversion(ac["dn_min"], dn_det, d["Lc"], wl))))
            deg = min(2, len(wls) - 1)
            dn_min_f = np.polyval(np.polyfit(wls, [p["dn_min"] for p in pts], deg), fine)
            dn_det_f = np.polyval(np.polyfit(wls, [p["dn_det"] for p in pts], deg), fine)
            eta = conversion(dn_min_f, dn_det_f, d["Lc"], fine)
            out.append(dict(m=d["m"], wa=d["wa"], points=pts, wl=fine.tolist(),
                            loss_dB=(-to_dB(eta)).tolist(),
                            worst_residual_c_band_dB=float(to_dB(1 - eta[band]).max())))
            print(f"  TE0-TE{d['m']}  W_a = {d['wa']:4.0f} nm:  worst unconverted power in the C-band "
                  f"{out[-1]['worst_residual_c_band_dB']:6.1f} dB")
        self.res["wavelength"] = out
        self.save()

    def step_bend(self):
        """Bend loss of the access waveguide, which could set a lower limit on its width."""
        cfg, wl = self.cfg, self.cfg["wavelength"]
        out = []
        print("\n[bend] loss of the access waveguide per 90 degree bend")
        for wa in cfg["access_widths"]:
            n0 = self.n_iso(wa, wl)
            for r in cfg["bend_radii"]:
                key = f"bend2|{self.s.resolution}|{wl}|{wa}|{r}"   # bend2: loss referenced to the core radius
                if key not in self.cache:
                    try:
                        self.cache[key] = list(self.s.bend_loss(wa, r, wl, n_guess=n0))
                    except Exception as err:                       # keep the rest of the study alive
                        print(f"  bend solve failed for W_a = {wa}, R = {r}: {err}")
                        self.cache[key] = [float("nan"), float("nan")]
                neff, loss = self.cache[key]
                per90 = loss * (math.pi / 2) * r * 1e-9            # dB/m (at the core) times the arc length in m
                out.append(dict(wa=wa, radius=r, neff=neff, loss_dB_per_m=loss, loss_dB_per_90deg=per90))
                print(f"  W_a = {wa:4.0f} nm, R = {r / 1e3:4.1f} um:  {loss:10.3g} dB/m  = {per90:9.3g} dB per 90 deg")
        self.res["bend"] = out
        self.save()

    def step_validate(self):
        """Checks that the numbers can be trusted: mesh convergence and published designs."""
        cfg, wl, gap, base = self.cfg, self.cfg["wavelength"], self.cfg["gap"], self.cfg["baseline"]
        val = {}
        d1 = next((d for d in self._designs() if d["m"] == 1 and d["wa"] == base), None)
        if d1 is None:
            print("\n[validate] skipped: needs the TE0-TE1 coupler at the baseline access width")
            return

        print("\n[validate] 1. Mesh convergence of the baseline TE0-TE1 coupler")
        print("  grid(nm)  n_eff(TE0, access)  W_bus*(nm)  L_c(um)")
        keep, rows = self.s.resolution, []
        for res in cfg["convergence_resolutions"]:
            self.s.resolution = res
            ac = self.anticrossing(base, gap, wl, d1["wb_star"])
            rows.append(dict(resolution=res, n_a=self.n_iso(base, wl), wb_star=ac["wb_star"],
                             Lc=wl / (2 * ac["dn_min"])))
            print(f"  {res:6.0f}  {rows[-1]['n_a']:14.4f}  {ac['wb_star']:12.1f}  {rows[-1]['Lc'] / 1e3:8.2f}")
        self.s.resolution = keep
        val["convergence"] = rows

        w = WANG_2022
        print("\n[validate] 2. Published TE0-TE1 coupler (Wang et al. 2022: conventional ADC, "
              f"{w['access']} nm access, {w['gap']} nm gap)")
        print(f"  bus width, isolated phase matching:   {d1['wb_iso']:7.1f} nm    paper {w['bus']} nm "
              "(bus of its corrugated coupler)")
        print(f"  bus width, anticrossing (this study): {d1['wb_star']:7.1f} nm")
        print(f"  coupling length from supermodes:      {d1['Lc'] / 1e3:7.2f} um    paper {w['Lc_um']} um")
        val["wang"] = dict(wb_iso=d1["wb_iso"], wb_star=d1["wb_star"], Lc=d1["Lc"], paper=w)

        p = DAI_2013
        print("\n[validate] 3. Published TM0-TM1 coupler (Dai et al. 2013: "
              f"{p['access']} nm access, {p['gap']} nm gap, {p['wavelength']} nm)")
        saved = (self.s.side_margin, self.s.vert_margin, self.s.fixed_indices,
                 cfg["modes_single"], cfg["modes_coupled"])
        self.s.side_margin, self.s.vert_margin = 2000, 1500        # TM modes reach further out
        self.s.fixed_indices = (p["n_si"], p["n_sio2"])            # the paper's constant indices
        cfg["modes_single"], cfg["modes_coupled"] = 12, 14
        try:
            n_a = self.n_iso(p["access"], p["wavelength"], 0, "TM")
            wb = np.arange(900, 1151, 50, dtype=float)
            n_b = np.array([self.n_iso(x, p["wavelength"], 1, "TM") for x in wb])
            ok = np.isfinite(n_b)
            wb_iso = width_at_index(wb[ok], n_b[ok], n_a)
            ac = self.anticrossing(p["access"], p["gap"], p["wavelength"], wb_iso, "TM")
            lc = p["wavelength"] / (2 * ac["dn_min"])
            print(f"  bus width, isolated phase matching:   {wb_iso:7.1f} nm    paper {p['bus']} nm")
            print(f"  bus width, anticrossing:              {ac['wb_star']:7.1f} nm")
            print(f"  coupling length from supermodes:      {lc / 1e3:7.2f} um    paper {p['Lc_um']} um")
            print("  (The paper's lengths are straight sections from 3D FDTD. Its S-bends add coupling,")
            print("   so the straight section is shorter than the supermode coupling length.)")
            val["dai"] = dict(wb_iso=wb_iso, wb_star=ac["wb_star"], Lc=lc, paper=p)
        except Exception as err:
            print(f"  TM benchmark failed: {err}")
        finally:
            self.s.side_margin, self.s.vert_margin, self.s.fixed_indices = saved[:3]
            cfg["modes_single"], cfg["modes_coupled"] = saved[3:]

        if "tolerance" in self.res:
            print("\n[validate] 4. Re-solved tolerance against the first-order coupled-mode estimate")
            for t, d in zip(self.res["tolerance"], self._designs()):
                print(f"  TE0-TE{t['m']}  W_a = {t['wa']:4.0f} nm:  re-solved +/-{t['tol']:4.1f} nm   "
                      f"first-order +/-{d['tol_cmt']:4.1f} nm")
        self.res["validate"] = val
        self.save()

    def step_modes(self):
        """Mode fields of every coupler, saved for figures, and checks that the tolerance
        comes from the intended two-mode coupling and not from something else.

        For each design and each width error in cfg['mode_errors'] (same geometry rule as
        the tolerance step) three cross-sections are solved on the coupler's grid: the
        coupler (two supermodes), the access strip alone (TE0) and the bus strip alone
        (TE1 or TE2). Each supermode is fitted with the two strip modes. Checks:
          share     share of the upper supermode's power in the access mode, from the
                    fit, against the two-mode model of the tolerance step,
                    1/2 (1 - dn_det/dn_s). 0.5 is an even mixture (phase matched).
          dn_s      supermode index difference solved at this exact geometry, against
                    the anticrossing fit the tolerance step uses.
          residual  share of each supermode's field that the two strip modes do not
                    explain: a third mode taking part would show up here.
          edge      share of a mode's field within 300 nm of the window walls.
          tail      access mode alone: |Ex|^2 at the bus edge on the mid-plane, relative
                    to its peak. The coupling strength follows this tail.
        Fields go to <out>/modes/*.npz (read them with modefields.load), the checks to
        results.json ('modes') and modes_summary.csv.
        """
        if not hasattr(self.s, "mode_fields"):
            print("\n[modes] skipped: this solver does not return fields")
            return
        cfg, gap = self.cfg, self.cfg["gap"]
        folder = os.path.join(self.out, "modes")
        os.makedirs(folder, exist_ok=True)
        tol = {(t["m"], t["wa"]): t for t in self.res.get("tolerance", [])}
        print(f"\n[modes] width errors {cfg['mode_errors']} nm; fields saved in {folder}")
        print("                         dn_s (1e-3)     access share of    unconverted at   two-mode")
        print("                                         upper supermode    L_c (dB)         residual")
        print("  coupler  W_a   dW    solved  model     fields  model      fields  model    upper")
        rows = []
        for d in self._designs():
            t = tol.get((d["m"], d["wa"]))
            for dw in cfg["mode_errors"]:
                dw = float(dw)
                cores = [(0.0, d["wa"] + dw), (d["wa"] / 2 + gap + d["wb_star"] / 2, d["wb_star"] + dw)]
                tag = f"TE0-TE{d['m']}_wa{d['wa']:g}_dw{dw:+g}"
                path = os.path.join(folder, tag + ".npz")
                key = "|".join(str(v) for v in (
                    self.s.name, self.s.resolution, self.s.side_margin, self.s.vert_margin, self.s.h_si,
                    cfg["wavelength"], self.s.fixed_indices, cfg["mode_crop"],
                    ";".join(f"{c:.2f},{w:.2f}" for c, w in cores)))
                meta = None
                if os.path.exists(path):
                    try:
                        meta = modefields.load(path)["meta"]
                    except Exception:
                        meta = None
                    if meta is not None and meta.get("key") != key:
                        meta = None                       # saved for another geometry or grid
                if meta is None:
                    meta = self._solve_mode_set(d, dw, cores, key, path, tag)
                r = self._mode_row(d, dw, meta, t)
                rows.append(r)
                print(f"  TE0-TE{d['m']}  {d['wa']:4.0f}  {dw:+4.0f}   {1e3 * r['dn_s']:6.2f} "
                      f"{1e3 * r['dn_s_model']:6.2f}     {r['share_upper']:5.3f}  {r['share_model']:5.3f}      "
                      f"{r['unconverted_fields_dB']:6.1f}  {r['unconverted_model_dB']:6.1f}   "
                      f"{100 * r['residual_upper']:5.2f} %")
        self.res["modes"] = rows
        self.save()
        self._modes_report(rows)

    def _guided_te(self, neff, te):
        """Indices of the guided TE modes, highest index first (neff is sorted)."""
        return [i for i in range(len(neff)) if neff[i] > N_GUIDED and te[i] > 0.5]

    def _solve_mode_set(self, d, dw, cores, key, path, tag):
        """Solve a coupler and its two strips on one grid, check the fields, and save
        them to `path` (no file if path is None). Returns the checks (meta)."""
        s, cfg, wl, m = self.s, self.cfg, self.cfg["wavelength"], d["m"]
        nc, tc, fc = s.mode_fields(cores, wl, cfg["modes_coupled"])
        na, ta, fa = s.mode_fields(cores[:1], wl, cfg["modes_single"], frame=cores)
        nb, tb, fb = s.mode_fields(cores[1:], wl, cfg["modes_single"], frame=cores)
        self.n_new += 3
        x, y = fc["x"], fc["y"]
        for f in (fa, fb):
            if f["x"].shape != x.shape or f["y"].shape != y.shape or not (
                    np.allclose(f["x"], x) and np.allclose(f["y"], y)):
                raise RuntimeError(f"{tag}: the strip solves are not on the coupler's grid")
        ga, gb, gc = self._guided_te(na, ta), self._guided_te(nb, tb), self._guided_te(nc, tc)
        if not ga or len(gb) <= m or len(gc) < 2:
            raise RuntimeError(f"{tag}: guided TE modes missing (access {len(ga)}, bus {len(gb)}, "
                               f"coupler {len(gc)})")
        n_a = self.n_iso(cores[0][1], wl)                 # picks the supermode pair, as in splitting()
        k = int(np.argmin(np.abs((nc[gc[:-1]] + nc[gc[1:]]) / 2 - n_a)))
        iu, il = gc[k], gc[k + 1]

        comps = ("Ex", "Ey", "Hx", "Hy") if all("Hx" in f and "Hy" in f for f in (fa, fb, fc)) else ("Ex", "Ey")
        w = modefields.weights(x, y)

        def mode(f, i):
            return modefields.normalised({c: f[c][i] for c in comps}, w)

        (x_acc, _), (x_bus, w_bus) = cores
        lobe = (x_bus - w_bus / 2 + w_bus / (2 * (m + 1)), 0.0)   # centre of the bus lobe next to the gap
        acc, bus = mode(fa, ga[0]), mode(fb, gb[m])
        acc = modefields.rotated(acc, modefields.phase_at(acc, x, y, (x_acc, 0.0)))
        bus = modefields.rotated(bus, modefields.phase_at(bus, x, y, lobe))
        out, checks = dict(access=acc, bus=bus), {}
        for name, i in (("upper", iu), ("lower", il)):
            sup = mode(fc, i)
            alpha, beta, share, residual = modefields.decompose(sup, acc, bus, w)
            out[name] = modefields.rotated(sup, np.conj(alpha) / abs(alpha))
            checks[name] = dict(share=share, residual=residual,
                                bus_sign=int(np.sign(np.real(beta * np.conj(alpha)))))
        picked = dict(access=(na, ta, ga[0]), bus=(nb, tb, gb[m]), upper=(nc, tc, iu), lower=(nc, tc, il))
        meta = dict(key=key, tag=tag, backend=s.name, resolution=s.resolution, wavelength=wl, h_si=s.h_si,
                    coupler=m, access_width=d["wa"], width_error=dw,
                    cores=[[float(c), float(cw)] for c, cw in cores],
                    norm="power" if "Hx" in comps else "field",
                    modes={n: dict(neff=float(nn[i]), te=float(tt[i])) for n, (nn, tt, i) in picked.items()},
                    checks=checks, dn_s=float(nc[iu] - nc[il]),
                    tail_dB=modefields.level_dB(acc, x, y, x_bus - w_bus / 2),
                    edge_fraction=max(modefields.edge_fraction(f, x, y, w) for f in out.values()),
                    imaginary_fraction=max(modefields.imaginary_fraction(f, w) for f in out.values()))
        if path is not None:
            c = cfg["mode_crop"]
            xlim = (min(cc - cw / 2 for cc, cw in cores) - c, max(cc + cw / 2 for cc, cw in cores) + c)
            modefields.save(path, x, y, out, meta, xlim, (-s.h_si / 2 - c, s.h_si / 2 + c))
        return meta

    # ------------------------------------------------- bus at the phase-matched width
    def _matched_set(self, d, wb, dw):
        """Checks of one coupler with its bus at width wb (nominal), under width error dw.
        Cached in cache.json, without fields."""
        gap, wl = self.cfg["gap"], self.cfg["wavelength"]
        cores = [(0.0, d["wa"] + dw), (d["wa"] / 2 + gap + wb / 2, wb + dw)]
        s = self.s
        key = "set|" + "|".join(str(v) for v in (
            s.name, s.resolution, s.side_margin, s.vert_margin, s.h_si, wl, s.fixed_indices,
            ";".join(f"{c:.2f},{w:.2f}" for c, w in cores)))
        if key not in self.cache:
            self.cache[key] = self._solve_mode_set(d, dw, cores, key, None, f"matched TE0-TE{d['m']}")
        return self.cache[key]

    def step_matched(self):
        """Tolerance of each coupler rebuilt with its bus at the phase-matched width.

        The 'modes' step shows that W*, the anticrossing minimum, is wider than the bus
        width at which the supermodes are an even mixture. Here each coupler is rebuilt
        with its bus at that width, W_pm, and its tolerance is taken from the fields:
          1. W_pm from the 'modes' step, checked with one solve and corrected (at most
             twice) until the upper supermode's access share is 0.5 +/- 0.02;
          2. for each dW in cfg['matched_errors'] (access W_a + dW, bus W_pm + dW,
             gap g - dW, centre lines fixed) the coupler and its two strips are solved;
             the access share s gives dn_det = (1 - 2 s) dn_s and
             dn_min = 2 sqrt(s (1 - s)) dn_s;
          3. the coupler length is L_pm = lambda / (2 dn_s) at dW = 0, and with quadratic
             fits of dn_min and dn_det over dW the converted power is the tolerance
             step's eta(dn_min, dn_det, L_pm);
          4. tolerance = largest |dW| for which 1 - eta stays below the limit.
        """
        cfg, wl = self.cfg, self.cfg["wavelength"]
        if not hasattr(self.s, "mode_fields"):
            print("\n[matched] skipped: this solver does not return fields")
            return
        if "modes" not in self.res:
            self.step_modes()
        even = {(r["m"], r["wa"]): r["wb_even_fields"] for r in self.res["modes"] if r["dw"] == 0}
        errors = sorted(float(e) for e in cfg["matched_errors"])
        if 0.0 not in errors:
            errors = sorted(errors + [0.0])
        fine = np.arange(errors[0], errors[-1] + 0.01, 0.25)
        tol_w = {(t["m"], t["wa"]): t["tol"] for t in self.res.get("tolerance", [])}
        print(f"\n[matched] bus at the phase-matched width; width errors {errors} nm")
        print("  coupler  W_a    W*      W_pm   share   L_c(W*)  L_pm(um)  tolerance: model at W*  fields at W_pm")
        out = []
        for d in self._designs():
            wb = even.get((d["m"], d["wa"]), d["wb_iso"])
            for attempt in range(3):                      # check; correct at most twice, then re-check
                meta = self._matched_set(d, wb, 0.0)
                s0 = meta["checks"]["upper"]["share"]
                if abs(s0 - 0.5) <= 0.02:
                    break
                if attempt < 2:
                    wb -= (1 - 2 * s0) * meta["dn_s"] / d["s_b"]
            else:
                print(f"  warning: TE0-TE{d['m']} W_a = {d['wa']:g} nm: access share {s0:.3f} "
                      f"after two corrections; W_pm = {wb:.1f} nm is kept")
            pts = []
            for dw in errors:
                meta = self._matched_set(d, wb, dw)
                s, dn_s = meta["checks"]["upper"]["share"], meta["dn_s"]
                pts.append(dict(dw=dw, share=s, dn_s=dn_s, dn_det=(1 - 2 * s) * dn_s,
                                dn_min=2 * math.sqrt(s * (1 - s)) * dn_s,
                                residual=max(meta["checks"]["upper"]["residual"],
                                             meta["checks"]["lower"]["residual"])))
            p0 = next(p for p in pts if p["dw"] == 0)
            L_pm = wl / (2 * p0["dn_s"])
            for p in pts:
                p["eta"] = float(conversion(p["dn_min"], p["dn_det"], L_pm, wl))
            deg = min(2, len(errors) - 1)
            dn_min_f = np.polyval(np.polyfit(errors, [p["dn_min"] for p in pts], deg), fine)
            dn_det_f = np.polyval(np.polyfit(errors, [p["dn_det"] for p in pts], deg), fine)
            residual = to_dB(1 - conversion(dn_min_f, dn_det_f, L_pm, wl))
            tol = symmetric_tolerance(fine, residual, cfg["residual_limit_dB"])
            out.append(dict(m=d["m"], wa=d["wa"], wb_star=d["wb_star"], wb_iso=d["wb_iso"], wb_pm=float(wb),
                            share0=p0["share"], Lc_star=d["Lc"], Lc_pm=float(L_pm), points=pts,
                            dw=fine.tolist(), residual_dB=residual.tolist(), tol=tol,
                            tol_is_lower_bound=bool(tol >= min(-errors[0], errors[-1]) - 1e-9),
                            tol_model=tol_w.get((d["m"], d["wa"]), float("nan"))))
            r = out[-1]
            print(f"  TE0-TE{d['m']}  {d['wa']:4.0f}  {d['wb_star']:7.1f}  {wb:7.1f}  {p0['share']:5.3f}"
                  f"  {d['Lc'] / 1e3:7.2f}  {L_pm / 1e3:7.2f}        +/-{r['tol_model']:4.2f}"
                  f"          +/-{tol:4.2f}")
            self.save()                                   # keep the solved sets if a later one fails
        self.res["matched"] = out
        self.save()

    def _model_at(self, t, dw):
        """dn_min and dn_det of the tolerance step's two-mode model at width error dw."""
        pts = t["points"]
        p = next((p for p in pts if abs(p["dw"] - dw) < 1e-9), None)
        if p is not None:
            return p["dn_min"], p["dn_det"]
        e = [p["dw"] for p in pts]
        if not min(e) <= dw <= max(e):
            return float("nan"), float("nan")
        deg = min(2, len(e) - 1)
        return (float(np.polyval(np.polyfit(e, [p["dn_min"] for p in pts], deg), dw)),
                float(np.polyval(np.polyfit(e, [p["dn_det"] for p in pts], deg), dw)))

    def _mode_row(self, d, dw, meta, t):
        """One line of the field checks, next to the two-mode model of the tolerance step.

        In two-mode coupled-mode theory the upper supermode's access share s fixes the
        detuning, dn_det = (1 - 2 s) dn_s (= n_bus - n_access; > 0: the bus is too wide),
        and the largest convertible power, 4 s (1 - s). At the nominal coupler length L_c:
            eta = 4 s (1 - s) sin^2(pi dn_s L_c / lambda)
        which is the tolerance step's formula with the mixing measured on the fields.
        """
        ck, md, wl = meta["checks"], meta["modes"], self.cfg["wavelength"]
        s_u, dn_s = ck["upper"]["share"], meta["dn_s"]
        eta = 4 * s_u * (1 - s_u) * np.sin(np.pi * dn_s * d["Lc"] / wl) ** 2
        row = dict(m=d["m"], wa=d["wa"], dw=dw, file=f"modes/{meta['tag']}.npz", norm=meta["norm"],
                   wb_star=d["wb_star"], wb_iso=d["wb_iso"], s_b=d["s_b"], Lc=d["Lc"],
                   n_access=md["access"]["neff"], n_bus=md["bus"]["neff"],
                   n_upper=md["upper"]["neff"], n_lower=md["lower"]["neff"],
                   te_upper=md["upper"]["te"], te_lower=md["lower"]["te"], dn_s=dn_s,
                   share_upper=s_u, share_lower=ck["lower"]["share"],
                   residual_upper=ck["upper"]["residual"], residual_lower=ck["lower"]["residual"],
                   bus_sign_upper=ck["upper"]["bus_sign"], bus_sign_lower=ck["lower"]["bus_sign"],
                   dn_det_fields=(1 - 2 * s_u) * dn_s, eta_fields=float(eta),
                   unconverted_fields_dB=float(to_dB(1 - eta)),
                   tail_dB=meta["tail_dB"], edge_fraction=meta["edge_fraction"])
        # Bus width at which the nominal coupler's supermodes would be an even mixture:
        # W* moved by the detuning the fields show, over the bus slope dn/dW.
        row["wb_even_fields"] = float(d["wb_star"] - row["dn_det_fields"] / d["s_b"]) if dw == 0 else float("nan")
        dn_min, dn_det = self._model_at(t, dw) if t else (float("nan"), float("nan"))
        dn_s_model = float(np.hypot(dn_min, dn_det))
        eta_model = float(conversion(dn_min, dn_det, d["Lc"], wl))
        row.update(dn_min_model=dn_min, dn_det_model=dn_det, dn_s_model=dn_s_model,
                   share_model=0.5 * (1 - dn_det / dn_s_model) if dn_s_model > 0 else float("nan"),
                   eta_model=eta_model,
                   unconverted_model_dB=float(to_dB(1 - eta_model)) if np.isfinite(eta_model) else float("nan"))
        return row

    def _modes_report(self, rows):
        """Summary of the field checks, and modes_summary.csv."""
        fin = [r for r in rows if np.isfinite(r["share_model"])]
        res = max(max(r["residual_upper"], r["residual_lower"]) for r in rows)
        sign = all(r["bus_sign_upper"] > 0 and r["bus_sign_lower"] < 0 for r in rows)
        print("\n  Is the coupling the intended two-mode coupling?")
        print(f"    The two strip modes explain each supermode to within {100 * res:.2f} % of its field "
              "(largest residual).")
        if fin:
            dn = max(abs(r["dn_s"] - r["dn_s_model"]) / r["dn_s_model"] for r in fin)
            print(f"    Supermode splitting solved at the exact geometry against the anticrossing fit: "
                  f"largest difference {100 * dn:.1f} %.")
        print(f"    Upper supermode in phase and lower in anti-phase across the gap in every case: {sign}.")
        print(f"    Lowest TE fraction of a supermode {min(min(r['te_upper'], r['te_lower']) for r in rows):.3f}; "
              f"largest share of a field within 300 nm of the window walls "
              f"{max(r['edge_fraction'] for r in rows):.1e}.")
        nominal = [r for r in rows if r["dw"] == 0]
        tails = {r["wa"]: r["tail_dB"] for r in nominal}
        if tails:
            print("  Why the coupling is stronger: |Ex|^2 of the access mode alone at the bus edge, "
                  "relative to its peak:")
            print("    " + ", ".join(f"{wa:.0f} nm: {v:.1f} dB" for wa, v in sorted(tails.items())))
        if nominal:
            print("  Phase matching of the nominal designs (dW = 0). The model assumes the upper supermode is")
            print("  an even mixture (access share 0.5) at the anticrossing minimum W*. The fields give:")
            print("    coupler  W_a   access share  unconverted   bus width (nm): anticrossing  isolated   "
                  "even mixture")
            print("                   (fields)      at L_c (dB)                   minimum W*    W_iso      (fields)")
            for r in nominal:
                print(f"    TE0-TE{r['m']}  {r['wa']:4.0f}     {r['share_upper']:5.3f}      "
                      f"{r['unconverted_fields_dB']:6.1f}                     {r['wb_star']:7.1f}     "
                      f"{r['wb_iso']:7.1f}     {r['wb_even_fields']:7.1f}")
            print("    'even mixture' is W* moved by the detuning the fields show, dn_det = (1 - 2 share) dn_s,")
            print("    divided by the bus slope dn/dW.")
        if fin:
            ds = max(abs(r["share_upper"] - r["share_model"]) for r in fin)
            print(f"  Access share of the upper supermode, fields against the model: largest difference {ds:.3f}.")
        else:
            print("  No tolerance results: the fields were not compared with the two-mode model.")

        path = os.path.join(self.out, "modes_summary.csv")
        cols = [("coupler", lambda r: f"TE0-TE{r['m']}"), ("access_width_nm", lambda r: f"{r['wa']:g}"),
                ("width_error_nm", lambda r: f"{r['dw']:g}"), ("n_upper", lambda r: f"{r['n_upper']:.5f}"),
                ("n_lower", lambda r: f"{r['n_lower']:.5f}"),
                ("dn_s_solved", lambda r: f"{r['dn_s']:.6f}"), ("dn_s_model", lambda r: f"{r['dn_s_model']:.6f}"),
                ("access_share_upper_fields", lambda r: f"{r['share_upper']:.4f}"),
                ("access_share_upper_model", lambda r: f"{r['share_model']:.4f}"),
                ("access_share_lower_fields", lambda r: f"{r['share_lower']:.4f}"),
                ("detuning_fields", lambda r: f"{r['dn_det_fields']:.6f}"),
                ("detuning_model", lambda r: f"{r['dn_det_model']:.6f}"),
                ("unconverted_at_Lc_fields_dB", lambda r: f"{r['unconverted_fields_dB']:.2f}"),
                ("unconverted_at_Lc_model_dB", lambda r: f"{r['unconverted_model_dB']:.2f}"),
                ("residual_upper", lambda r: f"{r['residual_upper']:.5f}"),
                ("residual_lower", lambda r: f"{r['residual_lower']:.5f}"),
                ("te_fraction_upper", lambda r: f"{r['te_upper']:.4f}"),
                ("te_fraction_lower", lambda r: f"{r['te_lower']:.4f}"),
                ("access_tail_at_bus_dB", lambda r: f"{r['tail_dB']:.2f}"),
                ("edge_fraction", lambda r: f"{r['edge_fraction']:.2e}"),
                ("bus_width_even_mixture_nm",
                 lambda r: f"{r['wb_even_fields']:.1f}" if np.isfinite(r["wb_even_fields"]) else ""),
                ("file", lambda r: r["file"])]
        with open(path, "w") as f:
            f.write(",".join(c for c, _ in cols) + "\n")
            for r in rows:
                f.write(",".join(fn(r) for _, fn in cols) + "\n")
        print(f"  Mode summary table: {path}")

    def step_plots(self):
        import plots
        plots.make_all(self.res, self.cfg, self.out)

    def write_summary(self):
        """One table with the main numbers, as CSV."""
        if not {"design", "tolerance"} <= set(self.res):
            return
        wav = {(w["m"], w["wa"]): w for w in self.res.get("wavelength", [])}
        mat = {(r["m"], r["wa"]): r for r in self.res.get("matched", [])}
        path = os.path.join(self.out, "summary.csv")
        with open(path, "w") as f:
            f.write("coupler,access_width_nm,bus_width_nm,coupling_length_um,kappa_per_um,"
                    "sensitivity_mismatch_per_nm,tolerance_nm,tolerance_is_lower_bound,"
                    "tolerance_first_order_nm,worst_residual_c_band_dB"
                    + (",bus_width_phase_matched_nm,coupling_length_phase_matched_um,"
                       "tolerance_phase_matched_nm" if mat else "") + "\n")
            for d, t in zip(self._designs(), self.res["tolerance"]):
                w = wav.get((d["m"], d["wa"]), {})
                f.write(f"TE0-TE{d['m']},{d['wa']},{d['wb_star']:.1f},{d['Lc'] / 1e3:.2f},"
                        f"{d['kappa_per_um']:.4f},{d['s_a'] - d['s_b']:.5f},{t['tol']:.2f},"
                        f"{t['tol_is_lower_bound']},{d['tol_cmt']:.2f},"
                        f"{w.get('worst_residual_c_band_dB', float('nan')):.1f}")
                if mat:
                    r = mat.get((d["m"], d["wa"]))
                    f.write(f",{r['wb_pm']:.1f},{r['Lc_pm'] / 1e3:.2f},{r['tol']:.2f}" if r else ",,,")
                f.write("\n")
        print(f"\nSummary table: {path}")


STEPS = ["sweep", "design", "tolerance", "wavelength", "bend", "validate", "modes", "matched", "plots"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", choices=["emode"], default="emode",
                    help="the mode solver: EMode2D, the only one (kept so earlier command lines still work)")
    ap.add_argument("--quick", action="store_true", help="coarse grid and fewer points")
    ap.add_argument("--steps", default=",".join(STEPS), help="comma-separated: check," + ",".join(STEPS))
    ap.add_argument("--resolution", type=float, help="grid step in nm (overrides the configuration)")
    ap.add_argument("--couplers", default="1,2", help="which couplers to run: 1 = TE0-TE1, 2 = TE0-TE2")
    ap.add_argument("--access", help="access widths in nm, comma-separated (overrides the configuration)")
    ap.add_argument("--out", help="results folder (default results_emode[_quick] next to this script)")
    args = ap.parse_args()

    cfg = dict(CFG, **(QUICK if args.quick else {}))
    if args.resolution:                               # 10, not 10.0: the cache keys contain it as text
        cfg["resolution"] = int(args.resolution) if args.resolution.is_integer() else args.resolution
    cfg["couplers"] = [int(c) for c in args.couplers.split(",")]
    if args.access:
        cfg["access_widths"] = [float(w) for w in args.access.split(",")]
    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    # Default results folder next to this script, so the run finds earlier results
    # (and its cache) wherever it is started from.
    outdir = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "results_emode" + ("_quick" if args.quick else ""))

    if steps == ["plots"]:
        import plots
        plots.make_all(json.load(open(os.path.join(outdir, "results.json"))), cfg, outdir)
        return
    os.makedirs(outdir, exist_ok=True)
    from solver_emode import EModeSolver
    solver = EModeSolver(resolution=cfg["resolution"], save_path=outdir)       # adc_study.eph goes there

    study, t0 = Study(solver, cfg, outdir), time.time()
    try:
        for step in steps:
            getattr(study, f"step_{step}")()
        study.write_summary()
    finally:
        study.save()
        solver.close()
    print(f"\nDone in {(time.time() - t0) / 60:.1f} min, {study.n_new} new mode solves. Results in {outdir}/")


if __name__ == "__main__":
    main()
