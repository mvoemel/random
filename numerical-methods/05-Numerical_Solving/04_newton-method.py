import numpy as np
import sympy as sp

def newton_method(f, x, x0, tol=1e-6, max_iter=100):
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

        # Update the current point
        x0 = x0 + delta_x

        # Compute the norm of the function value
        fnorm = np.linalg.norm(f_subs, 2)
        if fnorm <= tol: return x0, fnorm, k

        k += 1
    return x0, fnorm, k


# Example usage
x, y = sp.symbols('x y')
c = 1
f1 = c*x + y - 4
f2 = x**2 + y**2 - 9
f = [f1, f2]
x0 = [0, 3]
symbols = [x, y]

sqrt_part = np.sqrt(9*c**2 - 7)
x_exact = (4*c - sqrt_part) / (c**2 + 1)
y_exact = (c * sqrt_part - 4 * c**2) / (c**2 + 1) + 4
exact = np.array([x_exact, y_exact])

xn, fnorm, k = newton_method(f, symbols, x0, tol=1e-4, max_iter=100)
print("Result:")
print(k)
print(xn)
