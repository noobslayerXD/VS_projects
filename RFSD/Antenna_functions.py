"""
Hertz-dipole (wire-antenna) model of the meander-line antenna from
O.P.N. Calla et al., "Empirical Relation for Designing the Meander Line
Antenna", ICM-2008, following Ch. 1 of the RF System Design Integration Note
(eqs. 1.1-1.7).

The trace is split into short straight segments; each segment is a Hertz
dipole with its own orientation h_hat, and the fields of all dipoles are
summed as vectors in global Cartesian coordinates at every observation point.
"""

import itertools

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

C0 = 299_792_458.0      # speed of light [m/s]
ETA0 = 120 * np.pi      # free-space wave impedance [ohm]

_trapezoid = getattr(np, "trapezoid", None) or np.trapz   # numpy >= 2.0 renamed trapz


# =============================================================================
# Geometry
# =============================================================================
def n_points(length, resolution, wavelength_g, min_points=2):
    """Number of samples on a straight run, so that `resolution` samples span one guided wavelength."""
    return max(min_points, round(resolution * length / wavelength_g))


def segment(p0, p1, resolution, wavelength_g):
    """Evenly spaced (x, y) samples from p0 to p1, both end points included."""
    (x0, y0), (x1, y1) = p0, p1
    n = n_points(np.hypot(x1 - x0, y1 - y0), resolution, wavelength_g)
    return np.linspace(x0, x1, n), np.linspace(y0, y1, n)


def meander_line_geometry(frequency, hertz_dipole_resolution, h_sub=3.2e-3, e_r=4.4, plot=False):
    """
    Meander-line centre line, sized with the paper's design equations (1)-(6), (11).

    Parameters:
    - frequency: design frequency [Hz]
    - hertz_dipole_resolution: Hertz dipoles per guided wavelength
    - h_sub: substrate height [m]
    - e_r: substrate relative permittivity

    Returns:
    - points: (N+1, 2) wire sample points, feed first, open end last, centred on the origin
    - params: dict with the wavelengths, e_r_eff and the dimensions d, s, L, w
    """
    wavelength0 = C0 / frequency
    w_eq11 = C0 / (2 * frequency) * np.sqrt(2 / (e_r + 1))                         # eq. 11
    e_r_eff = (e_r + 1) / 2 + (e_r - 1) / 2 * (1 + 10 * h_sub / w_eq11) ** -0.5     # eq. 6
    wavelength_g = wavelength0 / np.sqrt(e_r_eff)                                    # eq. 5

    d = 0.16 * wavelength_g   # eq. 1
    s = 0.42 * wavelength_g   # eq. 2
    L = 0.70 * wavelength_g   # eq. 3 (only used by the paper's closed-form beamwidths)
    w = 0.05 * wavelength_g   # eq. 4

    waypoints = [
        (0, 0),
        (s + w, 0),
        (s + w, -d),
        (0, -d),
        (0, -2 * d),
        (s + w, -2 * d),
        (s + w, -3 * d),
        (0, -3 * d),
        (0, -4 * d),
    ]

    xs, ys = [], []
    for n, (p0, p1) in enumerate(itertools.pairwise(waypoints)):
        x_seg, y_seg = segment(p0, p1, hertz_dipole_resolution, wavelength_g)
        if n > 0:   # first sample is the corner already added by the previous run
            x_seg, y_seg = x_seg[1:], y_seg[1:]
        xs.append(x_seg)
        ys.append(y_seg)

    points = np.column_stack((np.concatenate(xs), np.concatenate(ys)))
    points -= (points.max(axis=0) + points.min(axis=0)) / 2     # centre the antenna on the origin

    params = dict(frequency=frequency, wavelength0=wavelength0, wavelength_g=wavelength_g,
                  e_r=e_r, e_r_eff=e_r_eff, h_sub=h_sub, d=d, s=s, L=L, w=w)

    if plot:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(points[:, 0] * 1e3, points[:, 1] * 1e3, 'b.-', markersize=3, linewidth=1)
        ax.plot(*points[0] * 1e3, 'go', markersize=8, label='Feed')
        ax.plot(*points[-1] * 1e3, 'ro', markersize=8, label='Open end')
        ax.set_title(f'Meander-line antenna ({len(points) - 1} Hertz dipoles)')
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('y [mm]')
        ax.set_aspect('equal')
        ax.grid(True)
        ax.legend()

    return points, params


