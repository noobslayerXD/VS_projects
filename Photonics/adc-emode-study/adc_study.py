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

1. Scan the bus width through the anticrossing. dn_s is smallest where the two
   strips are phase matched:
        dn_s(W_bus)^2 = dn_min^2 + [c * (W_bus - W_star)]^2
   W_star is the phase-matched bus width, dn_min gives the coupling coefficient
   kappa = pi*dn_min/lambda and the coupling length L_c = lambda/(2*dn_min).
2. For a coupler that is detuned (wrong width or wavelength) the converted power
   after a length L is (two-mode coupled-mode theory):
        eta = (dn_min/dn_s)^2 * sin^2(pi * dn_s * L / lambda)
   The first factor is the phase-matching penalty, the second the length penalty.
3. Fabrication tolerance: every waveguide is dW wider (dW < 0: narrower) while the
   centre lines stay where they are. So access -> W_a + dW, bus -> W_star + dW and
   gap -> gap - dW. The coupler length stays at the nominal L_c. The tolerance is
   the largest |dW| for which the unconverted power 1 - eta stays below -15 dB.

Usage
-----
    python adc_study.py --backend emode --steps check     # one solve, tests the EMode link
    python adc_study.py --backend emode --quick           # coarse first look (minutes)
    python adc_study.py --backend emode                   # full study
    python adc_study.py --backend empy --quick            # open-source cross-check, no EMode
    python adc_study.py --backend emode --steps plots     # redraw figures from saved results

Steps: check, sweep, design, tolerance, wavelength, bend, validate, plots.
Solved cross-sections are cached in results_<backend>/cache.json, so a rerun only
solves what is new. Delete that file to force new solves.
"""
import argparse
import json
import math
import os
import time

import numpy as np
from scipy.interpolate import PchipInterpolator

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
        w, n, _ = self._curves()[m]
        if not (n.min() < n_target < n.max()):
            raise RuntimeError(f"TE{m} never reaches n_eff = {n_target:.3f}: widen bus_sweep")
        return float(np.interp(n_target, n, w))

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
        """Bend loss of the access waveguide: the practical lower limit on its width."""
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
        self.s.fixed_indices = (p["n_si"], p["n_sio2"])            # the paper's constant indices (both backends)
        cfg["modes_single"], cfg["modes_coupled"] = 12, 14
        try:
            n_a = self.n_iso(p["access"], p["wavelength"], 0, "TM")
            wb = np.arange(900, 1151, 50, dtype=float)
            n_b = np.array([self.n_iso(x, p["wavelength"], 1, "TM") for x in wb])
            ok = np.isfinite(n_b)
            wb_iso = float(np.interp(n_a, n_b[ok], wb[ok]))
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

    def step_plots(self):
        import plots
        plots.make_all(self.res, self.cfg, self.out, self.s.name)

    def write_summary(self):
        """One table with the main numbers, as CSV."""
        if not {"design", "tolerance"} <= set(self.res):
            return
        wav = {(w["m"], w["wa"]): w for w in self.res.get("wavelength", [])}
        path = os.path.join(self.out, "summary.csv")
        with open(path, "w") as f:
            f.write("coupler,access_width_nm,bus_width_nm,coupling_length_um,kappa_per_um,"
                    "sensitivity_mismatch_per_nm,tolerance_nm,tolerance_is_lower_bound,"
                    "tolerance_first_order_nm,worst_residual_c_band_dB\n")
            for d, t in zip(self._designs(), self.res["tolerance"]):
                w = wav.get((d["m"], d["wa"]), {})
                f.write(f"TE0-TE{d['m']},{d['wa']},{d['wb_star']:.1f},{d['Lc'] / 1e3:.2f},"
                        f"{d['kappa_per_um']:.4f},{d['s_a'] - d['s_b']:.5f},{t['tol']:.2f},"
                        f"{t['tol_is_lower_bound']},{d['tol_cmt']:.2f},"
                        f"{w.get('worst_residual_c_band_dB', float('nan')):.1f}\n")
        print(f"\nSummary table: {path}")


STEPS = ["sweep", "design", "tolerance", "wavelength", "bend", "validate", "plots"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", choices=["emode", "empy"], default="emode")
    ap.add_argument("--quick", action="store_true", help="coarse grid and fewer points")
    ap.add_argument("--steps", default=",".join(STEPS), help="comma-separated: check," + ",".join(STEPS))
    ap.add_argument("--resolution", type=float, help="grid step in nm (overrides the configuration)")
    ap.add_argument("--couplers", default="1,2", help="which couplers to run: 1 = TE0-TE1, 2 = TE0-TE2")
    ap.add_argument("--access", help="access widths in nm, comma-separated (overrides the configuration)")
    ap.add_argument("--out", help="results folder (default results_<backend>[_quick])")
    args = ap.parse_args()

    cfg = dict(CFG, **(QUICK if args.quick else {}))
    if args.resolution:
        cfg["resolution"] = args.resolution
    cfg["couplers"] = [int(c) for c in args.couplers.split(",")]
    if args.access:
        cfg["access_widths"] = [float(w) for w in args.access.split(",")]
    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    outdir = args.out or f"results_{args.backend}" + ("_quick" if args.quick else "")

    if steps == ["plots"]:
        import plots
        plots.make_all(json.load(open(os.path.join(outdir, "results.json"))), cfg, outdir, args.backend)
        return
    os.makedirs(outdir, exist_ok=True)
    if args.backend == "emode":
        from solver_emode import EModeSolver
        solver = EModeSolver(resolution=cfg["resolution"], save_path=outdir)   # adc_study.eph goes there
    else:
        from solver_empy import EMpySolver
        solver = EMpySolver(resolution=cfg["resolution"])

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
