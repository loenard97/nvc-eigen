import scipy
import numpy as np

from nvceigen.vector import Vector3D
from nvceigen.util import deg_to_rad
from nvceigen.units import MHz, G


class HSolver:

    def __init__(self, **kwargs):
        """
        NV Hamiltonian solver.
        Constants E, G and g can be set individually through kwargs.
        """
        self.E = 5
        self.D = 2870
        self.g = 2.8

        allowed_keys = {'E', 'D', 'g'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def solve_energy_levels(self, B_field: Vector3D):
        """
        Get Energy Levels from B-field shift
        :param Vector3D B: B-field vector along NV axis in G
        :returns: Energy levels in MHz, sorted ascending
        """
        D, E, g = self.D, self.E, self.g
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

    def solve_resonances(self, B_field: Vector3D):
        """
        Get resonances from B-field vector
        :param B_field Vector3D: B-field vector
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
            E1, E2, E3 = self.solve_energy_levels(B_NV_1)
            resonances.append(E3 - E1)
            resonances.append(E2 - E1)
        
        return np.sort(resonances)

    def resonance_error_function(self, B_field, *freq_meas) -> float:
        """
        Error function between measured and calculated resonances
        """
        freq_calc = self.solve_resonances(Vector3D(*B_field))
        return np.sum([np.power(f_meas - f_calc, 2) for f_meas, f_calc in zip(freq_meas, freq_calc)])

    def solve_b_field(self, resonances, B_estimate):
        """
        Find B-field Vector from given resonances
        :param list resonances: Measured frequencies in MHz
        :param Vector3D B_estimate: Initial B-field estimate
        """
        # convert freq_meas to tuple first. somehow doesn't work as list? don't know why. probably mutability bs again.
        result = scipy.optimize.minimize(self.resonance_error_function, x0=[*B_estimate], args=tuple(resonances))
        return Vector3D(*result.x)
