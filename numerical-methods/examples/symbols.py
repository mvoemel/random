import numpy as np
import sympy as sp

# Create the symbols
x, y, z = sp.symbols('x y z')

# Define a variable representing a function
f1 = x**2 + y - 3 * z

print(f1)

# Substitute values for these symbols
h = f1.subs([(x, 1), (y, 2), (z, 3)])

# Evaluate the expression
print(h.evalf())

# Differentiate a function expression
print(sp.diff(f1, y))

# Convert for computing values of the expression (Bridging to numpy)

# Use this args in [] to call it with an array.
f = sp.lambdify([(x, y, z)], f1, 'numpy')
print(f(np.array([1, 2, 3])))

# Use this without [] to call it normally
f = sp.lambdify((x,y,z), f1, 'numpy')
print(f(1,2,3))


