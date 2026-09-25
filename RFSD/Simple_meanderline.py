import itertools

import Antenna_functions as af
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
wavelength_g = wavelength0 / np.sqrt(e_r_eff)  # eq. 5

# ---------------- Meander-line dimensions, exactly per the paper's eqs 1-4 ----------------
d = 0.16 * wavelength_g   # eq. 1
s = 0.42 * wavelength_g   # eq. 2
L = 0.70 * wavelength_g   # eq. 3 -- used ONLY in the closed-form validation below;
                          # the repeating meander unit itself is fully defined by d, s, w (eqs 1,2,4)
w = 0.05 * wavelength_g   # eq. 4

# ---------------- Hertz dipole resolution (ADJUSTABLE) ----------------
hertz_dipole_resolution = 1000   # samples per one guided wavelength

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
    xseg, yseg = af.segment(p0, p1, hertz_dipole_resolution, wavelength_g)
    xs.append(xseg)
    ys.append(yseg)

x = np.concatenate(xs)
y = np.concatenate(ys)
N = len(x)

current_distribution = af.current(
    wavelength_g,
    hertz_dipole_resolution,
    N,
    I0=1.0,
)

dipole_length = wavelength_g / hertz_dipole_resolution
print(f"Hertz dipole resolution: {hertz_dipole_resolution} samples/lambda_g")
print(f"Number of elemental dipoles: {N}")
print(f"dipole_length / wavelength_g = {dipole_length / wavelength_g:.4f}  (must stay << {wavelength_g/50:.4f})")

thetas = np.linspace(0, np.pi, 180)

E_r_all = []
E_theta_all = []
E_phi_all = []
H_r_all = []
H_theta_all = []
H_phi_all = []

for theta in thetas:
    E_r, E_theta, E_phi = af.E_fields(current_distribution, dipole_length, 10, theta, wavelength_g)
    H_r, H_theta, H_phi = af.H_fields(current_distribution, dipole_length, 10, theta, wavelength_g)
    
    E_r_all.append(E_r)
    E_theta_all.append(E_theta)
    E_phi_all.append(E_phi)
    H_r_all.append(H_r)
    H_theta_all.append(H_theta)
    H_phi_all.append(H_phi)
    print (f"All E-field components at theta={theta} rad: E_r={E_r}, E_theta={E_theta}, E_phi={E_phi}")
    print (f"All H-field components at theta={theta} rad: H_r={H_r}, H_theta={H_theta}, H_phi={H_phi}")

print("Field computation complete.")
print(f"All E-field components for the first dipole:{E_r_all[0]}, {E_theta_all[0]}, {E_phi_all[0]}")
print(f"All H-field components for the first dipole:{H_r_all[0]}, {H_theta_all[0]}, {H_phi_all[0]}")

# combine x and y into a single array of shape (N, 2)
points = np.column_stack((x, y))
print(f"Points array: {points}")

# plot the points in 2D
plt.figure(figsize=(8, 6))
plt.plot(points[:, 0], points[:, 1], 'o-', markersize=3)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Meander-line Geometry')
plt.grid(True)
plt.show()