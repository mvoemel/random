import sympy as sp
import numpy as np
from newton.functions import dampened_newton

def task1():
    x1, x2 = sp.symbols("x1 x2")
    f1 = 20 - 18 * x1 - 2 * x2 ** 2
    f2 = -4 * x2 * (x1 - x2 ** 2)

    f = sp.Matrix([f1, f2])

    Df = f.jacobian(sp.Matrix([x1, x2]))
    Df = sp.lambdify([(x1, x2)], Df, 'numpy')
    f = sp.lambdify([(x1, x2)], f, 'numpy')

    max_iter = 3
    curr_iter = 0
    x_current = np.array([1.1, 0.9])
    x_iterations = [x_current]

    while curr_iter < max_iter:
        curr_iter += 1
        Df_current = Df(x_current)
        f_current = f(x_current)
        delta = np.linalg.solve(Df_current, -f_current).flatten()
        x_current = x_current + delta
        x_iterations.append(x_current)

    print(x_iterations)


def task2():
    x, y = sp.symbols('x y')
    f1 = x**2 / 186**2 - y**2 / (300**2 - 186**2) - 1
    f2 = (y - 500)**2 / 279**2 - (x - 300)**2 / (500**2 - 279**2) - 1

    p1 = sp.plot_implicit(sp.Eq(f1, 0), (x, -2000, 2000), (y, -2000, 2000), show=False)
    p2 = sp.plot_implicit(sp.Eq(f2, 0), (x, -2000, 2000), (y, -2000, 2000), show=False)

    f = sp.Matrix([f1, f2])
    func = sp.lambdify([x, y], f, 'numpy')
    #newton_system(f, )

    p1.append(p2[0])
    p1.show()


def task3():
    x1, x2, x3 = sp.symbols("x1 x2 x3")
    f1 = x1 + x2 ** 2 - x3 ** 2 - 13
    f2 = sp.ln(x2 / 4) + sp.E ** (0.5*x3-1) - 1
    f3 = (x2 - 3) ** 2 - x3 ** 3 + 7

    f = sp.Matrix([f1, f2, f3])

    x0 = np.array([ [1.5], [3], [2.5]], dtype=np.float64)
    Df = f.jacobian(sp.Matrix([x1, x2, x3]))
    print(dampened_newton(f, Df, [x1, x2, x3], x0, 1e-5))



#task1()
#task2()
task3()