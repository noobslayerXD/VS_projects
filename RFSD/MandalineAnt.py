from math import e, pi

from matplotlib import projections
import numpy as np
import matplotlib.pyplot as plt

# --- Physical / substrate parameters ----------------------------------------
C0 = 299792458.0          # speed of light in vacuum [m/s]
f = 1060e6                # design frequency [Hz]
h = 3.2e-3                # substrate height [m]
e_r = 4.4                 # substrate relative permittivity

wavelength = C0 / f
w = C0 / (2 * f) * np.sqrt(2 / (e_r + 1))
e_r_eff = (e_r + 1) / 2 + (e_r - 1) / 2 * (1 + 10 * h / w) ** (-0.5)
wavelength_g = wavelength / np.sqrt(e_r_eff)
#print(wavelength_g)
# --- Meander-line geometry (in units of the guided wavelength) --------------
d = 0.16 * wavelength_g
s = 0.42 * wavelength_g
L = 0.07 * wavelength_g
w = 0.05 * wavelength_g          


# --- Resolution control ------------------------------------------------------
# "resolution" = number of points per ONE guided wavelength (wavelength_g).
# A segment that is 0.5*wavelength_g long then gets 0.5*resolution points:
#   resolution = 10   -> 5 points
#   resolution = 100  -> 50 points
#   resolution = 1000 -> 500 points
resolution = 100


def n_points(length, resolution=resolution, wavelength_g=wavelength_g, min_points=2):
    """Number of samples for a straight segment of the given physical length,
    scaled so that `resolution` points correspond to one guided wavelength."""
    return max(min_points, int(round(resolution * length / wavelength_g)))


def segment(p0, p1, resolution=resolution, wavelength_g=wavelength_g):
    """(x, y) arrays for a straight line from p0 to p1, point count scaled
    by segment length relative to wavelength_g (see n_points)."""
    x0, y0 = p0
    x1, y1 = p1
    length = np.hypot(x1 - x0, y1 - y0)
    n = n_points(length, resolution, wavelength_g)
    return np.linspace(x0, x1, n), np.linspace(y0, y1, n)

### Plotting the whole line
# --- Build the meander path (same shape as the original 8 segments) --------
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
for p0, p1 in zip(waypoints[:-1], waypoints[1:]):
    xseg, yseg = segment(p0, p1)
    xs.append(xseg)
    ys.append(yseg)

x = np.concatenate(xs)
y = np.concatenate(ys)
z = np.zeros_like(x)

# --- Plot ---------------------------------------------------------------
fig = plt.figure() 
ax = plt.subplot(projection = '3d')
ax.plot(x, y, z, color='blue', marker='o', markersize=3)
ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.set_aspect('equal')
ax.set_title(f'Meander-line antenna ({resolution} pts / \u03bb$_g$, {len(x)} pts total)')
plt.savefig('meander_antenna.png', dpi=150, bbox_inches='tight')
#plt.show()



### Setting the current for each point on the line

sep = 360/resolution

dipoles = np.arange(252) * sep
current = np.sin(np.deg2rad(x))**2

dipole_length = wavelength_g/resolution
#print(dipole_length)

Radiation_resistance = 80*pi**2*(dipole_length/wavelength_g)**2
#print(Radiation_resistance)
Radiated_power = (1/2)*current**2 * Radiation_resistance
print(max(Radiated_power))
#print(current)

### Calculate the E field
# first the E_r field is calculated
eta = 120*pi
k = 2*pi/wavelength_g
E_r(theta,r) = eta*(current*cos(theta)/(2*pi*r**2))*(1+(1/(j*k*r)))*e**(-j*k*r)

E_theta(theta,r) = j* eta* ((k* current* h* sin(theta))/(4* pi* r))*(1+((1)/(j*k*r))-(1)/(k*r)**2)*e**-j*k*r
