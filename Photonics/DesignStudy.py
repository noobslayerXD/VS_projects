import argparse

import matplotlib.pyplot as plt
import numpy as np

# ============================== CONFIGURATION ==============================
CFG = {
    # --- waveguide cross-section (EMode, nm) ---
    "core_material": "Si",
    "box_material": "SiO2",
    "cladding_material": "SiO2",   # background = top/side cladding
    "w_core": 500,                 # core width
    "h_core": 220,                 # core height
    "h_clad": 1000,                # BOX thickness and top cladding thickness
    "w_side": 1500,                # cladding on each side of the core
    "dx": 10, "dy": 10,               # mesh resolution

    # --- channels (one per laser in the array) ---
    "n_channels": 4,
    "lambda_center": 1550.0,       # nm
    "channel_spacing": 1.6,        # nm (~200 GHz)

    # --- AWG ---
    "order": None,                 # diffraction order m; None = choose so FSR = N * spacing
    "n_arms": 24,                  # number of arrayed waveguides
    "L0_um": 50.0,                 # length of the shortest arm (only affects loss)
    "gaussian_edge": 0.15,         # relative illumination of the outermost arms

    # --- sweep ---
    "n_sweep": 9,                  # EMode wavelength points
    "sim_name": "awg_arm",
    "results_file": "awg_emode_results.npz",
}
# ===========================================================================

DB_PER_NEPER_POWER = 10 * np.log10(np.e)    # 4.343 dB per neper of power


def sweep_wavelengths(cfg):
    """Wavelength grid covering all channels with some margin on both sides."""
    half_span = 0.75 * cfg["n_channels"] * cfg["channel_spacing"]
    return np.linspace(cfg["lambda_center"] - half_span,
                       cfg["lambda_center"] + half_span, cfg["n_sweep"])


def channel_wavelengths(cfg):
    N, s = cfg["n_channels"], cfg["channel_spacing"]
    return cfg["lambda_center"] + (np.arange(N) - (N - 1) / 2) * s


