import matplotlib.pyplot as plt

def modified_euler(y_diff, x0, y0, h, interval):
    x_vals = [x0]
    y_vals = [y0]
    x = x0
    y = y0
    while x < interval[1]:
        k1 = y_diff(x, y)
        k2 = y_diff(x + h, y + h * y_diff(x, y))
        x = x + h
        y = y + h * ((k1 + k2) / 2)
        x_vals.append(x)
        y_vals.append(y)

    plt.plot(x_vals, y_vals, label="Modified Euler")
    plt.grid(True)
    plt.legend()
    plt.show()

def y_diff(x, y):
    return -2 * y + 1


modified_euler(y_diff, 0, 0, 0.05, [0, 1])

