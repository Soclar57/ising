import numpy as np
from numba import jit

@jit(nopython=True, fastmath=True, cache=True)
def simulation(N,T,S=None):
    # N: Número de pasos
    # T: Temperatura (en unidades de energía)
    # Constante de acoplamiento J = 1

    # Matriz de espines inicial 20x20
    if S is None:
        L=20
        S = np.empty((L, L), dtype=np.int64)
        for i in range(L):
            for j in range(L):
                S[i, j] = 1 if np.random.rand() < 0.5 else -1

    # Matriz de energía local por estado
    Eloc = np.empty((L, L, N+1), dtype=np.float64)
    for i in range(L):
        for j in range(L):
            s = S[i,j]

            top = S[(i-1) % L,j]
            bottom = S[(i+1) % L,j]
            left = S[i,(j-1) % L]
            right = S[i,(j+1) % L]

            Eloc[i,j,0] = -s*(top + bottom + left + right)*0.25 # contamos 4 veces cada interacción

    # Magnetización total por estado
    M = np.empty(N+1, dtype=np.int64) # N pasos son N+1 estados
    M[0] = np.sum(S)

    # Paso montecarlo (L*L intentos de cambio de espín)
    for n in range(N):
        Eloc[:,:,n+1] = Eloc[:,:,n]
        M[n+1] = M[n]

        for _ in range(L*L):
            # Elegimos un espín aleatorio
            i = np.random.randint(0, L)
            j = np.random.randint(0, L)

            s = S[i,j]

            top = S[(i-1) % L,j]
            bottom = S[(i+1) % L,j]
            left = S[i,(j-1) % L]
            right = S[i,(j+1) % L]

            dE = 2*s*(top + bottom + left + right) # Cambio de energía si se voltea el espín

            # Criterio de Metropolis
            if dE <= 0 or np.random.rand() < np.exp(-dE/T):
                # Aceptamos el cambio
                S[i,j] = -s

                M[n+1] = M[n+1] - 2*s

                Eloc[i,j,n+1] = Eloc[i,j,n+1] + dE*0.25
                Eloc[(i-1) % L,j,n+1] = Eloc[(i-1) % L,j,n+1] + 2*s*top*0.25
                Eloc[(i+1) % L,j,n+1] = Eloc[(i+1) % L,j,n+1] + 2*s*bottom*0.25
                Eloc[i,(j-1) % L,n+1] = Eloc[i,(j-1) % L,n+1] + 2*s*left*0.25
                Eloc[i,(j+1) % L,n+1] = Eloc[i,(j+1) % L,n+1] + 2*s*right*0.25
            
    return M, Eloc, S