def coordinates(points_2d, z=3.2e-3, plot=False):
    """Lift the 2D trace to 3D, placing it at height z."""
    points_3d = np.column_stack((points_2d, np.full(len(points_2d), z)))

    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(*points_3d.T, s=4)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.set_title('Antenna in 3D')

    return points_3d


# =============================================================================
# Current distribution
# =============================================================================
def current(antenna_points, wavelength_g, I0=1.0, plot=False):
    """
    Standing-wave current, zero at the open end of the wire:

        I(u) = I0 * sin(2*pi*u / wavelength_g),   u = distance along the wire to the open end

    evaluated at the midpoint of every Hertz dipole, using the true arc length
    of each segment.

    Returns:
    - I: (N,) current of each Hertz dipole [A]
    """
    seg_len = np.linalg.norm(np.diff(antenna_points, axis=0), axis=1)
    s_mid = np.cumsum(seg_len) - seg_len / 2          # arc length from the feed to each midpoint
    u = seg_len.sum() - s_mid                         # arc length from each midpoint to the open end
    I = I0 * np.sin(2 * np.pi * u / wavelength_g)

    if plot:
        plt.figure(figsize=(8, 4))
        plt.stem(s_mid * 1e3, I, linefmt='b-', markerfmt='b.', basefmt='k-')
        plt.title('Current distribution along the meander line (feed at 0)')
        plt.xlabel('Position along the wire [mm]')
        plt.ylabel('Current [A]')
        plt.grid(True)

    return I


# =============================================================================
# Fields (design note eqs. 1.1 - 1.3)
# =============================================================================
def dipole_segments(antenna_points):
    """Centre, unit axis h_hat and length of every Hertz dipole (one per pair of consecutive points)."""
    seg = np.diff(antenna_points, axis=0)
    dl = np.linalg.norm(seg, axis=1)
    centers = (antenna_points[:-1] + antenna_points[1:]) / 2
    h_hat = seg / dl[:, None]
    return centers, h_hat, dl


def local_angles(s_hat, h_hat):
    """
    Eqs. 1.2 and 1.3: angle between one dipole axis h_hat (3,) and the
    directions s_hat (M,3) to the observation points, plus that dipole's
    theta_hat / phi_hat, all as global Cartesian vectors.
    """
    cos_theta = s_hat @ h_hat
    cross = np.cross(h_hat, s_hat)
    sin_theta = np.linalg.norm(cross, axis=1)
    safe = np.maximum(sin_theta, 1e-12)[:, None]       # theta_hat/phi_hat undefined on the dipole axis
    phi_hat = cross / safe
    theta_hat = (cos_theta[:, None] * s_hat - h_hat) / safe
    return cos_theta, sin_theta, theta_hat, phi_hat


def hertz_dipole_field(I, dl, r, cos_theta, sin_theta, k):
    """Eq. 1.1: E_r, E_theta and H_phi of one Hertz dipole in its own local frame."""
    jkr = 1j * k * r
    moment = I * dl * np.exp(-jkr)
    E_r = ETA0 * moment * cos_theta / (2 * np.pi * r**2) * (1 + 1 / jkr)
    E_theta = 1j * ETA0 * k * moment * sin_theta / (4 * np.pi * r) * (1 + 1 / jkr - 1 / (k * r)**2)
    H_phi = 1j * k * moment * sin_theta / (4 * np.pi * r) * (1 + 1 / jkr)
    return E_r, E_theta, H_phi


def compute_total_field(observation_points, antenna_points, current, wavelength):
    """
    Total E and H field of all Hertz dipoles at every observation point.

    Dipoles are handled one at a time and added straight into the running
    total, so memory use only grows with the number of observation points.

    Parameters:
    - observation_points: (..., 3) array (e.g. a (n_theta, n_phi, 3) grid)
    - antenna_points: (N+1, 3) wire sample points
    - current: (N,) current of each Hertz dipole
    - wavelength: wavelength used for k = 2*pi/wavelength. The guided
      wavelength is used throughout this project, as in the reference
      implementation (github.com/PhillipRambo/meander_line_simulation).

    Returns:
    - E, H: complex arrays with the same shape as observation_points
    """
    obs = np.asarray(observation_points, dtype=float)
    shape = obs.shape
    obs = obs.reshape(-1, 3)
    k = 2 * np.pi / wavelength

    E = np.zeros(obs.shape, dtype=complex)
    H = np.zeros(obs.shape, dtype=complex)

    for center, h_hat, dl, I in zip(*dipole_segments(antenna_points), current):
        s = obs - center
        r = np.linalg.norm(s, axis=1)
        s_hat = s / r[:, None]                                         # = r_hat of this dipole (eq. 1.2)
        cos_theta, sin_theta, theta_hat, phi_hat = local_angles(s_hat, h_hat)
        E_r, E_theta, H_phi = hertz_dipole_field(I, dl, r, cos_theta, sin_theta, k)

        E += E_r[:, None] * s_hat + E_theta[:, None] * theta_hat
        H += H_phi[:, None] * phi_hat

    return E.reshape(shape), H.reshape(shape)


