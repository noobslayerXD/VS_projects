import matplotlib.pyplot as plt
import numpy as np
from scipy.special import sici


def n_points(length, resolution, wavelength_g, min_points=2):
    return max(min_points, round(resolution * length / wavelength_g))


def segment(p0, p1, resolution, wavelength_g):
    x0, y0 = p0
    x1, y1 = p1
    length = np.hypot(x1 - x0, y1 - y0)
    n = n_points(length, resolution, wavelength_g)
    return np.linspace(x0, x1, n), np.linspace(y0, y1, n)

def current(wavelength_g, hertz_dipole_resolution, N, I0=1.0):
    """
    Compute the current distribution along a meander-line antenna.

    Parameters:
    - wavelength_g: guided wavelength
    - hertz_dipole_resolution: length of the sine wave in guided wavelengths
    - N: number of current values to calculate
    - I0: peak current amplitude (default is 1.0)
    - segment_place: array of segment positions along the antenna

    Returns:
    - I: array of current values corresponding to each dipole segment along the antenna
    """
    
    if N < 1:
        raise ValueError("N must be at least 1.")

    phase = np.linspace(
        0.0,
        2 * np.pi * hertz_dipole_resolution,
        N,
    )
    I = I0 * np.sin(phase)

    return np.flip(I)


def Cart_coordinate_to_spherical_global(A_x, A_y, A_z, theta, phi):
    A_r = A_y*np.sin(theta)*np.sin(phi) + A_x*np.sin(theta)*np.cos(phi) + A_z*np.cos(theta)
    A_theta = A_y*np.cos(theta)*np.sin(phi) + A_x*np.cos(theta)*np.cos(phi) - A_z*np.sin(theta)
    A_phi = A_y*np.cos(phi) - A_x*np.sin(phi)
    return A_r, A_theta, A_phi


def Cart_amplitude(I0, dipole_length, r, mu, wavelength_g):
    """
    Compute the amplitude of the electric field in spherical coordinates from a Hertzian dipole.

    Parameters:
    - I0: peak current amplitude
    - dipole_length: length of the dipole
    - r: radial distance from the dipole
    - mu: dont know what this is
    - wavelength_g: guided wavelength

    Returns:
    - A_z: amplitude of the electric field in spherical coordinates (A_r, A_theta, A_phi)
    """
    k = 2 * np.pi / wavelength_g
    
    A_z = (mu*I0*dipole_length*np.e**(-1j*k*r))/(4*np.pi*r) 
    
    return A_z

def Cart_coordinate_to_spherical_local(A_x, A_y, A_z, theta, phi):
    '''
    Convert Cartesian coordinates to spherical coordinates in a local coordinate system.
    Assuming the local coordinate system A_x = A_y = 0, A_z = 1, and the spherical coordinates are defined by angles theta and phi.
    Parameters:
    
    '''
    
    A_r = A_z*np.cos(theta)
    A_theta = -A_z*np.sin(theta)
    A_phi = 0
    return A_r, A_theta, A_phi

def E_fields(I0, dipole_length, r, theta, wavelength_g):
    '''
    Compute the electric field components in spherical coordinates from a Hertzian dipole.
    
    input parameters:
    - I0: peak current amplitude
    - dipole_length: length of the dipole
    - r: radial distance from the dipole
    - theta: polar angle in spherical coordinates
    - wavelength_g: guided wavelength
    
    '''
    
    k = 2 * np.pi / wavelength_g
    eta = 120 * np.pi  # intrinsic impedance of free space

    E_r = eta*(I0*dipole_length*np.cos(theta))/(2*np.pi*r**2)*(1 + 1/(1j*k*r))*np.e**(-1j*k*r)
    E_theta = 1j*eta*(k*I0*dipole_length*np.sin(theta))/(4*np.pi*r)*(1 + 1/(1j*k*r) - 1/((k*r)**2))*np.e**(-1j*k*r)
    E_phi = 0
    
    return E_r, E_theta, E_phi

def H_fields(I0, dipole_length, r, theta, wavelength_g):
    '''
    Compute the magnetic field components in spherical coordinates from a Hertzian dipole.
    
    input parameters:
    - I0: peak current amplitude
    - dipole_length: length of the dipole
    - r: radial distance from the dipole
    - theta: polar angle in spherical coordinates
    - wavelength_g: guided wavelength
    
    '''
    
    k = 2 * np.pi / wavelength_g

    H_r = 0
    H_theta = 0
    H_phi = 1j*(k*I0*dipole_length*np.sin(theta))/(4*np.pi*r)*(1 + 1/(1j*k*r))*np.e**(-1j*k*r)
    
    return H_r, H_theta, H_phi