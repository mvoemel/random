import numpy as np


def sum_rectangle_rule(f, a, b, n):
    """ 
    """

    h = (b - a) / n
    xn = b
    sum_f = 0

    for i in range(n):
        xi = a + i * h
        sum_f += f(xi + (h / 2))
        
    rf = h * sum_f
    return rf


f = lambda x: (1 / x)
a, b = 2, 4
n = 4

print(sum_rectangle_rule(f, a, b, n))