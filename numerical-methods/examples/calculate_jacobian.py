import autograd.numpy as np
import sympy as sp
from autograd import grad, jacobian

def fun(x):
    return np.array([
        5 * x[0] * x[1],
        x[0] ** 2 * x[1] ** 2 + x[0] + 2 * x[1]
    ])

# With autograd
df = jacobian(fun)(np.array([1, 2], dtype=float))
print(df)

# With sympy

x, y, z = sp.symbols('x y z')

# Define function expressions
f1 = x**2 + y - 3*z
f2 = sp.exp(y) - sp.sin(z)

f = sp.Matrix([f1, f2])
print(f)

X = sp.Matrix([x, y, z])

Df = f.jacobian(X)

print(X)
print(Df)

Df0 = Df.subs([(x, 3), (y, 4), (z, 5)])
print(Df0)
print(Df0.evalf())


