import sympy as sp
import numpy as np

#Symbolic part
x1,x2 = sp.symbols("x1 x2")
x = sp.Matrix([x1,x2])

f1 = x1**2/186**2-x2**2/(300**2-186**2)-1
f2 = (x2-500)**2/279**2-(x1-300)**2/(500**2-279**2)-1

f = sp.Matrix([f1,f2])

Df = f.jacobian(x)

print("f:\n",f,"\n")
print("Df:\n",Df,"\n")

# Numerical part
f = sp.lambdify([([x1],[x2])], f, "numpy")
Df = sp.lambdify([([x1],[x2])], Df, "numpy")

def newt(x, nmax, tol):
    n=0
    while n<nmax and tol<np.linalg.norm(f(x)):
        n+=1
        delta = np.linalg.solve(Df(x), -f(x))        
        x = x + delta        
    return x
        
nmax = 100
x0 = np.array([[-1300],[1600]])
print(newt(x0, nmax, 1e-5))





