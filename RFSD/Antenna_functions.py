from numbers import Real
import itertools
import numpy as np
import matplotlib.pyplot as plt


def n_points(length, resolution, wavelength_g, min_points=2):
    return max(min_points, round(resolution * length / wavelength_g))

def segment(p0, p1, resolution, wavelength_g):
    x0, y0 = p0
    x1, y1 = p1
    length = np.hypot(x1 - x0, y1 - y0)
    n = n_points(length, resolution, wavelength_g)
    return np.linspace(x0, x1, n), np.linspace(y0, y1, n)

def current(hertz_dipole_resolution, antenna_length, wavelength_g, I0=1.0, plot=False):

    s = np.linspace(0, antenna_length, hertz_dipole_resolution)

    I = I0 * np.sin(2 * np.pi * s / wavelength_g)

    if plot:
        # plot the current distribution along the antenna (stem plot)
        plt.figure(figsize=(8, 4))
        plt.stem(s, I, linefmt='b-', markerfmt='bo', basefmt='none')
        plt.title('Current Distribution Along Meander-Line Antenna')
        plt.xlabel('Position Along Antenna [m]')
        plt.ylabel('Current Amplitude [A]')
        plt.grid(True)
        plt.show()

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

def field_calcualtions(I0, dipole_length, r_array, wavelength_g, cos_theta, sin_theta, theta_hat, phi_hat, r_hat):
    '''
    Compute the electric field components in spherical coordinates from a Hertzian dipole.
    
    input parameters:
    - I0: peak current amplitude
    - dipole_length: length of the dipole
    - r_array: array of radial distances from the dipole
    - theta_array: array of polar angles in spherical coordinates
    - wavelength_g: guided wavelength

    Returns:
    - E_array: array of electric field components in spherical coordinates (E_r, E_theta, E_phi)
    - H_array: array of magnetic field components in spherical coordinates (H_r, H_theta, H_phi)
    
    '''
    N = len(r_array) 
    
    k = 2 * np.pi / wavelength_g
    eta = 120 * np.pi  # intrinsic impedance of free space

    for i in range(N):

        E_r = eta*(I0*dipole_length*cos_theta[i])/(2*np.pi*r_array[i]**2)*(1 + 1/(1j*k*r_array[i]))*np.e**(-1j*k*r_array[i])
        E_theta = 1j*eta*(k*I0*dipole_length*sin_theta[i])/(4*np.pi*r_array[i])*(1 + 1/(1j*k*r_array[i]) - 1/((k*r_array[i])**2))*np.e**(-1j*k*r_array[i])
        E_phi = 0

        H_r = 0
        H_theta = 0
        H_phi = 1j*(k*I0*dipole_length*sin_theta[i])/(4*np.pi*r_array[i])*(1 + 1/(1j*k*r_array[i]))*np.e**(-1j*k*r_array[i])

        E_array = np.array([E_r, E_theta, E_phi])
        H_array = np.array([H_r, H_theta, H_phi])

        E_global_cart = E_array[0]*r_hat[i] + E_array[1]*theta_hat[i] + E_array[2]*phi_hat[i]
        H_global_cart = H_array[0]*r_hat[i] + H_array[1]*theta_hat[i] + H_array[2]*phi_hat[i]

        E_cart_array.append(E_global_cart)
        H_cart_array.append(H_global_cart)

    E_cart_array = np.array(E_cart_array)
    H_cart_array = np.array(H_cart_array)
    
    E_cart_total = np.sum(E_cart_array, axis=0)
    H_cart_total = np.sum(H_cart_array, axis=0)
    
    return E_cart_array, H_cart_array, E_cart_total, H_cart_total

def local_point_relation(measure_point, antenna_point):
    '''
    
    Parameters:
    - measure_point: coordinates of the measurement point (x, y, z)
    - antenna_point: coordinates of the antenna point (x, y, z)

    Returns:
    - r_array: radial distance from the antenna to the measurement point
    - r_hat: unit vector in the radial direction
    - theta_hat: unit vector in the polar direction
    - phi_hat: unit vector in the azimuthal direction
    '''
    
    s_array, h_array, s_hat_array, h_hat_array, r_array = [], [], [], [], []
    measurement_point = np.array(measure_point)
    center = (np.array(antenna_point[:-1])+np.array(antenna_point[1:]))/2 # centering the measurement point to the antenna point
    N = len(center)

    for i in range(N):
        s = measurement_point[i] - center[i]
        h = np.array([0, 0, 1]) # dipole axis normal vector
        s_hat = s/np.linalg.norm(s)
        h_hat = h/np.linalg.norm(h)
        r = np.linalg.norm(s)

        s_array.append(s)
        h_array.append(h)
        s_hat_array.append(s_hat)
        h_hat_array.append(h_hat)
        r_array.append(r)
    
    return r_array, s_hat_array, h_hat_array, s_array, h_array

