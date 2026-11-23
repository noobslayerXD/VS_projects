"""Figures for the ADC tolerance study. Reads the results dictionary written by adc_study.py
and, for fig8 to fig11, the mode fields saved in <outdir>/modes/."""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Colours are matplotlib's defaults: C0 for TE0->TE1, C1 for TE0->TE2, C<i> for the i-th access
# width, black for reference lines. Mode maps use EMode's colour scale (see _field_panel).
COUPLER = {1: "TE$_0$→TE$_1$", 2: "TE$_0$→TE$_2$"}

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "lines.linewidth": 1.8, "lines.markersize": 6.5, "legend.frameon": False, "legend.fontsize": 8.5,
    "xtick.major.size": 0, "ytick.major.size": 0, "figure.dpi": 110, "savefig.dpi": 200,
})


def _save(fig, outdir, name, note):
    fig.text(0.995, -0.035, note, ha="right", va="top", fontsize=6.5)
    path = os.path.join(outdir, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", path)


def fig_phase_matching(res, cfg, outdir, note):
    sw, base = res["sweep"], cfg["baseline"]
    w = np.array(sw["width"])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for m in (0, 1, 2):
        n = np.array(sw[f"TE{m}"], dtype=float)
        ok = np.isfinite(n)
        ax.plot(w[ok], n[ok], label=f"TE$_{m}$")
        ax.annotate(f"TE$_{m}$", (w[ok][-1], n[ok][-1]), xytext=(5, 0), textcoords="offset points", va="center")
    if "design" in res:
        n_a = next(d["n_a"] for d in res["design"] if d["wa"] == base)
        xs = [base] + [d["wb_iso"] for d in res["design"] if d["wa"] == base]
        ax.plot(xs, [n_a] * len(xs), "o--", color="k", lw=0.9, zorder=3)
        ax.annotate(f"access TE$_0$, {base:.0f} nm", (base, n_a), xytext=(8, 6), textcoords="offset points",
                    fontsize=8)
        for x, lab in zip(xs[1:], ("W$_1$", "W$_2$")):
            ax.annotate(f"{lab} = {x:.0f} nm", (x, n_a), xytext=(4, -13), textcoords="offset points", fontsize=8)
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
        name = COUPLER[m]
        w = np.array(d["scan_w"])
        wf = np.linspace(w[0], w[-1], 200)
        ax.plot(wf, 1e3 * np.hypot(d["dn_min"], d["slope"] * (wf - d["wb_star"])), color=f"C{m - 1}", label="fit")
        ax.plot(w, 1e3 * np.array(d["scan_dn"]), "ko", label="mode solves")
        ax.plot([d["wb_star"]] * 2, [0, 1e3 * d["dn_min"]], color="k", lw=0.9, ls=(0, (4, 3)))
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
            ds = [d for d in res["design"] if d["m"] == m]
            ax.plot([d["wa"] for d in ds], [f(d) for d in ds], "o-", color=f"C{m - 1}", label=COUPLER[m])
        ax.set_xlabel("Access width W$_a$ (nm)")
        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.set_ylim(bottom=0)
    axes[0].legend(loc="upper left")
    fig.tight_layout()
    _save(fig, outdir, "fig3_design.png", note)


def fig_tolerance_curves(res, cfg, outdir, note):
    lim = cfg["residual_limit_dB"]
    widths = sorted({t["wa"] for t in res["tolerance"]})
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        for t in [t for t in res["tolerance"] if t["m"] == m]:
            col = f"C{widths.index(t['wa'])}"
            ax.plot(t["dw"], t["residual_dB"], color=col, label=f"{t['wa']:.0f} nm")
            ax.plot([p["dw"] for p in t["points"]],
                    [float(10 * np.log10(max(1 - p["eta"], 1e-6))) for p in t["points"]], "o", color=col, ms=5)
        ax.axhline(lim, color="k", lw=0.9, ls=(0, (4, 3)))
        ax.annotate(f"limit {lim:.0f} dB", (ax.get_xlim()[0], lim), xytext=(4, 3), textcoords="offset points",
                    fontsize=8)
        ax.set_title(COUPLER[m])
        ax.set_xlabel("Uniform width error ΔW (nm)")
        ax.set_ylim(-45, 0)
    axes[0].set_ylabel("Unconverted power (dB)")
    used = [ax for ax in axes if ax.get_legend_handles_labels()[0]]
    if used:
        used[-1].legend(title="Access width", loc="lower right", ncol=2)
    fig.suptitle("Unconverted power against width error at fixed coupler length",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig4_tolerance_curves.png", note)


def fig_tolerance_summary(res, cfg, outdir, note):
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        ts = [t for t in res["tolerance"] if t["m"] == m]
        ds = [d for d in res["design"] if d["m"] == m]
        wa = [t["wa"] for t in ts]
        ax.plot(wa, [t["tol"] for t in ts], "o-", color=f"C{m - 1}", label="re-solved supermodes")
        ax.plot(wa, [d["tol_cmt"] for d in ds], "s", ls=(0, (4, 3)), color=f"C{m - 1}", mfc="none",
                label="first-order estimate")
        for t in ts:
            if t["tol_is_lower_bound"]:
                ax.annotate("≥", (t["wa"], t["tol"]), xytext=(0, 6), textcoords="offset points",
                            ha="center", fontsize=9)
        ax.set_title(COUPLER[m])
        ax.set_xlabel("Access width W$_a$ (nm)")
        ax.set_ylim(bottom=0)
    axes[0].set_ylabel(f"Width tolerance ±ΔW (nm) at {cfg['residual_limit_dB']:.0f} dB")
    axes[0].legend(loc="upper right")
    fig.suptitle("Width tolerance against access width", x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig5_tolerance_summary.png", note)


def fig_wavelength(res, cfg, outdir, note):
    widths = sorted({w["wa"] for w in res["wavelength"]})
    top = 1.08 * max(max(w["loss_dB"]) for w in res["wavelength"])
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        ax.axvspan(*cfg["c_band"], alpha=0.1, lw=0, zorder=0)
        for w in [w for w in res["wavelength"] if w["m"] == m]:
            ax.plot(w["wl"], w["loss_dB"], color=f"C{widths.index(w['wa'])}", label=f"{w['wa']:.0f} nm")
        ax.set_title(COUPLER[m])
        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylim(0, top)
        ax.annotate("C-band", (np.mean(cfg["c_band"]), top), xytext=(0, -11),
                    textcoords="offset points", ha="center", fontsize=8)
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
        print("  no positive bend-loss data: fig7 skipped")
        return
    radii = sorted({b["radius"] for b in rows})
    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    for r in radii:
        sel = [b for b in rows if b["radius"] == r]
        ax.semilogy([b["wa"] for b in sel], [b["loss_dB_per_90deg"] for b in sel], "o-", label=f"R = {r / 1e3:.0f} µm")
    ax.set_xlabel("Access width W$_a$ (nm)")
    ax.set_ylabel("Loss per 90° bend (dB)")
    ax.set_title("Bend loss of the access waveguide")
    ax.legend()
    _save(fig, outdir, "fig7_bend_loss.png", note)


# ------------------------------------------------------------------ mode fields
def _mode_sets(res, outdir):
    """The saved mode files that exist, keyed (coupler, access width, width error)."""
    import modefields
    sets = {}
    for r in res.get("modes", []):
        path = os.path.join(outdir, r["file"])
        if os.path.exists(path):
            sets[(r["m"], r["wa"], r["dw"])] = modefields.load(path)
    return sets


def _mode_rows(res):
    return {(r["m"], r["wa"], r["dw"]): r for r in res.get("modes", [])}


def _views(rows, margin=450, ymargin=380):
    """x and y limits (nm) for each row of field panels. `rows` holds one list of stored mode
    sets per row. Every row gets the same span, so all panels share one scale; each row is
    centred on its own couplers and kept inside its stored windows, because beyond them
    there is no field to draw and the window edge would show on EMode's colour scale."""
    def box(sets):
        cores = [c for s in sets for c in s["meta"]["cores"]]
        return (min(c - w / 2 for c, w in cores), max(c + w / 2 for c, w in cores),
                max(s["x"][0] for s in sets), min(s["x"][-1] for s in sets))

    boxes = [box(r) for r in rows]
    widest = max(right - left for left, right, _, _ in boxes)
    span = max(min(widest + 2 * margin, min(hi - lo for _, _, lo, hi in boxes)), widest + 100)
    every = [s for r in rows for s in r]
    h = every[0]["meta"]["h_si"]
    my = max(0.0, min(ymargin, -h / 2 - max(s["y"][0] for s in every), min(s["y"][-1] for s in every) - h / 2))
    views = []
    for left, right, lo, hi in boxes:
        x0 = (left + right - span) / 2
        if hi - lo >= span:                     # else (windows saved narrower) stay centred
            x0 = min(max(x0, lo), hi - span)
        views.append(((x0, x0 + span), (-h / 2 - my, h / 2 + my)))
    return views


def _field_panel(ax, data, name, xlim, ylim):
    """|Ex| of one stored mode, scaled to its own peak, on EMode's colour scale ('plasma', as
    EMode's plot() uses), with the silicon outlined in white as EMode does. A sign change
    shows as a dark line (a zero of the field)."""
    x, y = data["x"], data["y"]
    ex = np.abs(data["modes"][name]["Ex"])
    dx, dy = np.diff(x).mean(), np.diff(y).mean()
    im = ax.imshow((ex / ex.max()).T, origin="lower", cmap="plasma", vmin=0, vmax=1,
                   extent=[x[0] - dx / 2, x[-1] + dx / 2, y[0] - dy / 2, y[-1] + dy / 2],
                   interpolation="bilinear")
    h = data["meta"]["h_si"]
    for c, w in data["meta"]["cores"]:
        ax.add_patch(Rectangle((c - w / 2, -h / 2), w, h, fill=False, ec="white", lw=0.7))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    return im


def _scale_bar(ax, xlim, ylim, length=500):
    x0, y0 = xlim[0] + 0.04 * (xlim[1] - xlim[0]), ylim[0] + 0.1 * (ylim[1] - ylim[0])
    ax.plot([x0, x0 + length], [y0, y0], color="white", lw=1.2, solid_capstyle="butt")
    ax.text(x0 + length / 2, y0 + 0.04 * (ylim[1] - ylim[0]), f"{length:g} nm", ha="center", va="bottom",
            fontsize=7, color="white")


def _field_grid(nrows, ncols, pw, ph, left=1.2, right=1.05, top=0.78, bottom=0.12, gapw=0.08, gaph=0.16):
    """A grid of field panels sized in inches, so equal-aspect maps fill their axes,
    plus a colour-bar axis in the right margin."""
    fw = left + ncols * pw + (ncols - 1) * gapw + right
    fh = top + nrows * ph + (nrows - 1) * gaph + bottom
    fig, axes = plt.subplots(nrows, ncols, figsize=(fw, fh), squeeze=False)
    fig.subplots_adjust(left=left / fw, right=(fw - right) / fw, bottom=bottom / fh, top=(fh - top) / fh,
                        wspace=gapw / pw, hspace=gaph / ph)
    ch = min(2.2, nrows * ph)
    cax = fig.add_axes([(fw - right + 0.18) / fw, (bottom + (nrows * ph + (nrows - 1) * gaph - ch) / 2) / fh,
                        0.09 / fw, ch / fh])
    return fig, axes, cax


def _field_colorbar(fig, im, cax):
    cb = fig.colorbar(im, cax=cax, ticks=[0, 0.5, 1])
    cb.set_label("|E$_x$|, each mode scaled to its peak")
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=0)
    cb.ax.grid(False)                                    # no style grid line across the scale


def fig_mode_gallery(res, cfg, outdir, note, m):
    """The four modes of every nominal coupler of one kind (width error 0)."""
    sets = {k: v for k, v in _mode_sets(res, outdir).items() if k[0] == m and k[2] == 0}
    if not sets:
        return
    rows = _mode_rows(res)
    widths = sorted(k[1] for k in sets)
    views = _views([[sets[(m, wa, 0)]] for wa in widths])
    xlim, ylim = views[0]
    pw = 2.15
    ph = pw * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    fig, axes, cax = _field_grid(len(widths), 4, pw, ph)
    cols = [("access", "Access strip alone: TE$_0$"), ("bus", f"Bus strip alone: TE$_{m}$"),
            ("upper", "Upper supermode"), ("lower", "Lower supermode")]
    for i, wa in enumerate(widths):
        data, r = sets[(m, wa, 0)], rows[(m, wa, 0)]
        xlim, ylim = views[i]
        for j, (name, title) in enumerate(cols):
            ax = axes[i, j]
            im = _field_panel(ax, data, name, xlim, ylim)
            label = f"n$_{{eff}}$ {data['modes'][name]['neff']:.3f}"
            if name in ("upper", "lower"):
                label += f"   access {100 * r['share_' + name]:.0f} %"
            ax.text(0.02, 0.95, label, transform=ax.transAxes, va="top", ha="left", fontsize=7.5, color="white")
            if i == 0:
                ax.set_title(title, fontsize=9)
        wb = data["meta"]["cores"][1][1]
        axes[i, 0].text(-0.03, 0.5, f"W$_a$ {wa:.0f} nm\nbus {wb:.0f} nm", transform=axes[i, 0].transAxes,
                        ha="right", va="center", fontsize=8)
    _scale_bar(axes[-1, 0], xlim, ylim)
    _field_colorbar(fig, im, cax)
    fig.suptitle(f"{COUPLER[m]} couplers as designed (bus width W*): the strip modes and the two "
                 "supermodes", x=0.01, ha="left", fontsize=10, fontweight="bold")
    _save(fig, outdir, f"fig{7 + m}_modes_TE0-TE{m}.png", note)


def fig_supermodes_error(res, cfg, outdir, note):
    """Upper supermode of the narrowest and widest coupler of each kind under width errors."""
    sets, rows = _mode_sets(res, outdir), _mode_rows(res)
    if not sets:
        return
    errors = sorted({k[2] for k in sets})
    picks = []
    for m in sorted({k[0] for k in sets}):
        ws = sorted({k[1] for k in sets if k[0] == m})
        for wa in dict.fromkeys([ws[0], ws[-1]]):
            if all((m, wa, e) in sets for e in errors):
                picks.append((m, wa))
    if not picks:
        return
    views = _views([[sets[(m, wa, e)] for e in errors] for m, wa in picks])
    xlim, ylim = views[0]
    pw = 2.4
    ph = pw * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    fig, axes, cax = _field_grid(len(picks), len(errors), pw, ph)
    for i, (m, wa) in enumerate(picks):
        xlim, ylim = views[i]
        for j, e in enumerate(errors):
            ax, r = axes[i, j], rows[(m, wa, e)]
            im = _field_panel(ax, sets[(m, wa, e)], "upper", xlim, ylim)
            ax.text(0.02, 0.95, f"access {100 * r['share_upper']:.0f} %", transform=ax.transAxes,
                    va="top", ha="left", fontsize=7.5, color="white")
            if i == 0:
                ax.set_title(f"ΔW = {e:+g} nm", fontsize=9)
        axes[i, 0].text(-0.03, 0.5, f"{COUPLER[m]}\nW$_a$ {wa:.0f} nm", transform=axes[i, 0].transAxes,
                        ha="right", va="center", fontsize=8)
    _scale_bar(axes[-1, 0], xlim, ylim)
    _field_colorbar(fig, im, cax)
    fig.suptitle("Upper supermode under a uniform width error: its share in the access strip "
                 "(50 % = phase matched)", x=0.01, ha="left", fontsize=10, fontweight="bold")
    _save(fig, outdir, "fig10_supermodes_width_error.png", note)


def fig_mode_checks(res, cfg, outdir, note):
    """Why the coupling grows, whether the coupling is two-mode, and where phase matching is."""
    rows = res.get("modes", [])
    sets = _mode_sets(res, outdir)
    nominal = [r for r in rows if r["dw"] == 0]
    if not nominal:
        return
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.5))

    ax = axes[0]                                          # access mode alone along the mid-plane
    gap = cfg["gap"]
    m0 = min(r["m"] for r in nominal)
    for k, wa in enumerate(sorted({r["wa"] for r in nominal})):
        data = sets.get((m0, wa, 0))
        if data is None:
            continue
        x, y = data["x"], data["y"]
        j = int(np.argmin(np.abs(y)))
        ex2 = np.abs(np.real(data["modes"]["access"]["Ex"][:, j])) ** 2
        u = x - wa / 2                                    # distance from the access strip's gap-side wall
        keep = (u >= 0) & (u <= gap + 400)
        ax.plot(u[keep], 10 * np.log10(ex2[keep] / ex2.max() + 1e-12), color=f"C{k}", label=f"{wa:.0f} nm")
    ax.axvspan(gap, gap + 400, alpha=0.1, lw=0, zorder=0)
    ax.annotate("bus strip", (gap + 12, -1.5), ha="left", va="top", fontsize=8)
    ax.set_xlim(0, gap + 400)
    ax.set_ylim(-35, 1)
    ax.set_xlabel("Distance from the access strip's wall (nm)")
    ax.set_ylabel("|E$_x$|$^2$ of the access mode alone (dB)")
    ax.set_title("Narrower access: stronger tail at the bus")
    if ax.get_legend_handles_labels()[0]:
        ax.legend(title="Access width", loc="upper right", fontsize=7.5, title_fontsize=8)

    ax = axes[1]                                          # two-mode residual
    for m in sorted({r["m"] for r in rows}):
        ws = sorted({r["wa"] for r in rows if r["m"] == m})
        worst = [100 * max(max(r["residual_upper"], r["residual_lower"]) for r in rows
                           if r["m"] == m and r["wa"] == wa) for wa in ws]
        ax.plot(ws, worst, "o-", color=f"C{m - 1}", label=COUPLER[m])
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Access width W$_a$ (nm)")
    ax.set_ylabel("Field not explained by the two strip modes (%)")
    ax.set_title("Supermodes are two-mode mixtures")
    ax.legend(loc="upper right")

    ax = axes[2]                                          # design point: W* against phase matching
    for m in sorted({r["m"] for r in nominal}):
        name, col = COUPLER[m], f"C{m - 1}"
        sel = sorted((r for r in nominal if r["m"] == m), key=lambda r: r["wa"])
        wa = [r["wa"] for r in sel]
        ax.plot(wa, [r["wb_star"] - r["wb_even_fields"] for r in sel], "o-", color=col,
                label=f"{name}: even mixture (fields)")
        ax.plot(wa, [r["wb_star"] - r["wb_iso"] for r in sel], "s", ls=(0, (4, 3)), color=col, mfc="none",
                label=f"{name}: equal strip indices")
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Access width W$_a$ (nm)")
    ax.set_ylabel("W* minus phase-matched bus width (nm)")
    ax.set_title("Anticrossing minimum W* sits too wide")
    ax.legend(loc="upper right", fontsize=7.5)
    fig.suptitle("Mode-field checks", x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig11_mode_checks.png", note)


def fig_tolerance_fields(res, cfg, outdir, note):
    """Unconverted power at the nominal length: two-mode model (lines) against the fields (dots)."""
    rows = res.get("modes", [])
    if not rows or "tolerance" not in res:
        return
    lim = cfg["residual_limit_dB"]
    widths = sorted({t["wa"] for t in res["tolerance"]})
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        for t in [t for t in res["tolerance"] if t["m"] == m]:
            col = f"C{widths.index(t['wa'])}"
            ax.plot(t["dw"], t["residual_dB"], color=col, lw=1.4, label=f"{t['wa']:.0f} nm")
            sel = sorted((r for r in rows if r["m"] == m and r["wa"] == t["wa"]), key=lambda r: r["dw"])
            ax.plot([r["dw"] for r in sel], [max(r["unconverted_fields_dB"], -45) for r in sel], "o",
                    color=col, ms=6.5)
        ax.axhline(lim, color="k", lw=0.9, ls=(0, (4, 3)))
        ax.annotate(f"limit {lim:.0f} dB", (ax.get_xlim()[0], lim), xytext=(4, 3), textcoords="offset points",
                    fontsize=8)
        ax.set_title(COUPLER[m])
        ax.set_xlabel("Uniform width error ΔW (nm)")
        ax.set_ylim(-45, 0)
    axes[0].set_ylabel("Unconverted power at L$_c$ (dB)")
    used = [ax for ax in axes if ax.get_legend_handles_labels()[0]]
    if used:
        used[-1].legend(title="Access width", loc="lower right", ncol=2)
    fig.suptitle("Coupler as designed: two-mode model (lines) and mode fields (dots)",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig12_tolerance_fields.png", note)


def fig_tolerance_matched(res, cfg, outdir, note):
    """Tolerance against access width: model with the bus at W*, fields with the bus at the
    phase-matched width ('matched' step)."""
    mat = res.get("matched", [])
    if not mat:
        return
    lim = cfg["residual_limit_dB"]
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4), sharey=True)
    for ax, m in zip(axes, (1, 2)):
        sel = sorted((r for r in mat if r["m"] == m), key=lambda r: r["wa"])
        if not sel:
            ax.set_axis_off()
            continue
        wa = [r["wa"] for r in sel]
        ax.plot(wa, [r["tol_model"] for r in sel], "o-", color=f"C{m - 1}", label="two-mode model, bus at W*")
        ax.plot(wa, [r["tol"] for r in sel], "o", ls=(0, (4, 3)), color=f"C{m - 1}", mfc="none",
                label="mode fields, bus at phase-matched width")
        ax.set_title(COUPLER[m])
        ax.set_xlabel("Access width W$_a$ (nm)")
        ax.set_ylim(bottom=0)
    axes[0].set_ylabel(f"Width tolerance ±ΔW (nm) at {lim:.0f} dB")
    used = [ax for ax in axes if ax.get_legend_handles_labels()[0]]
    if used:
        used[0].legend(loc="upper right")
    fig.suptitle("Tolerance of the couplers rebuilt with the bus at the phase-matched width",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    _save(fig, outdir, "fig13_tolerance_matched.png", note)


def make_all(res, cfg, outdir):
    note = f"Solver: EMode2D · grid {cfg['resolution']:g} nm"
    print("\n[plots]")
    for need, fn in (("sweep", fig_phase_matching), ("design", fig_anticrossing), ("design", fig_design),
                     ("tolerance", fig_tolerance_curves), ("tolerance", fig_tolerance_summary),
                     ("wavelength", fig_wavelength), ("bend", fig_bend)):
        if need in res:
            fn(res, cfg, outdir, note)
    if res.get("modes"):
        for m in (1, 2):
            fig_mode_gallery(res, cfg, outdir, note, m)
        fig_supermodes_error(res, cfg, outdir, note)
        fig_mode_checks(res, cfg, outdir, note)
        fig_tolerance_fields(res, cfg, outdir, note)
    if res.get("matched"):
        fig_tolerance_matched(res, cfg, outdir, note)
