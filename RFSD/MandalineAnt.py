"""
Meander-line antenna (Calla et al., "Empirical Relation for Designing the
Meander Line Antenna", ICM-2008) -- Hertz-dipole superposition model.
=============================================================================

Simulates the radiation pattern of the meander line antenna by treating the
printed trace as a chain of infinitesimal (Hertz) dipoles, each carrying a
standing-wave current, and summing their far fields. Extracts the 3 dB
E-plane / H-plane beamwidths and directivity from the simulated pattern,
and independently computes the same quantities from the paper's own
closed-form formulas (eqs. 12-16) for validation.

GEOMETRY (Calla et al., eqs. 1-6, 11), at f = 1060 MHz, FR4 (er=4.4,
h=3.2 mm):
    d = 0.16*lambda_g      (eq 1)
    s = 0.42*lambda_g      (eq 2)
    L = 0.70*lambda_g      (eq 3)  -- NOTE: an earlier version of this script
                                      had L = 0.07*lambda_g (decimal typo).
                                      L isn't used to build the trace itself
                                      (only d, s, w are), but IS used below
                                      in the paper's own eqs. 12-14.
    w = 0.05*lambda_g      (eq 4)
    lambda_g = lambda0 / sqrt(er_eff)                          (eq 5)
    er_eff = (er+1)/2 + (er-1)/2 * (1+10*h/w_ms)^-0.5           (eq 6)
    w_ms = c/(2*fr) * sqrt(2/(er+1))    (eq 11, initial microstrip width
                                          estimate used only to get er_eff)

FIELD MODEL: each of the N sample points along the trace is a Hertz dipole
oriented along the local trace direction (always +-x or +-y for this
right-angled meander). In the far field, the radiated E-field of a Hertz
dipole with moment I*dl*h_hat is (dropping the negligible near-field terms,
valid since k0*r >> 1 here):
    E_theta = (j*eta*k0*I*dl / (4*pi*r)) * (h_hat . theta_hat) * exp(-j*k0*r)
    E_phi   = (j*eta*k0*I*dl / (4*pi*r)) * (h_hat . phi_hat)   * exp(-j*k0*r)
with, for h_hat = x_hat:  x.theta_hat = cos(theta)cos(phi), x.phi_hat = -sin(phi)
 and  for h_hat = y_hat:  y.theta_hat = cos(theta)sin(phi), y.phi_hat =  cos(phi)
Summing over all N elements (each with its own position -> extra path-length
phase, and its own standing-wave current) gives the total E_theta, E_phi.

VALIDATION: Calla et al. eqs. 12-16 estimate the E-/H-plane half-power
beamwidths and directivity directly from L, w, h and er_eff (treating the
meander as an equivalent microstrip-patch radiator):
    k0p    = pi / (sqrt(er_eff) * L)                                  (14)
    theta_E = 2*asin( sqrt(7.03 / ((3*L^2 + h^2) * k0p^2)) )          (12)
    theta_H = 2*asin( sqrt(1 / (2 + k0p*w)) )                         (13)
    D0     = 41253 / (theta_E[deg] * theta_H[deg])                    (15)
    Gain   = 32400 / (theta_E[deg] * theta_H[deg])                    (16)
(k0p here is the paper's own symbol, distinct from the true free-space k0
used in the field simulation above.)
"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# =============================================================================
# 1. Substrate / frequency
# =============================================================================
C0 = 299_792_458.0
f = 1060e6
h_sub = 3.2e-3     # FR4 thickness [m] (the paper's abstract says "3.2cm", which
                    # is almost certainly a typo for 3.2 mm -- a completely
                    # standard FR4 thickness, and consistent with the rest of
                    # the paper's own numbers)
e_r = 4.4

wavelength0 = C0 / f
k0 = 2 * np.pi / wavelength0                      # TRUE free-space wavenumber (radiation)

w_ms = C0 / (2 * f) * np.sqrt(2 / (e_r + 1))       # eq 11
e_r_eff = (e_r + 1) / 2 + (e_r - 1) / 2 * (1 + 10 * h_sub / w_ms) ** (-0.5)  # eq 6
wavelength_g = wavelength0 / np.sqrt(e_r_eff)      # eq 5

# =============================================================================
# 2. Meander-line geometry (Calla et al. eqs. 1-4)
# =============================================================================
d = 0.16 * wavelength_g    # eq 1
s = 0.42 * wavelength_g    # eq 2
L = 0.70 * wavelength_g    # eq 3  (corrected: was 0.07 -- see docstring)
w = 0.05 * wavelength_g    # eq 4

print("=== Geometry ===")
print(f"wavelength0 = {wavelength0*100:.3f} cm   wavelength_g = {wavelength_g*100:.3f} cm   er_eff = {e_r_eff:.3f}")
print(f"d = {d*1000:.3f} mm   s = {s*1000:.3f} mm   L = {L*1000:.3f} mm   w = {w*1000:.3f} mm")

# =============================================================================
# 3. Hertz-dipole discretisation ("Hertz dipole resolution")
# =============================================================================
resolution = 100   # sample points per one guided wavelength. Lower this for a
                    # fast/coarse debug run; raise it to check convergence of
                    # the extracted beamwidths/directivity.


def n_points(length, resolution=resolution, wavelength_g=wavelength_g, min_points=2):
    return max(min_points, round(resolution * length / wavelength_g))


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

element_centres = []
element_directions = []
element_lengths = []
for p0, p1 in itertools.pairwise(waypoints):
    start = np.asarray(p0, dtype=float)
    end = np.asarray(p1, dtype=float)
    section_vector = end - start
    section_length = np.linalg.norm(section_vector)
    n = n_points(section_length)

    edges = np.linspace(0.0, 1.0, n + 1)
    element_centres.append(
        start + (edges[:-1] + 0.5 * np.diff(edges))[:, None] * section_vector
    )
    element_directions.append(
        np.tile(section_vector / section_length, (n, 1))
    )
    element_lengths.append(np.full(n, section_length / n))

positions = np.vstack(element_centres)
H = np.vstack(element_directions)
dl = np.concatenate(element_lengths)
x, y = positions[:, 0], positions[:, 1]
N = len(dl)
print(f"\nNumber of elemental (Hertz) dipoles: {N}  (resolution = {resolution} pts/lambda_g)")

# =============================================================================
# 4. Standing-wave current, zero at the open (last) end
# =============================================================================
I0 = 1.0
guided_wavenumber = 2 * np.pi / wavelength_g
distance_from_feed = np.cumsum(dl) - 0.5 * dl
distance_from_open_end = distance_from_feed[-1] + 0.5 * dl[-1] - distance_from_feed
current = I0 * np.sin(guided_wavenumber * distance_from_open_end)

# =============================================================================
# 5. Far field: closed-form (h_hat . theta_hat), (h_hat . phi_hat) projections
# =============================================================================
eta = 120 * np.pi
r = 10.0

n_theta, n_phi = 181, 361      # 1 deg steps -- fine enough for beamwidth extraction
theta = np.linspace(1e-6, np.pi, n_theta)
phi = np.linspace(0, 2 * np.pi, n_phi)
THETA, PHI = np.meshgrid(theta, phi, indexing="ij")

cos_t, sin_t = np.cos(THETA), np.sin(THETA)
cos_p, sin_p = np.cos(PHI), np.sin(PHI)

x_dot_theta, x_dot_phi = cos_t * cos_p, -sin_p
y_dot_theta, y_dot_phi = cos_t * sin_p, cos_p

rx, ry = sin_t * cos_p, sin_t * sin_p     # for the array-factor path-length phase

prefactor = 1j * eta * k0 * np.exp(-1j * k0 * r) / (4 * np.pi * r)

E_theta_total = np.zeros_like(THETA, dtype=complex)
E_phi_total = np.zeros_like(THETA, dtype=complex)

for i in range(N):
    hx, hy = H[i]
    path_diff = x[i] * rx + y[i] * ry
    phase_i = np.exp(1j * k0 * path_diff)
    dot_theta = hx * x_dot_theta + hy * y_dot_theta
    dot_phi = hx * x_dot_phi + hy * y_dot_phi
    E_theta_total += current[i] * dl[i] * phase_i * dot_theta
    E_phi_total += current[i] * dl[i] * phase_i * dot_phi

E_theta_total *= prefactor
E_phi_total *= prefactor

E_mag = np.sqrt(np.abs(E_theta_total) ** 2 + np.abs(E_phi_total) ** 2)
E_norm = E_mag / E_mag.max()
U_norm = E_norm ** 2   # normalized power pattern

print(f"\nMax |E| at r={r} m: {E_mag.max():.4e} V/m")

# =============================================================================
# 6. Directivity (numerical integration of the simulated pattern)
# =============================================================================
def directivity_numeric(U, theta, phi):
    integrand = U * np.sin(theta)[:, None]
    inner = np.trapezoid(integrand, theta, axis=0)
    total = np.trapezoid(inner, phi)
    return 4 * np.pi * U.max() / total


D0_sim = directivity_numeric(U_norm, theta, phi)

# =============================================================================
# 7. 3 dB E-plane / H-plane beamwidths from the SIMULATED pattern
# =============================================================================
def half_power_beamwidth_deg(angle_deg, power_norm):
    """power_norm: normalized POWER pattern (peak = 1) vs angle_deg (0..360)."""
    i_peak = np.argmax(power_norm)
    target = 0.5
    i = i_peak
    while i > 0 and power_norm[i] >= target:
        i -= 1
    ang_lo = angle_deg[i] if i == i_peak else np.interp(
        target, [power_norm[i], power_norm[i + 1]], [angle_deg[i], angle_deg[i + 1]])
    i = i_peak
    nmax = len(power_norm)
    while i < nmax - 1 and power_norm[i] >= target:
        i += 1
    ang_hi = angle_deg[i] if i == i_peak else np.interp(
        target, [power_norm[i], power_norm[i - 1]], [angle_deg[i], angle_deg[i - 1]])
    return ang_hi - ang_lo, ang_lo, ang_hi


def principal_plane_cut(phi_value):
    """Full 0-360 deg power pattern around broadside through phi_value/phi_value+180."""
    idx_a = np.argmin(np.abs(phi - phi_value))
    idx_b = np.argmin(np.abs(phi - (phi_value + np.pi) % (2 * np.pi)))
    ang = np.concatenate([np.degrees(theta), 360 - np.degrees(theta[::-1])])
    pwr = np.concatenate([U_norm[:, idx_a], U_norm[::-1, idx_b]])
    return ang, pwr


# E-plane: phi = 0/180 (contains the meander's long "x" axis -> the "L" direction)
ang_E, pwr_E = principal_plane_cut(0.0)
hpbw_E, E_lo, E_hi = half_power_beamwidth_deg(ang_E, pwr_E)

# H-plane: phi = 90/270 (contains "y" -> the "w" direction)
ang_H, pwr_H = principal_plane_cut(np.pi / 2)
hpbw_H, H_lo, H_hi = half_power_beamwidth_deg(ang_H, pwr_H)

# =============================================================================
# 8. Paper's closed-form validation formulas (Calla et al., eqs. 12-16)
# =============================================================================
k0p = np.pi / (np.sqrt(e_r_eff) * L)                                                            # eq 14
theta_E_paper = 2 * np.degrees(np.arcsin(np.sqrt(7.03 / ((3 * L**2 + h_sub**2) * k0p**2))))     # eq 12
theta_H_paper = 2 * np.degrees(np.arcsin(np.sqrt(1 / (2 + k0p * w))))                           # eq 13
D0_paper = 41253 / (theta_E_paper * theta_H_paper)                                              # eq 15
G_paper = 32400 / (theta_E_paper * theta_H_paper)                                               # eq 16

# =============================================================================
# 9. Results / validation table
# =============================================================================
print("\n=== Simulated (Hertz-dipole superposition, this script) ===")
print(f"E-plane 3 dB beamwidth: {hpbw_E:.2f} deg   ({E_lo:.1f} to {E_hi:.1f} deg)")
print(f"H-plane 3 dB beamwidth: {hpbw_H:.2f} deg   ({H_lo:.1f} to {H_hi:.1f} deg)")
print(f"Directivity D0:         {D0_sim:.4f}  ({10*np.log10(D0_sim):.3f} dBi)")

print("\n=== Calla et al. (2008) closed-form formulas, eqs. 12-16 ===")
print(f"theta_E: {theta_E_paper:.2f} deg")
print(f"theta_H: {theta_H_paper:.2f} deg")
print(f"Directivity D0: {D0_paper:.4f}  ({10*np.log10(D0_paper):.3f} dBi)")
print(f"Gain (incl. paper's assumed efficiency): {G_paper:.4f}  ({10*np.log10(G_paper):.3f} dBi)")
print("(Compare the simulated D0 to the paper's Directivity, not Gain -- Gain")
print(" already bakes in an assumed loss/efficiency factor this lossless")
print(" Hertz-dipole simulation doesn't model.)")

# =============================================================================
# 10. Plots
# =============================================================================
R = E_norm
X, Y, Z = R * rx, R * sin_t * sin_p, R * cos_t

fig = plt.figure(figsize=(16, 5.5))

ax1 = fig.add_subplot(1, 3, 1, projection="3d")
colors = plt.cm.viridis(R / R.max())
ax1.plot_surface(X, Y, Z, facecolors=colors, rstride=1, cstride=1,
                  linewidth=0, antialiased=True, shade=False)
ax1.set_title(f"3D |E| pattern\n({N} elements, f={f/1e6:.0f} MHz, r={r:.0f} m)")
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("z")
ax1.set_box_aspect([1, 1, 1])

ax2 = fig.add_subplot(1, 3, 2, projection="polar")
ax2.plot(np.deg2rad(ang_E), pwr_E, linewidth=1.5)
ax2.plot(np.deg2rad(ang_E), 0.5 * np.ones_like(ang_E), "r--", linewidth=1, label="-3 dB")
ax2.plot(np.deg2rad([E_lo, E_hi]), [0.5, 0.5], "ro", zorder=5)
ax2.set_theta_zero_location("N")
ax2.set_title(f"E-plane (phi=0/180)\nHPBW = {hpbw_E:.1f} deg", pad=20)
ax2.legend(loc="lower right", bbox_to_anchor=(1.3, -0.05), fontsize=8)

ax3 = fig.add_subplot(1, 3, 3, projection="polar")
ax3.plot(np.deg2rad(ang_H), pwr_H, linewidth=1.5)
ax3.plot(np.deg2rad(ang_H), 0.5 * np.ones_like(ang_H), "r--", linewidth=1, label="-3 dB")
ax3.plot(np.deg2rad([H_lo, H_hi]), [0.5, 0.5], "ro", zorder=5)
ax3.set_theta_zero_location("N")
ax3.set_title(f"H-plane (phi=90/270)\nHPBW = {hpbw_H:.1f} deg", pad=20)
ax3.legend(loc="lower right", bbox_to_anchor=(1.3, -0.05), fontsize=8)

plt.tight_layout()
plt.savefig("meander_antenna_validation.png", dpi=150, bbox_inches="tight")
plt.show()