# =============================================================================
# Observation points, power density and directivity (eqs. 1.5 - 1.7)
# =============================================================================
def observation_grid(distance, step_deg=2.0):
    """
    Regular theta/phi grid on a sphere of radius `distance` (theta from +z, phi from +x).

    Returns:
    - theta: (n_theta,) [rad], phi: (n_phi,) [rad]
    - points: (n_theta, n_phi, 3) Cartesian observation points
    """
    theta = np.linspace(0, np.pi, round(180 / step_deg) + 1)
    phi = np.linspace(0, 2 * np.pi, round(360 / step_deg) + 1)
    TH, PH = np.meshgrid(theta, phi, indexing='ij')
    points = distance * np.stack((np.sin(TH) * np.cos(PH),
                                  np.sin(TH) * np.sin(PH),
                                  np.cos(TH)), axis=-1)
    return theta, phi, points


def radial_power_density(E, H, observation_points):
    """Eq. 1.7: S_r = 1/2 Re{E x H*} . r_hat at every observation point."""
    S = 0.5 * np.real(np.cross(E, np.conj(H)))
    r_hat = observation_points / np.linalg.norm(observation_points, axis=-1, keepdims=True)
    return np.sum(S * r_hat, axis=-1)


def directivity(S_r, theta, phi):
    """
    Eqs. 1.5/1.6: D0 = 4*pi*r^2 * S_max / P_rad, with P_rad integrated over
    the theta/phi grid (S_r has shape (n_theta, n_phi); r^2 cancels).
    """
    integrand = S_r * np.sin(theta)[:, None]
    P_over_r2 = _trapezoid(_trapezoid(integrand, phi, axis=1), theta)
    return 4 * np.pi * S_r.max() / P_over_r2


# =============================================================================
# E-/H-plane cuts and 3 dB beamwidth
# =============================================================================
def principal_plane_cuts(E, observation_points, n_points=720):
    """
    Great circles through the direction of maximum radiation:
    the E-plane contains the peak direction and the E-field vector there,
    the H-plane contains the peak direction and is perpendicular to the E-plane.

    Returns a dict with:
    - 'peak_theta_deg', 'peak_phi_deg': direction of maximum |E|
    - 'alpha': (n_points,) angle from the peak direction [rad]
    - 'E-plane', 'H-plane': (n_points, 3) observation points on each cut
    """
    E_flat = E.reshape(-1, 3)
    pts = observation_points.reshape(-1, 3)
    i_peak = np.argmax(np.sum(np.abs(E_flat)**2, axis=1))

    R = np.linalg.norm(pts[i_peak])
    r0 = pts[i_peak] / R
    E0 = E_flat[i_peak] - (E_flat[i_peak] @ r0) * r0       # transverse part of E at the peak
    psi = -0.5 * np.angle(E0 @ E0)                          # rotate to the polarisation-ellipse major axis
    e_hat = np.real(E0 * np.exp(1j * psi))
    e_hat /= np.linalg.norm(e_hat)
    h_hat = np.cross(r0, e_hat)

    alpha = np.linspace(-np.pi, np.pi, n_points, endpoint=False)

    def great_circle(u):
        return R * (np.cos(alpha)[:, None] * r0 + np.sin(alpha)[:, None] * u)

    return {
        'peak_theta_deg': np.degrees(np.arccos(np.clip(r0[2], -1, 1))),
        'peak_phi_deg': np.degrees(np.arctan2(r0[1], r0[0])) % 360,
        'alpha': alpha,
        'E-plane': great_circle(e_hat),
        'H-plane': great_circle(h_hat),
    }


