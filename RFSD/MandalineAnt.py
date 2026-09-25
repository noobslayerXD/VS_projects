"""
Meander-line antenna at 1060 MHz -- Hertz-dipole simulation + validation
=========================================================================

Builds the meander line antenna from:
  O.P.N. Calla et al., "Empirical Relation for Designing the Meander
  Line Antenna", Proc. Int. Conf. on Microwave 2008 (eqs 1-16),
and simulates its far field as a superposition of Hertz dipoles
(RF System Design Integration Note, Ch. 1), then checks the
simulated 3 dB E-/H-plane beamwidths and directivity against the
PAPER'S OWN closed-form (patch-antenna-style) formulas (eqs 12-16).

FAR-FIELD SIMPLIFICATION
------------------------
At the chosen observation distance, k0*r >> 1 (deep far field), so
the near-field terms in the exact Hertz-dipole formula are negligible
and we can use the simpler, purely-far-field vector formula for a
dipole with moment p = I*dl*h_hat:

    E_far = (j*eta*k0/(4*pi*r)) * I*dl * exp(-j*k0*r) * [h_hat - (h_hat.r_hat) r_hat]

Projecting onto the OBSERVER's spherical unit vectors theta_hat, phi_hat
(and using r_hat.theta_hat = r_hat.phi_hat = 0) collapses this to simple
dot products -- no near-field correction terms, no per-element angle
bookkeeping:

    E_theta_i = C_i * (h_hat_i . theta_hat)
    E_phi_i   = C_i * (h_hat_i . phi_hat)
    C_i = j*eta*k0*I_i*dl*exp(-j*k0*r_i) / (4*pi*r)

with theta_hat = (cos(t)cos(p), cos(t)sin(p), -sin(t)) and
     phi_hat   = (-sin(p), cos(p), 0)      [global, at the observer]
This matches (and generalizes to arbitrary h_hat_i) the single-dipole
projection formula already used for the x/y-axis dipole check.

E-PLANE / H-PLANE CONVENTION
-----------------------------
The meander's long radiating segments run along x, so x is the
antenna's polarization axis:
    E-plane = x-z plane (phi = 0 / 180 deg)
    H-plane = y-z plane (phi = 90 / 270 deg)
The 3 dB beamwidth in each cut is found around that CUT's own local
peak (not assumed to sit at theta = 0), by walking outward from the
peak to the -3 dB crossings.

HERTZ DIPOLE RESOLUTION
------------------------
`hertz_dipole_resolution` sets how many Hertz-dipole samples are used
per one guided wavelength. Raise it to check the simulation has
converged; lower it for a fast, coarse run while debugging.
"""

import itertools

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (enables 3D projection)

# ---------------- Physical / substrate parameters (paper, Sec. II) ----------------
C0 = 299_792_458.0
f = 1060e6
h_sub = 3.2e-3        # substrate height [m]  (paper: "3.2 mm" -- the abstract's "3.2cm" is a typo)
e_r = 4.4             # substrate relative permittivity

wavelength0 = C0 / f                     # free-space wavelength
k0 = 2 * np.pi / wavelength0             # free-space wavenumber (radiation)

w_ms = C0 / (2 * f) * np.sqrt(2 / (e_r + 1))                      # eq. 11 (patch-width helper, for eps_reff only)
e_r_eff = (e_r + 1) / 2 + (e_r - 1) / 2 * (1 + 10 * h_sub / w_ms) ** (-0.5)   # eq. 6
wavelength_g = wavelength0 / np.sqrt(e_r_eff)                      # eq. 5

# ---------------- Meander-line dimensions, exactly per the paper's eqs 1-4 ----------------
d = 0.16 * wavelength_g   # eq. 1
s = 0.42 * wavelength_g   # eq. 2
L = 0.70 * wavelength_g   # eq. 3 -- used ONLY in the closed-form validation below;
                          # the repeating meander unit itself is fully defined by d, s, w (eqs 1,2,4)
w = 0.05 * wavelength_g   # eq. 4

# ---------------- Hertz dipole resolution (ADJUSTABLE) ----------------
hertz_dipole_resolution = 100   # samples per one guided wavelength


def n_points(length, resolution=hertz_dipole_resolution, wavelength_g=wavelength_g, min_points=2):
    return max(min_points, round(resolution * length / wavelength_g))


