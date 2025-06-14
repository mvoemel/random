import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

g = 9.81

def w(v0, alpha):
    return (v0 ** 2 * np.sin(2 * np.radians(alpha))) / g

[v0, alpha] = np.meshgrid(np.linspace(0, 100, 500), np.linspace(0, 100, 500))

z = w(v0, alpha)
# Plot in 3d wireframe
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Axes3D.plot_surface(ax, v0, alpha, z, cmap='viridis')

plt.title("Task 1")
Axes3D.set_xlabel(ax, "Speed")
Axes3D.set_ylabel(ax, "Angle")
Axes3D.set_zlabel(ax, "Distance")

plt.show()

fig = plt.figure()
cont = plt.contour(v0, alpha, z, cmap=cm.coolwarm)

plt.show()