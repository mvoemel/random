import numpy as np
import sympy as sp


def damping_factor(x, x0, M_f, f_subs, delta_x):
    alpha = 1.0
    while True:
        new_x0 = x0 + alpha * delta_x
        new_f_subs = np.array(M_f.subs(dict(zip(x, new_x0))).evalf(), dtype=np.float64).flatten()
        if np.linalg.norm(new_f_subs, 2) < np.linalg.norm(f_subs, 2):
            break
        alpha *= 0.5
    return new_x0,new_f_subs

def damped_newton_method(f, x, x0, tol=1e-6, max_iter=100):
    """
    Damped Newton method for solving non-linear equations.
    Params:
        f: A vector function (list or matrix).
        x: A vector of variables (list or matrix).
        x0: Initial guess (list or array).
        tol: Tolerance for convergence.
        max_iter: Maximum number of iterations.
    """
    M_f = sp.Matrix(f)
    M_x = sp.Matrix(x)
    J = M_f.jacobian(M_x)
    x0 = np.array(x0, dtype=np.float64)  # Convert initial guess to NumPy array
    fnorm = 1 + tol
    k = 0

    while fnorm > tol and k < max_iter:
        # Compute the function value at the current point
        f_subs = np.array(M_f.subs(dict(zip(x, x0))).evalf(), dtype=np.float64).flatten()

        # Compute the Jacobian matrix at the current point
        J_subs = np.array(J.subs(dict(zip(x, x0))).evalf(), dtype=np.float64)

        # Solve for the Newton step
        delta_x = -np.linalg.solve(J_subs, f_subs)

        # Damping factor
        new_x0, new_f_subs = damping_factor(x, x0, M_f, f_subs, delta_x)

        # Update the current point
        x0 = new_x0

        # Compute the norm of the function value
        fnorm = np.linalg.norm(new_f_subs, 2)

        k += 1

    return x0, fnorm, k

# Example usage
x1, x2, x3 = sp.symbols('x1 x2 x3')
f1 = x1 + x2**2 - x3**2 - 13
f2 = sp.ln(x2 / 4) + sp.exp(0.5*x3 - 1) - 1
f3 = (x2 - 3)**2 - x3**3 + 7

f = [f1, f2, f3]
x0 = [1.5, 3, 2.5]
symbols = [x1, x2, x3]

xn, fnorm, k = damped_newton_method(f, symbols, x0, tol=1e-6, max_iter=100)
print("Result:")
print(xn)
