#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 11:25:04 2026

@author: patricklewenstein
"""


import numpy as np
import matplotlib.pyplot as plt
from simulation import simulation     


L = 20
N = 10000                     
temperatures = [1.0, 1.5, 2.0, 2.2, 2.4, 2.6, 3.0]
k_factor = 10                 # t_eq ≈ k * tau
max_lag = 500                 



def energia_mitjana(Eloc):
    return np.mean(Eloc, axis=(0,1))


def autocorrelacio_normalitzada(data, max_lag):
    
    data = np.array(data, dtype=float)
    data -= np.mean(data)

    C = []
    var = np.mean(data*data)

    for tau in range(max_lag+1):
        prod = 0.0
        N = len(data) - tau
        for t in range(N):
            prod += data[t] * data[t+tau]
        prod /= N
        C.append(prod / var)

    return np.array(C)


def tau_integrat(C):
    """
    tau_int = 1/2 + suma C(tau) fins que es torni 0 o negatiu
    """
    tau = 0.5
    for k in range(1, len(C)):
        if C[k] <= 0:
            break
        tau += C[k]
    return tau


resultats = []

for T in temperatures:


    M, Eloc, S = simulation(N, T)

 
    Mps = M / (L*L)

    
    M2 = Mps[len(Mps)//2:]

    
    C = autocorrelacio_normalitzada(M2, max_lag=max_lag)

    
    tau = tau_integrat(C)

    
    t_eq = k_factor * tau

    resultats.append((T, tau, t_eq))

    print(f"tau ≈ {tau:.2f}")
    print(f"temps equilibri estimat t_eq ≈ {t_eq:.0f} passos")



Ts = [r[0] for r in resultats]
taus = [r[1] for r in resultats]

plt.figure(figsize=(7,5))
plt.plot(Ts, taus, "o-")
plt.xlabel("Temperatura T")
plt.ylabel("Temps d'autocorrelació tau")
plt.title("Tau vs Temperatura (autocorrelació)")
plt.grid(True)
plt.show()
