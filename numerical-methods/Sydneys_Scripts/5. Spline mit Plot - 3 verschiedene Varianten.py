# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:58:31 2021

@author: Sydney Nguyen
"""

import numpy as np
import matplotlib.pyplot as plt

"""
normaler Spline
"""
def spline(x,y,xx):   
    n = len(x)-1  
    yy = []
    a = y
    h = [] 
    c = []
    z = []
    b = []
    d = []
          
    for i in range(n):
        h.append(x[i+1]-x[i])
    A_len = len(h)-1 #check this
    A = np.zeros((A_len,A_len))

    for i in range(A_len):
        if (i != 0):
            A[i][i-1] = h[i] 
        if (i != A_len-1):
            A[i][i+1] = h[i+1]        
        A[i][i] = 2*(h[i]+h[i+1])
    for i in range(n-1):
        z.append(3*((y[i+2]-y[i+1])/h[i+1]-(y[i+1]-y[i])/h[i]))
    tmp = np.linalg.solve(A,z)
    c.append(0)
    for i in range(len(tmp)):
        c.append(tmp[i])
    c.append(0)
    for i in range(n):
        b.append((y[i+1]-y[i])/h[i]-h[i]/3*(c[i+1]+2*c[i]))
        d.append(1/(3*h[i])*(c[i+1]-c[i]))
    j = 0
    for i in range(n):
        while j < len(xx) and xx[j] <= x[i+1]:
            yy.append(d[i]*(xx[j]-x[i])**3+c[i]*(xx[j]-x[i])**2+b[i]*(xx[j]-x[i])+a[i])
            #print(j,xx[j],yy[j])
            j+=1
            
    print("n:",n)        
    print("a:",a)   
    print("b:",b)
    print("c:",c)  
    print("d:",d)        
    plt.plot(xx,yy)
    #plt.show()
    
#gegeben
x = np.array([1900,1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010])
y = np.array([75.995,91.972,105.711,123.203,131.669,150.697,179.323,203.212,226.505,249.633,281.422,308.745])

xx = np.arange(min(x),max(x),0.1)
spline(x,y,xx)

"""
natürliche kubische Splinefunktion mit scipy.interpolate
"""
from scipy import interpolate
cs = interpolate.CubicSpline(x,y)
plt.plot(xx,cs(xx), "--")


"""
np.polyfit() und np.polyval mit verschiebung der Zeitreihe
"""
xx = np.arange(min(x),max(x),0.1)
p = np.polyfit(x-min(x),y,len(x)-1)
val = np.polyval(p,xx-min(x))
plt.plot(xx,val,"--")

plt.legend(["spline","cubicspline","polyfit"])
