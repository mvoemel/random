import numpy as np
import sympy as sp

def gauss_newton_d(g, Dg, lam0, tol, max_iter, pmax, damping):
    k=0
    lam=np.copy(lam0).flatten()
    increment = tol+1
    err_func = np.linalg.norm(g(lam))**2
    
    while (increment > tol and k < max_iter):
        [Q,R] = np.linalg.qr(Dg(lam))
        delta = np.linalg.solve(R,-Q.T @ g(lam)).flatten()
        
        p=0
        while p < pmax and damping == 1 and np.linalg.norm(g(lam + (delta/2**p)), 2)**2 >= np.linalg.norm(g(lam), 2)**2:
            p += 1
        if p >= pmax:
            p = 0
                       
        lam = lam + (delta / 2**p)
        err_func = np.linalg.norm(g(lam))**2
        increment = np.linalg.norm(delta / (2**p))
        k = k+1
        print('Iteration: ',k)
        print('lambda = ',lam)
        print('Inkrement = ',increment)
        print('Fehlerfunktional =', err_func)
    return(lam,k)

x = np.array([0.1, 0.3, 0.7, 1.2, 1.6, 2.2, 2.7, 3.1, 3.5, 3.9], dtype=np.float64)
y = np.array([0.558, 0.569, 0.176, -0.207, -0.133, 0.132, 0.055, -0.090, -0.069, 0.027], dtype=np.float64)
tol = 1e-5
max_iter = 30
lam0 = np.array([1, 2, 2, 1],dtype=np.float64)
tol = 1e-5

def f(x,p):
    return (p[0]*sp.exp(-p[1]*x)*sp.sin(p[2]*x+p[3]))

p = sp.symbols('p:{n:d}'.format(n=lam0.size))
g = sp.Matrix([y[k]-f(x[k],p) for k in range(len(x))])
Dg = g.jacobian(p)

g = sp.lambdify([p], g, 'numpy')
Dg = sp.lambdify([p], Dg, 'numpy')


tol = 1e-5
max_iter = 30
pmax = 5
damping = 1
[lam_with,n] = gauss_newton_d(g, Dg, lam0, tol, max_iter, pmax, damping)
