import numpy as np
import matplotlib.pyplot as plt



def euler_method(f, xi, yi, h):
    return yi + h * f(xi, yi)

def middle_point_method(f, xi, yi, h):
    x_h2 = xi + (h / 2)
    y_h2 = yi + (h / 2) * f(xi, yi)
    yin = yi + h * f(x_h2, y_h2)
    return yin

def mod_euler_method(f, xi, yi, h, xin):
    y_euler_in = yi + h * f(xi, yi)
    k1 = f(xi, yi)
    k2 = f(xin, y_euler_in)
    yin = yi + h * ((k1 + k2) / 2)
    return yin

    

def solve_ivp(f, a, b, n, y0):
    """
    This function solve the initial value problem for function f.
    It calculates the respective values with three different methods:
    1. Euler method
    2. Middle point method
    3. modified Euler method
    
    Paramters:
    f: function to solve
    a: start point
    b: end point
    n: number of steps
    y0: initial value
    
    Return:
    x: list of x values
    y_euler: list of y values calculated with Euler method
    y_middle_point: list of y values calculated with middle point method
    y_mod_euler: list of y values calculated with modified Euler method
    """
    h = (b - a) / n
    xi = a
    y_euler_i, y_middle_point_i, y_mod_euler_i = y0, y0, y0
    x, y_euler, y_middle_point, y_mod_euler = [], [], [], []

    x.append(xi)
    y_euler.append(y_euler_i)
    y_middle_point.append(y_middle_point_i)
    y_mod_euler.append(y_mod_euler_i)
    for _ in range(n):
        xin = xi + h
        y_euler_in = euler_method(f, xi, y_euler_i, h)
        y_euler.append(y_euler_in)

        y_middle_point_in = middle_point_method(f, xi, y_middle_point_i, h)
        y_middle_point.append(y_middle_point_in)

        y_mod_euler_in = mod_euler_method(f, xi, y_mod_euler_i, h, xin)
        y_mod_euler.append(y_mod_euler_in)
        x.append(xin)

        xi = xin
        y_euler_i = y_euler_in
        y_middle_point_i = y_middle_point_in
        y_mod_euler_i = y_mod_euler_in
        
    
    return x, y_euler, y_middle_point, y_mod_euler


a = -1.5
b = 1.5
y0 = 0
n = 5

fprime = lambda t, y: t**2 + 0.1 * y
f = lambda t: -10 * t**2 - 200 * t - 2000 + 1722.5 * np.exp(0.05*(2*t+3))

x = np.linspace(-1.5, 1.5)

x_m, y_euler, y_middle_point, y_mod_euler = solve_ivp(fprime, a, b, n, y0)

plt.plot(x_m, y_euler)
plt.plot(x_m, y_middle_point)
plt.plot(x_m, y_mod_euler)
plt.plot(x, f(x))
plt.title("Euler method vs. middle point method vs. modified Euler method")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["Euler method", "Middle point method", "Modified Euler method", "Exact solution"])
plt.show()
