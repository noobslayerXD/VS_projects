"""Figures for the ADC tolerance study. Reads the results dictionary written by adc_study.py."""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3de"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"          # one colour per mode / coupler
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]  # light -> dark = narrow -> wide access
COUPLER = {1: ("TE$_0$→TE$_1$", BLUE), 2: ("TE$_0$→TE$_2$", ORANGE)}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "font.size": 9, "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": "#c9c8c2", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "lines.linewidth": 1.8, "lines.markersize": 6.5, "lines.markeredgecolor": SURFACE,
    "lines.markeredgewidth": 1.2, "legend.frameon": False, "legend.fontsize": 8.5,
    "xtick.major.size": 0, "ytick.major.size": 0, "figure.dpi": 110, "savefig.dpi": 200,
})


def _ramp(widths):
    """One blue step per access width (the widths are an ordered quantity)."""
    widths = sorted(widths)
    idx = np.round(np.linspace(0, len(RAMP) - 1, len(widths))).astype(int)
    return {w: RAMP[i] for w, i in zip(widths, idx)}


def _save(fig, outdir, name, note):
    fig.text(0.995, -0.035, note, ha="right", va="top", fontsize=6.5, color=INK2)
    path = os.path.join(outdir, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", path)


def fig_phase_matching(res, cfg, outdir, note):
    sw, base = res["sweep"], cfg["baseline"]
    w = np.array(sw["width"])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for m, col in zip((0, 1, 2), (BLUE, ORANGE, AQUA)):
        n = np.array(sw[f"TE{m}"], dtype=float)
        ok = np.isfinite(n)
        ax.plot(w[ok], n[ok], color=col, label=f"TE$_{m}$")
        ax.annotate(f"TE$_{m}$", (w[ok][-1], n[ok][-1]), xytext=(5, 0), textcoords="offset points",
                    va="center", color=INK)
    if "design" in res:
        n_a = next(d["n_a"] for d in res["design"] if d["wa"] == base)
        xs = [base] + [d["wb_iso"] for d in res["design"] if d["wa"] == base]
        ax.plot([base, max(xs)], [n_a, n_a], color=INK2, lw=0.9, ls=(0, (4, 3)), zorder=1)
        ax.plot(xs, [n_a] * len(xs), "o", color=INK, zorder=3)
        ax.annotate(f"access TE$_0$, {base:.0f} nm", (base, n_a), xytext=(8, 6), textcoords="offset points",
                    fontsize=8, color=INK2)
        for x, lab in zip(xs[1:], ("W$_1$", "W$_2$")):
            ax.annotate(f"{lab} = {x:.0f} nm", (x, n_a), xytext=(4, -13), textcoords="offset points",
                        fontsize=8, color=INK2)
    ax.set_xlabel("Strip width (nm)")
    ax.set_ylabel("Effective index")
    ax.set_title("Phase matching: equal effective index sets the bus widths")
    ax.legend(loc="lower right")
    _save(fig, outdir, "fig1_phase_matching.png", note)


def fig_anticrossing(res, cfg, outdir, note):
    base = cfg["baseline"]
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.3), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        d = next((d for d in res["design"] if d["m"] == m and d["wa"] == base), None)
        if d is None:
            ax.set_axis_off()
            continue
        name, col = COUPLER[m]
        w = np.array(d["scan_w"])
        wf = np.linspace(w[0], w[-1], 200)
        ax.plot(wf, 1e3 * np.hypot(d["dn_min"], d["slope"] * (wf - d["wb_star"])), color=col, label="fit")
        ax.plot(w, 1e3 * np.array(d["scan_dn"]), "o", color=INK, label="mode solves")
        ax.plot([d["wb_star"]] * 2, [0, 1e3 * d["dn_min"]], color=INK2, lw=0.9, ls=(0, (4, 3)))
        ax.set_ylim(bottom=0)
        ax.set_title(f"{name}:  W* = {d['wb_star']:.0f} nm,  L$_c$ = {d['Lc'] / 1e3:.1f} µm")
        ax.set_xlabel("Bus width (nm)")
        ax.legend(loc="upper center")
    axes[0].set_ylabel("Supermode splitting Δn$_s$ (10$^{-3}$)")
    fig.suptitle(f"Anticrossing scan of the baseline coupler (access {base:.0f} nm, gap {cfg['gap']} nm)",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig2_anticrossing.png", note)


def fig_design(res, cfg, outdir, note):
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.2))
    panels = [("Coupling length L$_c$ (µm)", lambda d: d["Lc"] / 1e3, "Narrower access: shorter coupler"),
              ("S$_a$ − S$_m$ (10$^{-3}$ per nm)", lambda d: 1e3 * (d["s_a"] - d["s_b"]),
               "…but a larger sensitivity mismatch"),
              ("Δn$_{min}$ / (S$_a$ − S$_m$) (nm)", lambda d: d["fom_nm"], "Coupling strength over mismatch")]
    for ax, (ylab, f, title) in zip(axes, panels):
        for m in (1, 2):
            name, col = COUPLER[m]
            ds = [d for d in res["design"] if d["m"] == m]
            ax.plot([d["wa"] for d in ds], [f(d) for d in ds], "o-", color=col, label=name)
        ax.set_xlabel("Access width W$_a$ (nm)")
        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.set_ylim(bottom=0)
    axes[0].legend(loc="upper left")
    fig.tight_layout()
    _save(fig, outdir, "fig3_design.png", note)


