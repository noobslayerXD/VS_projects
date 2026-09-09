"""
Crosstalk (NEXT / FEXT) plotter for two coupled transmission lines
===================================================================

Implements the classic near-end / far-end crosstalk waveform formulas for a
pair of coupled lossless transmission lines, for the three standard
termination cases:

    Case 1: both ends of the (quiet) line matched, R_near = R_far = Zo
            -> Near end sees a trapezoidal pulse that returns to 0.
            -> Far end sees a narrow rectangular pulse of width Tr.

    Case 2: near end matched (R_near = Zo), far end OPEN (unterminated)
            -> Near end: same trapezoid as Case 1.
            -> Far end: crosstalk does NOT return to zero -- it ramps up
               and saturates (charges up the open end).

    Case 3: near end OPEN/mismatched, far end matched (R_far = Zo)
            -> The mismatch at the near end reflects the aggressor's edge,
               which travels the line again and creates a SECOND crosstalk
               event at the far end, arriving after a full round trip
               (i.e. around t = 3*Td instead of t = Td).

    (Case is selected automatically per line, by comparing that line's
    near/far termination resistors against Zo.)

Inductance / capacitance MATRICES
----------------------------------
L and C are given as 2x2 per-unit-length matrices for the coupled pair,
following the same convention as the Maxwell capacitance-matrix derivation
(KCL: I1 = (Cg+Cm) dV1/dt - Cm dV2/dt  ->  matrix has -Cm off-diagonal):

    C_matrix = [[Cg + Cm,   -Cm   ],        L_matrix = [[L11,  Lm ],
                [  -Cm,    Cg + Cm]]                     [Lm,  L22]]

    (capacitance off-diagonal carries a MINUS sign in front of Cm;
     inductance off-diagonal is the mutual inductance Lm directly,
     no sign flip -- this is standard for coupled telegrapher's equations)

From these matrices the script extracts, per line i:
    L_i  = L_matrix[i,i]                       (self inductance)
    Lm   = L_matrix[0,1]                       (mutual inductance)
    Cg_i = C_matrix[i,i] + C_matrix[i,(1-i)]   (line-to-ground self capacitance,
                                                 i.e. Cg = (Cg+Cm) - Cm)
    Cm   = -C_matrix[0,1]                      (mutual capacitance)

and then uses the standard weak-coupling coefficients:
    Kn = 0.25 * (Lm/L + Cm/Cg)     near-end coupling coefficient
    Kf = (Lm/L - Cm/Cg)            far-end coupling coefficient
    Td = X * sqrt(L * Cg)          one-way propagation delay

Driver launch voltage (source-resistor divider)
------------------------------------------------
Each driver Vs_i has a series source resistor -- this is exactly R_near_i,
the resistor sitting between the source and the near end of the line (see
the original diagram: V(input) -- R=Zo -- line). Before any
reflections come back, the line simply looks like a resistor of value Zo,
so the amplitude that actually launches onto the line is the divided-down
value, not the raw source voltage:

    V_launched = Vs * Zo / (Rs + Zo)

This launched amplitude (not the raw Vs) is what feeds the Kn/Kf crosstalk
formulas above, since those describe the response to the traveling wave
actually on the line.

Two independent drivers Vs1 (on line 1) and Vs2 (on line 2) are supported.
Vs1 induces crosstalk onto line 2 (its near/far ends); Vs2 induces
crosstalk onto line 1 (its near/far ends). Because the system is linear,
these two contributions could simply be added if you want the total
disturbance seen with both drivers active simultaneously.

Edit the "USER INPUTS" section below and run the script.
"""

import matplotlib.pyplot as plt
import numpy as np


def extract_line_params(L_matrix, C_matrix, line_index):
    """
    Pull the self/mutual inductance & capacitance a single line needs for
    the crosstalk formulas, out of the full 2x2 L and C matrices.

    line_index: 0 for line 1, 1 for line 2.
    """
    L_matrix = np.asarray(L_matrix, dtype=float)
    C_matrix = np.asarray(C_matrix, dtype=float)
    other = 1 - line_index

    L_self = L_matrix[line_index, line_index]
    Lm = L_matrix[line_index, other]

    # Diagonal C entry is (Cg + Cm); off-diagonal entry is already -Cm.
    # Adding them cancels Cm, leaving the line-to-ground self capacitance.
    Cg = C_matrix[line_index, line_index] + C_matrix[line_index, other]
    Cm = -C_matrix[line_index, other]

    return L_self, Lm, Cg, Cm


