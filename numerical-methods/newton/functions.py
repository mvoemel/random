import numpy as np
import sympy as sp

def quadratic_newton(f_sym, Df_sym, vars, x0, tol=1e-5, max_iter=100):
    """
    Generic Newton-Raphson method for systems of nonlinear equations.

    Parameters:
        f_sym (sp.Matrix): Symbolic function vector.
        Df_sym (sp.Matrix): Symbolic Jacobian of f.
        vars (list): List of sympy symbols [x1, x2, ..., xn].
        x0 (np.ndarray): Initial guess (n x 1 array).
        tol (float): Convergence tolerance.
        max_iter (int): Maximum number of iterations.

    Returns:
        np.ndarray: Approximate solution.
    """
    xk = x0.copy()

    for _ in range(max_iter):
        subs = {vars[i]: xk[i, 0] for i in range(len(vars))}
        fk = np.array(f_sym.subs(subs), dtype=np.float64)
        Df_eval = np.array(Df_sym.subs(subs), dtype=np.float64)

        delta = np.linalg.solve(Df_eval, -fk)
        xk = xk + delta.reshape(-1, 1)

        if np.linalg.norm(fk, 2) < tol:
            break

    return xk

def simple_newton(f_sym, Df_sym, vars, x0, tol=1e-5, max_iter=100):
    """
    Simplified Newton-Raphson method for systems of nonlinear equations.
    The Jacobian is evaluated once at the initial guess.

    Parameters:
        f_sym (sp.Matrix): Symbolic function vector.
        Df_sym (sp.Matrix): Symbolic Jacobian of f.
        vars (list): List of sympy symbols [x1, x2, ..., xn].
        x0 (np.ndarray): Initial guess (n x 1 array).
        tol (float): Convergence tolerance.
        max_iter (int): Maximum number of iterations.

    Returns:
        np.ndarray: Approximate solution.
    """
    xk = x0.copy()
    Df_eval = np.array(Df_sym.subs({vars[i]: x0[i, 0] for i in range(len(vars))}), dtype=np.float64)

    for _ in range(max_iter):
        subs = {vars[i]: xk[i, 0] for i in range(len(vars))}
        fk = np.array(f_sym.subs(subs), dtype=np.float64)

        delta = np.linalg.solve(Df_eval, -fk)
        xk = xk + delta.reshape(-1, 1)

        if np.linalg.norm(fk, 2) < tol:
            break

    return xk

def dampened_newton(f_sym, Df_sym, vars, x0, tol=1e-5, max_iter=100):
    """
    Dampened Newton-Raphson method for systems of nonlinear equations.
    Uses a line search to choose an appropriate step size to ensure descent.

    Parameters:
        f_sym (sp.Matrix): Symbolic function vector.
        Df_sym (sp.Matrix): Symbolic Jacobian of f.
        vars (list): List of sympy symbols [x1, x2, ..., xn].
        x0 (np.ndarray): Initial guess (n x 1 array).
        tol (float): Convergence tolerance.
        max_iter (int): Maximum number of iterations.

    Returns:
        np.ndarray: Approximate solution.
    """
    xk = x0.copy()

    def find_minimal_k(xk, delta):
        for k in range(1000):
            trial_x = xk + delta.reshape(-1, 1) / (2 ** k)
            subs_trial = {vars[i]: trial_x[i, 0] for i in range(len(vars))}
            subs_current = {vars[i]: xk[i, 0] for i in range(len(vars))}
            residual_k = np.array(f_sym.subs(subs_trial), dtype=np.float64)
            residual = np.array(f_sym.subs(subs_current), dtype=np.float64)
            if np.linalg.norm(residual_k, 2) < np.linalg.norm(residual, 2):
                return k
        return 0

    for _ in range(max_iter):
        subs = {vars[i]: xk[i, 0] for i in range(len(vars))}
        fk = np.array(f_sym.subs(subs), dtype=np.float64)
        Df_eval = np.array(Df_sym.subs(subs), dtype=np.float64)

        delta = np.linalg.solve(Df_eval, -fk)
        k = find_minimal_k(xk, delta)
        xk = xk + delta.reshape(-1, 1) / (2 ** k)

        if np.linalg.norm(fk, 2) < tol:
            break

    return xk


#USAGE EXAMPLE NEWTON:

"""
x, y = sp.symbols('x y')
f1 = x**2/186**2 - y**2/(300**2 - 186**2) - 1
f2 = (y-500)**2/279**2 - (x-300)**2/(500**2-279**2) - 1

f = sp.Matrix([f1, f2])
Df = f.jacobian(sp.Matrix([x, y]))

s1 = np.array([ [240], [216] ], dtype=np.float64)
s2 = np.array([ [740], [900] ], dtype=np.float64)
s3 = np.array([ [-1270], [1600] ], dtype=np.float64)
s4 = np.array([ [-200], [70] ], dtype=np.float64)

print(simple_newton(f, Df, [x, y], s1, 10 ** -5, 10))
"""