def segment(p0, p1, resolution=hertz_dipole_resolution, wavelength_g=wavelength_g):
    x0, y0 = p0
    x1, y1 = p1
    length = np.hypot(x1 - x0, y1 - y0)
    n = n_points(length, resolution, wavelength_g)
    return np.linspace(x0, x1, n), np.linspace(y0, y1, n)


waypoints = [
    (0,     0),
    (s + w, 0),
    (s + w, -d),
    (0,     -d),
    (0,     -2 * d),
    (s + w, -2 * d),
    (s + w, -3 * d),
    (0,     -3 * d),
    (0,     -4 * d),
]

xs, ys = [], []
for p0, p1 in itertools.pairwise(waypoints):
    xseg, yseg = segment(p0, p1)
    xs.append(xseg)
    ys.append(yseg)

x = np.concatenate(xs)
y = np.concatenate(ys)
N = len(x)

dipole_length = wavelength_g / hertz_dipole_resolution
print(f"Hertz dipole resolution: {hertz_dipole_resolution} samples/lambda_g")
print(f"Number of elemental dipoles: {N}")
print(f"dipole_length / wavelength_g = {dipole_length / wavelength_g:.4f}  (must stay << {wavelength_g/50:.4f})")

# ---- orientation h_hat_i: direction from dipole i toward dipole i+1 ----
# (duplicated corner points give a zero-length step -> fall back to the incoming
#  heading; the last dipole has no "next" point and does the same.)
H = np.zeros((N, 3))
for i in range(N):
    if i < N - 1:
        ddx, ddy = x[i + 1] - x[i], y[i + 1] - y[i]
        if np.hypot(ddx, ddy) < 1e-12:
            ddx, ddy = x[i] - x[i - 1], y[i] - y[i - 1]
    else:
        ddx, ddy = x[i] - x[i - 1], y[i] - y[i - 1]
    norm = np.hypot(ddx, ddy)
    H[i] = [ddx / norm, ddy / norm, 0.0]

# ---------------- Standing-wave current, zero at the open (last) end ----------------
sep = 360.0 / hertz_dipole_resolution
phase_from_open_end = (N - 1 - np.arange(N)) * sep
I0 = 1.0
current = I0 * np.sin(np.deg2rad(phase_from_open_end))

# ---------------- Far-field constants ----------------
eta = 120 * np.pi
r = 10.0
print(f"k0*r = {k0 * r:.1f}  (>> 1: far-field approximation is valid)")

# ---------------- theta/phi grid ----------------
n_theta, n_phi = 181, 361
theta = np.linspace(1e-6, np.pi, n_theta)
phi = np.linspace(0, 2 * np.pi, n_phi)
THETA, PHI = np.meshgrid(theta, phi, indexing="ij")

theta_hat_x = np.cos(THETA) * np.cos(PHI)
theta_hat_y = np.cos(THETA) * np.sin(PHI)
theta_hat_z = -np.sin(THETA)
phi_hat_x = -np.sin(PHI)
phi_hat_y = np.cos(PHI)
# phi_hat_z = 0

rx = np.sin(THETA) * np.cos(PHI)     # r_hat, used only for the array-factor path length
ry = np.sin(THETA) * np.sin(PHI)

# ---------------- Sum all N elements (far-field dot-product formula) ----------------
Etheta_total = np.zeros_like(THETA, dtype=complex)
Ephi_total = np.zeros_like(THETA, dtype=complex)

prefac = 1j * eta * k0 * dipole_length / (4 * np.pi * r) * np.exp(-1j * k0 * r)

for i in range(N):
    hx, hy = H[i, 0], H[i, 1]
    h_dot_theta = hx * theta_hat_x + hy * theta_hat_y   # + 0*theta_hat_z, since hz=0
    h_dot_phi = hx * phi_hat_x + hy * phi_hat_y

    path_diff = x[i] * rx + y[i] * ry
    C_i = prefac * current[i] * np.exp(1j * k0 * path_diff)

    Etheta_total += C_i * h_dot_theta
    Ephi_total += C_i * h_dot_phi

E_mag = np.sqrt(np.abs(Etheta_total) ** 2 + np.abs(Ephi_total) ** 2)
U = E_mag ** 2
U_norm = U / U.max()

