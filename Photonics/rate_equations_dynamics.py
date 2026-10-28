"""
Laser dynamics with the rate equations (see the exercises for the equations).

    1/tau_sp(N) = A + B*N + C*N**2
    g(N)        = a*(N - N_tr)

N: carrier density, S: photon density of the lasing mode.
Units: cm, s, A.  N and S in cm^-3.

Fill in the two lines marked TODO in rate_equations(), then run:
    python rate_equations_dynamics.py
The script then produces all the plots used in the exercises.
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

SAVE_FIGURES = False

# ---------------------------------------------------------------- constants
q = 1.602e-19        # elementary charge [C]
h = 6.626e-34        # Planck constant [J s]
c = 2.998e10         # speed of light [cm/s]

# ---------------------------------------------------------------- cavity (edge emitter)
lam = 1550e-7        # lasing wavelength [cm]
n_g = 3.0            # group index
L_cav = 0.1          # cavity length [cm]  (1 mm)
r = 0.3              # |rho_1 rho_2|
alpha_cav = 0.24     # average cavity loss [cm^-1]
Gamma = 0.025        # optical confinement factor
V_act = 5e-12        # active volume [cm^3]  (5 um^3)

v_g = c / n_g                                  # group velocity [cm/s]
alpha_mi = -np.log(r) / L_cav                  # mirror loss [cm^-1]
tau_ph = 1.0 / (v_g * (alpha_cav + alpha_mi))  # photon lifetime [s]
g_th = (alpha_cav + alpha_mi) / Gamma          # threshold gain [cm^-1]

# ---------------------------------------------------------------- material (InGaAsP quantum wells)
eta_i = 0.8          # injection efficiency
A = 1e8              # SRH coefficient [s^-1]
B = 1e-10            # radiative coefficient [cm^3/s]
C = 3e-29            # Auger coefficient [cm^6/s]
a = 5e-16            # differential gain [cm^2]
N_tr = 1.5e18        # transparency carrier density [cm^-3]
beta = 1e-5          # spontaneous emission factor

N_th = N_tr + g_th / a   # threshold carrier density [cm^-3]
alpha_H = 3.0            # linewidth enhancement factor (for the chirp)


def tau_sp(N):
    return 1.0 / (A + B * N + C * N**2)


def gain(N):
    return a * (N - N_tr)


def rate_equations(t, y, I):
    N, S = y
    dN = None        # TODO: right-hand side of the carrier equation
    dS = None        # TODO: right-hand side of the photon equation
    return [dN, dS]


def output_power(S):
    """Total power leaving through both mirrors [W]."""
    eta_opt = alpha_mi / (alpha_mi + alpha_cav)
    E_photon = h * c / lam
    return eta_opt * E_photon * S * (V_act / Gamma) / tau_ph


def simulate(I, t_end, y0=(0.0, 0.0)):
    """Solve the rate equations at constant current I [A] from t = 0 to t_end [s],
    starting from y0 = (N, S). Returns t, N(t), S(t)."""
    sol = solve_ivp(rate_equations, (0, t_end), y0, args=(I,),
                    method="LSODA", rtol=1e-8, atol=[1e6, 1e-2],
                    max_step=t_end / 5000)
    return sol.t, sol.y[0], sol.y[1]


def steady_state(I):
    """Steady-state (N, S) at constant current I [A], found by simulating
    long enough for the turn-on transient to die out."""
    if I == 0:
        return 0.0, 0.0
    t, N, S = simulate(I, 30e-9)
    return N[-1], S[-1]


def jacobian(N0, S0):
    """Partial derivatives of (dN/dt, dS/dt) with respect to (N, S),
    evaluated at the steady state (N0, S0)."""
    g0 = gain(N0)
    dN_dN = -(A + 2 * B * N0 + 3 * C * N0**2) - v_g * a * S0
    dN_dS = -v_g * g0
    dS_dN = Gamma * v_g * a * S0 + 2 * Gamma * beta * B * N0
    dS_dS = Gamma * v_g * g0 - 1 / tau_ph
    return np.array([[dN_dN, dN_dS], [dS_dN, dS_dS]])


def finish(fig, name):
    fig.tight_layout()
    if SAVE_FIGURES:
        fig.savefig(name, dpi=150)


if __name__ == "__main__":
    print(f"alpha_mi = {alpha_mi:.2f} cm^-1, tau_ph = {tau_ph*1e12:.2f} ps, "
          f"g_th = {g_th:.0f} cm^-1, N_th = {N_th:.3e} cm^-3")

    # ---- 1. Current step from 0 to 5 mA
    t, N, S = simulate(5e-3, 6e-9)
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6, 5))
    ax[0].plot(t * 1e9, N / 1e18)
    ax[0].axhline(N_th / 1e18, ls="--", c="gray", label="$N_{th}$")
    ax[0].set_ylabel("N [$10^{18}$ cm$^{-3}$]"); ax[0].legend()
    ax[1].plot(t * 1e9, output_power(S) * 1e3)
    ax[1].set_ylabel("P [mW]"); ax[1].set_xlabel("t [ns]")
    ax[0].set_title("Current step from 0 to 5 mA")
    finish(fig, "step_response.png")

    # ---- 2. Steady state against current
    currents = np.linspace(0, 10e-3, 21)
    NS = np.array([steady_state(I) for I in currents])
    P_ss = output_power(NS[:, 1])
    upper = currents >= 5e-3                       # fit the linear part of the L-I curve
    slope, offset = np.polyfit(currents[upper], P_ss[upper], 1)
    I_th = -offset / slope
    print(f"From the L-I curve: I_th = {I_th*1e3:.2f} mA, slope efficiency = {slope:.2f} W/A")
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
    ax[0].plot(currents * 1e3, P_ss * 1e3, "o-")
    ax[0].set_xlabel("I [mA]"); ax[0].set_ylabel("P [mW]")
    ax[1].plot(currents * 1e3, NS[:, 0] / 1e18, "o-")
    ax[1].axhline(N_th / 1e18, ls="--", c="gray", label="$N_{th}$"); ax[1].legend()
    ax[1].set_xlabel("I [mA]"); ax[1].set_ylabel("N [$10^{18}$ cm$^{-3}$]")
    finish(fig, "LI_curve.png")

    # ---- 3. Steps to 5 mA from different bias currents (turn-on and chirp)
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6, 5))
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    for I_b, label in [(0.0, "from 0"), (0.9 * I_th, "from 0.9 $I_{th}$"),
                       (1.1 * I_th, "from 1.1 $I_{th}$")]:
        t, N, S = simulate(5e-3, 4e-9, steady_state(I_b))
        P = output_power(S)
        ax[0].plot(t * 1e9, N / 1e18, label=label)
        ax[1].plot(t * 1e9, P * 1e3, label=label)
        # chirp, shown only while the laser emits light
        dnu = alpha_H / (4 * np.pi) * Gamma * v_g * a * (N - N_th)
        ax2.plot(t * 1e9, np.where(P > 0.05 * P[-1], dnu / 1e9, np.nan), label=label)
    ax[0].axhline(N_th / 1e18, ls="--", c="gray")
    ax[0].set_ylabel("N [$10^{18}$ cm$^{-3}$]"); ax[0].legend()
    ax[1].set_ylabel("P [mW]"); ax[1].set_xlabel("t [ns]")
    ax[0].set_title("Steps to 5 mA from different bias currents")
    ax2.set_xlabel("t [ns]"); ax2.set_ylabel("$\\Delta\\nu$ [GHz]"); ax2.legend()
    ax2.set_title("Frequency deviation (chirp)")
    finish(fig, "turn_on.png")
    finish(fig2, "chirp.png")

    # ---- 4. Small-signal modulation response
    # The small-signal amplitudes x = (dN, dS) solve (2j*pi*f*1 - J) x = b,
    # with b = (eta_i/(q*V_act), 0) for a current amplitude of 1 A.
    f = np.linspace(1e7, 15e9, 3000)
    b = np.array([eta_i / (q * V_act), 0.0])
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for I0 in (2e-3, 5e-3, 10e-3):
        N0, S0 = steady_state(I0)
        J = jacobian(N0, S0)
        dS = np.array([np.linalg.solve(2j * np.pi * fi * np.eye(2) - J, b)[1] for fi in f])
        H = np.abs(dS / dS[0])
        f_R = np.sqrt(v_g * a * S0 / tau_ph) / (2 * np.pi)
        f_3dB = f[np.where(H >= 1 / np.sqrt(2))[0][-1]]
        print(f"I0 = {I0*1e3:4.1f} mA: peak at {f[np.argmax(H)]/1e9:.2f} GHz "
              f"({20*np.log10(H.max()):.1f} dB), f_R = {f_R/1e9:.2f} GHz, "
              f"3-dB bandwidth = {f_3dB/1e9:.2f} GHz")
        ax.plot(f / 1e9, 20 * np.log10(H), label=f"{I0*1e3:.0f} mA")
    ax.axhline(-3, ls=":", c="gray"); ax.set_ylim(-20, 20)
    ax.set_xlabel("modulation frequency [GHz]"); ax.set_ylabel("$|\\delta S/\\delta S(0)|$ [dB]")
    ax.legend(); ax.set_title("Small-signal modulation response")
    finish(fig, "modulation_response.png")

    plt.show()
