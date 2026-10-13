import matplotlib.pyplot as plt
import numpy as np

import Antenna_functions as af

# ---------------- Simulation parameters (ADJUSTABLE) ----------------
frequency = 1060e6                # design frequency [Hz]
hertz_dipole_resolution = 1000     # Hertz dipoles per guided wavelength (higher = more accurate, slower)
measure_distance = 10.0           # radius of the observation sphere [m]
angular_step_deg = 2.0            # theta/phi step of the observation grid [deg]
plot_setup = True                 # also plot the geometry and the current distribution
dB_plots = False                  # plot |E| in dB instead of linear

# Legacy adjustable example retained for local debugging.
# hertz_dipole_resolution = 106
# measure_distance = 100.0
# measure_resolution = 100000
# total_length, wavelength_g, points = af.maenderline_antenna_geometry(hertz_dipole_resolution, plot=True)
# dipole_length = total_length / hertz_dipole_resolution
# measurement_points = af.measurement_sphere(measure_distance, measure_resolution, plot=True)

# ---------------- Antenna geometry ----------------
points_2d, params = af.meander_line_geometry(frequency, hertz_dipole_resolution, plot=plot_setup)
antenna_points = af.coordinates(points_2d, z=params['h_sub'])
wavelength_g = params['wavelength_g']

# ---------------- Current distribution ----------------
current_distribution = af.current(antenna_points, wavelength_g, I0=1.0, plot=plot_setup)

# ---------------- Fields on the observation sphere ----------------
theta, phi, observation_points = af.observation_grid(measure_distance, angular_step_deg)
E, H = af.compute_total_field(observation_points, antenna_points, current_distribution, wavelength_g)

# ---------------- Directivity ----------------
S_r = af.radial_power_density(E, H, observation_points)
D0 = af.directivity(S_r, theta, phi)

# ---------------- E- and H-plane cuts and 3 dB beamwidths ----------------
cuts = af.principal_plane_cuts(E, observation_points)
alpha = cuts['alpha']
E_Eplane, _ = af.compute_total_field(cuts['E-plane'], antenna_points, current_distribution, wavelength_g)
E_Hplane, _ = af.compute_total_field(cuts['H-plane'], antenna_points, current_distribution, wavelength_g)
hpbw_E = af.half_power_beamwidth(alpha, E_Eplane)
hpbw_H = af.half_power_beamwidth(alpha, E_Hplane)

# ---------------- Validation against the paper (eqs. 12-16) ----------------
theta_E_paper, theta_H_paper, D_paper, G_paper = af.paper_closed_form(params)


def fmt_deg(value):
    return f'{value:8.1f} deg' if value is not None else '  no 3 dB points'


print(f'Hertz dipoles:            {len(current_distribution)}')
print(f'Main beam direction:      theta = {cuts["peak_theta_deg"]:.1f} deg, phi = {cuts["peak_phi_deg"]:.1f} deg')
print()
print(f'{"":26s}{"Simulation":>18s}{"Paper (eq. 12-15)":>20s}')
print(f'{"E-plane 3 dB angle":26s}{fmt_deg(hpbw_E):>18s}{theta_E_paper:15.1f} deg')
print(f'{"H-plane 3 dB angle":26s}{fmt_deg(hpbw_H):>18s}{theta_H_paper:15.1f} deg')
print(f'{"Directivity (eq. 1.6)":26s}{10 * np.log10(D0):14.2f} dBi{10 * np.log10(D_paper):16.2f} dBi')
if hpbw_E is not None and hpbw_H is not None:
    D_beamwidth = 41253 / (hpbw_E * hpbw_H)
    print(f'{"Directivity (eq. 15)":26s}{10 * np.log10(D_beamwidth):14.2f} dBi'
          '   <- eq. 15 applied to the simulated 3 dB angles')
print(f'{"Gain (paper, eq. 16)":26s}{"":18s}{10 * np.log10(G_paper):16.2f} dB')
print(f'Half-power beamwidth: E-plane = {fmt_deg(hpbw_E).strip()}, H-plane = {fmt_deg(hpbw_H).strip()}')
# ---------------- Plots ----------------
af.plot_E_magnitude_3d(E, observation_points, dB=dB_plots)
af.plot_E_magnitude_2d([
    (f'E-plane (3 dB: {fmt_deg(hpbw_E).strip()})', alpha, E_Eplane),
    (f'H-plane (3 dB: {fmt_deg(hpbw_H).strip()})', alpha, E_Hplane),
], dB=dB_plots, title='E- and H-plane cuts, |E| (0 deg = main beam)')

# ---------------- Field calculations (ADJUSTABLE) ----------------
E_cart_array, H_cart_array, E_cart_total, H_cart_total = af.field_calcualtions(current_distribution, dipole_length, r_array, wavelength_g, cos_theta, sin_theta, theta_hat, phi_hat, r_hat)

Poynting = af.poynting_vector(E_cart_total, H_cart_total)
D0 = af.directivity(Poynting)
print(D0)

# af.plot_radiation_pattern(E_cart_array, H_cart_array, measurement_points)

plt.show()