print(f"Max |E| at r={r} m: {E_mag.max():.4e} V/m")

# ---------------- Directivity (numerical integration) ----------------
_trapz = getattr(np, "trapezoid", None) or np.trapz


def directivity_numeric(U, theta, phi):
    integrand = U * np.sin(theta)[:, None]
    inner = _trapz(integrand, theta, axis=0)
    total = _trapz(inner, phi)
    return 4 * np.pi * U.max() / total


D0_sim = directivity_numeric(U, theta, phi)
print(f"\nSimulated directivity D0 = {D0_sim:.4f}  ({10 * np.log10(D0_sim):.3f} dBi)")

# ---------------- 3 dB E-plane / H-plane beamwidth from the simulated pattern ----------------
def half_power_beamwidth(angles, U_norm_cut):
    """Walk outward from the cut's own peak to the -3 dB (half-power) crossings.
    Returns (angle_lo, angle_hi, hpbw); any of these is None if the cut never
    drops 3 dB below its peak within the swept range (beamwidth > 360 deg,
    i.e. effectively omnidirectional in that cut)."""
    i_peak = int(np.argmax(U_norm_cut))
    n = len(U_norm_cut)

    i = i_peak
    while i > 0 and U_norm_cut[i] >= 0.5:
        i -= 1
    if U_norm_cut[i] < 0.5:
        u0, u1 = U_norm_cut[i], U_norm_cut[i + 1]
        t0, t1 = angles[i], angles[i + 1]
        angle_lo = t0 + (0.5 - u0) * (t1 - t0) / (u1 - u0)
    else:
        angle_lo = None

    j = i_peak
    while j < n - 1 and U_norm_cut[j] >= 0.5:
        j += 1
    if U_norm_cut[j] < 0.5:
        u0, u1 = U_norm_cut[j - 1], U_norm_cut[j]
        t0, t1 = angles[j - 1], angles[j]
        angle_hi = t0 + (0.5 - u0) * (t1 - t0) / (u1 - u0)
    else:
        angle_hi = None

    if angle_lo is None or angle_hi is None:
        return angle_lo, angle_hi, None
    return angle_lo, angle_hi, (angle_hi - angle_lo)


# E-plane: x-z plane, phi = 0 / 180 -> build a full 0..2pi loop over theta
idx_phi0 = 0
idx_phi180 = np.argmin(np.abs(phi - np.pi))
theta_loop = np.concatenate([theta, 2 * np.pi - theta[::-1]])
U_E = np.concatenate([U_norm[:, idx_phi0], U_norm[::-1, idx_phi180]])
thE_lo, thE_hi, hpbw_E = half_power_beamwidth(theta_loop, U_E)

# H-plane: y-z plane, phi = 90 / 270
idx_phi90 = np.argmin(np.abs(phi - np.pi / 2))
idx_phi270 = np.argmin(np.abs(phi - 3 * np.pi / 2))
U_H = np.concatenate([U_norm[:, idx_phi90], U_norm[::-1, idx_phi270]])
thH_lo, thH_hi, hpbw_H = half_power_beamwidth(theta_loop, U_H)

print("\n=== Simulated 3 dB beamwidths ===")
if hpbw_E is not None:
    print(f"E-plane (x-z, phi=0/180): crossings at {np.degrees(thE_lo):.2f} / {np.degrees(thE_hi):.2f} deg "
          f"-> HPBW = {np.degrees(hpbw_E):.2f} deg")
else:
    print("E-plane (x-z, phi=0/180): pattern stays within 3 dB of its peak over the whole cut "
          "-> HPBW undefined (> 360 deg)")

if hpbw_H is not None:
    print(f"H-plane (y-z, phi=90/270): crossings at {np.degrees(thH_lo):.2f} / {np.degrees(thH_hi):.2f} deg "
          f"-> HPBW = {np.degrees(hpbw_H):.2f} deg")
else:
    print("H-plane (y-z, phi=90/270): pattern stays within 3 dB of its peak over the whole cut "
          "-> HPBW undefined (> 360 deg) -- similar to a single dipole's omnidirectional H-plane")

