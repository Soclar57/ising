import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from pathlib import Path
from simulation import simulation

# Numba no se traga np.mean con ejes múltiples
@jit(nopython=True, fastmath=True)
def meanEloc(arr):
    n, m, p = arr.shape
    result = np.empty(p, dtype=np.float64)
    
    for k in range(p):
        total = 0.0
        for i in range(n):
            for j in range(m):
                total += arr[i, j, k]
        result[k] = total / (n*m)
    
    return result


@jit(nopython=True, fastmath=True)
def calcular_medias(N_eq, N_avg, n):
    ti, tf = 1.3, 3.3
    t = np.linspace(-0.9, 0.9, n)
    x = np.arctanh(t)
    x = (x - x.min()) / (x.max() - x.min())
    temp = ti + (tf - ti) * x

    M_medias = np.empty(n, dtype=np.float64)
    E_medias = np.empty(n, dtype=np.float64)
    X_medias = np.empty(n, dtype=np.float64)
    C_medias = np.empty(n, dtype=np.float64)
    S = None

    # Invertir vector de temperaturas (es bueno para el annealing porque los sistemas calientes llegan antes al equilibrio)
    temp = temp[::-1]

    for i, T in enumerate(temp):
        M, Eloc, S = simulation(N_eq + N_avg, T, S)

        E = meanEloc(Eloc)

        M_medias[i] = np.mean(np.abs(M[N_eq:]))
        E_medias[i] = np.mean(E[N_eq:])
        X_medias[i] = (np.mean(M[N_eq:]**2) - np.mean(np.abs(M[N_eq:]))**2) / T
        C_medias[i] = np.var(E[N_eq:]) / (T*T)

    return temp, M_medias, E_medias, X_medias, C_medias

# Ejecutar simulación
N_eq = 1000000
N_avg = 100000
n = 50
temp, M_medias, E_medias, X_medias, C_medias = calcular_medias(N_eq, N_avg, n)

# Guardar datos en data.dat
out_path = Path(__file__).resolve().parent / 'data.dat'
data = np.column_stack((temp, M_medias, E_medias, X_medias, C_medias))
np.savetxt(out_path, data, header='T M_medias E_medias X_medias C_medias')
print(f'Datos guardados en: {out_path}')

# Guardar datos para la regresión de la beta
# Tomamos temperaturas entre 2 y Tc_C (más fiable que Tc_X)
# excluir delta==0 y M_medias<=0
Tc_C = temp[np.argmax(C_medias)]
mask = (temp >= 2.0) & (temp < Tc_C) & (M_medias > 0)
log_delta = np.log(np.abs(temp[mask]-Tc_C))
log_M = np.log(M_medias[mask])
# Guardar datos en .dat (dos columnas: log_delta, log_M)
data = np.column_stack((log_delta, log_M))
out_path = Path(__file__).resolve().parent / 'beta_logdata.dat'
np.savetxt(out_path, data, header='log_delta log_M')
print(f'Datos guardados en: {out_path}')