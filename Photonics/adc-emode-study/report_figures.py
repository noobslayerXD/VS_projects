"""
Figures and tables for the design-study report (Photonics/mdm-design-study/report.tex).

Reads the EMode results (results_emode/) and writes report-sized PDF figures and
LaTeX table bodies:

    ../mdm-design-study/figures/report_*.pdf
    ../mdm-design-study/generated/table_designs.tex      Table 1
    ../mdm-design-study/generated/table_matched.tex      Table 2, only once the 'matched'
                                                          step has been run in EMode

    python report_figures.py

It also prints the numbers quoted in the report text. Rerun it after a new EMode run;
the report picks the new files up on the next build.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import modefields
import plots
from plots import COUPLER, INK, INK2, SURFACE, _field_panel, _ramp

HERE = os.path.dirname(os.path.abspath(__file__))
EMODE = os.path.join(HERE, "results_emode")
REPORT = os.path.join(HERE, "..", "mdm-design-study")
FIGS = os.path.join(REPORT, "figures")
GEN = os.path.join(REPORT, "generated")
TEXTWIDTH = 6.5                                   # inches, the report's text width

# DejaVu Sans ships with matplotlib, so the figures look the same on any machine.
plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans",
                     "font.size": 7.5, "axes.titlesize": 7.8, "axes.labelsize": 7.5, "legend.fontsize": 6.6,
                     "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "lines.linewidth": 1.4, "lines.markersize": 4.6, "lines.markeredgewidth": 0.9,
                     "savefig.dpi": 300, "pdf.fonttype": 42})


def load(folder):
    return json.load(open(os.path.join(folder, "results.json")))


def save(fig, name):
    os.makedirs(FIGS, exist_ok=True)
    path = os.path.join(FIGS, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", os.path.relpath(path, HERE))


def panel_label(ax, text):
    ax.set_title(text, loc="left", fontweight="bold")


# ---------------------------------------------------------------------- figures
def fig_tradeoff(res):
    """(a) coupling coefficient, (b) sensitivity mismatch, (c) their ratio."""
    fig, axes = plt.subplots(1, 3, figsize=(TEXTWIDTH, 1.72))
    panels = [("(a) Coupling coefficient", "$\\kappa$ (µm$^{-1}$)", lambda d: d["kappa_per_um"]),
              ("(b) Sensitivity mismatch", "$S_a - S_m$ (10$^{-3}$ nm$^{-1}$)", lambda d: 1e3 * (d["s_a"] - d["s_b"])),
              ("(c) Coupling over mismatch", "$\\Delta n_{min}/(S_a - S_m)$ (nm)", lambda d: d["fom_nm"])]
    for ax, (title, ylab, f) in zip(axes, panels):
        for m in (1, 2):
            name, col = COUPLER[m]
            ds = sorted((d for d in res["design"] if d["m"] == m), key=lambda d: d["wa"])
            ax.plot([d["wa"] for d in ds], [f(d) for d in ds], "o-", color=col, label=name)
        panel_label(ax, title)
        ax.set_xlabel("Access width $W_a$ (nm)")
        ax.set_ylabel(ylab)
        ax.set_ylim(bottom=0)
        ax.set_xticks([320, 360, 400, 440, 480])
    axes[0].legend(loc="upper right")
    fig.tight_layout(w_pad=1.2)
    save(fig, "report_tradeoff.pdf")


def fig_tolerance(res):
    """(a, b) unconverted power against width error; (c) tolerance against access width."""
    lim = -15.0
    ramp = _ramp(sorted({t["wa"] for t in res["tolerance"]}))
    fig, axes = plt.subplots(1, 3, figsize=(TEXTWIDTH, 1.85), gridspec_kw=dict(width_ratios=[1, 1, 1.05]))
    for ax, m, tag in ((axes[0], 1, "(a)"), (axes[1], 2, "(b)")):
        for t in sorted((t for t in res["tolerance"] if t["m"] == m), key=lambda t: t["wa"]):
            ax.plot(t["dw"], t["residual_dB"], color=ramp[t["wa"]], label=f"{t['wa']:.0f} nm")
            ax.plot([p["dw"] for p in t["points"]],
                    [10 * np.log10(max(1 - p["eta"], 1e-6)) for p in t["points"]], "o", color=ramp[t["wa"]], ms=3.6)
        ax.axhline(lim, color=INK2, lw=0.8, ls=(0, (4, 3)))
        ax.set_ylim(-40, 0)
        ax.set_xlim(-20.5, 20.5)
        ax.set_xticks([-20, -10, 0, 10, 20])
        ax.set_xlabel("Width error $\\Delta W$ (nm)")
        panel_label(ax, f"{tag} {COUPLER[m][0]}")
    axes[0].set_ylabel("Unconverted power at $L_c$ (dB)")
    axes[1].legend(title="$W_a$", loc="lower right", fontsize=6, title_fontsize=6.4, ncol=1, handlelength=1.2,
                   labelspacing=0.25, borderaxespad=0.2)
    ax = axes[2]
    for m in (1, 2):
        name, col = COUPLER[m]
        ts = sorted((t for t in res["tolerance"] if t["m"] == m), key=lambda t: t["wa"])
        ds = {d["wa"]: d for d in res["design"] if d["m"] == m}
        wa = [t["wa"] for t in ts]
        ax.plot(wa, [t["tol"] for t in ts], "o-", color=col, label=f"{name}, re-solved")
        ax.plot(wa, [ds[w]["tol_cmt"] for w in wa], "s", ls=(0, (3, 2)), color=col, mfc=SURFACE, mec=col,
                label=f"{name}, first order")
    panel_label(ax, "(c) Tolerance at $-$15 dB")
    ax.set_xlabel("Access width $W_a$ (nm)")
    ax.set_ylabel("Tolerance $\\pm\\Delta W$ (nm)")
    ax.set_ylim(0, 10.5)
    ax.set_xticks([320, 360, 400, 440, 480])
    ax.legend(loc="upper right", fontsize=6, handlelength=2.0, labelspacing=0.25)
    fig.tight_layout(w_pad=1.0)
    save(fig, "report_tolerance.pdf")


def fig_modes(res):
    """Mode gallery: access mode, bus mode and the two supermodes of three nominal couplers."""
    rows = [(1, 320), (1, 480), (2, 320)]
    sets = [modefields.load(os.path.join(EMODE, "modes", f"TE0-TE{m}_wa{wa}_dw+0.npz")) for m, wa in rows]
    info = {(r["m"], r["wa"]): r for r in res["modes"] if r["dw"] == 0}
    xlim, ylim = plots._extent(sets, margin=380)
    ylim = (-110 - 300, 110 + 300)
    pw = (TEXTWIDTH - 1.25) / 4
    ph = pw * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    fig, axes, cax = plots._field_grid(len(rows), 4, pw, ph, left=0.82, right=0.55, top=0.2, bottom=0.05,
                                       gapw=0.04, gaph=0.06)
    cols = [("access", "Access strip alone"), ("bus", "Bus strip alone"),
            ("upper", "Upper supermode"), ("lower", "Lower supermode")]
    for i, ((m, wa), data) in enumerate(zip(rows, sets)):
        r = info[(m, wa)]
        for j, (name, title) in enumerate(cols):
            ax = axes[i, j]
            im = _field_panel(ax, data, name, xlim, ylim)
            for p in ax.patches:
                p.set_linewidth(0.5)
            label = f"{data['modes'][name]['neff']:.3f}"
            if name in ("upper", "lower"):
                label += f", {100 * r['share_' + name]:.0f} %"
            ax.text(0.02, 0.94, label, transform=ax.transAxes, va="top", ha="left", fontsize=6.2, color=INK)
            if i == 0:
                ax.set_title(title, fontsize=7.2, fontweight="bold", loc="left")
        wb = data["meta"]["cores"][1][1]
        axes[i, 0].text(-0.04, 0.5, f"{COUPLER[m][0]}\n$W_a$ {wa} nm\nbus {wb:.0f} nm", transform=axes[i, 0].transAxes,
                        ha="right", va="center", fontsize=6.4, color=INK2, linespacing=1.15)
    plots._scale_bar(axes[-1, 0], xlim, ylim, length=500)
    for t in axes[-1, 0].texts[-1:]:
        t.set_fontsize(5.8)
    cb = fig.colorbar(im, cax=cax, ticks=[-1, 0, 1])
    cb.set_label("Re$(E_x)$, scaled to peak", color=INK2, fontsize=6.4)
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=0, labelsize=6.2)
    save(fig, "report_modes.pdf")


def fig_fieldchecks(res):
    """(a) access-mode tail, (b) W* against the phase-matched width, (c) coupler at W*."""
    nominal = [r for r in res["modes"] if r["dw"] == 0]
    gap = 200
    ramp = _ramp(sorted({r["wa"] for r in nominal}))
    fig, axes = plt.subplots(1, 3, figsize=(TEXTWIDTH, 1.76))
    ax = axes[0]
    for wa in sorted(ramp):
        data = modefields.load(os.path.join(EMODE, "modes", f"TE0-TE1_wa{wa:g}_dw+0.npz"))
        x, y = data["x"], data["y"]
        j = int(np.argmin(np.abs(y)))
        ex2 = np.abs(np.real(data["modes"]["access"]["Ex"][:, j])) ** 2
        u = x - wa / 2
        keep = (u >= 0) & (u <= gap + 350)
        ax.plot(u[keep], 10 * np.log10(ex2[keep] / ex2.max() + 1e-12), color=ramp[wa], label=f"{wa:g} nm")
    ax.axvspan(gap, gap + 350, color="#efeeea", zorder=0, lw=0)
    ax.text(gap + 10, -1.2, "bus", ha="left", va="top", fontsize=6.4, color=INK2)
    ax.set_xlim(0, gap + 350)
    ax.set_ylim(-35, 1)
    ax.set_xlabel("Distance from access wall (nm)")
    ax.set_ylabel("$|E_x|^2$, access mode alone (dB)")
    panel_label(ax, "(a) Evanescent tail")
    ax.legend(title="$W_a$", loc="upper right", fontsize=5.8, title_fontsize=6.2, handlelength=1.2,
              labelspacing=0.2, borderaxespad=0.2)
    ax = axes[1]
    for m in (1, 2):
        name, col = COUPLER[m]
        sel = sorted((r for r in nominal if r["m"] == m), key=lambda r: r["wa"])
        wa = [r["wa"] for r in sel]
        ax.plot(wa, [r["wb_star"] - r["wb_even_fields"] for r in sel], "o-", color=col, label=f"{name}, fields")
        ax.plot(wa, [r["wb_star"] - r["wb_iso"] for r in sel], "s", ls=(0, (3, 2)), color=col, mfc=SURFACE,
                mec=col, label=f"{name}, $n_a = n_m$")
    ax.set_ylim(bottom=0)
    ax.set_xticks([320, 360, 400, 440, 480])
    ax.set_xlabel("Access width $W_a$ (nm)")
    ax.set_ylabel("$W^* - W_{pm}$ (nm)")
    panel_label(ax, "(b) Offset of $W^*$")
    ax.legend(loc="upper right", fontsize=5.8, handlelength=2.0, labelspacing=0.2)
    ax = axes[2]
    for m in (1, 2):
        name, col = COUPLER[m]
        sel = sorted((r for r in nominal if r["m"] == m), key=lambda r: r["wa"])
        ax.plot([r["wa"] for r in sel], [r["unconverted_fields_dB"] for r in sel], "o-", color=col, label=name)
    ax.axhline(-15, color=INK2, lw=0.8, ls=(0, (4, 3)))
    ax.set_ylim(-26, -8)
    ax.set_xticks([320, 360, 400, 440, 480])
    ax.set_xlabel("Access width $W_a$ (nm)")
    ax.set_ylabel("Unconverted power (dB)")
    panel_label(ax, "(c) Built at $W^*$, $\\Delta W = 0$")
    ax.legend(loc="upper right", fontsize=6)
    fig.tight_layout(w_pad=1.0)
    save(fig, "report_fieldchecks.pdf")


# ----------------------------------------------------------------------- tables
def table_designs(res):
    """Table 1: design and tolerance of every coupler (EMode)."""
    tol = {(t["m"], t["wa"]): t for t in res["tolerance"]}
    wav = {(w["m"], w["wa"]): w for w in res["wavelength"]}
    mod = {(r["m"], r["wa"]): r for r in res["modes"] if r["dw"] == 0}
    lines = []
    for m in (1, 2):
        ds = sorted((d for d in res["design"] if d["m"] == m), key=lambda d: d["wa"])
        lines.append(f"\\multicolumn{{10}}{{l}}{{\\TE{{0}}$\\to$\\TE{{{m}}}}} \\\\")
        for d in ds:
            k = (m, d["wa"])
            lines.append(
                f"{d['wa']:.0f} & {d['wb_star']:.1f} & {mod[k]['wb_even_fields']:.1f} & {d['Lc'] / 1e3:.1f} & "
                f"{d['kappa_per_um']:.3f} & {1e3 * (d['s_a'] - d['s_b']):.2f} & {tol[k]['tol']:.2f} & "
                f"{d['tol_cmt']:.2f} & \\num{{{mod[k]['unconverted_fields_dB']:.1f}}} & "
                f"\\num{{{wav[k]['worst_residual_c_band_dB']:.1f}}} \\\\")
        if m == 1:
            lines.append("\\addlinespace")
    write("table_designs.tex", lines)


def table_matched(res):
    """Table 2: tolerance with the bus at W* (model) and at the phase-matched width (fields)."""
    mat = sorted(res["matched"], key=lambda r: (r["m"], r["wa"]))
    widths = sorted({r["wa"] for r in mat})
    lines = []
    for m in (1, 2):
        sel = {r["wa"]: r for r in mat if r["m"] == m}
        cells = [f"{sel[w]['tol_model']:.2f} / {sel[w]['tol']:.2f}" if w in sel else "" for w in widths]
        lines.append(f"\\TE{{0}}$\\to$\\TE{{{m}}} & " + " & ".join(cells) + " \\\\")
    lines.append("% access widths (columns): " + ", ".join(f"{w:g}" for w in widths) + " nm")
    write("table_matched.tex", lines)


def write(name, lines):
    os.makedirs(GEN, exist_ok=True)
    path = os.path.join(GEN, name)
    with open(path, "w") as f:
        f.write("% Generated by adc-emode-study/report_figures.py. Do not edit by hand.\n")
        f.write("\n".join(lines) + "\n")
    print("wrote", os.path.relpath(path, HERE))


def summary(res):
    """The numbers quoted in the report text."""
    des = {(d["m"], d["wa"]): d for d in res["design"]}
    tol = {(t["m"], t["wa"]): t for t in res["tolerance"]}
    for m in (1, 2):
        lo, hi = des[(m, 320)], des[(m, 480)]
        print(f"TE0-TE{m}: kappa {hi['kappa_per_um']:.4f} -> {lo['kappa_per_um']:.4f} "
              f"({lo['kappa_per_um'] / hi['kappa_per_um']:.2f}x), mismatch "
              f"{1e3 * (hi['s_a'] - hi['s_b']):.3f} -> {1e3 * (lo['s_a'] - lo['s_b']):.3f} "
              f"({(lo['s_a'] - lo['s_b']) / (hi['s_a'] - hi['s_b']):.2f}x), ratio {hi['fom_nm']:.1f} -> "
              f"{lo['fom_nm']:.1f} nm ({lo['fom_nm'] / hi['fom_nm']:.2f}x), L_c {hi['Lc'] / 1e3:.2f} -> "
              f"{lo['Lc'] / 1e3:.2f} um, tolerance {tol[(m, 480)]['tol']:.2f} -> {tol[(m, 320)]['tol']:.2f} nm "
              f"({tol[(m, 320)]['tol'] / tol[(m, 480)]['tol']:.2f}x)")
        print("   first order minus re-solved (nm):",
              {wa: round(d["tol_cmt"] - tol[(m, wa)]["tol"], 2) for (mm, wa), d in des.items() if mm == m})
    rows = res["modes"]
    print("\nmax two-mode residual (EMode): %.4f" % max(max(r["residual_upper"], r["residual_lower"]) for r in rows))
    print("max |dn_s solved - fit| / fit: %.4f" % max(abs(r["dn_s"] - r["dn_s_model"]) / r["dn_s_model"] for r in rows))
    print("min TE fraction: %.3f" % min(min(r["te_upper"], r["te_lower"]) for r in rows))
    print("max edge fraction: %.1e" % max(r["edge_fraction"] for r in rows))
    print("tails:", {r["wa"]: round(r["tail_dB"], 1) for r in rows if r["dw"] == 0 and r["m"] == 1})
    for r in rows:
        if r["dw"] == 0:
            print(f"  TE0-TE{r['m']} {r['wa']}: share {r['share_upper']:.3f}, "
                  f"unconverted {r['unconverted_fields_dB']:.1f} dB, W* {r['wb_star']:.1f}, "
                  f"W_even {r['wb_even_fields']:.1f}, W_iso {r['wb_iso']:.1f}")
    print("convergence:", [(c["resolution"], round(c["wb_star"], 1), round(c["Lc"] / 1e3, 2))
                           for c in res["validate"]["convergence"]])
    v = res["validate"]
    print("wang:", round(v["wang"]["wb_iso"], 1), round(v["wang"]["wb_star"], 1), round(v["wang"]["Lc"] / 1e3, 2))
    print("dai:", round(v["dai"]["wb_iso"], 1), round(v["dai"]["wb_star"], 1), round(v["dai"]["Lc"] / 1e3, 2))
    print("bend (dB/90deg):", [(b["wa"], b["radius"], f"{b['loss_dB_per_90deg']:.2g}") for b in res["bend"]])


def main():
    res = load(EMODE)
    fig_tradeoff(res)
    fig_tolerance(res)
    fig_modes(res)
    fig_fieldchecks(res)
    table_designs(res)
    stale = os.path.join(GEN, "table_matched.tex")
    if res.get("matched"):
        table_matched(res)
    elif os.path.exists(stale):
        os.remove(stale)                                  # no EMode 'matched' run: no Table 2
        print("removed", os.path.relpath(stale, HERE))
    summary(res)


if __name__ == "__main__":
    main()
