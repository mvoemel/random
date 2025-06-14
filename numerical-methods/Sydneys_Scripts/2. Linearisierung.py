import sympy as sp
import numpy as np
x, y, z = sp.symbols('x y z')

f1 = x+y**2-z**2-13
f2 = sp.ln(y/4)+sp.exp(0.5*z-1)-1
f3 = (y-3)**2-z**3+7


f = sp.Matrix([f1,f2,f3])
X = sp.Matrix([x,y,z])
Df = f.jacobian(X)

#Startwert f(x0)
f_x0 = f.subs([(x,1.5),(y,3),(z,2.5)])
#print(f_x0.evalf()) # evalf() berechnet als float

#Jacobi an Stelle x0: Df(x0)
Df0 = Df.subs([(x,1.5),(y,3),(z,2.5)])

x0 = sp.Matrix([1.5,3,2.5])
vec = sp.Matrix([x,y,z])

# Linearisierugsgleichung aufstellen: g(x) = f(x0) + Df(x0)*(x-x0)
g = f_x0+Df0*(vec-x0)

numpy_g = sp.lambdify([([x],[y],[z])], g, "numpy")
print(numpy_g(np.array([[1],[-1],[0]]))) # Auswertung der Funktion an der Stelle 1,-1,0
