#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 11:58:31 2026

@author: patricklewenstein
"""

import numpy as np
import matplotlib.pyplot as plt
from simulation import simulation

def estimate_equilibrium_time(M, E_local, window=100):
    """
    Estima tiempo de equilibrio combinando magnetización y energía
    """
    M_norm = M / (20*20)
    E_norm = np.mean(E_local, axis=(0, 1)) / (20*20)
    
    # Buscar donde ambas se estabilizan
    for i in range(window, len(M_norm)-window):
        # Fluctuación de magnetización
        std_M = np.std(M_norm[i-window:i])
        
        # Fluctuación de energía
        std_E = np.std(E_norm[i-window:i])
        
        # Criterio combinado
        if std_M < 0.02 and std_E < 0.01:
            return i
    
    return len(M_norm)

# Simulación
temperaturas = [1.0, 1.5, 2.0, 2.2, 2.4, 2.6, 3.0, 4.0]
eq_times = []

for T in temperaturas:
    print(f"T = {T}...")
    M, Eloc, S = simulation(5000, T)
    
    t_eq = estimate_equilibrium_time(M, Eloc, window=150)
    eq_times.append(t_eq)
    
    print(f"  Tiempo de equilibrio: {t_eq} pasos")

# Gráfica
plt.figure(figsize=(8, 5))
plt.plot(temperaturas, eq_times, 'o-', linewidth=2, markersize=8)
plt.xlabel('Temperatura T')
plt.ylabel('Pasos hasta el equilibrio')
plt.title('Tiempo de equilibrio vs Temperatura')
plt.grid(True, alpha=0.3)
plt.axvline(x=2.269, color='red', linestyle='--', label='Tc ≈ 2.269')
plt.legend()
plt.show()