import sympy as sp

x = sp.Symbol('x')

def lagrange_poly(x_vals, y_vals):
    if len(x_vals) != len(y_vals):
        raise ValueError('x and w must have same length')
    poly = 0
    for i in range(len(x_vals)): # Range is exclusive so (n = len(x_vals) - 1)
        term = y_vals[i]
        for j in range(len(x_vals)):
            if i != j:
                term *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        poly += term
    return sp.expand(poly)

def lagrange_error(poly, f_exact, x_vals, x_eval):
    """
    Estimates the interpolation error bound |f(x) - P_n(x)| at x_eval.

    Parameters:
        poly (sympy expression): The Lagrange interpolating polynomial
        f_exact (sympy expression): The exact function f(x)
        x_vals (list of float): Interpolation x-points [x0, ..., xn]
        x_eval (float): Point at which to estimate the error

    Returns:
        float: Estimated error bound
    """
    n = len(x_vals) - 1
    fact = sp.factorial(n + 1)

    # Product term: |(x - x0)(x - x1)...(x - xn)|
    omega = 1
    for xi in x_vals:
        omega *= (x_eval - xi)
    omega = abs(omega)

    # (n+1)th derivative of the exact function
    f_diff = f_exact
    for _ in range(n + 1):
        f_diff = sp.diff(f_diff, x)

    # Lambdify and find max on [min(x_vals), max(x_vals)]
    f_diff_lam = sp.lambdify(x, f_diff, 'numpy')

    from scipy.optimize import minimize_scalar
    def neg_abs_fdiff(xi):
        return -abs(f_diff_lam(xi))

    res = minimize_scalar(neg_abs_fdiff, bounds=(min(x_vals), max(x_vals)), method='bounded')
    max_fdiff = abs(f_diff_lam(res.x))

    return omega * max_fdiff / fact


poly = lagrange_poly([0, 250, 500, 1000], [1013, 747, 540, 226])

result = float(poly.subs(x, 375))
print(result)