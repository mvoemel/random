# Lagrange vs Polyfit – When to Use Which

1. Use `scipy.interpolate.lagrange` when:
   - You have a small number of data points.
   - You want the polynomial to pass exactly through all points.
   - The data is noise-free and exact interpolation is the goal.

2. Use `numpy.polyfit` when:
   - The data contains noise or measurement error.
   - You want a best-fit polynomial (regression), not exact interpolation.
   - You have many points or want better numerical stability.


Use `numpy.polyval` to compute values of a polynomial with known coefficients.

> Note: For symbolic expressions, consider `sympy` instead.

## How to use polyfit and polyval

```python 
import numpy as np
import matplotlib.pyplot as plt

x_vals = np.array([1981, 1984, 1989, 1993, 1997, 2000, 2001, 2003, 2004, 2010])
y_vals = np.array([0.5, 8.2, 15, 22.9, 36.6, 51, 56.3, 61.8, 65, 76.7])
coefficients = np.polyfit(x_vals, y_vals, len(x_vals) - 1)

xAxis = np.arange(1975, 2020, 0.1)

poly = np.polyval(coefficients, xAxis)

plt.scatter(x_vals, y_vals)
plt.plot(xAxis, poly)
plt.ylim(-100, 250)
plt.show()
```