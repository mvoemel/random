import numpy as np
import sympy as sp

def xi(a, i, h): return a + (i * h)

def sum_trapezoidal(f, a, h, n):
    res = 0
    for i in range(1, n):
        res += f(xi(a, i, h))
    return res

def trapezoidal(f, a, b, j):
    """ 
    The trapezoidal rule for the function f on the interval [a, b].
    The formula is:
    Tj = (b - a) / 2**j * (f(a) + f(b)) + sum(f(xi(a, i, h))) for i in range(1, n)
    where n = 2^j
    """
    hj = (b - a) / 2**j
    nj = 2 ** j
    return hj * (((f(a) + f(b)) / 2) + sum_trapezoidal(f, a, hj, nj))

def Tj0(f, a, b, j):
    """
    Returns the first column of the romber schema for the trapezoidal rule.
    """
    return np.array([trapezoidal(f, a, b, i) for i in range(0, j)])

def Tjk(tjk, tjp1k, k):
    """
    The romberg extrapolation.
    The formula is:
    Tjk = (4^k * Tj+1,k - Tjk) / (4^k - 1)
    where k is the order of the extrapolation.
    """
    return (4**k * tjp1k - tjk) / (4**k - 1)

def romberg_extrapolation(f, a, b, m):
    """
    Returns the romber extrapolation for the function f, the best approximation and the schema.
    The schema is a matrix of the approximations.
    The first column is the trapezoidal rule, the second column is the extrapolation of the first column.
    The third column is the extrapolation of the second column and so on.
    """
    m = m + 1
    T = np.zeros((m, m))
    T[:, 0] = Tj0(f, a, b, m)

    for k in range(1, m):
        for j in range(0, m - k):
            T[j, k] = Tjk(T[j, k - 1], T[j + 1, k - 1], k)
    return T[0, m - 1], T


# Derivation in appendix/Serie-10
def f1(v): return 97000 / (-5*v**2 - 570000)
def f2(v): return (97000 * v) / (-5*v**2 - 570000)

sym_x = sp.symbols('v')

a, b, m = 100, 0, 4
T1, schema1 = romberg_extrapolation(f1, a, b, m)
T2, schema2 = romberg_extrapolation(f2, a, b, m)

print("Function 1:")
print(f"T = {T1}")
print(f"Schema: {schema1}")
print("\nFunction 2:")
print(f"T = {T2}")
print(f"Schema: {schema2}")