import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

data_path = Path(__file__).resolve().parent / 'data.dat'

if not data_path.exists():
    print(f'Error: no existe el archivo {data_path}')
    sys.exit(1)

data = np.loadtxt(data_path)

temp = data[:, 0]
M_medias = data[:, 1]
E_medias = data[:, 2]
X_medias = data[:, 3]
C_medias = data[:, 4]

print('Estimaciones de Tc:')
Tc_C = temp[np.argmax(C_medias)]
Tc_X = temp[np.argmax(X_medias)]
print(f'Tc estimada por calor específico: {Tc_C}')
print(f'Tc estimada por susceptibilidad magnética: {Tc_X}')
print(f'Tc teórica: 2.269') # Fórmula 19 de la página 494 del Pathia (K definido en la fórmula 1)

plt.figure(figsize=(12, 10))
plt.subplot(2, 2, 1)
plt.plot(temp, M_medias, 'o')
plt.title('Magnetización media vs temperatura')
plt.xlabel('Temperatura T')
plt.ylabel('Magnetización media |M|')
plt.subplot(2, 2, 2)
plt.plot(temp, E_medias, 'o')
plt.title('Energía por partícula media vs temperatura')
plt.xlabel('Temperatura T')
plt.ylabel('Energía por partícula media E/N')
plt.subplot(2, 2, 3)
plt.plot(temp, X_medias, 'o')
plt.title('Susceptibilidad magnética vs temperatura')
plt.xlabel('Temperatura T')
plt.ylabel('Susceptibilidad magnética X')
plt.subplot(2, 2, 4)
plt.plot(temp, C_medias, 'o')
plt.title('Calor específico vs temperatura')
plt.xlabel('Temperatura T')
plt.ylabel('Calor específico C')
plt.tight_layout()
plt.show()