import sympy as sp

def linearize_non_linear_function(f, x, subs):
    """
    Linearize a non-linear function f at a point given by subs.
    Params:
        f: A non-linear function (list or matrix).
        x: A vector of variables (list or matrix).
        subs: A list of tuples for substitutions (variable, value).
    """
    M_f = sp.Matrix(f)
    M_x = sp.Matrix(x)
    J = M_f.jacobian(M_x)
    
    # Substitute the values into the Jacobian matrix
    J_subs = J.subs(subs)

    # Compute the function value at the point given by subs
    f_subs = M_f.subs(subs)
    
    # Compute the linearized function
    linearized_function = f_subs + J_subs * (sp.Matrix(x) - sp.Matrix(x).subs(subs))
    
    return linearized_function

# Example usage
x, x1, x2, x3 = sp.symbols('x x1 x2 x3')
f1 = x1 + x2**2 - x3**2 - 13
f2 = sp.ln(x2 / 4) + sp.exp(0.5*x3 - 1) - 1
f3 = (x2 - 3)**2 - x3**3 + 7

f = [f1, f2, f3]
x = [x1, x2, x3]
subs = [(x1, 1.5), (x2, 3), (x3, 2.5)]

linearized_function = linearize_non_linear_function(f, x, subs)
print("Linearized function:")
print(linearized_function)