# ------------------------------ 1. EMode ----------------------------------
def run_emode(cfg, wl_nm):
    """Solve the fundamental TE mode at each wavelength with EMode's FDM solver."""
    import emodeconnection as emc

    em = emc.EMode(simulation_name=cfg["sim_name"])
    em.settings(
        wavelength=float(wl_nm[len(wl_nm) // 2]),
        x_resolution=cfg["dx"], y_resolution=cfg["dy"],
        window_width=cfg["w_core"] + 2 * cfg["w_side"],
        window_height=cfg["h_core"] + 2 * cfg["h_clad"],
        num_modes=1, boundary_condition="TE",
        background_material=cfg["cladding_material"])

    em.shape(name="BOX", material=cfg["box_material"], height=cfg["h_clad"])
    em.shape(name="core", material=cfg["core_material"],
             width=cfg["w_core"], height=cfg["h_core"])

    # Check the mode at the centre wavelength before sweeping
    em.FDM()
    em.report()
    em.plot(component="Ex", file_name="mode_profile_center", file_type="png")

    em.sweep(key="wavelength", values=list(map(float, wl_nm)),
             result=["effective_index", "loss_dB_per_m"])
    em.close()

    # Read the stored sweep data (this part works without a licence)
    data = emc.get(variable="sweep_data", simulation_name=cfg["sim_name"])
    wl = np.asarray(data["values"], dtype=float)
    n_eff = np.asarray(data["effective_index"], dtype=float).reshape(len(wl), -1)[:, 0]
    loss = np.asarray(data["loss_dB_per_m"], dtype=float).reshape(len(wl), -1)[:, 0]
    order = np.argsort(wl)
    return wl[order], n_eff[order], loss[order]


def demo_data(wl_nm):
    """PLACEHOLDER numbers roughly like a 500x220 nm SOI wire. Not simulation results."""
    d = wl_nm - 1550.0
    n_eff = 2.44 - 1.135e-3 * d - 2e-7 * d**2
    loss = np.full_like(wl_nm, 200.0)       # 2 dB/cm
    return wl_nm, n_eff, loss


# ------------------------------ 2. Model ----------------------------------
class ModeModel:
    """n_eff(lambda), n_g(lambda) and kappa(lambda) from the sweep points."""

    def __init__(self, wl, n_eff, loss_dB_per_m):
        self.wl, self.n_eff_pts, self.loss_pts = wl, n_eff, loss_dB_per_m
        deg = min(2, len(wl) - 1)
        self.p = np.polyfit(wl, n_eff, deg)
        self.dp = np.polyder(self.p)
        self.p_loss = np.polyfit(wl, loss_dB_per_m, min(1, len(wl) - 1))

    def n_eff(self, lam):
        return np.polyval(self.p, lam)

    def n_g(self, lam):
        return self.n_eff(lam) - lam * np.polyval(self.dp, lam)

    def alpha_power_per_nm(self, lam):
        return np.polyval(self.p_loss, lam) / DB_PER_NEPER_POWER * 1e-9

    def kappa(self, lam):
        # alpha = 4*pi*kappa/lambda0   ->   kappa = alpha*lambda0/(4*pi)
        return self.alpha_power_per_nm(lam) * lam / (4 * np.pi)

    def beta(self, lam):
        return 2 * np.pi * self.n_eff(lam) / lam             # rad/nm

    def H(self, lam, L_nm):
        """Complex field transfer of a straight section of length L."""
        return np.exp(-1j * self.beta(lam) * L_nm) * \
               np.exp(-2 * np.pi * self.kappa(lam) * L_nm / lam)


def wrap(phi):
    return (phi + np.pi) % (2 * np.pi) - np.pi


# ------------------------------ 3-5. Design --------------------------------
def design(cfg, model, order=None):
    lam_c = cfg["lambda_center"]
    N, s = cfg["n_channels"], cfg["channel_spacing"]
    n_c, ng_c = model.n_eff(lam_c), model.n_g(lam_c)

    # FSR ~ lambda_c * n_eff / (n_g * m); choose m so FSR = N * channel spacing
    if order is None:
        order = cfg["order"] or max(1, round(lam_c * n_c / (ng_c * N * s)))
    dL = order * lam_c / n_c                                   # Scenario 1
    fsr = lam_c**2 / (ng_c * dL)
    return {"order": order, "dL": dL, "fsr": fsr, "n_c": n_c, "ng_c": ng_c}


def transfer_matrix(cfg, model, d, lam):
    """Array-factor model: power at each output port vs wavelength.

    Arm k has length L0 + k*dL. The output star coupler turns a linear phase
    tilt psi across the arms into a focal position; output port p sits where
    channel p focuses, i.e. it collects tilt psi_p = psi(lambda_p).
    """
    M = cfg["n_arms"]
    k = np.arange(M) - (M - 1) / 2
    sigma = (M / 2) / np.sqrt(-2 * np.log(cfg["gaussian_edge"]))
    w = np.exp(-k**2 / (2 * sigma**2))                         # illumination
    L0 = cfg["L0_um"] * 1e3

    lam_ch = channel_wavelengths(cfg)
    psi_port = wrap(model.beta(lam_ch) * d["dL"])              # port positions

    lam = np.atleast_1d(lam)
    H_arms = model.H(lam[:, None], L0 + (k + (M - 1) / 2)[None, :] * d["dL"])
    # constant phase of the shortest arm is irrelevant -> remove it
    H_arms = H_arms * np.exp(1j * model.beta(lam)[:, None] * L0)
    steer = np.exp(1j * np.outer(psi_port, k))                 # (ports, arms)
    a = (H_arms * w[None, :]) @ steer.T / w.sum()              # (lam, ports)
    return np.abs(a)**2, psi_port


def report(cfg, model, d):
    lam_ch = channel_wavelengths(cfg)
    print("\n=== Mode data from sweep ===")
    print(f"{'lambda (nm)':>12} {'n_eff':>10} {'loss (dB/cm)':>13} {'kappa':>11}")
    for l, n, a in zip(model.wl, model.n_eff_pts, model.loss_pts):
        print(f"{l:12.2f} {n:10.6f} {a/100:13.3f} {model.kappa(l):11.3e}")

    print("\n=== Scenario 1 design ===")
    print(f"centre wavelength      : {cfg['lambda_center']:.2f} nm")
    print(f"n_eff / n_g at centre  : {d['n_c']:.5f} / {d['ng_c']:.5f}")
    print(f"diffraction order m    : {d['order']}  (phase step 2*pi*m at centre)")
    print(f"length increment dL    : {d['dL']/1e3:.4f} um")
    print(f"free spectral range    : {d['fsr']:.3f} nm "
          f"(channels span {cfg['n_channels']*cfg['channel_spacing']:.2f} nm)")

    print("\n=== Verification: phase per arm step for each channel ===")
    print(f"{'channel':>8} {'lambda (nm)':>12} {'n_eff':>10} "
          f"{'beta*dL (rad)':>14} {'tilt (deg)':>11} {'|H(dL)|':>9}")
    for i, l in enumerate(lam_ch):
        phi = model.beta(l) * d["dL"]
        print(f"{i:8d} {l:12.2f} {model.n_eff(l):10.6f} {phi:14.4f} "
              f"{np.degrees(wrap(phi)):11.2f} {abs(model.H(l, d['dL'])):9.5f}")

    T, _ = transfer_matrix(cfg, model, d, lam_ch)
    T = T.T                                                    # rows = ports
    print("\n=== Transfer matrix T[port, channel] (power, linear) ===")
    for row in T:
        print("  [" + "  ".join(f"{v:6.3f}" for v in row) + " ]")
    diag = np.diag(T)
    off = T - np.diag(diag)
    print(f"insertion loss (worst) : {-10*np.log10(diag.min()):.2f} dB")
    print(f"crosstalk (worst)      : {10*np.log10(off.max()/diag.min()):.1f} dB")
    return T


def plot(cfg, model, d, T, fname="awg_design.png"):
    lam_ch = channel_wavelengths(cfg)
    lam_f = np.linspace(cfg["lambda_center"] - d["fsr"] / 2,
                        cfg["lambda_center"] + d["fsr"] / 2, 2000)
    spec, _ = transfer_matrix(cfg, model, d, lam_f)

    fig, ax = plt.subplots(2, 2, figsize=(11, 8))

    a = ax[0, 0]
    lf = np.linspace(model.wl.min(), model.wl.max(), 200)
    a.plot(model.wl, model.n_eff_pts, "o", label="EMode n_eff")
    a.plot(lf, model.n_eff(lf), "-", label="fit")
    a.set_xlabel("wavelength (nm)"); a.set_ylabel("n_eff")
    a2 = a.twinx(); a2.plot(lf, model.n_g(lf), "r--", label="n_g")
    a2.set_ylabel("n_g", color="r")
    a.legend(loc="upper right"); a.set_title("Mode indices")

    a = ax[0, 1]
    tilt = np.degrees(wrap(model.beta(lam_f) * d["dL"]))
    a.plot(lam_f, tilt, "k.", ms=1)
    for l in lam_ch:
        a.plot(l, np.degrees(wrap(model.beta(l) * d["dL"])), "o")
    a.set_xlabel("wavelength (nm)"); a.set_ylabel("phase step per arm (deg, wrapped)")
    a.set_title(f"Phase tilt, m = {d['order']}, dL = {d['dL']/1e3:.3f} um")

    a = ax[1, 0]
    for p in range(cfg["n_channels"]):
        a.plot(lam_f, 10 * np.log10(spec[:, p] + 1e-12), label=f"port {p}")
    for l in lam_ch:
        a.axvline(l, color="gray", lw=0.5, ls=":")
    a.set_ylim(-50, 1); a.set_xlabel("wavelength (nm)")
    a.set_ylabel("transmission (dB)"); a.legend(); a.set_title("Output port spectra (one FSR)")

    a = ax[1, 1]
    im = a.imshow(T, cmap="viridis", vmin=0, vmax=max(T.max(), 1e-3))
    for (i, j), v in np.ndenumerate(T):
        a.text(j, i, f"{v:.2f}", ha="center", va="center",
               color="w" if v < 0.5 * T.max() else "k")
    a.set_xlabel("input channel i"); a.set_ylabel("output port")
    a.set_xticks(range(cfg["n_channels"])); a.set_yticks(range(cfg["n_channels"]))
    a.set_title("Transfer matrix T (power)")
    fig.colorbar(im, ax=a)

    fig.tight_layout()
    fig.savefig(fname, dpi=200)
    print(f"\nFigure saved to {fname}")
    plt.show()


# --------------------------------- main ------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="placeholder data, no EMode")
    ap.add_argument("--from-file", action="store_true", help="re-use saved EMode results")
    ap.add_argument("--order", type=int, default=None, help="force diffraction order m")
    args = ap.parse_args()

    wl = sweep_wavelengths(CFG)
    if args.demo:
        print("DEMO MODE: placeholder n_eff model, not EMode results")
        wl, n_eff, loss = demo_data(wl)
    elif args.from_file:
        f = np.load(CFG["results_file"])
        wl, n_eff, loss = f["wl"], f["n_eff"], f["loss"]
    else:
        wl, n_eff, loss = run_emode(CFG, wl)
        np.savez(CFG["results_file"], wl=wl, n_eff=n_eff, loss=loss)

    model = ModeModel(wl, n_eff, loss)
    d = design(CFG, model, args.order)
    T = report(CFG, model, d)
    plot(CFG, model, d, T)


if __name__ == "__main__":
    main()