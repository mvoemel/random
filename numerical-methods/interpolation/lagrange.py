import numpy as np
from scipy.interpolate import lagrange

# USAGE

# Given points
x = np.array([0, 250, 500, 1000])
w = np.array([1013, 747, 540, 226])

poly = lagrange(x, w)

print(poly(375))
