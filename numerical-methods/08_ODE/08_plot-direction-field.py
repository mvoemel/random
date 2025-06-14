import matplotlib.pyplot as plt
import numpy as np

def plot_direction_field(f, xmin, xmax, ymin, ymax, hx, hy):
    """
    Plots the direction field of a function over the specified range.
    1. Create a meshgrid of x and y values.
    2. Evaluate the slope at each point in the grid using the function f.
    3. Use plt.quiver to plot the direction field

    Parameters:
    f: function to plot
    xmin: minimum x value
    xmax: maximum x value
    ymin: minimum y value
    ymax: maximum y value
    hx: step size in x direction
    hy: step size in y direction

    Return:
    Nothing, plots the direction field directly.
    """

    x = np.arange(xmin, xmax, hx)
    y = np.arange(ymin, ymax, hy)
    [X, Y] = np.meshgrid(x, y)

    y_diff = f(X, Y)
    x_matrix = np.ones(shape=y_diff.shape)
    plt.quiver(X, Y, x_matrix, y_diff)


def mod_runge_kutta(f, a, b, h, y0):
    """
    """
    n = round(int((b - a) / h))
    xi = a
    yi = y0

    x, yn = [], []
    x.append(xi)
    yn.append(yi)
    for _ in range(n):
        k1 = f(xi, yi)
        k2 = f(xi + (2*h / 3), yi + (2*h / 3) * k1)

        xin = xi + h
        yin = yi + h * ((1/4)*k1 + (3/4)*k2)

        x.append(xin)
        yn.append(yin)
        xi = xin
        yi = yin

    return x, yn

fprime = lambda x, y: x**2 - y
x = np.linspace(-1.5, 1.5)

a = 0
b = 2
y0 = 1
h = 0.1


x_rk, y_rk = mod_runge_kutta(fprime, a, b, h, y0)
plot_direction_field(fprime, xmin=a, xmax=b, ymin=0, ymax=2, hx=h, hy=0.2)
plt.plot(x_rk, y_rk)
plt.title("Runge Kutta")
plt.xlabel("x")
plt.ylabel("y")
plt.legend(["Richtungsfeld", "Mod. Runge-Kutta"])
plt.show()