def launched_voltage(Vs, Rs, Zo):
    """Voltage-divider amplitude actually launched onto a line of
    impedance Zo, driven through series source resistor Rs."""
    return Vs * Zo / (Rs + Zo)


# ----------------------------------------------------------------------
# Core waveform model
# ----------------------------------------------------------------------

def _trapezoid(t, t_start, t_rise, t_flat, t_fall, level):
    """Piecewise-linear pulse: 0 -> level over t_rise, flat for t_flat,
    back to 0 over t_fall, starting at t_start. Works for level < 0 too."""
    y = np.zeros_like(t)

    r0, r1 = t_start, t_start + t_rise
    f0, f1 = r1 + t_flat, r1 + t_flat + t_fall

    # rising edge
    m = (t >= r0) & (t < r1)
    if t_rise > 0:
        y[m] = level * (t[m] - r0) / t_rise

    # flat top
    m = (t >= r1) & (t < f0)
    y[m] = level

    # falling edge
    m = (t >= f0) & (t < f1)
    if t_fall > 0:
        y[m] = level * (1 - (t[m] - f0) / t_fall)

    return y


def _saturating_ramp(t, t_start, t_rise, level):
    """0 -> level ramp starting at t_start, then holds at 'level' forever
    (models an open/unterminated far end that charges up and stays there)."""
    y = np.zeros_like(t)
    r0, r1 = t_start, t_start + t_rise
    m = (t >= r0) & (t < r1)
    if t_rise > 0:
        y[m] = level * (t[m] - r0) / t_rise
    y[t >= r1] = level
    return y


def crosstalk_waveforms(t, Vin, L, C, Lm, Cm, Tr, X, Zo, R_near, R_far, tol=1e-6):
    """
    Compute near-end and far-end crosstalk voltage waveforms induced onto
    a quiet victim line, when the adjacent line is driven by a step/ramp
    of LAUNCHED amplitude Vin (i.e. already after the source-resistor
    divider -- see launched_voltage()) and rise time Tr.

    R_near, R_far: termination resistors on the AGGRESSOR line (these are
    what determine reflections of the aggressor's edge, i.e. which of the
    three textbook cases applies).

    Returns (v_near, v_far, case_used)
    """
    Td = X * np.sqrt(L * C)
    Kn = 0.25 * (Lm / L + Cm / C)
    Kf = (Lm / L - Cm / C)

    near_matched = abs(R_near - Zo) < tol * max(Zo, 1)
    far_matched = abs(R_far - Zo) < tol * max(Zo, 1)

    A = Vin * Kn  # near-end plateau amplitude (same in all cases)

    if near_matched and far_matched:
        # ---- Case 1: both ends matched ----
        case = 1
        v_near = _trapezoid(t, 0.0, Tr, max(2 * Td - Tr, 0.0), Tr, A)

        B = -Vin * Td / (2 * Tr) * Kf
        v_far = _trapezoid(t, Td, Tr / 2, 0.0, Tr / 2, B)  # narrow pulse, width Tr

    elif near_matched and not far_matched:
        # ---- Case 2: near matched, far end open/unterminated ----
        case = 2
        v_near = _trapezoid(t, 0.0, Tr, max(2 * Td - Tr, 0.0), Tr, A)

        C_final = -Vin * Td / Tr * Kf
        v_far = _saturating_ramp(t, Td, Tr, C_final)

    else:
        # ---- Case 3: near end open/mismatched, far end matched ----
        case = 3
        v_near = _trapezoid(t, 0.0, Tr, max(2 * Td - Tr, 0.0), Tr, A)

        # First pulse arrives after one line delay (like Case 1),
        # a second (reflected) pulse arrives after a full round trip.
        B1 = -Vin * Td / (2 * Tr) * Kf
        B2 = B1  # first-order approximation: reflected pulse of similar size
        pulse1 = _trapezoid(t, Td, Tr / 2, 0.0, Tr / 2, B1)
        pulse2 = _trapezoid(t, 3 * Td, Tr / 2, 0.0, Tr / 2, B2)
        v_far = pulse1 + pulse2

    return v_near, v_far, case


# ----------------------------------------------------------------------
# USER INPUTS
# ----------------------------------------------------------------------

# Driver amplitudes (V) and rise time (s)
Vs1 = 2.0        # source (open-circuit) voltage on line 1 -> crosstalk on line 2
Vs2 = 2.0        # source (open-circuit) voltage on line 2 -> crosstalk on line 1
Tr = 1e-10       # rise time [s]

# Line geometry
X = 0.05         # coupled length [m]

# Per-unit-length INDUCTANCE matrix [H/m]:  [[L11, Lm], [Lm, L22]]
L_matrix = np.array([
    [400e-9,  80e-9],
    [ 80e-9, 400e-9],
])

