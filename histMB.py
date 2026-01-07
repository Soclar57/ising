import numpy as np
import matplotlib.pyplot as plt
from simulation import simulation

# Hacer histograma de energías de las partículas

temperaturas = [1.0, 2.5, 100.0] 
N_eq = 5000
N_avg = 10000
for T in temperaturas:

    # Probabiliddes teóricas
    Z = np.exp(1/T) + np.exp(0.5/T) + 1 + np.exp(-0.5/T) + np.exp(-1/T)
    probs = [np.exp(1/T)/Z, np.exp(0.5/T)/Z, 1/Z, np.exp(-0.5/T)/Z, np.exp(-1/T)/Z]

    # Generamos los datos
    M, Eloc, S = simulation(N_eq + N_avg, T)
    Eloc = Eloc[:,:, -N_avg:]
    data = Eloc.flatten()

    # Bins centrados en los valores posibles: extendemos los bordes para que capten extremos
    bins = [-1.25, -0.75, -0.25, 0.25, 0.75, 1.25]
    plt.figure(figsize=(6,4))

    # Normalizamos el histograma para obtener probabilidades por bin
    weights = np.ones_like(data) / len(data)
    n, bins_out, patches = plt.hist(data, bins=bins, color="#4C72B0", edgecolor="black",
                                    linewidth=1.0, alpha=0.9, weights=weights)

    # Centros de bins (valores de energía)
    bin_centers = [-1.0, -0.5, 0.0, 0.5, 1.0]

    # Dibujar probabilidades teóricas sobre el histograma
    plt.plot(bin_centers, probs, 'o-', color='red', markersize=7, label='Prob. teórica')

    # --- NUEVO: ajustar eje y para evitar solapamientos ---
    y_max = max(np.max(n), max(probs))
    pad = max(0.03, 0.12 * y_max)  # margen mínimo y relativo
    plt.ylim(0, y_max + pad)
    label_offset = pad * 0.5
    # ----------------------------------------------------

    # Etiquetas y estética
    plt.xticks([-1, -0.5, 0, 0.5, 1])
    plt.xlabel('Energía por partícula E/N')
    plt.ylabel('Densidad de probabilidad')
    plt.title(f'Histograma de energías por partícula a T={T}')

    # Anotar contadores (recuento entero) encima de cada barra y anotar prob. teórica
    total_samples = len(data)
    for rect, p_sample, x_center, p_theo in zip(patches, n, bin_centers, probs):
        # recuento entero por barra
        count_int = int(round(p_sample * total_samples))
        height = rect.get_height()
        if height > 0:
            plt.text(rect.get_x() + rect.get_width()/2, height + label_offset, str(count_int),
                     ha='center', va='bottom', fontsize=9)
        # etiqueta de probabilidad teórica (en la escala de probabilidades)
        plt.text(x_center, p_theo + label_offset, f"{p_theo:.3f}", color='red',
                 ha='center', va='bottom', fontsize=9)

    plt.legend()
    plt.tight_layout()

    plt.show()
