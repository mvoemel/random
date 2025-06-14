import numpy as np

def li(x_int, x, i, n):
    lp = 1
    for j in range(0, n):
        if(i != j):
            lp *= ((x_int - x[j]) / (x[i] - x[j]))
    return lp
            

def lagrange_interpolation(x,y,x_int):
    if(x.size != y.size): return Exception("x and y must have the same size.")
    n = x.size
    y_int = 0
    for i in range(0, n):
        y_int += li(x_int, x, i, n) * y[i]
    return y_int

# Small test with task 1
x = np.array([0, 2500, 5000, 10000])
y = np.array([1013, 747, 540, 226])
x_int = 3750

y_int = lagrange_interpolation(x, y, x_int)
y_int