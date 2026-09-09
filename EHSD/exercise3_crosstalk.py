"""
EHSD Exercise 3 - Crosstalk Between Transmission Lines
========================================================

Reproduces the calculations and plots from the exercise solution:
two coupled transmission lines (aggressor = line 1, victim = line 2),
given as per-unit-length inductance/capacitance MATRICES.

    L = [[L11, L12],     C = [[C11, C12],
         [L21, L22]]          [C21, C22]]

Part 1 (Theory):
  Q1. Characteristic impedance Z0 and time delay TD of each line (as a
      single, uncoupled line), from L11, C11.
  Q2. Near-end and far-end crosstalk on the victim line for the fully
      matched case (Zs1=Zs2=Z01=Z02=Zt1=Zt2=Z0), using the textbook
      "Case 1" formulas.
  Q3. Time-domain plots of the aggressor and victim near/far-end
      voltages, reproducing "Aggressor Line Signals" / "Victim Line
      Signals" from the solution.
  Q4. Recalculation of near/far crosstalk when the victim line's own
      terminations are mismatched (Zs2 != Z0, Zt2 != Z0), using the
      reflection-coefficient correction (1 + Gamma) applied to each
      end's crosstalk component, plus the new DC operating point.

Part 2A: equivalent lumped LC-ladder model sizing (coupling factor K,
minimum number of segments N, and per-segment L0/C0/Cm values) -- these
are the values you'd plug into an LTSpice ladder network; this script
just prints them, it does not run a SPICE-style transient simulation.

All formulas follow the same convention as the exercise:
    V_input      = Vs1 * Z0  / (Zs1 + Z0)     launched aggressor amplitude
    V_victimDC   = Vs2 * Zt2 / (Zs2 + Zt2)    victim's own DC operating point
    Kn = L12/L11 + C12/C11                    (near-end coupling term)
    Kf = L12/L11 - C12/C11                    (far-end coupling term)
    V_near_crosstalk = V_input/4 * Kn
    V_far_crosstalk  = -V_input*TD/(2*Tr) * Kf
"""

import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------
# Waveform building blocks
# ----------------------------------------------------------------------

def step_ramp(t, t_start, t_rise, level):
    """0 -> level ramp starting at t_start, holding at 'level' forever
    after (models a driven line's own transmitted step/edge)."""
    y = np.zeros_like(t)
    r0, r1 = t_start, t_start + t_rise
    m = (t >= r0) & (t < r1)
    if t_rise > 0:
        y[m] = level * (t[m] - r0) / t_rise
    y[t >= r1] = level
    return y


def near_end_pulse(t, TD, Tr, amplitude):
    """Near-end crosstalk trapezoid: rises 0->amplitude over Tr, holds
    for (2*TD - Tr), falls back to 0 over Tr. Total width = 2*TD + Tr."""
    y = np.zeros_like(t)
    r0, r1 = 0.0, Tr
    flat = max(2 * TD - Tr, 0.0)
    f0, f1 = r1 + flat, r1 + flat + Tr

    m = (t >= r0) & (t < r1)
    if Tr > 0:
        y[m] = amplitude * (t[m] - r0) / Tr
    m = (t >= r1) & (t < f0)
    y[m] = amplitude
    m = (t >= f0) & (t < f1)
    if Tr > 0:
        y[m] = amplitude * (1 - (t[m] - f0) / Tr)
    return y


def far_end_pulse(t, TD, Tr, amplitude):
    """Far-end crosstalk: a genuine RECTANGULAR pulse of width Tr,
    arriving after one line delay TD. Rise/fall time is zero here because
    this pulse is proportional to the derivative of the aggressor's ramp,
    which jumps abruptly from 0 to V/Tr at t=0 and back to 0 at t=Tr --
    i.e. the far-end response inherits the same abrupt edges, not a
    smoothed transition."""
    return np.where((t >= TD) & (t < TD + Tr), amplitude, 0.0)


# ----------------------------------------------------------------------
# USER INPUTS
# ----------------------------------------------------------------------

