import numpy as np
import matplotlib.pyplot as plt

def four_step_runge_kutta(f, a, b, n, y0):
    """
    """
    h = (b - a) / n
    xi = a
    yi = y0

    x, yn = [], []
    x.append(xi)
    yn.append(yi)
    for _ in range(n):
        k1 = f(xi, yi)
        k2 = f(xi + (h / 2), yi + (h / 2) * k1)
        k3 = f(xi + (h / 2), yi + (h / 2) * k2)
        k4 = f(xi + h, yi + h * k3)

        xin = xi + h
        yin = yi + h * (1/6) * (k1 + 2*k2 + 2*k3 + k4)

        x.append(xin)
        yn.append(yin)
        xi = xin
        yi = yin

    return x, yn

fprime = lambda t, y: t**2 + 0.1 * y
f = lambda t: -10 * t**2 - 200 * t - 2000 + 1722.5 * np.exp(0.05*(2*t+3))
x = np.linspace(-1.5, 1.5)

a = -1.5
b = 1.5
y0 = 0
n = 5

x_rk, y_rk = four_step_runge_kutta(fprime, a, b, n, y0)
plt.plot(x_rk, y_rk)
plt.plot(x, f(x))
plt.title("Runge Kutta")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["Runge Kutta method", "Exact solution"])
plt.show()