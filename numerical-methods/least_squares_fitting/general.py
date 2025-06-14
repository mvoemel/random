import numpy as np
import matplotlib.pyplot as plt

def nonlinear_least_squares(f, jacobian, x0, y, initial_params, max_iter=10):
    """
    Solves a nonlinear least squares problem using the Gauss-Newton method.

    Parameters
    ----------
    f : callable
        Vector-valued function f(params) -> np.ndarray
    jacobian : callable
        Function returning the Jacobian matrix Df(params) -> np.ndarray
    x0 : array_like
        Input x-values used in the model (passed to f and jacobian internally).
    y : array_like
        Measured y-values.
    initial_params : np.ndarray
        Initial guess for the parameter vector.
    max_iter : int
        Maximum number of Gauss-Newton iterations.

    Returns
    -------
    params : np.ndarray
        Estimated parameter vector minimizing the residual norm.
    """
    y = np.array(y)
    params = np.array(initial_params, dtype=float)

    for _ in range(max_iter):
        r = y - f(params)
        J = jacobian(params)
        delta = np.linalg.lstsq(J, r, rcond=None)[0]
        params = params + delta

    return params

"""Example
# Data points
x_data = np.array([0, 1, 2, 3, 4])
y_data = np.array([3, 1, 0.5, 0.2, 0.05])

# Model: f(x) = a * exp(b * x)
def f_ab(params):
    a, b = params
    return a * np.exp(b * x_data)

# Jacobian of f(x) = a * exp(b * x) with respect to [a, b]
def jacobian_ab(params):
    a, b = params
    J = np.zeros((len(x_data), 2))
    exp_bx = np.exp(b * x_data)
    J[:, 0] = exp_bx
    J[:, 1] = a * x_data * exp_bx
    return J

initial_guess = [1.0, -1.0]
estimated_params = nonlinear_least_squares(f_ab, jacobian_ab, x_data, y_data, initial_guess)

print("Estimated parameters [a, b]:", estimated_params)

# Plotting
x_plot = np.linspace(0, 4, 100)
y_fit = estimated_params[0] * np.exp(estimated_params[1] * x_plot)

plt.scatter(x_data, y_data, color='red', label='Data')
plt.plot(x_plot, y_fit, label='Fitted curve')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Nonlinear Least Squares Fit: a * exp(b * x)')
plt.grid(True)
plt.show()

"""