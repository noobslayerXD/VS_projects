"""Design study: a 4-channel arrayed waveguide grating (AWG) demultiplexer.

Workflow:
  1. EMode (finite-difference mode solver) computes the effective index n_eff
     and the propagation loss of the waveguide mode on a wavelength grid.
  2. A polynomial model of n_eff(lambda) gives the group index n_g and the
     extinction coefficient kappa.
  3. The AWG is dimensioned from the model: diffraction order m, length
     increment dL between neighbouring arms, and free spectral range (FSR).
  4. An array-factor model predicts the transmission from the input to every
     output port, which is verified in text form and plotted.
"""
import argparse  # command line flags (--demo, --from-file, --order)

import matplotlib.pyplot as plt  # plotting
import numpy as np  # numerics (arrays, polynomial fits, complex exponentials)

# ============================== CONFIGURATION ==============================
# All design parameters live in this one dictionary so they can be changed
# without touching the rest of the code.
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
    "n_channels": 4,               # number of wavelength channels / output ports
    "lambda_center": 1550.0,       # nm
    "channel_spacing": 1.6,        # nm (~200 GHz)

    # --- AWG ---
    "order": None,                 # diffraction order m; None = choose so FSR = N * spacing
    "n_arms": 24,                  # number of arrayed waveguides
    "L0_um": 50.0,                 # length of the shortest arm (only affects loss)
    "gaussian_edge": 0.15,         # relative illumination of the outermost arms

    # --- sweep ---
    "n_sweep": 9,                  # EMode wavelength points
    "sim_name": "awg_arm",         # name of the EMode simulation (its data file)
    "results_file": "awg_emode_results.npz",  # cache of the sweep result (for --from-file)
}
# ===========================================================================

# Converts a loss in dB to nepers (power): 10*log10(e) = 4.343 dB per neper.
DB_PER_NEPER_POWER = 10 * np.log10(np.e)    # 4.343 dB per neper of power


def sweep_wavelengths(cfg):
    """Wavelength grid covering all channels with some margin on both sides."""
    # Half of the channel span (N * spacing) plus 50 % margin => 0.75 * N * spacing
    half_span = 0.75 * cfg["n_channels"] * cfg["channel_spacing"]
    # Evenly spaced points centred on the centre wavelength
    return np.linspace(cfg["lambda_center"] - half_span,
                       cfg["lambda_center"] + half_span, cfg["n_sweep"])


def channel_wavelengths(cfg):
    """Centre wavelengths of the N channels, spaced by channel_spacing around lambda_center."""
    N, s = cfg["n_channels"], cfg["channel_spacing"]
    # (arange(N) - (N-1)/2) = symmetric offsets, e.g. -1.5, -0.5, 0.5, 1.5 for N = 4
    return cfg["lambda_center"] + (np.arange(N) - (N - 1) / 2) * s


