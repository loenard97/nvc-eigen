import numpy as np


def rad_to_deg(angle):
    """
    Convert radians to degrees
    """
    return 360 / (2*np.pi) * angle


def deg_to_rad(angle):
    """
    Convert degrees to radians
    """
    return 2*np.pi / 360 * angle
