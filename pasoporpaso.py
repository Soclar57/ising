import numpy as np
import matplotlib.pyplot as plt
from simulation import simulation

# Graficar energía media y magnetización total en función del número de pasos para diversas temperaturas

N = 400
temperaturas = [1.0, 2.5, 100.0] 
for T in temperaturas:
    M, Eloc, S = simulation(N, T)
    E = np.mean(Eloc, axis=(0, 1))
    # Graficar magnetización y energía
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(M, color='orange',label=f'T={T}')
    plt.title('Magnetización total vs pasos')
    plt.xlabel('Número de pasos')
    plt.ylabel('Magnetización total M')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(E, label=f'T={T}')
    plt.title('Energía media vs pasos')
    plt.xlabel('Número de pasos')
    plt.ylabel('Energía media E')
    plt.legend()
    plt.tight_layout()
    plt.show()