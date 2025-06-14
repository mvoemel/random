import sympy as sp
import numpy as np

def linearize(f_sym, vars, x0):
    """
    Returns the linear approximation g(x) ≈ f(x₀) + Df(x₀) · (x - x₀) of a vector-valued function f around a point x₀.

    Parameters:
        f_sym (sp.Matrix): The symbolic vector-valued function to linearize.
        vars (list): The list of sympy symbols representing the input variables.
        x0 (np.ndarray): The point around which to linearize, given as a NumPy array.

    Returns:
        function: A function g(x) that computes the linearized approximation at a new point x.
    """
    J = f_sym.jacobian(vars)
    f_func = sp.lambdify([vars], f_sym, 'numpy')
    J_func = sp.lambdify([vars], J, 'numpy')

    f_x0 = f_func(x0)
    J_x0 = J_func(x0)

    def g(x):
        return f_x0 + J_x0 @ sp.Matrix([xi - x0i for xi, x0i in zip(x, x0)])

    return g


"""
How to use:
x1, x2, x3 = sp.symbols('x1 x2 x3')
f1 = sp.sin(x2 + 2 * x3)
f2 = sp.cos(2 * x1 + x2)
f_sym = sp.Matrix([f1, f2])
x_0 = np.array([np.pi / 4, 0, np.pi])

g = linearize(f_sym, [x1, x2, x3], x_0)
print(g([x1, x2, x3]))
"""