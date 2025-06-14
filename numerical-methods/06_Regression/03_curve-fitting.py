import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def error_functional(p, f, x, y):
    yy = np.array([sum(p[j] * f[j](xv) for j in range(len(f))) for xv in x])
    return sum((y - yy)**2)

def plot_curve_fitting(x, y, xx, yy):
    """
    plot_curve_fitting - plots the original data points and the fitted curve
    Args:
        x (numpy.ndarray): The x values for the data points.
        y (numpy.ndarray): The y values for the data points.
        xx (numpy.ndarray): The x values for the fitted curve.
        yy (numpy.ndarray): The y values for the fitted curve.
    """
    plt.scatter(x, y, color='red', label='Data points')
    plt.plot(xx, yy, label='Fitted curve')
    plt.title("Curve Fitting")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()

def build_A(f, x):
    """
    build_A - builds the matrix A for the curve fitting problem
    Matrix A holds all function values for each point in T.
    Returns:
        A (numpy.ndarray): The matrix A for the curve fitting problem.
    """
    A = np.empty((0, len(f)))
    for i in range(len(x)):
        row = np.array([f[j](x[i]) for j in range(len(f))])
        A = np.vstack((A, row))
    return A

def curve_fitting(f, x, y, xx, g=True, non_qr=True):
    """
    curve_fitting - performs curve fitting using the least squares method
    Args:
        f (list): List of functions to fit.
        x (numpy.ndarray): The x values for the data points.
    Returns:
        p (numpy.ndarray): The coefficients of the fitted polynomial.
    """
    A = build_A(f, x)

    if not non_qr: 
        Q, R = np.linalg.qr(A)
        p = np.linalg.solve(R, Q.T @ y)
    else:
        p = np.linalg.solve(A.T @ A, A.T @ y)

    yy = np.array([sum(p[j] * f[j](xv) for j in range(len(f))) for xv in xx])
    if g:
        plot_curve_fitting(x, y, xx, yy)
    return p


xi = [0, 1, 2, 3, 4]
yi = [6, 12, 30, 80, 140]
x = sp.symbols('x')
f = [x**2, x]
f = [sp.lambdify(x, func) for func in f]
xx = np.linspace(xi[0], xi[-1], 500)

p = curve_fitting(f, xi, yi, xx)
