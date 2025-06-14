import matplotlib.pyplot as plt

def runge_kutta(y_diff, x0, y0, h, interval):
    x_vals = [x0]
    y_vals = [y0]
    x = x0
    y = y0
    while x < interval[1]:
        k1 = y_diff(x, y)
        k2 = y_diff(x + (h/2), y + (h/2) * k1)
        k3 = y_diff(x + (h/2), y + (h/2) * k2)
        k4 = y_diff(x + h, y + (h * k2))
        x = x + h
        y = y + h * (1/6) * (k1 + 2 * k2 + 2 * k3 + k4)
        x_vals.append(x)
        y_vals.append(y)

    plt.plot(x_vals, y_vals, label="Runge Kutta")
    plt.grid(True)
    plt.legend()
    plt.show()

def y_diff(x, y):
    return -2 * y + 1


runge_kutta(y_diff, 0, 0, 0.05, [0, 1])