def fig_tolerance_curves(res, cfg, outdir, note):
    lim = cfg["residual_limit_dB"]
    ramp = _ramp(cfg["access_widths"])
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        for t in [t for t in res["tolerance"] if t["m"] == m]:
            ax.plot(t["dw"], t["residual_dB"], color=ramp[t["wa"]], label=f"{t['wa']:.0f} nm")
            ax.plot([p["dw"] for p in t["points"]], [float(10 * np.log10(max(1 - p["eta"], 1e-6))) for p in t["points"]],
                    "o", color=ramp[t["wa"]], ms=5)
        ax.axhline(lim, color=INK2, lw=0.9, ls=(0, (4, 3)))
        ax.annotate(f"limit {lim:.0f} dB", (ax.get_xlim()[0], lim), xytext=(4, 3), textcoords="offset points",
                    fontsize=8, color=INK2)
        ax.set_title(COUPLER[m][0])
        ax.set_xlabel("Uniform width error ΔW (nm)")
        ax.set_ylim(-45, 0)
    axes[0].set_ylabel("Unconverted power (dB)")
    axes[1].legend(title="Access width", loc="lower right", ncol=2)
    fig.suptitle("Unconverted power against width error at fixed coupler length",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig4_tolerance_curves.png", note)


def fig_tolerance_summary(res, cfg, outdir, note):
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        name, col = COUPLER[m]
        ts = [t for t in res["tolerance"] if t["m"] == m]
        ds = [d for d in res["design"] if d["m"] == m]
        wa = [t["wa"] for t in ts]
        ax.plot(wa, [t["tol"] for t in ts], "o-", color=col, label="re-solved supermodes")
        ax.plot(wa, [d["tol_cmt"] for d in ds], "s", ls=(0, (4, 3)), color=INK2, label="first-order estimate")
        for t in ts:
            if t["tol_is_lower_bound"]:
                ax.annotate("≥", (t["wa"], t["tol"]), xytext=(0, 6), textcoords="offset points",
                            ha="center", fontsize=9, color=INK)
        ax.set_title(name)
        ax.set_xlabel("Access width W$_a$ (nm)")
        ax.set_ylim(bottom=0)
    axes[0].set_ylabel(f"Width tolerance ±ΔW (nm) at {cfg['residual_limit_dB']:.0f} dB")
    axes[0].legend(loc="upper right")
    fig.suptitle("Width tolerance against access width", x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig5_tolerance_summary.png", note)


def fig_wavelength(res, cfg, outdir, note):
    ramp = _ramp(cfg["access_widths"])
    top = 1.08 * max(max(w["loss_dB"]) for w in res["wavelength"])
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        ax.axvspan(*cfg["c_band"], color="#efeeea", zorder=0)
        for w in [w for w in res["wavelength"] if w["m"] == m]:
            ax.plot(w["wl"], w["loss_dB"], color=ramp[w["wa"]], label=f"{w['wa']:.0f} nm")
        ax.set_title(COUPLER[m][0])
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylim(0, top)
        ax.annotate("C-band", (np.mean(cfg["c_band"]), top), xytext=(0, -11),
                    textcoords="offset points", ha="center", fontsize=8, color=INK2)
    axes[0].set_ylabel("Conversion loss (dB)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title="Access width", loc="lower center", ncol=len(labels),
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Conversion loss against wavelength at fixed coupler length",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    _save(fig, outdir, "fig6_wavelength.png", note)


def fig_bend(res, cfg, outdir, note):
    rows = [b for b in res["bend"] if np.isfinite(b["loss_dB_per_90deg"]) and b["loss_dB_per_90deg"] > 0]
    if not rows:
        print("  no bend-loss data (this solver has no bend solver): fig7 skipped")
        return
    radii = sorted({b["radius"] for b in rows})
    cols = dict(zip(radii, [ORANGE, AQUA, BLUE]))
    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    for r in radii:
        sel = [b for b in rows if b["radius"] == r]
        ax.semilogy([b["wa"] for b in sel], [b["loss_dB_per_90deg"] for b in sel], "o-",
                    color=cols.get(r, INK2), label=f"R = {r / 1e3:.0f} µm")
    ax.set_xlabel("Access width W$_a$ (nm)")
    ax.set_ylabel("Loss per 90° bend (dB)")
    ax.set_title("Bend loss sets the lower limit on the access width")
    ax.legend()
    _save(fig, outdir, "fig7_bend_loss.png", note)


def make_all(res, cfg, outdir, backend):
    note = {"emode": "EMode2D", "empy": "open-source cross-check solver (EMpy), not EMode"}.get(backend, backend)
    note = f"Solver: {note} · grid {cfg['resolution']:g} nm"
    print("\n[plots]")
    for need, fn in (("sweep", fig_phase_matching), ("design", fig_anticrossing), ("design", fig_design),
                     ("tolerance", fig_tolerance_curves), ("tolerance", fig_tolerance_summary),
                     ("wavelength", fig_wavelength), ("bend", fig_bend)):
        if need in res:
            fn(res, cfg, outdir, note)
