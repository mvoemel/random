import sympy as sp

def jacobian_matrix(f, x):
    """
    Compute the Jacobian matrix of a vector function f.
    Params:
        f: A vector function (list or matrix).
        x: A vector of variables (list or matrix).
    """
    M_f = sp.Matrix(f)
    M_x = sp.Matrix(x)
    J = M_f.jacobian(M_x)
    return J

def jacobian_matrix_with_subs(f, x, subs):
    """
    Compute the Jacobian matrix of a vector function f with substitutions.
    Params:
        f: A vector function (list or matrix).
        x: A vector of variables (list or matrix).
        subs: A list of tuples for substitutions (variable, value).
    """
    J = jacobian_matrix(f, x)
    J_subs = J.subs(subs)
    return J_subs

# Example usage
x, x1, x2, x3 = sp.symbols('x x1 x2 x3')
f1 = x1 + x2**2 - x3**2 - 13
f2 = sp.ln(x2 / 4) + sp.exp(0.5*x3 - 1) - 1
f3 = (x2 - 3)**2 - x3**3 + 7

f = [f1, f2, f3]
x = [x1, x2, x3]
subs = [(x1, 1.5), (x2, 3), (x3, 2.5)]

J = jacobian_matrix_with_subs(f, x, subs)
print("Jacobian matrix:")
print(J)