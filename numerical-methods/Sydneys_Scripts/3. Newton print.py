# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:44:00 2021

"""

import sympy as sp
import numpy as np

#Symbolic part
x1,x2 = sp.symbols("x1 x2")
x = sp.Matrix([x1,x2])

# Gegeben:
f1 = 20-18*x1-2*x2**2
f2 = -4*x2*(x1-x2**2)
x0 = np.array([[1.1],[0.9]])

f = sp.Matrix([f1,f2])
Df = f.jacobian(x)

print("f:\n",f,"\n")
print("Df:\n",Df,"\n")

# Numerical part
f = sp.lambdify([([x1],[x2])], f, "numpy")
Df = sp.lambdify([([x1],[x2])], Df, "numpy")

def newt(x, nmax):
    n=0
    print("x0 =\n",x)
    while n < nmax:
        
        print("\nn =",n,":")
        print("D(x) =\n", Df(x))
        print("f(x) =\n", f(x))
        print("Df(x)*δ = -f(x) nach δ auflösen")
        delta = np.linalg.solve(Df(x), -f(x))
        print("δ =\n",delta)
        xold = x
        x = x + delta
        print("x(n+1) = xn + δ =\n",x)
        
        #Zusätzlich werden die folgenden 2-Norme berechnet
        print("\n2-Norm f(x(n)) =\n", np.linalg.norm(f(x)))
        print("2-Norm x(n+1)-x(n) =\n", np.linalg.norm(x-xold))
        n+=1
        
newt(x0, 2)
