# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 15:45:17 2021

@author: Sydney Nguyen
"""

"""
a)
    Ausgleichsrechnung = Regression
"""
import numpy as np
import matplotlib.pyplot as plt

def f1(x):
    return x**2

def f2(x):
    return x

def f3(x):
    return 1

def f(x, λ):
    return λ[0]*f1(x) + λ[1]*f2(x) + λ[2]*f3(x)

# Gegeben:
x = np.array([0,10,20,30,40,50,60,70,80,90,100])
y = np.array([999.9,999.7,998.2,995.7,992.2,988.1,983.2,977.8,971.8,965.3,958.4])
n = len(x)
m = 3
# Falls Data in Matrix gegeben:
#x = data[:,0]
#y = data[:,1]
#[n,m] = np.shape(data)

# Fehlergleichungssystem A
A = np.zeros([n,m])
A[:,0] = f1(x)
A[:,1] = f2(x)
A[:,2] = f3(x)

# Normalgleichungssystem
# A.T @ A @ λ = A.T @ y
# λ ist Lösungsvektor
λ = np.linalg.solve(A.T @ A, A.T @ y)

# QR
# R @ λ = Q.T @ y
[Q,R] = np.linalg.qr(A)
λ_qr = np.linalg.solve(R, Q.T @ y)

# Graf
plt.plot(x,y,"*")
xx = np.linspace(np.min(x)-0.5,np.max(x)+0.5)
plt.plot(xx,f(xx, λ),"--")
plt.plot(xx,f(xx, λ_qr),"--")
plt.legend(["Exact points","Regression","QR"])
plt.xlabel("°C / Τ")
plt.ylabel("g/l / ρ")
#plt.show()

"""
b)
    Kond(A.T@A): 154508460.5769
    -> Sehr gross.
    Kond(R)l: 12272.5476
    -> Kleiner. R ist besser konditioniert
    
"""
cond = np.linalg.cond(A.T @ A, np.inf)
cond_r = np.linalg.cond(R, np.inf)
print("Kond(A.T @ A):",cond.round(4))
print("Kond(R)l:",cond_r.round(4))

"""
c)
    Polyfit()
"""
p = np.polyfit(x-x[0],y,len(x)-1)
val = np.polyval(p,xx-x[0])
plt.plot(xx,val,"--")

# Grafik
plt.legend(["Exact points","Regression","QR","Polyfit"])
plt.xlabel("°C / Τ")
plt.ylabel("g/l / ρ")
plt.show()

"""
d) 
    Fehlerfunktionale:
    Fehler Polyfit ist minim
    
"""
def E(f,y):
    tmp = (f-y)
    return tmp.T@tmp #skalarprodukt, equivalent zu: Σ (f(xi)-yi)**2

print("Fehler normal:",E(f(x,λ),y))
print("Fehler QR:",E(f(x,λ_qr),y))
print("Fehler polyfit:",E(np.polyval(p,x),y))