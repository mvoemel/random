import matplotlib.pyplot as plt

def midpoint_method(y_diff, x0, y0, h, interval):
    x_vals = [x0]
    y_vals = [y0]
    x = x0
    y = y0
    while x < interval[1]:
        x_mid = x + (h/2)
        y_mid = y + (h/2) * y_diff(x, y)
        y = y + h * y_diff(x_mid, y_mid)
        x = x + h
        x_vals.append(x)
        y_vals.append(y)

    plt.plot(x_vals, y_vals, label="Midpoint Method")
    plt.grid(True)
    plt.legend()
    plt.show()

def y_diff(x, y):
    return -2 * y + 1


midpoint_method(y_diff, 0, 0, 0.05, [0, 1])

