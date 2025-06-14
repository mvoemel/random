import sympy as sp
import autograd.numpy as np
from autograd import grad, jacobian

# Task 1
# def f(x):
#     return np.array([
#         5 * x[0] * x[1],
#         x[0] ** 2 * x[1] ** 2 + x[0] + 2 * x[1]
#     ])
#
# df = jacobian(f)(np.array([1, 2], dtype=float))
# print(df)

# Task 2

x1, x2, x3 = sp.symbols('x1 x2 x3')

f1 = x1 + x2 ** 2 - x3 ** 2 - 13
f2 = sp.ln(x2 / 4) + sp.E ** (0.5 * x3 - 1) - 1
f3 = (x2 - 3) ** 2 - x3 ** 3 + 7

f = sp.Matrix([f1, f2, f3])

X = sp.Matrix([x1, x2, x3])
Df = f.jacobian(X)
print(Df)

f0 = f.subs([(x1, 1.5), (x2, 3), (x3, 2.5)])

Df0 = Df.subs([(x1, 1.5), (x2, 3), (x3, 2.5)])

print(Df0)

result = f0 + Df0 @ sp.Matrix([x1 - 1.5, x2 - 3, x3 - 2.5])

print(result)




