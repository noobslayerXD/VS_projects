import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (enables 3D projection)

# ---------------- Physical / substrate parameters ----------------
C0 = 299_792_458.0
f = 1060e6
h_sub = 3.2e-3        # substrate height [m]
e_r = 4.4             # substrate relative permittivity

wavelength0 = C0 / f                     # FREE-SPACE wavelength
k0 = 2 * np.pi / wavelength0             # FREE-SPACE wavenumber (used for radiation)

w_ms = C0 / (2 * f) * np.sqrt(2 / (e_r + 1))
e_r_eff = (e_r + 1) / 2 + (e_r - 1) / 2 * (1 + 10 * h_sub / w_ms) ** (-0.5)
wavelength_g = wavelength0 / np.sqrt(e_r_eff)     # GUIDED wavelength (trace sizing only)

# ---------------- Meander-line geometry (units of wavelength_g) ----------------
d = 0.16 * wavelength_g
s = 0.42 * wavelength_g
L = 0.07 * wavelength_g
w = 0.05 * wavelength_g

resolution = 10   # sample points per one guided wavelength


def n_points(length, resolution=resolution, wavelength_g=wavelength_g, min_points=2):
    return max(min_points, round(resolution * length / wavelength_g))


def segment(p0, p1, resolution=resolution, wavelength_g=wavelength_g):
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

# --- build (x, y) samples ---
xs, ys = [], []
for p0, p1 in itertools.pairwise(waypoints):
    xseg, yseg = segment(p0, p1)
    xs.append(xseg)
    ys.append(yseg)

x = np.concatenate(xs)
y = np.concatenate(ys)
N = len(x)
print(f"Number of elemental dipoles: {N}")


# ---------------- Elemental dipole current distribution (standing wave) ----------------
sep = 360.0 / resolution                              # deg of guided-wave phase per sample
phase_from_open_end = (N - 1 - np.arange(N)) * sep    # deg; 0 exactly at the LAST dipole

I0 = 1.0                                               # standing-wave current amplitude [A]
current = I0 * np.sin(np.deg2rad(phase_from_open_end))    # REAL-valued; current[-1] == 0

dipole_length = wavelength_g / resolution              # physical length of ONE element [m]


# ---------------- Far field of a single infinitesimal dipole ----------------
eta = 120 * np.pi   # free-space wave impedance [Ohm]
r = 10.0            # observation distance [m]


# Calculate the far-field of a single infinitesimal dipole at the origin, oriented along the y-axis
y_axis_dipole = np.array([0.0, 1.0, 0.0])

# Spherical observation grid. theta is measured from +z and phi from +x.
theta = np.linspace(0.0, np.pi, 180)
phi = np.linspace(0.0, 2.0 * np.pi, 360)
theta_grid, phi_grid = np.meshgrid(theta, phi, indexing="ij")

# Spherical components of the y-directed dipole unit vector.
y_dot_theta = np.cos(theta_grid) * np.sin(phi_grid)
y_dot_phi = np.cos(phi_grid)

# E_ff = prefactor * [(y . theta_hat) theta_hat + (y . phi_hat) phi_hat].
far_field_prefactor = (
    1j * eta * k0 * I0 * dipole_length
    * np.exp(-1j * k0 * r)
    / (4.0 * np.pi * r)
)
e_theta = far_field_prefactor * y_dot_theta
e_phi = far_field_prefactor * y_dot_phi

electric_field_magnitude = np.sqrt(np.abs(e_theta) ** 2 + np.abs(e_phi) ** 2)
normalized_pattern = electric_field_magnitude / electric_field_magnitude.max()
power_pattern = normalized_pattern ** 2

# Plot the normalized field pattern as a 3D radiation surface.
radiation_x = normalized_pattern * np.sin(theta_grid) * np.cos(phi_grid)
radiation_y = normalized_pattern * np.sin(theta_grid) * np.sin(phi_grid)
radiation_z = normalized_pattern * np.cos(theta_grid)

figure = plt.figure("Y-directed infinitesimal dipole radiation pattern")
colormap = mpl.colormaps["viridis"]
axis = figure.add_subplot(111, projection="3d")
axis.plot_surface(
    radiation_x,
    radiation_y,
    radiation_z,
    facecolors=colormap(normalized_pattern),
    linewidth=0,
    antialiased=True,
)
axis.set_title("Normalized far-field radiation pattern")
axis.set_xlabel("x")
axis.set_ylabel("y")
axis.set_zlabel("z")
axis.set_box_aspect((1.0, 1.0, 1.0))
plt.show()
