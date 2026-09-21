import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# Physical / substrate parameters
# ============================================================================

C0 = 299792458.0          # speed of light in vacuum [m/s]
f = 1060e6               # design frequency [Hz]

h = 3.2e-3               # substrate height [m]
e_r = 4.4                # substrate relative permittivity

wavelength = C0 / f

# Width used in the effective-permittivity calculation
microstrip_w = C0 / (2 * f) * np.sqrt(2 / (e_r + 1))

e_r_eff = (
    (e_r + 1) / 2
    + (e_r - 1) / 2 * (1 + 10 * h / microstrip_w) ** (-0.5)
)

wavelength_g = wavelength / np.sqrt(e_r_eff)

# Free-space and guided wavenumbers
k0 = 2 * np.pi / wavelength
kg = 2 * np.pi / wavelength_g


# ============================================================================
# Meander-line geometry
# ============================================================================

d = 0.16 * wavelength_g
s = 0.42 * wavelength_g
L = 0.07 * wavelength_g
trace_w = 0.05 * wavelength_g

waypoints = np.array([
    (0, 0),
    (s + trace_w, 0),
    (s + trace_w, -d),
    (0, -d),
    (0, -2 * d),
    (s + trace_w, -2 * d),
    (s + trace_w, -3 * d),
    (0, -3 * d),
    (0, -4 * d),
], dtype=float)


# ============================================================================
# Resolution
# ============================================================================

# Number of small elements per guided wavelength
resolution = 100


def n_elements(length, resolution=resolution, wavelength_g=wavelength_g):
    """
    Number of short Hertzian dipole elements used to represent
    a straight section.
    """
    return max(1, int(round(resolution * length / wavelength_g)))


# ============================================================================
# Discretize the meander into short Hertzian-dipole elements
# ============================================================================

dipole_positions = []
dipole_directions = []
dipole_lengths = []

for p0, p1 in zip(waypoints[:-1], waypoints[1:]):

    # Length of this straight section
    section_length = np.linalg.norm(p1 - p0)

    # Number of small dipole elements
    N = n_elements(section_length)

    # Points along this section
    t = np.linspace(0.0, 1.0, N + 1)

    points = (
        p0[None, :]
        + t[:, None] * (p1 - p0)[None, :]
    )

    # Each short segment is represented by one Hertzian dipole
    p_start = points[:-1]
    p_end = points[1:]

    # Dipole centre positions
    centres = 0.5 * (p_start + p_end)

    # Dipole lengths
    dl = np.linalg.norm(p_end - p_start, axis=1)

    # Unit vectors along the meander
    tangent = (p_end - p_start) / dl[:, None]

    dipole_positions.append(centres)
    dipole_directions.append(tangent)
    dipole_lengths.append(dl)


# Combine all straight sections
r2 = np.vstack(dipole_positions)       # [Ndip, 2]
t2 = np.vstack(dipole_directions)      # [Ndip, 2]
dl = np.concatenate(dipole_lengths)     # [Ndip]

N_dipoles = len(dl)

# Put the dipoles into 3D
r = np.column_stack((
    r2[:, 0],
    r2[:, 1],
    np.zeros(N_dipoles)
))

t_hat = np.column_stack((
    t2[:, 0],
    t2[:, 1],
    np.zeros(N_dipoles)
))


# ============================================================================
# Distance along the meander
# ============================================================================

# The centre of each short element occurs half-way through that element.
distance_from_feed = np.cumsum(dl) - 0.5 * dl

L_total = np.sum(dl)

# Distance from each dipole to the LAST end of the meander
distance_from_end = L_total - distance_from_feed


# ============================================================================
# Sinusoidal current distribution
# ============================================================================

I_peak = 1.0   # A
I = I_peak * np.sin(kg * distance_from_end)

# I is real-valued here:
#   I = 0 at the final end
#   current changes sign according to the standing-wave sinusoid
#
# This sign change is important because it produces a 180-degree
# phase reversal and must be preserved when summing the radiation fields.


# ============================================================================
# Optional: plot current distribution
# ============================================================================

plt.figure(figsize=(8, 4))

plt.plot(
    distance_from_feed / wavelength_g,
    I,
    marker='.',
    markersize=2
)

plt.xlabel(r'Distance along meander, $s/\lambda_g$')
plt.ylabel('Current [A]')
plt.title('Sinusoidal current distribution')
plt.grid(True)

plt.tight_layout()
plt.show()


# ============================================================================
# Radiation pattern calculation
# ============================================================================

