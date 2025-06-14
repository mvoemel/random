import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Example function
def f(x, y):
    return x**2 + y**2

# Altitude lines
[x, y] = np.meshgrid(np.linspace(-5, 5), np.linspace(-5, 5))
z = f(x, y)

fig = plt.figure(0)
cont = plt.contour(x, y, z, cmap=cm.coolwarm)
fig.colorbar(cont, shrink=0.5, aspect=5)
plt.title('Plot')
plt.xlabel('x')
plt.ylabel('y')

plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Axes3D.plot_surface(ax, x, y, z)
Axes3D.set_xlabel(ax, "X label")
Axes3D.set_ylabel(ax, "Y label")
Axes3D.set_zlabel(ax, "Z label")

plt.show()