def half_power_beamwidth(alpha, E_cut):
    """
    3 dB beamwidth [deg] of one cut. alpha must cover a full circle evenly
    (no repeated end point); the search wraps around the circle. Returns None
    if the cut never drops 3 dB below its maximum.
    """
    P = np.sum(np.abs(E_cut)**2, axis=-1)
    P = P / P.max()
    if P.min() >= 0.5:
        return None

    n = len(P)
    step = alpha[1] - alpha[0]
    i0 = int(np.argmax(P))

    def walk(direction):
        j = i0
        while P[(j + direction) % n] >= 0.5:
            j += direction
        p_in, p_out = P[j % n], P[(j + direction) % n]
        return (abs(j - i0) + (p_in - 0.5) / (p_in - p_out)) * step

    return np.degrees(walk(+1) + walk(-1))


def paper_closed_form(params):
    """Paper eqs. 12-16: theta_E, theta_H [deg], directivity and gain (linear)."""
    L, w, h = params['L'], params['w'], params['h_sub']
    k_o = np.pi / (np.sqrt(params['e_r_eff']) * L)                                     # eq. 14
    theta_E = 2 * np.degrees(np.arcsin(np.sqrt(7.03 / ((3 * L**2 + h**2) * k_o**2))))  # eq. 12
    theta_H = 2 * np.degrees(np.arcsin(np.sqrt(1 / (2 + k_o * w))))                     # eq. 13
    D = 41253 / (theta_E * theta_H)                                                     # eq. 15
    G = 32400 / (theta_E * theta_H)                                                     # eq. 16
    return theta_E, theta_H, D, G


# =============================================================================
# Plots of |E|
# =============================================================================
def plot_E_magnitude_3d(E, observation_points, dB=False, dB_floor=-30, cmap='rainbow',
                        title='3D radiation pattern, |E|'):
    """
    3D pattern of the normalised |E| on a theta/phi grid (as returned by
    observation_grid): radius and colour both show the field strength.
    """
    E_norm = np.linalg.norm(E, axis=-1)
    E_norm = E_norm / E_norm.max()

    if dB:
        level = np.clip(20 * np.log10(np.maximum(E_norm, 1e-12)), dB_floor, 0)
        radius = (level - dB_floor) / -dB_floor
        color_norm, color_values, label = Normalize(dB_floor, 0), level, 'Normalised |E| [dB]'
    else:
        radius = E_norm
        color_norm, color_values, label = Normalize(0, 1), E_norm, 'Normalised |E|'

    r_hat = observation_points / np.linalg.norm(observation_points, axis=-1, keepdims=True)
    X, Y, Z = np.moveaxis(radius[..., None] * r_hat, -1, 0)
    colormap = plt.get_cmap(cmap)

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(X, Y, Z, facecolors=colormap(color_norm(color_values)),
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)
    fig.colorbar(ScalarMappable(norm=color_norm, cmap=colormap), ax=ax, shrink=0.6, label=label)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)
    return fig, ax


def plot_E_magnitude_2d(cuts, dB=False, dB_floor=-30, title='2D radiation pattern, |E|'):
    """
    Polar plot of one or more cuts. `cuts` is a list of (label, alpha, E_cut)
    with alpha [rad] measured from the main-beam direction (drawn pointing up).
    All cuts share one normalisation so their levels can be compared.
    """
    E_max = max(np.linalg.norm(E_cut, axis=-1).max() for _, _, E_cut in cuts)

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(projection='polar')

    for label, alpha, E_cut in cuts:
        E_norm = np.linalg.norm(E_cut, axis=-1) / E_max
        a = np.append(alpha, alpha[0] + 2 * np.pi)          # close the curve
        E_norm = np.append(E_norm, E_norm[0])
        values = np.clip(20 * np.log10(np.maximum(E_norm, 1e-12)), dB_floor, 0) if dB else E_norm
        ax.plot(a, values, linewidth=1.5, label=label)

    circle = np.linspace(0, 2 * np.pi, 361)
    level = -3 if dB else 10 ** (-3 / 20)
    ax.plot(circle, np.full_like(circle, level), 'k--', linewidth=0.8, label='-3 dB')
    if dB:
        ax.set_ylim(dB_floor, 0)

    ax.set_theta_zero_location('N')
    ax.set_title(title, pad=20)
    ax.legend(loc='lower right', bbox_to_anchor=(1.3, -0.05))
    return fig, ax