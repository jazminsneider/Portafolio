from typing import List
import random
def leer_datos(archivo: str) -> List[List[int]]:
    with open(archivo, 'r') as file:
        lines = file.readlines()

    dimension = 0
    data = []
    leer_matriz = False

    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            dimension = int(line.split()[-1])
        elif leer_matriz:
            if line == 'EOF':
                break
            data.extend(map(int, line.split()))
        elif line == 'EDGE_WEIGHT_SECTION':
            leer_matriz = True

    # Construimos la matriz de adyacencia con pesos
    matriz = []
    indice = 0
    for i in range(dimension):
        fila = data[indice:indice + dimension]
        matriz.append(fila)
        indice += dimension
    return matriz

