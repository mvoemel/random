import numpy as np

def linear_least_squares(x, y, basis_functions):
    """
    Solves a linear least squares problem using normal equations.

    Parameters
    ----------
    x : array_like
        Input x-values.
    y : array_like
        Measured y-values.
    basis_functions : list of callable
        List of basis functions f_j(x) that define the model.

    Returns
    -------
    coeffs : np.ndarray
        Coefficient vector λ that minimizes the least squares error.
    """
    x = np.array(x)
    y = np.array(y)
    A = np.column_stack([f(x) for f in basis_functions])
    ATA = A.T @ A
    ATy = A.T @ y
    coeffs = np.linalg.solve(ATA, ATy)
    return coeffs

def print_fehlersystem(x, y, basis_functions):
    """
    Prints the components of the Fehlergleichungssystem:
    A, A^T A, and A^T y for the given basis functions and data.

    Parameters
    ----------
    x : array_like
        Input x-values.
    y : array_like
        Measured y-values.
    basis_functions : list of callable
        List of basis functions f_j(x) that define the model.
    """
    x = np.array(x)
    y = np.array(y)
    A = np.column_stack([f(x) for f in basis_functions])
    ATA = A.T @ A
    ATy = A.T @ y

    print("Design matrix A:")
    print(A)
    print("\nA^T A:")
    print(ATA)
    print("\nA^T y:")
    print(ATy)

"""
Example Usage

x_vals = [1, 2, 3, 4]
y_vals = [6, 6.8, 10, 10.5]
basis = [lambda x: x, lambda x: np.ones_like(x)]

basis can be changed for example: (for ax^2 + bx + c)
basis = [lambda x: x**2, lambda x: x, lambda x: np.ones_like(x)]

coeffs = linear_least_squares(x_vals, y_vals, basis)
print("Coefficients (a, b):", coeffs)
print_fehlersystem(x_vals, y_vals, basis)
"""