# Per-unit-length matrices (as given in the exercise)
L_matrix = np.array([
    [400e-9, 80e-9],
    [80e-9, 400e-9],
])  # H/m

C_matrix = np.array([
    [80e-12, 10e-12],
    [10e-12, 80e-12],
])  # F/m

X = 5e-2          # coupled line length [m]

Vs1 = 2.0         # aggressor source step amplitude [V]
Tr = 100e-12      # aggressor rise time [s]
Vs2 = 2.0         # victim source DC level [V]

# --- Case A: fully matched system (Q1-Q3) ---
Zs1_matched = Zt1_matched = Zs2_matched = Zt2_matched = None  # set below, after Z0 is known

# --- Case B: victim terminations mismatched (Q4) ---
Zs2_mismatch = 40.0     # ohm
Zt2_mismatch = 1000.0   # ohm
# (aggressor stays fully matched: Zs1 = Z01 = Zt1 = Z0)


# ----------------------------------------------------------------------
# Q1: Characteristic impedance and time delay
# ----------------------------------------------------------------------

L11, L12 = L_matrix[0, 0], L_matrix[0, 1]
L22 = L_matrix[1, 1]
C11, C12 = C_matrix[0, 0], C_matrix[0, 1]
C22 = C_matrix[1, 1]

Z0 = np.sqrt(L11 / C11)
TD = X * np.sqrt(L11 * C11)

Zs1_matched = Zt1_matched = Zs2_matched = Zt2_matched = Z0

print("=" * 60)
print("Q1: Characteristic impedance and time delay")
print("=" * 60)
print(f"Z0 = sqrt(L11/C11) = {Z0:.2f} ohm")
print(f"TD = X*sqrt(L11*C11) = {TD*1e12:.1f} ps")


# ----------------------------------------------------------------------
# Q2: Crosstalk pulses, fully matched case (Case 1)
# ----------------------------------------------------------------------

Kn = L12 / L11 + C12 / C11
Kf = L12 / L11 - C12 / C11

V_input = Vs1 * Z0 / (Zs1_matched + Z0)
V_victimDC = Vs2 * Zt2_matched / (Zs2_matched + Zt2_matched)

V_near_crosstalk = V_input / 4 * Kn
V_far_crosstalk = -V_input * TD / (2 * Tr) * Kf

V_near_total = V_victimDC + V_near_crosstalk
V_far_total = V_victimDC + V_far_crosstalk

print()
print("=" * 60)
print("Q2: Crosstalk, fully matched system (Case 1)")
print("=" * 60)
print(f"V_input      = {V_input:.4f} V")
print(f"V_victimDC   = {V_victimDC:.4f} V")
print(f"V_near_crosstalk = {V_near_crosstalk*1e3:.2f} mV")
print(f"V_near_total     = {V_near_total:.5f} V")
print(f"V_far_crosstalk  = {V_far_crosstalk*1e3:.2f} mV")
print(f"V_far_total      = {V_far_total:.4f} V")


# ----------------------------------------------------------------------
# Q3: Time-domain waveforms (matched case)
# ----------------------------------------------------------------------

t_end = 2 * TD + 3 * Tr
t = np.linspace(0, t_end, 4000)

aggressor_near = step_ramp(t, 0.0, Tr, V_input)
aggressor_far = step_ramp(t, TD, Tr, V_input)

victim_near = V_victimDC + near_end_pulse(t, TD, Tr, V_near_crosstalk)
victim_far = V_victimDC + far_end_pulse(t, TD, Tr, V_far_crosstalk)

t_ns = t * 1e9

fig1, axes1 = plt.subplots(1, 2, figsize=(11, 4.2))

axes1[0].plot(t_ns, aggressor_near, label="Near End", color="tab:blue")
axes1[0].plot(t_ns, aggressor_far, label="Far End", color="tab:orange")
axes1[0].set_title("Aggressor Line Signals")
axes1[0].set_xlabel("Time [ns]")
axes1[0].set_ylabel("Voltage [V]")
axes1[0].legend()
axes1[0].grid(True, alpha=0.3)

