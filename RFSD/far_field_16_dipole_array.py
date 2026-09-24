import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 16-element infinitesimal dipole array
# ============================================================
# Assumptions:
#   - Free space
#   - All dipoles are z-directed
#   - Identical infinitesimal dipole lengths l
#   - Supplied currents are real current amplitudes
#   - exp(+j*omega*t) convention
#
# Far-zone field:
#
# E_theta(r,theta) =
#     j*eta0*k*l*exp(-j*k*r)/(4*pi*r)
#       * sin(theta)
#       * sum_n I_n exp(j*k*z_n*cos(theta))
#
# The supplied data do not include frequency, dipole length, or
# observation distance, so the script calculates the normalized
# angular field exactly and also provides a function for the
# absolute field when those quantities are supplied.

# -----------------------------
# Input data
# -----------------------------
z = np.array([
    -0.066628, -0.06810863, -0.06958925, -0.07106987,
    -0.07255049, -0.07403112, -0.07551174, -0.07699236, -0.07847298,
    -0.07995361, -0.08143423, -0.08291485, -0.08439547, -0.08587610,
    -0.08735672, -0.08883734
], dtype=float)

I = np.array([
    8.09016994e-01,
    7.70513243e-01,
    7.28968627e-01,
    6.84547106e-01,
    6.37423990e-01,
    5.87785252e-01,
    5.35826795e-01,
    4.81753674e-01,
    4.25779292e-01,
    3.68124553e-01,
    3.09016994e-01,
    2.48689887e-01,
    1.87381315e-01,
    1.25333234e-01,
    6.27905195e-02,
    0.00000000e+00
], dtype=float)


# -----------------------------
# Constants
# -----------------------------
c0 = 299_792_458.0
eta0 = np.pi*120

# -----------------------------
# Operating frequency
# -----------------------------
# CHANGE THIS to your actual frequency.
f = 1060e6  # Hz

lam = c0 / f
k = 2*np.pi / lam

# -----------------------------
# Angular coordinates
# -----------------------------
theta_deg = np.linspace(0.0, 180.0, 3601)
theta = np.deg2rad(theta_deg)

# -----------------------------
# Array factor
# -----------------------------
#
# AF(theta) = sum I_n exp(j*k*z_n*cos(theta))
#
phase = np.exp(
    1j * k
    * z[:, None]
    * np.cos(theta)[None, :]
)

AF = np.sum(I[:, None] * phase, axis=0)

# -----------------------------
# Hertzian dipole element factor
# -----------------------------
#
# z-directed infinitesimal dipole:
# element factor = sin(theta)
#
element_factor = np.sin(theta)

# -----------------------------
# Total far-field angular factor
# -----------------------------
#
# E_theta proportional to:
# sin(theta) * AF(theta)
#
E_theta_angular = element_factor * AF

# Normalize field to maximum
E_norm = E_theta_angular / np.max(np.abs(E_theta_angular))

# Magnitude
E_mag = np.abs(E_norm)

# dB field magnitude
E_db = 20*np.log10(np.maximum(E_mag, 1e-12))

# Power-pattern form, also normalized
P_norm = E_mag**2
P_db = 10*np.log10(np.maximum(P_norm, 1e-12))

# Array-factor-only pattern
AF_norm = np.abs(AF) / np.max(np.abs(AF))
AF_db = 20*np.log10(np.maximum(AF_norm, 1e-12))

# -----------------------------
# Basic geometry information
# -----------------------------
dz = np.diff(z)
d = np.mean(np.abs(dz))

print("="*60)
print("16-element dipole array")
print("="*60)
print(f"Number of dipoles          : {len(z)}")
print(f"Frequency                  : {f/1e9:.6f} GHz")
print(f"Wavelength                 : {lam*1e3:.9f} mm")
print(f"Mean element spacing      : {d*1e3:.9f} mm")
print(f"Spacing / wavelength      : {d/lam:.9f}")
print(f"Array length               : {(np.max(z)-np.min(z))*1e3:.9f} mm")
print()

print("Shifted z positions [m]:")
print(z)
print()

print("Currents:")
print(I)
print()

# Maximum
imax = np.argmax(E_mag)
print(f"Maximum |E_theta|          : {E_mag[imax]:.6f}")
print(f"Maximum angle theta        : {theta_deg[imax]:.6f} deg")
print()

# Sample values
sample_deg = np.array([0, 30, 60, 90, 120, 150, 180], dtype=float)
sample_theta = np.deg2rad(sample_deg)

sample_phase = np.exp(
    1j * k
    * z[:, None]
    * np.cos(sample_theta)[None, :]
)
sample_AF = np.sum(I[:, None] * sample_phase, axis=0)
sample_E = (
    np.sin(sample_theta) * sample_AF
    / np.max(np.abs(E_theta_angular))
)

