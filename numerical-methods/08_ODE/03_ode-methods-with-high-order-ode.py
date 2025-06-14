import matplotlib.pyplot as plt
import numpy as np

def middle_point_method(f, xi, yi, h):
    k1 = f(xi, yi)
    k2 = f(xi + h/2, yi + h/2 * k1)
    return yi + h * k2

def mod_euler_method(f, xi, yi, h, xin):
    z = f(xi, yi)
    y_euler_in = yi + h * z
    k1 = f(xi, yi)
    k2 = f(xin, y_euler_in)
    yin = yi + h * ((k1 + k2) / 2)
    return yin

def euler_method(f, xi, yi, h):
    return yi + h * f(xi, yi)

def solve_ivp_euler(f, a, b, h, z0):
    n = int((b - a) / h)
    x = np.linspace(a, b, n+1)
    y = np.zeros((n+1, len(z0)))
    y[0] = z0

    for i in range(1, n+1):
        y[i] = middle_point_method(f, x[i-1], y[i-1], h)
    return x, y

z0 = np.array([0, 2, 0, 0])
zprime = lambda x, z: np.array([
    z[1],
    z[2],
    z[3],
    np.sin(x) + 5 - 1.1 * z[3] + 0.1 * z[2] + 0.4 * z[0]
])

a, b = 0, 1
h = 0.1
x, y = solve_ivp_euler(zprime, a, b, h, z0)

plt.plot(x, y[:, 0], label="z0")
plt.plot(x, y[:, 1], label="z1")
plt.plot(x, y[:, 2], label="z2")
plt.plot(x, y[:, 3], label="z3")
plt.legend()
plt.show()

