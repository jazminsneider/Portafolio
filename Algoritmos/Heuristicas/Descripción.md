# Algoritmos de Optimización: Heurísticas, Búsqueda Local y Metaheurísticas

Este trabajo tiene como objetivo explorar distintas estrategias para encontrar soluciones aproximadas al **Problema del Viajante (TSP)**, utilizando heurísticas golosas, operadores de búsqueda local y metaheurísticas. Todas las implementaciones están hechas en Python y organizadas en tres bloques:

## Archivos

- `heurísticas.py`: Implementaciones de cuatro heurísticas golosas para generar soluciones iniciales.
- `búsqueda_local.py`: Implementaciones de operadores de búsqueda local para mejorar soluciones existentes.
- `metaheurísticas.py`: Implementación de la metaheurística **Iterated Local Search (ILS)**.

---

## Ejercicio 1: Heurísticas Golosas

Se implementaron cuatro estrategias para generar caminos iniciales:

1. **Ciudad más cercana**: visita la ciudad más cercana desde la última visitada.
2. **Llegada más cercana**: elige la ciudad a la que es más barato llegar.
3. **Menor distancia promedio**: combina la distancia desde la ciudad actual con la distancia promedio del destino al resto de las no visitadas.
4. **Mínimo de distancias**: evalúa dos ciudades hacia adelante, buscando el menor costo acumulado.

---

## Ejercicio 2: Búsqueda Local

Se aplicaron cuatro operadores para mejorar una solución inicial:

1. **Relocate**: mueve nodos a nuevas posiciones si mejora el costo.
2. **Swap**: intercambia posiciones de dos nodos y acepta los cambios que mejoran el recorrido.
3. **2-opt**: reordena segmentos del camino para eliminar cruces y mejorar la solución.
4. **2-opt mejorado**: aplica 2-opt sobre la mejor solución encontrada hasta el momento.

Todos los operadores reciben una solución generada por una heurística como punto de partida.

---

## Ejercicio 3: Metaheurística - Iterated Local Search (ILS)

La estrategia consiste en:

- Perturbar la mejor solución encontrada (por ejemplo con `relocate` o `swap`).
- Volver a aplicar la heurística para obtener una nueva solución.
- Repetir el proceso durante varias iteraciones y quedarse con el mejor resultado.

Se trabajó con dos enfoques:
- Uno que perturba siempre 6 nodos aleatorios.
- Otro que calcula el 6% del tamaño de la instancia para determinar cuántos nodos alterar.

---

## Objetivo Final

Comparar el rendimiento de las heurísticas y operadores:
- En tiempo de ejecución.
- En calidad de las soluciones obtenidas.
- En cómo se acercan al óptimo global en instancias complejas.

---
 Este proyecto fue desarrollado con fines educativos para el estudio de estrategias de optimización combinatoria.
