import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

def task1():
    x = np.array([0, 2500, 5000, 10000])
    w = np.array([1013, 747, 540, 226])

    poly = lagrange(x, w)

    print(poly(3750))

def task2():
    x_vals = np.array([1981, 1984, 1989, 1993, 1997, 2000, 2001, 2003, 2004, 2010])
    y_vals = np.array([0.5, 8.2, 15, 22.9, 36.6, 51, 56.3, 61.8, 65, 76.7])
    poly = Polynomial.fit(x_vals, y_vals, 4)

    xAxis = np.arange(1975, 2020, 0.1)
    poly_std = poly.convert()


    plt.scatter(x_vals, y_vals)
    plt.plot(xAxis, poly_std(xAxis))
    plt.ylim(-100, 250)
    plt.show()

task2()