# ------------------------------ 1. EMode ----------------------------------
def run_emode(cfg, wl_nm):
    """Solve the fundamental TE mode at each wavelength with EMode's FDM solver."""
    # Imported here so the demo / from-file modes work without EMode installed
    import emodeconnection as emc

    # Open (create) an EMode simulation
    em = emc.EMode(simulation_name=cfg["sim_name"])
    # Global solver settings: the mesh and the simulation window
    em.settings(
        wavelength=float(wl_nm[len(wl_nm) // 2]),          # start at the middle of the sweep
        x_resolution=cfg["dx"], y_resolution=cfg["dy"],    # mesh step in nm
        # Window = core + cladding on each side horizontally ...
        window_width=cfg["w_core"] + 2 * cfg["w_side"],
        # ... and BOX below + core + top cladding above vertically
        window_height=cfg["h_core"] + 2 * cfg["h_clad"],
        num_modes=1,                                       # only the fundamental mode
        boundary_condition="TE",                           # solve for the TE-polarised mode
        background_material=cfg["cladding_material"])      # everything not drawn = cladding

    # Geometry: buried oxide layer (BOX) at the bottom, silicon core on top of it
    em.shape(name="BOX", material=cfg["box_material"], height=cfg["h_clad"])
    em.shape(name="core", material=cfg["core_material"],
             width=cfg["w_core"], height=cfg["h_core"])

    # Check the mode at the centre wavelength before sweeping
    em.FDM()                                               # run the finite-difference mode solver
    em.report()                                            # print mode data to the console
    em.plot(component="Ex", file_name="mode_profile_center", file_type="png")  # save field plot

    # Repeat the solve for every wavelength and store n_eff and loss for each
    em.sweep(key="wavelength", values=list(map(float, wl_nm)),
             result=["effective_index", "loss_dB_per_m"])
    em.close()                                             # save and close the simulation

    # Read the stored sweep data (this part works without a licence)
    data = emc.get(variable="sweep_data", simulation_name=cfg["sim_name"])
    wl = np.asarray(data["values"], dtype=float)
    # Results are (n_wavelengths x n_modes); keep only column 0 = the fundamental mode
    n_eff = np.asarray(data["effective_index"], dtype=float).reshape(len(wl), -1)[:, 0]
    loss = np.asarray(data["loss_dB_per_m"], dtype=float).reshape(len(wl), -1)[:, 0]
    # Sort by wavelength so the arrays are monotonic (needed for fitting / plotting)
    order = np.argsort(wl)
    return wl[order], n_eff[order], loss[order]


def demo_data(wl_nm):
    """PLACEHOLDER numbers roughly like a 500x220 nm SOI wire. Not simulation results."""
    d = wl_nm - 1550.0                                     # detuning from 1550 nm
    # Quadratic dispersion: n_eff = 2.44 at 1550 nm, falling with wavelength
    n_eff = 2.44 - 1.135e-3 * d - 2e-7 * d**2
    loss = np.full_like(wl_nm, 200.0)       # 2 dB/cm (= 200 dB/m), constant
    return wl_nm, n_eff, loss


# ------------------------------ 2. Model ----------------------------------
class ModeModel:
    """n_eff(lambda), n_g(lambda) and kappa(lambda) from the sweep points."""

    def __init__(self, wl, n_eff, loss_dB_per_m):
        # Keep the raw sweep points (used for printing and plotting)
        self.wl, self.n_eff_pts, self.loss_pts = wl, n_eff, loss_dB_per_m
        # Quadratic fit of n_eff(lambda); lower degree if there are too few points
        deg = min(2, len(wl) - 1)
        self.p = np.polyfit(wl, n_eff, deg)
        # Derivative polynomial dn_eff/dlambda, needed for the group index
        self.dp = np.polyder(self.p)
        # Linear fit of the loss in dB/m
        self.p_loss = np.polyfit(wl, loss_dB_per_m, min(1, len(wl) - 1))

    def n_eff(self, lam):
        """Effective index from the fitted polynomial."""
        return np.polyval(self.p, lam)

    def n_g(self, lam):
        """Group index n_g = n_eff - lambda * dn_eff/dlambda."""
        return self.n_eff(lam) - lam * np.polyval(self.dp, lam)

    def alpha_power_per_nm(self, lam):
        """Power attenuation coefficient in 1/nm (dB/m -> nepers/m -> per nm)."""
        return np.polyval(self.p_loss, lam) / DB_PER_NEPER_POWER * 1e-9

    def kappa(self, lam):
        """Imaginary part of the effective index (extinction coefficient)."""
        # alpha = 4*pi*kappa/lambda0   ->   kappa = alpha*lambda0/(4*pi)
        return self.alpha_power_per_nm(lam) * lam / (4 * np.pi)

    def beta(self, lam):
        """Propagation constant beta = 2*pi*n_eff/lambda."""
        return 2 * np.pi * self.n_eff(lam) / lam             # rad/nm

    def H(self, lam, L_nm):
        """Complex field transfer of a straight section of length L."""
        # First factor: phase delay exp(-j*beta*L). Second factor: field loss
        # exp(-2*pi*kappa*L/lambda) (= half of the power attenuation).
        return np.exp(-1j * self.beta(lam) * L_nm) * \
               np.exp(-2 * np.pi * self.kappa(lam) * L_nm / lam)


def wrap(phi):
    """Wrap a phase into the interval [-pi, pi)."""
    return (phi + np.pi) % (2 * np.pi) - np.pi


# ------------------------------ 3-5. Design --------------------------------
def design(cfg, model, order=None):
    """Dimension the AWG: diffraction order m, arm length step dL and FSR."""
    lam_c = cfg["lambda_center"]
    N, s = cfg["n_channels"], cfg["channel_spacing"]
    # Effective and group index at the centre wavelength
    n_c, ng_c = model.n_eff(lam_c), model.n_g(lam_c)

    # FSR ~ lambda_c * n_eff / (n_g * m); choose m so FSR = N * channel spacing
    if order is None:
        # Priority: order from the config; otherwise computed and rounded to an integer (>= 1)
        order = cfg["order"] or max(1, round(lam_c * n_c / (ng_c * N * s)))
    # Path difference between neighbouring arms: m whole wavelengths in the waveguide
    # (phase step = 2*pi*m at the centre wavelength)
    dL = order * lam_c / n_c                                   # Scenario 1
    # Free spectral range: wavelength distance between repeating grating orders
    fsr = lam_c**2 / (ng_c * dL)
    return {"order": order, "dL": dL, "fsr": fsr, "n_c": n_c, "ng_c": ng_c}


def transfer_matrix(cfg, model, d, lam):
    """Array-factor model: power at each output port vs wavelength.

    Arm k has length L0 + k*dL. The output star coupler turns a linear phase
    tilt psi across the arms into a focal position; output port p sits where
    channel p focuses, i.e. it collects tilt psi_p = psi(lambda_p).
    """
    M = cfg["n_arms"]
    # Symmetric arm index around zero, e.g. -11.5 ... +11.5 for 24 arms
    k = np.arange(M) - (M - 1) / 2
    # Gaussian width chosen so the outermost arm (|k| = M/2) gets 'gaussian_edge' of the centre amplitude
    sigma = (M / 2) / np.sqrt(-2 * np.log(cfg["gaussian_edge"]))
    w = np.exp(-k**2 / (2 * sigma**2))                         # illumination
    L0 = cfg["L0_um"] * 1e3                                    # shortest arm: um -> nm

    # Each output port is placed where "its" channel wavelength focuses:
    # the phase step per arm at that wavelength (wrapped to +-pi)
    lam_ch = channel_wavelengths(cfg)
    psi_port = wrap(model.beta(lam_ch) * d["dL"])              # port positions

    lam = np.atleast_1d(lam)                                   # accept a scalar or an array
    # Field of every arm for every wavelength: shape (lam, arms);
    # arm i has length L0 + i*dL, with i = k + (M-1)/2 = 0 ... M-1
    H_arms = model.H(lam[:, None], L0 + (k + (M - 1) / 2)[None, :] * d["dL"])
    # constant phase of the shortest arm is irrelevant -> remove it
    H_arms = H_arms * np.exp(1j * model.beta(lam)[:, None] * L0)
    # Phase weights that "steer" the sum towards each port: (ports, arms)
    steer = np.exp(1j * np.outer(psi_port, k))                 # (ports, arms)
    # Weighted coherent sum over the arms for each port, normalised by the
    # total illumination => complex amplitude per (wavelength, port)
    a = (H_arms * w[None, :]) @ steer.T / w.sum()              # (lam, ports)
    # Power = |amplitude|^2; also return the port tilts
    return np.abs(a)**2, psi_port


def report(cfg, model, d):
    """Print mode data, the design, a phase check and the transfer matrix; return T."""
    lam_ch = channel_wavelengths(cfg)
    # Table of the raw EMode (or demo) sweep points; loss converted from dB/m to dB/cm
    print("\n=== Mode data from sweep ===")
    print(f"{'lambda (nm)':>12} {'n_eff':>10} {'loss (dB/cm)':>13} {'kappa':>11}")
    for l, n, a in zip(model.wl, model.n_eff_pts, model.loss_pts):
        print(f"{l:12.2f} {n:10.6f} {a/100:13.3f} {model.kappa(l):11.3e}")

    # The dimensioning result
    print("\n=== Scenario 1 design ===")
    print(f"centre wavelength      : {cfg['lambda_center']:.2f} nm")
    print(f"n_eff / n_g at centre  : {d['n_c']:.5f} / {d['ng_c']:.5f}")
    print(f"diffraction order m    : {d['order']}  (phase step 2*pi*m at centre)")
    print(f"length increment dL    : {d['dL']/1e3:.4f} um")
    print(f"free spectral range    : {d['fsr']:.3f} nm "
          f"(channels span {cfg['n_channels']*cfg['channel_spacing']:.2f} nm)")

    # Sanity check: at the centre wavelength the phase step is a multiple of 2*pi;
    # for the other channels the wrapped tilt shows how far they are steered
    print("\n=== Verification: phase per arm step for each channel ===")
    print(f"{'channel':>8} {'lambda (nm)':>12} {'n_eff':>10} "
          f"{'beta*dL (rad)':>14} {'tilt (deg)':>11} {'|H(dL)|':>9}")
    for i, l in enumerate(lam_ch):
        phi = model.beta(l) * d["dL"]                          # total phase step per arm
        print(f"{i:8d} {l:12.2f} {model.n_eff(l):10.6f} {phi:14.4f} "
              f"{np.degrees(wrap(phi)):11.2f} {abs(model.H(l, d['dL'])):9.5f}")

    # Evaluate the AWG exactly at the channel wavelengths
    T, _ = transfer_matrix(cfg, model, d, lam_ch)
    T = T.T                                                    # rows = ports
    print("\n=== Transfer matrix T[port, channel] (power, linear) ===")
    for row in T:
        print("  [" + "  ".join(f"{v:6.3f}" for v in row) + " ]")
    diag = np.diag(T)                                          # wanted: channel i -> port i
    off = T - np.diag(diag)                                    # unwanted: channel i -> port j != i
    # Worst insertion loss = weakest wanted transmission
    print(f"insertion loss (worst) : {-10*np.log10(diag.min()):.2f} dB")
    # Worst crosstalk = strongest unwanted signal relative to the weakest wanted one
    print(f"crosstalk (worst)      : {10*np.log10(off.max()/diag.min()):.1f} dB")
    return T


def plot(cfg, model, d, T, fname="awg_design.png"):
    """Make a 2x2 figure of the design, save it to `fname` and show it."""
    lam_ch = channel_wavelengths(cfg)
    # Fine wavelength grid over exactly one FSR around the centre wavelength
    lam_f = np.linspace(cfg["lambda_center"] - d["fsr"] / 2,
                        cfg["lambda_center"] + d["fsr"] / 2, 2000)
    # Transmission to all ports over that grid
    spec, _ = transfer_matrix(cfg, model, d, lam_f)

    fig, ax = plt.subplots(2, 2, figsize=(11, 8))

    # (top left) n_eff points, the fit, and n_g on a second y-axis
    a = ax[0, 0]
    lf = np.linspace(model.wl.min(), model.wl.max(), 200)
    a.plot(model.wl, model.n_eff_pts, "o", label="EMode n_eff")
    a.plot(lf, model.n_eff(lf), "-", label="fit")
    a.set_xlabel("wavelength (nm)"); a.set_ylabel("n_eff")
    a2 = a.twinx(); a2.plot(lf, model.n_g(lf), "r--", label="n_g")
    a2.set_ylabel("n_g", color="r")
    a.legend(loc="upper right"); a.set_title("Mode indices")

    # (top right) wrapped phase step per arm vs wavelength, with the channels marked
    a = ax[0, 1]
    tilt = np.degrees(wrap(model.beta(lam_f) * d["dL"]))
    a.plot(lam_f, tilt, "k.", ms=1)
    for l in lam_ch:
        a.plot(l, np.degrees(wrap(model.beta(l) * d["dL"])), "o")
    a.set_xlabel("wavelength (nm)"); a.set_ylabel("phase step per arm (deg, wrapped)")
    a.set_title(f"Phase tilt, m = {d['order']}, dL = {d['dL']/1e3:.3f} um")

    # (bottom left) spectrum of every output port in dB; dotted lines = channel wavelengths
    a = ax[1, 0]
    for p in range(cfg["n_channels"]):
        # + 1e-12 avoids log10(0) in the deep nulls
        a.plot(lam_f, 10 * np.log10(spec[:, p] + 1e-12), label=f"port {p}")
    for l in lam_ch:
        a.axvline(l, color="gray", lw=0.5, ls=":")
    a.set_ylim(-50, 1); a.set_xlabel("wavelength (nm)")
    a.set_ylabel("transmission (dB)"); a.legend(); a.set_title("Output port spectra (one FSR)")

    # (bottom right) transfer matrix as a heat map with the value in every cell
    a = ax[1, 1]
    im = a.imshow(T, cmap="viridis", vmin=0, vmax=max(T.max(), 1e-3))
    for (i, j), v in np.ndenumerate(T):
        # White text on dark cells, black on bright cells
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
    """Pick a data source (EMode / demo / file), build the model, design the AWG, report and plot."""
    # Command line options
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="placeholder data, no EMode")
    ap.add_argument("--from-file", action="store_true", help="re-use saved EMode results")
    ap.add_argument("--order", type=int, default=None, help="force diffraction order m")
    args = ap.parse_args()

    # Wavelengths at which the waveguide mode is needed
    wl = sweep_wavelengths(CFG)
    if args.demo:
        # 1a) Made-up numbers, quick test of the rest of the code
        print("DEMO MODE: placeholder n_eff model, not EMode results")
        wl, n_eff, loss = demo_data(wl)
    elif args.from_file:
        # 1b) Load the results of an earlier EMode run
        f = np.load(CFG["results_file"])
        wl, n_eff, loss = f["wl"], f["n_eff"], f["loss"]
    else:
        # 1c) Run EMode and save the results for later --from-file runs
        wl, n_eff, loss = run_emode(CFG, wl)
        np.savez(CFG["results_file"], wl=wl, n_eff=n_eff, loss=loss)

    model = ModeModel(wl, n_eff, loss)         # 2) fit n_eff, n_g and loss
    d = design(CFG, model, args.order)         # 3) order, dL and FSR
    T = report(CFG, model, d)                  # 4) print tables, get transfer matrix
    plot(CFG, model, d, T)                     # 5) figure


# Run main() only when the file is executed directly (not when imported)
if __name__ == "__main__":
    main()