def measurement_global(s_hat, h_hat):
    '''
    Parameters:
    - s_hat: Normalized direction vector fro mthe antenna psotion to the measurement point
    - h_hat: the dipole axis normal vector
    '''

    s_hat = np.array(s_hat) # Stores all s_hat values in a numpy array
    h_hat = np.array(h_hat) # Stores all h_hat values in a numpy array

    # Equation 1.2 from the design note
    r_hat = s_hat # The radial direction is the same as the direction from the antenna to the measurement point
    phi_hat = np.cross(h_hat, s_hat)/np.linalg.norm(np.cross(h_hat, s_hat)) # Normalized cross product of h_hat and s_hat
    theta_hat = np.cross(phi_hat, s_hat)/np.linalg.norm(np.cross(phi_hat, s_hat)) # Normalized cross product of phi_hat and s_hat

    # Equation 1.3 from the design note
    R_mark = np.linalg.norm(s_hat) # Calculate the distance from the antenna to the measurement point
    sin_theta = np.linalg.norm(np.cross(h_hat, s_hat)) # Calculate the sine of the polar angle
    cos_theta = np.dot(h_hat, s_hat) # Calculate the cosine of the polar angle

    return r_hat, theta_hat, phi_hat, R_mark, sin_theta, cos_theta

def poynting_vector(E_array, H_array):
    '''
    Compute the Poynting vector from the electric and magnetic field components.

    Parameters:
    - E_array: array of electric field components in spherical coordinates (E_r, E_theta, E_phi)
    - H_array: array of magnetic field components in spherical coordinates (H_r, H_theta, H_phi)

    Returns:
    - S: Poynting vector (S_r, S_theta, S_phi)
    '''
    
    S_array = 0.5* np.real(np.cross(E_array, np.conj(H_array))) # Calculate the Poynting vector using the cross product of E and H
    return S_array

def measurement_sphere(measure_distance, num_points, plot):
    indices = np.arange(0, num_points, dtype=float) + 0.5
    phi = 2 * np.pi * indices / ((1 + np.sqrt(5)) / 2)
    theta = np.arccos(1 - 2*indices/num_points)

    X = measure_distance * np.sin(theta) * np.cos(phi)
    Y = measure_distance * np.sin(theta) * np.sin(phi)
    Z = measure_distance * np.cos(theta)
    if plot==True:
        ### Print spherical surface points
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(X, Y, Z)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.set_title('Measurement Sphere Points')

        plt.show()
        return np.stack([X, Y, Z], axis=1)

def maenderline_antenna_geometry(hertz_dipole_resolution, plot):

    C0 = 299_792_458.0
    f = 1060e6
    h_sub = 3.2e-3        # substrate height [m]  (paper: "3.2 mm" -- the abstract's "3.2cm" is a typo)
    e_r = 4.4             # substrate relative permittivity

    wavelength0 = C0 / f                     # free-space wavelength

    w_ms = C0 / (2 * f) * np.sqrt(2 / (e_r + 1))                      # eq. 11 (patch-width helper, for eps_reff only)
    e_r_eff = (e_r + 1) / 2 + (e_r - 1) / 2 * (1 + 10 * h_sub / w_ms) ** (-0.5)   # eq. 6
    wavelength_g = wavelength0 / np.sqrt(e_r_eff)  # eq. 5

    d = 0.16 * wavelength_g   # eq. 1
    s = 0.42 * wavelength_g   # eq. 2
    L = 0.70 * wavelength_g   # eq. 3 -- used ONLY in the closed-form validation below;
                              # the repeating meander unit itself is fully defined by d, s, w (eqs 1,2,4)
    w = 0.05 * wavelength_g   # eq. 4

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
        xseg, yseg = segment(p0, p1, hertz_dipole_resolution, wavelength_g)
        xs.append(xseg)                
        ys.append(yseg)

        x = np.concatenate(xs)
        y = np.concatenate(ys)

    if plot==True:
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, 'b-', linewidth=2)
        plt.title('Meander-line Antenna Geometry')
        plt.xlabel('X [m]')
        plt.ylabel('Y [m]')
        plt.axis('equal')
        plt.grid(True)
        plt.show()

    total_length = 4 * d + 4 * s
    points = np.column_stack((x, y))
    return total_length, wavelength_g, points

def coordinates(points, plot=False):
    segmentations = []
    wire_coords = np.array(points)
    h = 3.2e-3
    
    N = len(points)
    for i in range(N):
        x, y = points[i]
        z = h
        segmentations.append([x, y, z])

    segmentations = np.array(segmentations)

    if plot:
        # 3d plot
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(segmentations[:, 0], segmentations[:, 1], segmentations[:, 2])
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show(block=False)

    return np.array(segmentations)