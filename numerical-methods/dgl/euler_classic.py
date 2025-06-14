import matplotlib.pyplot as plt

def euler_classic(y_diff, x0, y0, h, interval):
    """
    Solves a first-order ODE using the classic (explicit) Euler method.

    Parameters:
    y_diff (function): The derivative function f(x, y) defining the ODE y' = f(x, y).
    x0 (float): The initial x-value (start of integration).
    y0 (float): The initial y-value at x0.
    h (float): Step size for the Euler integration.
    interval (list or tuple): The [start, end] interval of x over which to integrate.

    Returns:
        None: The function plots the solution using matplotlib but does not return the values.
    """
    x_vals = [x0]
    y_vals = [y0]
    x = x0
    y = y0
    while x < interval[1]:
        y += h * y_diff(x, y)
        x += h
        x_vals.append(x)
        y_vals.append(y)
    plt.plot(x_vals, y_vals, label="Euler Classic")
    plt.grid(True)
    plt.legend()
    plt.show()

def y_diff(x, y):
    return -2 * y + 1

euler_classic(y_diff, 0, 0, 0.05, [0, 1])
