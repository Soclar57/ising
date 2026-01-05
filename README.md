# Simulaciones del modelo de Ising

Este repositorio contiene scripts para simular y analizar el modelo de Ising mediante Montecarlo.

Archivos y propósito
- `simulation.py`  
  Contiene la función que ejecuta la simulación de Montecarlo. Este script no se ejecuta directamente (exporta funciones usadas por otros scripts).

- `main.py`  
  Función principal: realiza simulaciones para muchas temperaturas y guarda los datos en archivos `.dat`. Tarda mucho en ejecutarse debido al gran número de pasos Monte Carlo necesarios (más de un millón).

- `pasoporpaso.py`  
  Grafica la magnetización total y la energía por partícula para ver en cuántos pasos se alcanza el equilibrio para distintas temperaturas.

- `histMB.py`  
  Grafica histogramas de las energías de cada spin y los compara con la distribución de Maxwell–Boltzmann a distintas temperaturas.

- `graficas.py`  
  Carga los datos guardados (`data.dat`), calcula la temperatura crítica a partir del máximo de la susceptibilidad y del calor específico, y grafica magnetización, energía, susceptibilidad y calor específico.

- `beta.py`  
  Carga los datos guardados (`beta_logdata.dat`), calcula el exponente beta mediante regresión lineal, grafica la recta ajustada y muestra el valor y el error de la pendiente.

- `equilibrio_autocorrelacion.py`  
  [Descripción vacía]

- `Equilibrio_magnetizacion_energia.py`  
  [Descripción vacía]

Ejecución
Para ejecutar un script, abrir la terminal en la carpeta del proyecto y ejecutar:
uv run .\[nombre_del_script]

Ejemplo:
uv run .\beta.py

Notas
- Dependencias: numpy, matplotlib, numba.