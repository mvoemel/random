import numpy as np
import matplotlib.pyplot as plt

def runge_kutta(f, xi, yi, h):
    k1 = f(xi, yi)
    k2 = f(xi + (h / 2), yi + (h / 2) * k1)
    k3 = f(xi + (h / 2), yi + (h / 2) * k2)
    k4 = f(xi + h, yi + h * k3)

    yin = yi + h * (1/6) * (k1 + 2*k2 + 2*k3 + k4)
    return yin

def runge_kutta_with_high_order_ode(f, a, b, z0, h):
    """
    """
    n = int((b - a) / h)
    x = np.linspace(a, b, n+1)
    y = np.zeros((n+1, len(z0)))
    y[0] = z0

    for i in range(1, n+1):
        y[i] = runge_kutta(f, x[i-1], y[i-1], h)
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
x, y = runge_kutta_with_high_order_ode(zprime, a, b, z0, h)

plt.plot(x, y[:, 0], label="z0")
plt.plot(x, y[:, 1], label="z1")
plt.plot(x, y[:, 2], label="z2")
plt.plot(x, y[:, 3], label="z3")
plt.legend()
plt.show()
