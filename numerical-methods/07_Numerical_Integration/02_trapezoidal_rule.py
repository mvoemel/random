import numpy as np

def sum_trapezoidal_rule(f, a, b, n):
    """
    """
    fab = (f(a) + f(b)) / 2
    h = (b - a) / n
    sum_f = 0

    for i in range(1, n):
        xi = a + i * h
        sum_f += f(xi)
    
    tf = h * (fab + sum_f)
    return tf

f = lambda x: (1 / x)
a, b = 2, 4
n = 4

print(sum_trapezoidal_rule(f, a, b, n))