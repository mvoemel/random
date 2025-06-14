import numpy as np
import matplotlib.pyplot as plt

def tridiag(a, b, c, k1=-1, k2=0, k3=1):
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

def plot_spline_interpolation(x, y, xx, yy, interval_indices):
        plt.scatter(x, y, color='red', label='Data points')
        plotted_intervals = set()
        for i in interval_indices:
            if i not in plotted_intervals:
                x_vals_in_interval = [xv for xv, idx in zip(xx, interval_indices) if idx == i]
                y_vals_in_interval = [yv for yv, idx in zip(yy, interval_indices) if idx == i]
                plt.plot(x_vals_in_interval, y_vals_in_interval, label=f'Interval [{x[i]}, {x[i+1]}]')
                plotted_intervals.add(i)

        plt.title("Cubic Spline Interpolation")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.show()

def cubic_spline_interpolation(x, y, xx, g=True):
    n = x.size - 1
    a = y # ai = yi
    h = [x[i+1] - x[i] for i in range(0, n)] # h[i] = x[i+1] - x[i]
    c0, cn = 0, 0

    # Create matrix A for Ac = z
    Ad = [2*(h[i] + h[i+1]) for i in range(0, n - 1)]
    Ah = [h[i] for i in range(1, n - 1)]
    A = tridiag(Ah, Ad, Ah)
    z = [3*((y[i+2] - y[i+1]) / h[i+1]) - 3* ((y[i+1] - y[i]) / h[i]) for i in range(0, n - 1)]
    c = np.linalg.solve(A, z)
    c = np.insert(c, 0, c0)
    c = np.insert(c, n, cn)

    b = [((y[i+1] - y[i]) / h[i]) - (h[i] / 3) * (c[i+1] + 2*c[i]) for i in range(0, n)]
    d = [(1 / (3*h[i])) * (c[i+1] - c[i]) for i in range(0, n)]

    yy = []
    interval_indices = []
    for xval in xx:
        i = next(i for i in range(n) if x[i] <= xval <= x[i + 1])
        dx = xval - x[i]
        yy.append(a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3)
        interval_indices.append(i)
    
    if g:
        plot_spline_interpolation(x, y, xx, yy, interval_indices)
    
    return yy


t = np.array([1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000])
p = np.array([75.995, 91.972, 105.711, 123.203, 131.669, 150.697, 179.323, 203.212, 226.505, 249.633, 281.422])
xx = np.linspace(t[0], t[-1], 500)
yy = cubic_spline_interpolation(t, p, xx)