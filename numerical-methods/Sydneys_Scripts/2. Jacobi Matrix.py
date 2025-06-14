
import sympy as sp
import numpy as np
x, y, z = sp.symbols('x y z')


# Zwei dimensional
f1 = 5*x*y
f2 = x**2*y**2+x+2*y

f = sp.Matrix([f1,f2])
X = sp.Matrix([x,y])

#Algemeine Jacobi Matrix
Df = f.jacobian(X)
print(Df)

#Berechnung mit eingesetzten Werten
Df0 = Df.subs([(x,1),(y,2)])
print(Df0)
#oder mit numpy
numpy_f = sp.lambdify([([x],[y])], Df, "numpy")
print(numpy_f([[1],[2]]))


#Drei dimensional
"""
f1 = sp.ln(x**2+y**2)+z**2
f2 = sp.exp(y**2+z**2)+x**2
f3 = 1/(z**2+x**2)+y**2

f = sp.Matrix([f1,f2,f3])
X = sp.Matrix([x,y,z])

#Algemeine Jacobi Matrix
Df = f.jacobian(X)
print(Df)
numpy_f = sp.lambdify([([x],[y],[z])], Df, "numpy")
#Berechnung mit eingesetzten Werten
Df0 = Df.subs([(x,1),(y,2),(z,3)])
print(Df0)
#oder mit numpy
print(numpy_f([[1],[2],[3]]))
"""
