import numpy as np
import sympy as sp

# Define symbols
x1, x2, x3 = sp.symbols('x1 x2 x3')

# Define individual functions f1, f2, ...fn
f1 = sp.sin(x2 + 2 * x3)
f2 = sp.cos(2 * x1 + x2)

#...

# Define vector valued function f
f_sym = sp.Matrix([f1, f2])
print(f"Function f: {f_sym}")

# Setup jacobian matrix Df
Df_sym = f_sym.jacobian((x1, x2, x3))
print(f"Jacobian Df: {Df_sym}")

# Define start vector
x_0 = np.array([np.pi / 4, 0, np.pi])

# Compute f with start vector x_0
f_func = sp.lambdify([(x1, x2, x3)], f_sym, 'numpy')
fx_0 = f_func(x_0)

print(f"Vector fx_0: {fx_0}")

# Compute Df with stat vector x_0
Df_func = sp.lambdify([(x1, x2, x3)], Df_sym, 'numpy')
Dfx_0 = Df_func(x_0)

print(f"Matrix Dfx_0: {Dfx_0}")

# General tangent equation

def g(x):
    return fx_0 + Dfx_0 @ sp.Matrix([x[0] - x_0[0], x[1] - x_0[1], x[2] - x_0[2]])

print(g([x1, x2, x3]))