# Per-unit-length CAPACITANCE matrix [F/m], Maxwell-matrix convention:
# diagonal = Cg + Cm, off-diagonal = -Cm   (see docstring above)
C_matrix = np.array([
    [8e-11, 1e-11],
    [1e-11, 8e-11],
])

# Characteristic impedance and terminations (Ohms)
Z0 = np.sqrt(L_matrix[0, 0] / C_matrix[0, 0])  # Zo of line 1 (assumed same for line 2)

# Terminations for line 1 (R_near_1 doubles as line 1's driver source
# resistor Rs1) -- determine the crosstalk case seen on line 2:
R_near_1 = Z0
R_far_1 = Z0
# Terminations for line 2 (R_near_2 doubles as line 2's driver source
# resistor Rs2) -- determine the crosstalk case seen on line 1:
R_near_2 = Z0
R_far_2 = Z0

# ----------------------------------------------------------------------
# Compute
# ----------------------------------------------------------------------

# Extract per-line self/mutual parameters from the matrices
L1, Lm1, Cg1, Cm1 = extract_line_params(L_matrix, C_matrix, line_index=0)
L2, Lm2, Cg2, Cm2 = extract_line_params(L_matrix, C_matrix, line_index=1)

# Time axis (based on line 1's propagation delay)
Td_est = X * np.sqrt(L1 * Cg1)
t_end = 6 * Td_est + 4 * Tr
t = np.linspace(0, t_end, 4000)

# Source-resistor divider: the amplitude that actually launches onto each
# line is Vs * Z0/(Rs + Z0), not the raw source voltage.
V1_launched = launched_voltage(Vs1, R_near_1, Z0)
V2_launched = launched_voltage(Vs2, R_near_2, Z0)

# Vs1 drives line 1 -> crosstalk observed on line 2
near2, far2, case2 = crosstalk_waveforms(t, V1_launched, L1, Cg1, Lm1, Cm1, Tr, X, Z0, R_near_1, R_far_1)

# Vs2 drives line 2 -> crosstalk observed on line 1
near1, far1, case1 = crosstalk_waveforms(t, V2_launched, L2, Cg2, Lm2, Cm2, Tr, X, Z0, R_near_2, R_far_2)

t_ns = t * 1e9

# ----------------------------------------------------------------------
# Plot
# ----------------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=True)

axes[0, 0].plot(t_ns, near2, color="tab:blue")
axes[0, 0].set_title(f"Near-end crosstalk on line 2 (from Vs1)  -  Case {case2}")
axes[0, 0].set_ylabel("V (near)")

axes[0, 1].plot(t_ns, far2, color="tab:red")
axes[0, 1].set_title(f"Far-end crosstalk on line 2 (from Vs1)  -  Case {case2}")
axes[0, 1].set_ylabel("V (far)")

axes[1, 0].plot(t_ns, near1, color="tab:blue")
axes[1, 0].set_title(f"Near-end crosstalk on line 1 (from Vs2)  -  Case {case1}")
axes[1, 0].set_xlabel("time [ns]")
axes[1, 0].set_ylabel("V (near)")

axes[1, 1].plot(t_ns, far1, color="tab:red")
axes[1, 1].set_title(f"Far-end crosstalk on line 1 (from Vs2)  -  Case {case1}")
axes[1, 1].set_xlabel("time [ns]")
axes[1, 1].set_ylabel("V (far)")

for ax in axes.flat:
    ax.axhline(0, color="gray", linewidth=0.6)
    ax.grid(True, alpha=0.3)

fig.suptitle("Coupled-line crosstalk (NEXT / FEXT)", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.96])

out_path = "crosstalk_plot.png"
fig.savefig(out_path, dpi=150)
print(f"Saved plot to {out_path}")
print(f"Extracted from matrices -> L1={L1:.3e} H/m, Lm={Lm1:.3e} H/m, "
      f"Cg1={Cg1:.3e} F/m, Cm={Cm1:.3e} F/m")
print(f"Z0 = {Z0:.2f} ohm, Td (one-way delay) = {Td_est*1e9:.3f} ns")
print(f"Launched voltage on line 1 (from Vs1={Vs1} V, Rs1={R_near_1:.2f}): {V1_launched:.4f} V")
print(f"Launched voltage on line 2 (from Vs2={Vs2} V, Rs2={R_near_2:.2f}): {V2_launched:.4f} V")
print(f"Case for line-2 crosstalk (driven by Vs1): {case2}")
print(f"Case for line-1 crosstalk (driven by Vs2): {case1}")

plt.show()