axes1[1].plot(t_ns, victim_near, label="Near End", color="tab:blue")
axes1[1].plot(t_ns, victim_far, label="Far End", color="tab:orange")
axes1[1].set_title("Victim Line Signals")
axes1[1].set_xlabel("Time [ns]")
axes1[1].set_ylabel("Voltage [V]")
axes1[1].legend()
axes1[1].grid(True, alpha=0.3)

fig1.suptitle("Q3: Matched system (Case 1)", fontsize=12)
fig1.tight_layout(rect=[0, 0, 1, 0.94])
fig1.savefig("q3_matched_case.png", dpi=150)


# ----------------------------------------------------------------------
# Q4: Mismatched victim terminations (Zs2, Zt2 != Z0)
# ----------------------------------------------------------------------

V_victimDC_new = Vs2 * Zt2_mismatch / (Zs2_mismatch + Zt2_mismatch)

Gamma_near = (Zs2_mismatch - Z0) / (Zs2_mismatch + Z0)
Gamma_far = (Zt2_mismatch - Z0) / (Zt2_mismatch + Z0)

V_near_crosstalk_new = V_near_crosstalk * (1 + Gamma_near)
V_far_crosstalk_new = V_far_crosstalk * (1 + Gamma_far)

V_near_new = V_victimDC_new + V_near_crosstalk_new
V_far_new = V_victimDC_new + V_far_crosstalk_new

print()
print("=" * 60)
print(f"Q4: Mismatched victim terminations (Zs2={Zs2_mismatch} ohm, Zt2={Zt2_mismatch} ohm)")
print("=" * 60)
print(f"V_victimDC_new = {V_victimDC_new:.3f} V")
print(f"Gamma_near = {Gamma_near:.4f}, Gamma_far = {Gamma_far:.4f}")
print(f"V_near_new = {V_near_new:.3f} V")
print(f"V_far_new  = {V_far_new:.3f} V")

# Bonus plot: victim signals for the mismatched case (aggressor is
# unaffected, since it's still fully matched)
victim_near_mismatch = V_victimDC_new + near_end_pulse(t, TD, Tr, V_near_crosstalk_new)
victim_far_mismatch = V_victimDC_new + far_end_pulse(t, TD, Tr, V_far_crosstalk_new)

fig2, ax2 = plt.subplots(figsize=(6.5, 4.2))
ax2.plot(t_ns, victim_near_mismatch, label="Near End", color="tab:blue")
ax2.plot(t_ns, victim_far_mismatch, label="Far End", color="tab:orange")
ax2.set_title(f"Q4: Victim Line Signals (Zs2={Zs2_mismatch} ohm, Zt2={Zt2_mismatch} ohm)")
ax2.set_xlabel("Time [ns]")
ax2.set_ylabel("Voltage [V]")
ax2.legend()
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig("q4_mismatched_case.png", dpi=150)


# ----------------------------------------------------------------------
# Part 2A: Equivalent lumped LC-ladder model sizing
# ----------------------------------------------------------------------

K_coupling = L12 / np.sqrt(L11 * L22)
N_segments = int(np.ceil(10 * TD / Tr))

L0_seg = (X / N_segments) * L11
C0_seg = (X / N_segments) * (C11 - C12)
Cm_seg = (X / N_segments) * C12

print()
print("=" * 60)
print("Part 2A: Equivalent lumped LC-ladder model")
print("=" * 60)
print(f"K (inductive coupling factor) = {K_coupling:.3f}")
print(f"N (minimum segments, N >= 10*TD/Tr) = {N_segments}")
print(f"L0_seg = {L0_seg*1e12:.1f} pH")
print(f"C0_seg = {C0_seg*1e15:.1f} fF")
print(f"Cm_seg = {Cm_seg*1e15:.2f} fF")

print()
print("Saved plots: q3_matched_case.png, q4_mismatched_case.png")

plt.show()