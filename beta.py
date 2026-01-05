from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import sys

data_path = Path(__file__).resolve().parent / 'beta_logdata.dat'

if not data_path.exists():
    print(f'Error: no existe el archivo {data_path}')
    sys.exit(1)

data = np.loadtxt(data_path)

x = data[:, 0]
y = data[:, 1]

# Ajuste lineal con covarianza
(p, cov) = np.polyfit(x, y, 1, cov=True)
slope, intercept = p[0], p[1]
stderr_slope = np.sqrt(cov[0, 0])

print(f'Slope = {slope:.6f} ± {stderr_slope:.6f}')

# Plot datos y recta ajustada
x_fit = np.linspace(x.min(), x.max(), 200)
y_fit = slope * x_fit + intercept

plt.figure()
plt.plot(x, y, 'o', label='Datos')
plt.plot(x_fit, y_fit, '-', label=f'Recta ajustada')
plt.xlabel('log|T - Tc|')
plt.ylabel('log|M|')
plt.legend()
plt.title('Regresión lineal de log|M| vs log|T-Tc|')
plt.show()