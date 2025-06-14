# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 18:16:46 2021

@author: Sydney Nguyen
"""

import numpy as np
import matplotlib.pyplot as plt

def lagrange(x,y,x_int):
    y_int = 0
    i_int = 1
    i = 0
    j = 1
    for i in range(len(y)):
        for j in range(len(x)):
            if (x[i] != x[j]):
                i_int *= (x_int-x[j])/(x[i]-x[j])
        #print("I",i,"=",i_int)
        y_int += i_int * y[i]
        i_int = 1
    return y_int

def plotLagrange(x,y,x_vec):
    y_vec = np.array([])
    for i in range(0,len(x_vec)):        
        y_vec = np.append(y_vec,np.array([lagrange(x,y,x_vec[i])]))
    plt.plot(x_vec,y_vec)
    # Grenzen
    plt.ylim(-100,250) # y ∈ [−100, 250]
    plt.xlim(1975,2020) # x ∈ [1981, 2010]
    plt.scatter(x,y)    
    plt.legend(["Lagrange" ])
    plt.show()      

# gegeben
x = [0,2500,5000,10000]
y = [1012,747,540,226]
x_int = 3750
# gesucht ist y_int zu x_int
y_int = lagrange(x,y,x_int)
print(y_int)

"""
plot
x_int ist jetzt ein Vektor und nicht nur ein Wert
"""
x = [1981.0,1984,1989,1993,1997,2000,2001,2003,2004,2010]
y = [0.5,8.2,15,22.9,36.6,51,56.3,61.8,65,76.6]
        
x_axis = np.arange(1975,2020,0.1)
plotLagrange(x,y,x_axis)