# ---------------- Paper's closed-form validation (eqs 12-16) ----------------
k_o_patch = np.pi / (np.sqrt(e_r_eff) * L)                                     # eq. 14
theta_E_paper = 2 * np.arcsin(np.sqrt(7.03 / ((3 * L**2 + h_sub**2) * k_o_patch**2)))   # eq. 12 [rad]
theta_H_paper = 2 * np.arcsin(np.sqrt(1 / (2 + k_o_patch * w)))                          # eq. 13 [rad]
theta_E_paper_deg = np.degrees(theta_E_paper)
theta_H_paper_deg = np.degrees(theta_H_paper)

D_paper = 41253 / (theta_E_paper_deg * theta_H_paper_deg)     # eq. 15
G_paper = 32400 / (theta_E_paper_deg * theta_H_paper_deg)     # eq. 16

print("\n=== Paper's closed-form (patch-style) estimate, eqs 12-16 ===")
print(f"theta_E (paper) = {theta_E_paper_deg:.2f} deg")
print(f"theta_H (paper) = {theta_H_paper_deg:.2f} deg")
print(f"D0 (paper)      = {D_paper:.4f}  ({10 * np.log10(D_paper):.3f} dBi)")
print(f"Gain (paper)    = {G_paper:.4f}  ({10 * np.log10(G_paper):.3f} dB)")

def fmt_deg(v):
    return f"{np.degrees(v):>10.2f} deg" if v is not None else f"{'undefined':>10s}    "


print("\n=== Simulation vs. paper ===")
print(f"{'':18s}{'Simulated':>15s}{'Paper':>15s}")
print(f"{'E-plane HPBW':18s}{fmt_deg(hpbw_E)}{theta_E_paper_deg:>10.2f} deg")
print(f"{'H-plane HPBW':18s}{fmt_deg(hpbw_H)}{theta_H_paper_deg:>10.2f} deg")
print(f"{'Directivity D0':18s}{D0_sim:>15.3f}{D_paper:>15.3f}")
print(f"{'Directivity dBi':18s}{10*np.log10(D0_sim):>11.2f} dB{10*np.log10(D_paper):>11.2f} dB")

# ---------------- Plots ----------------
R = U_norm
X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)

fig = plt.figure(figsize=(16, 5.5))

ax1 = fig.add_subplot(1, 3, 1, projection="3d")
colors = plt.cm.viridis(R / R.max())
ax1.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1,
                  linewidth=0, antialiased=True, shade=False)
ax1.set_title(f"3D |E| pattern (normalized)\n({N} elements, f={f/1e6:.0f} MHz, r={r:.0f} m)")
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("z")
ax1.set_box_aspect([1, 1, 1])

ax2 = fig.add_subplot(1, 3, 2, projection="polar")
ax2.plot(theta_loop, U_E, linewidth=1.5, label="simulated")
ax2.plot(theta_loop, 0.5 * np.ones_like(theta_loop), "r--", linewidth=1, label="-3 dB")
ax2.plot([thE_lo, thE_hi], [0.5, 0.5], "ro")
ax2.set_theta_zero_location("N")
ax2.set_title(f"E-plane (x-z) cut\nHPBW={np.degrees(hpbw_E):.1f} deg (paper: {theta_E_paper_deg:.1f} deg)", pad=20)
ax2.legend(loc="lower right", bbox_to_anchor=(1.3, -0.05), fontsize=8)

ax3 = fig.add_subplot(1, 3, 3, projection="polar")
ax3.plot(theta_loop, U_H, linewidth=1.5, label="simulated")
ax3.plot(theta_loop, 0.5 * np.ones_like(theta_loop), "r--", linewidth=1, label="-3 dB")
h_title = f"HPBW={np.degrees(hpbw_H):.1f} deg" if hpbw_H is not None else "HPBW undefined (>360 deg)"
if hpbw_H is not None:
    ax3.plot([thH_lo, thH_hi], [0.5, 0.5], "ro")
ax3.set_theta_zero_location("N")
ax3.set_title(f"H-plane (y-z) cut\n{h_title} (paper: {theta_H_paper_deg:.1f} deg)", pad=20)
ax3.legend(loc="lower right", bbox_to_anchor=(1.3, -0.05), fontsize=8)

plt.tight_layout()
plt.savefig("meander_validation.png", dpi=150, bbox_inches="tight")
plt.show()