import itertools

import Antenna_functions as af
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (enables 3D projection)

frequency = 1060e6  # Frequency in Hz 

# ---------------- Simulation parameters (ADJUSTABLE) ----------------
hertz_dipole_resolution = 100   # number of points along the mander-line antenna (higher value = more accurate simulation)
measure_distance = 10.0  # distance from the antenna to the measurement sphere (in meters)
measure_resolution = 1000  # number of points on the measurement sphere

# ---------------- Antenna geometry (ADJUSTABLE) ----------------
total_length, wavelength_g, points = af.maenderline_antenna_geometry(hertz_dipole_resolution, plot=True)
dipole_length = total_length/ hertz_dipole_resolution

# ---------------- Measurement sphere (ADJUSTABLE) ----------------
measurement_points = af.measurement_sphere(measure_distance, measure_resolution, plot=True)  # Example usage of the measurement_sphere function

# ---------------- Current distribution (ADJUSTABLE) ----------------
current_distribution = af.current(hertz_dipole_resolution, total_length, wavelength_g, I0=1.0, plot=True)  # Example usage of the current function
# ---------------- Generate 3D structure ----------------
segmentations = af.coordinates(points, plot=True)

# ---------------- Vecor calculations (ADJUSTABLE) ----------------
r_array, s_hat_array, h_hat_array, s_array, h_array= af.local_point_relation(measurement_points, segmentations)
r_hat, theta_hat, phi_hat, R_mark, sin_theta, cos_theta= af.measurement_global(s_hat_array, h_hat_array)

# ---------------- Field calculations (ADJUSTABLE) ----------------
E_cart_array, H_cart_array, E_cart_total, H_cart_total = af.field_calcualtions(current_distribution, dipole_length, r_array, wavelength_g, cos_theta, sin_theta, theta_hat, phi_hat, r_hat)
print(E_cart_total)