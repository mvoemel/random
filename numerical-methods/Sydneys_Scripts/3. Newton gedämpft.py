import sympy as sp
import numpy as np

#Symbolic part
x1,x2,x3 = sp.symbols("x1 x2 x3")
x = sp.Matrix([x1,x2,x3])

# Konvergiert nur mit Dämpfung 0 und 1
f1 = x1+x2**3-x3**3-13
f2 = sp.log(x2/4)+sp.exp(x3**2-1)-1
f3 = (x2-3)**3-x3**3+7

f = sp.Matrix([f1,f2,f3])

Df = f.jacobian(x)

# Numerical part
f = sp.lambdify([([x1],[x2],[x3])], f, "numpy")
Df = sp.lambdify([([x1],[x2],[x3])], Df, "numpy")

def newtDamp(x,k, nmax, tol):
    n=0
    while n<nmax and tol<np.linalg.norm(f(x)):
        n+=1
        xcopy = np.copy(x) # copy für Dämpfung
        δ = np.linalg.solve(Df(x), -f(x))
        x = x + δ
        
        # Dämpfung        
        i=0
        while i<=k and np.linalg.norm(f(xcopy+δ))>np.linalg.norm(f(xcopy)):
            i+=1
            δ /= 2           
        if i!=k+1 and i!=0:
            x = xcopy + δ   
            print("damping effective")
                
    print("number of iterations:",n)
    return x
        
nmax=100
k = 2 #Anzahl Dampingschritte ca. 4. Bei k=0 ist das Dämpfen ausgeschaltet
x0 = np.array([[3],[3],[2.5]])
xn = newtDamp(x0,k, nmax, 1e-5)
print("xn =\n", xn)
print("f(xn) =\n",f( xn))