def calculate_radiation_pattern(theta, phi, chunk_size=2000):
    """
    Calculate the coherent far-field radiation pattern.

    theta : polar angle measured from +z
    phi   : azimuth angle measured from +x

    Returns
    -------
    P : normalized radiation power pattern
    E : complex electric-field vector
    """

    # Observation unit vectors
    n_hat = np.stack([
        np.sin(theta) * np.cos(phi),
        np.sin(theta) * np.sin(phi),
        np.cos(theta)
    ], axis=-1)

    original_shape = theta.shape

    # Flatten observation directions
    n_hat = n_hat.reshape(-1, 3)

    E_total = np.zeros((len(n_hat), 3), dtype=complex)

    # Current moment for each short Hertzian dipole
    #
    # Current element = I * dl
    current_element = I * dl

    # ------------------------------------------------------------------------
    # Do the calculation in chunks so the RAM requirement remains reasonable
    # ------------------------------------------------------------------------

    for start in range(0, len(n_hat), chunk_size):

        stop = min(start + chunk_size, len(n_hat))

        n = n_hat[start:stop]

        # ------------------------------------------------------------
        # Phase caused by physical position of each dipole
        #
        # exp(j*k0*n.r)
        #
        # k0 = free-space wavenumber
        # ------------------------------------------------------------
        phase = np.exp(
            1j * k0 * (n @ r.T)
        )

        # ------------------------------------------------------------
        # Projection of each dipole onto the plane transverse
        # to the observation direction.
        #
        # t_perpendicular =
        #     t - n(n.t)
        #
        # This gives the electric-field polarization of each
        # Hertzian dipole in the far field.
        # ------------------------------------------------------------

        n_dot_t = n @ t_hat.T

        transverse = (
            t_hat[None, :, :]
            - n_dot_t[:, :, None] * n[:, None, :]
        )

        # ------------------------------------------------------------
        # Coherent vector summation
        # ------------------------------------------------------------

        E_total[start:stop] = np.sum(
            current_element[None, :, None]
            * transverse
            * phase[:, :, None],
            axis=1
        )

    # Restore angular grid
    E_total = E_total.reshape(original_shape + (3,))

    # Radiation intensity is proportional to |E|^2
    P = np.sum(np.abs(E_total) ** 2, axis=-1)

    # Normalize
    P = P / np.max(P)

    return P, E_total


# ============================================================================
# Angular grid
# ============================================================================

# Increase these values if you want a smoother pattern.
Ntheta = 91
Nphi = 181

theta = np.linspace(0, np.pi, Ntheta)
phi = np.linspace(0, 2 * np.pi, Nphi)

THETA, PHI = np.meshgrid(theta, phi, indexing='ij')


# ============================================================================
# Calculate total radiation pattern
# ============================================================================

P_norm, E = calculate_radiation_pattern(THETA, PHI)


# ============================================================================
# Convert to dB
# ============================================================================

P_dB = 10 * np.log10(np.maximum(P_norm, 1e-12))

# Limit plot range for visibility
P_dB_plot = np.maximum(P_dB, -30)


# ============================================================================
# 3D radiation pattern
# ============================================================================

# Use normalized field magnitude as radius.
# Since P ~ |E|^2:
R = np.sqrt(P_norm)

X = R * np.sin(THETA) * np.cos(PHI)
Y = R * np.sin(THETA) * np.sin(PHI)
Z = R * np.cos(THETA)


fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection='3d')

surface = ax.plot_surface(
    X, Y, Z,
    cmap='viridis',
    linewidth=0,
    antialiased=True
)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title(
    f'Meander antenna radiation pattern\n'
    f'{N_dipoles} Hertzian dipoles, '
    f'{resolution} elements/$\\lambda_g$'
)

# Equal aspect ratio
ax.set_box_aspect((1, 1, 1))

plt.tight_layout()

plt.savefig(
    'meander_radiation_pattern.png',
    dpi=200,
    bbox_inches='tight'
)

plt.show()


# ============================================================================
# Some useful numerical information
# ============================================================================

print(f"Free-space wavelength      = {wavelength:.6f} m")
print(f"Effective permittivity     = {e_r_eff:.4f}")
print(f"Guided wavelength          = {wavelength_g:.6f} m")
print(f"Total meander length       = {L_total:.6f} m")
print(f"Total meander length/lambda_g = "
      f"{L_total / wavelength_g:.4f}")
print(f"Number of Hertzian dipoles = {N_dipoles}")