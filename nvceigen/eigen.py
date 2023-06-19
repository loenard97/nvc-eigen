import scipy
import numpy as np

from vector import Vector3D
from util import deg_to_rad


def odmr_fit_func(x, c, a1, w1, f1, a2, w2, f2, a3, w3, f3, a4, w4, f4, a5, w5, f5, a6, w6, f6, a7, w7, f7, a8, w8, f8):
    """
    8 Lorentzian peaks
    """
    return c - \
           a1 * w1 / (4 * (x - f1) ** 2 + w1 ** 2) - \
           a2 * w2 / (4 * (x - f2) ** 2 + w2 ** 2) - \
           a3 * w3 / (4 * (x - f3) ** 2 + w3 ** 2) - \
           a4 * w4 / (4 * (x - f4) ** 2 + w4 ** 2) - \
           a5 * w5 / (4 * (x - f5) ** 2 + w5 ** 2) - \
           a6 * w6 / (4 * (x - f6) ** 2 + w6 ** 2) - \
           a7 * w7 / (4 * (x - f7) ** 2 + w7 ** 2) - \
           a8 * w8 / (4 * (x - f8) ** 2 + w8 ** 2)


def resonances(B_field: Vector3D):
    """
    Calculate resonances from B-field vector
    """
    resonances = []

    # rotate B_field onto each NV axis
    x_angle  = 54.735610317245350
    y_angle  = 45
    y_angles = [ x_angle,    180 - x_angle,  -x_angle,   -180 + x_angle ]
    z_angles = [ y_angle,    -y_angle,       y_angle,    -y_angle       ]

    # calculate energy levels for each NV axis
    for y_angle, z_angle in zip(y_angles, z_angles):
        y_angle = deg_to_rad(y_angle)
        z_angle = deg_to_rad(z_angle)
        B_NV_1 = B_field.rotate_axis('z', z_angle).rotate_axis('y', y_angle)
        E1, E2, E3 = energy_levels(B_NV_1)
        resonances.append(E3 - E1)
        resonances.append(E2 - E1)
    
    return resonances


def energy_levels(B_field: Vector3D):
    """
    Get Energy Levels from B-field shift
    :param Vector3D B: B-field vector along NV axis in G
    :returns: Energy levels in MHz, sorted ascending
    """
    E = 5       # MHz
    D = 2870    # MHz
    g = 2.8     # MHz / G
    rsqrt2 = 1 / np.sqrt(2)

    Hss = np.array([        # Spin-Spin Hamiltonian
        [ D, 0, E ], 
        [ 0, 0, 0 ], 
        [ E, 0, D ], 
    ])
    Hz = np.array([         # B-field Hamiltonian
        [ B_field.z,                            rsqrt2*(B_field.x + 1j*B_field.y),      0                                 ], 
        [ rsqrt2*(B_field.x - 1j*B_field.y),    0,                                      rsqrt2*(B_field.x + 1j*B_field.y) ], 
        [ 0,                                    rsqrt2*(B_field.x - 1j*B_field.y),      -B_field.z                        ], 
    ])
    Hamiltonian = Hss + g*Hz

    eigen_val, _ = np.linalg.eig(Hamiltonian)     # returns eigen values and eigen vectors
    eigen_val = np.abs(eigen_val)

    return np.sort(eigen_val)


def resonance_error_function(B_field, *freq_meas) -> float:
    """
    Error function between measured and calculated resonances
    """
    freq_calc = resonances(Vector3D(*B_field))
    return np.sum([np.power(f_meas - f_calc, 2) for f_meas, f_calc in zip(freq_meas, freq_calc)])


def find_b_field(B_estimate, freq_meas) -> Vector3D:
    """
    Find B-field Vector
    :param Vector3D B_estimate: Initial B-field estimate
    :param list freq_meas: Measured frequencies in MHz
    """
    # convert freq_meas to tuple first. somehow doesn't work as list? don't know why. probably mutability bs again.
    result = scipy.optimize.minimize(resonance_error_function, x0=[*B_estimate], args=tuple(freq_meas))
    print(result)
    return Vector3D(*result.x)
