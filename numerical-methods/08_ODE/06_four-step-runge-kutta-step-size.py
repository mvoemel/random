import numpy as np
import matplotlib.pyplot as plt

def four_runge_kutta_with_step_size(f, a, b, y0, h):
    """
    """
    xi = a
    yi = y0

    x, yn = [], []
    x.append(xi)
    yn.append(yi)
    while (xi + h <= b + (h / 2)):
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

fprime = lambda x, y: y
a, b = 0, 1
y0 = 1

x_rk1, y_rk1 = four_runge_kutta_with_step_size(fprime, a, b, y0, 0.1)
x_rk2, y_rk2 = four_runge_kutta_with_step_size(fprime, a, b, y0, 0.05)
print(x_rk2)
x = np.linspace(0, 1)
plt.plot(x_rk1, y_rk1, linestyle='-')
plt.plot(x_rk2, y_rk2, linestyle='--')
plt.plot(x, np.exp(x), linestyle=':', color='red')
plt.title("Runge Kutta method with different step sizes")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["h = 0.1", "h = 0.05", "Exact solution"])
plt.show()

# Error analysis
print("Global error for h = 0.1: ", abs(y_rk1[-1] - np.exp(1)))
print("Global error for h = 0.05: ", abs(y_rk2[-1] - np.exp(1)))
