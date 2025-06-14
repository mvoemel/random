import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x, y, z = sp.symbols('x y z')
f1 = x**2 + y - 3 * z

print(f1)

h = f1.subs([(x, 1), (y, 2), (z, 3)])
print(h.evalf())
print(sp.diff(f1, y))

# Use this args in [] to call it with an array.
f = sp.lambdify([(x, y, z)], f1, 'numpy')
print(f(np.array([1, 2, 3])))

# Use this without [] to call it normally
f = sp.lambdify((x,y,z), f1, 'numpy')
print(f(1,2,3))


