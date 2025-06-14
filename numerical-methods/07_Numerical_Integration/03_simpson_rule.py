import numpy as np

def simpson_rule(f, a, b, n):
    """
    """
    h = (b - a) / n
    fa = (1/2) * f(a)
    fb = (1/2) * f(b)
    sum_f = 0
    sum_f2 = 0
    prev_xi = a

    for i in range(1, n + 1):
        xi = a + i * h
        if(i < n): sum_f += f(xi)
        sum_f2 += f((prev_xi + xi) / 2)
        prev_xi = xi

    sf = (h / 3) * (fa + sum_f + 2 * sum_f2 + fb)
    return sf

f = lambda x: (1 / x)
a, b = 2, 4
n = 4

print(simpson_rule(f, a, b, n))
