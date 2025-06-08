# Búsqueda y Optimización para el Problema del Viajante (TSP)

Este proyecto implementa distintas estrategias para resolver el **Problema del Viajante** (TSP) en grafos dirigidos y asimétricos. Se utilizó un enfoque progresivo, comenzando con **heurísticas golosas**, pasando por **búsquedas locales**, y finalizando con una **metaheurística** de tipo ILS. Además, se probaron las soluciones con archivos clásicos de **TSPLIB**, permitiendo comparar contra soluciones óptimas conocidas.

## Estructura del proyecto

- `heurísticas.py`: Implementación de las 4 heurísticas golosas.
- `búsqueda_local.py`: Implementación de los 4 operadores de búsqueda local.
- `metaheurísticas.py`: Implementación del algoritmo **Iterated Local Search (ILS)**.
- `leer_archivo.py`: Lee los archivos de TSPLIB.

---

## Ejercicio 1 – Heurísticas Golosas

Se implementaron 4 heurísticas para generar soluciones iniciales:

1. **Ciudad más cercana**: desde la ciudad actual, elige la ciudad no visitada más cercana (A → B).
2. **Llegada más cercana**: desde la ciudad actual, elige la ciudad que tiene menor costo de llegada (B → A).
3. **Menor distancia promedio**: elige la ciudad cuya distancia promedio a las restantes (más la actual) sea la menor.
4. **Mínimo de distancias**: considera dos pasos hacia adelante: ciudad actual + su ciudad más cercana futura.

---

## Ejercicio 2 – Búsqueda Local

Se implementaron 4 operadores de mejora local para optimizar soluciones iniciales:

1. **Relocate**: mueve nodos de una posición a otra buscando mejorar el recorrido.
2. **Swap**: intercambia dos nodos y evalúa si mejora la solución.
3. **2-opt**: desconecta dos aristas y reconecta invirtiendo el camino intermedio.
4. **2-opt mejorado**: igual al 2-opt, pero se aplica iterativamente sobre la mejor solución hallada hasta el momento.

---

## Ejercicio 3 – Metaheurística: ILS (Iterated Local Search)

Se implementó la técnica de **búsqueda local iterada**, que funciona así:

- Se parte de una solución inicial generada con una heurística.
- Se **perturba** esa solución (swap, relocate o 2-opt) para escapar de óptimos locales.
- Se vuelve a aplicar la heurística a la solución perturbada.
- Se guarda la mejor solución encontrada.
- Se repite este proceso varias veces.

Se trabajó con dos enfoques:
- **Fijo**: se perturban 6 posiciones aleatorias.
- **Adaptativo**: se perturba el 6% del tamaño de la instancia (basado en experimentación).

---

## Evaluación con TSPLIB

Para validar la calidad de las soluciones, se utilizaron archivos clásicos de **[TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)**. Esto permitió:

- Comparar nuestras soluciones con las mejores soluciones conocidas.
- Medir qué tan cerca están las heurísticas y metaheurísticas del óptimo global.
- Evaluar el trade-off entre **tiempo de cómputo** y **calidad de solución**.
