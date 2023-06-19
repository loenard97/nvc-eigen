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