print("Normalized complex E_theta:")
for ang, val in zip(sample_deg, sample_E):
    print(
        f"theta = {ang:6.1f} deg : "
        f"{val.real:+.9f} {val.imag:+.9f}j"
    )

# -----------------------------
# Plot 1: total far-field
# -----------------------------
plt.figure(figsize=(9, 5.5))
plt.plot(theta_deg, E_db)
plt.xlabel(r"$\theta$ [deg]")
plt.ylabel(r"$|E_\theta|$ [dB, normalized]")
plt.title(
    f"16-element z-directed Hertzian dipole array "
    f"({f/1e9:g} GHz)"
)
plt.xlim(0, 180)
plt.ylim(-60, 0.5)
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# Plot 2: power pattern
# -----------------------------
plt.figure(figsize=(9, 5.5))
plt.plot(theta_deg, P_db)
plt.xlabel(r"$\theta$ [deg]")
plt.ylabel(r"$|E_\theta|^2$ [dB, normalized]")
plt.title("Normalized far-field power pattern")
plt.xlim(0, 180)
plt.ylim(-60, 0.5)
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# Plot 3: array factor vs element factor
# -----------------------------
EF_norm = np.abs(element_factor)
EF_db = 20*np.log10(np.maximum(EF_norm, 1e-12))

plt.figure(figsize=(9, 5.5))
plt.plot(theta_deg, AF_db, label="Array factor")
plt.plot(theta_deg, EF_db, label="Hertzian dipole element factor")
plt.xlabel(r"$\theta$ [deg]")
plt.ylabel("Magnitude [dB, normalized]")
plt.title("Array factor and dipole element factor")
plt.xlim(0, 180)
plt.ylim(-60, 0.5)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# Polar plot
# -----------------------------
plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection="polar")
ax.plot(theta, E_mag)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title("Normalized far-field magnitude", pad=20)
plt.tight_layout()
plt.show()

# -----------------------------
# 3D far-field radiation pattern
# -----------------------------
# The z-directed array has no phi dependence, so revolve the
# normalized theta pattern around the z-axis.
n_phi_3d = 181
phi_3d = np.linspace(0.0, 2.0 * np.pi, n_phi_3d)
THETA_3D, PHI_3D = np.meshgrid(theta, phi_3d, indexing="ij")
R_3D = E_mag[:, None]

X_3D = R_3D * np.sin(THETA_3D) * np.cos(PHI_3D)
Y_3D = R_3D * np.sin(THETA_3D) * np.sin(PHI_3D)
Z_3D = R_3D * np.cos(THETA_3D)

# Color the surface by the same normalized field level shown in dB.
E_db_3d = np.broadcast_to(E_db[:, None], THETA_3D.shape)
E_db_3d_plot = np.maximum(E_db_3d, -60.0)

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(
    X_3D,
    Y_3D,
    Z_3D,
    facecolors=plt.cm.viridis((E_db_3d_plot + 60.0) / 60.0),
    rstride=8,
    cstride=4,
    linewidth=0,
    antialiased=True,
)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title(
    f"3D normalized far-field radiation pattern\n"
    f"({f/1060e6:g} MHz, z-directed array)"
)
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=25.0, azim=35.0)
plt.tight_layout()
plt.show()

# ============================================================
# Absolute far-field function
# ============================================================
def absolute_Etheta(
    theta,
    frequency_hz,
    r_m,
    dipole_length_m,
    current_scale=1.0
):
    """
    Complex far-zone E_theta [V/m] for identical Hertzian dipoles.

    Parameters
    ----------
    theta : array_like
        Observation angle in radians.
    frequency_hz : float
        Operating frequency [Hz].
    r_m : float
        Observation distance [m].
    dipole_length_m : float
        Infinitesimal dipole length l [m].
    current_scale : float
        Optional multiplier for the listed current amplitudes.

    Returns
    -------
    E_theta : ndarray
        Complex electric-field component in V/m.
    """
    theta = np.asarray(theta, dtype=float)
    k_local = 2*np.pi*frequency_hz/c0

    AF_local = np.sum(
        (current_scale * I)[:, None]
        * np.exp(
            1j * k_local
            * z[:, None]
            * np.cos(theta)[None, :]
        ),
        axis=0
    )

    E_theta = (
        1j * eta0 * k_local * dipole_length_m
        * np.exp(-1j * k_local * r_m)
        / (4*np.pi*r_m)
        * np.sin(theta)
        * AF_local
    )

    return E_theta


# Example absolute-field calculation:
# Uncomment and set your physical dipole length and observation range.
#
# r_obs = 1.0            # m
# dipole_length = 1e-5   # m
# E_abs = absolute_Etheta(
#     theta,
#     frequency_hz=f,
#     r_m=r_obs,
#     dipole_length_m=dipole_length
# )
# print("Peak |E_theta| =", np.max(np.abs(E_abs)), "V/m")
