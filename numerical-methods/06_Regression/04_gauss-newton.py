import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def gauss_newton(g, Dg, lam0, tol, max_iter):
    """
    gauss_newton - Performs the Gauss-Newton optimization method.
    Args:
        g (function): Residual function.
        Dg (function): Jacobian of the residual function.
        lam0 (numpy.ndarray): Initial guess for parameters.
        tol (float): Tolerance for convergence.
        max_iter (int): Maximum number of iterations.
    Returns:
        lam (numpy.ndarray): Optimized parameters.
        k (int): Number of iterations performed.
    """
    k = 0
    lam = np.copy(lam0)
    increment = tol + 1
    err_func = np.linalg.norm(g(lam))**2

    while increment > tol and k < max_iter:
        Q, R = np.linalg.qr(Dg(lam))
        delta = np.linalg.solve(R, -Q.T @ g(lam)).flatten()

        lam = lam + delta
        err_func = np.linalg.norm(g(lam))**2
        increment = np.linalg.norm(delta)
        k += 1
    return lam, k, err_func

def generic_curve_fitting(x, y, f, lam0, tol=1e-5, max_iter=30):
    """
    generic_curve_fitting - Sets up and solves a curve fitting problem using Gauss-Newton.
    Args:
        x (numpy.ndarray): Data points for x.
        y (numpy.ndarray): Data points for y.
        f (function): Model function to fit.
        lam0 (numpy.ndarray): Initial guess for parameters.
        tol (float): Tolerance for convergence.
        max_iter (int): Maximum number of iterations.
    Returns:
        lam (numpy.ndarray): Optimized parameters.
        k (int): Number of iterations performed.
    """
    p = sp.symbols('p:{n:d}'.format(n=lam0.size))

    g = sp.Matrix([y[i] - f(x[i], p) for i in range(len(x))])
    Dg = g.jacobian(p)

    g = sp.lambdify([p], g, 'numpy')
    Dg = sp.lambdify([p], Dg, 'numpy')

    # Solve using Gauss-Newton
    return gauss_newton(g, Dg, lam0, tol, max_iter)

x = np.array([25, 35, 45, 55, 65], dtype=np.float64)
y = np.array([47, 114, 223, 81, 20], dtype=np.float64)
lam0 = np.array([10**8, 50, 600], dtype=np.float64)

f = lambda x, p: p[0] / ((x**2 - p[1]**2)**2 + p[2]**2)

lam, iterations, err_func = generic_curve_fitting(x, y, f, lam0)