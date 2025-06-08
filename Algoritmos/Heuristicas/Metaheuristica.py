from typing import List
import random
import Busquedas_locales as bl
import Leer_archivo as leer_archivo
import Heuristicas_golosas as res

####### 1era versión ######
#Hacemos swap de 6 nodos de la instancia sin importar su tamaño

#Implementamos ILS

def swap_no_minimo(camino, data): #O(|V|)
  camino_nuevo=(camino[0].copy(), camino[1]) #O(|V|)
  nodos_random=random.sample(range(len(camino[0])),6) #O(1)
  #Elegimos 6 nodos random y los swapeamos entre si para realizar la perturbación.
  camino_nuevo[0][nodos_random[0]], camino_nuevo[0][nodos_random[3]] = camino_nuevo[0][nodos_random[3]], camino_nuevo[0][nodos_random[0]] #O(1)
  camino_nuevo[0][nodos_random[2]], camino_nuevo[0][nodos_random[4]] = camino_nuevo[0][nodos_random[4]], camino_nuevo[0][nodos_random[2]] #O(1)
  camino_nuevo[0][nodos_random[5]], camino_nuevo[0][nodos_random[1]] = camino_nuevo[0][nodos_random[1]], camino_nuevo[0][nodos_random[5]] #O(1)
  costo_nuevo = bl.calcular_costo(data, camino_nuevo[0]) #O(|V|)
  return (camino_nuevo[0], costo_nuevo) #O(1)


def romper(camino, data): #O(|V|^2) Función que rompe el camino actual para cambiar de vecindario.
  nuevo_camino=(camino[0].copy(), camino[1]) #O(|V|)
  for i in range(len(camino[0])): #O(|V|)
    nuevo_camino=swap_no_minimo(camino, data) #O(|V|)
  return nuevo_camino #O(1)


def ils_atsp(solucion, cant_iteraciones, data): #O(cant_iteraciones*|V|^3)
  mejor_actual=solucion[0].copy() #O(|V|)
  minimo_costo=solucion[1] #O(1)
  costo_nuevo=10e10 #O(1)
  camino_nuevo=(solucion[0].copy(),solucion[1]) #O(|V|)
  #Por una cantidad determinada de iteraciones vamos a ir perturbando la solución actual y
  #realizando un operador de BL para ver si podemos encontrar una mejora en los distintos vecindarios
  for iter in range(cant_iteraciones): #O(cant_iteraciones)
    busqueda_local=bl.relocate(camino_nuevo, data) #O(|V|^3) buscamos optimos
    if busqueda_local[1]<minimo_costo: #O(1)
      minimo_costo=busqueda_local[1] #O(1)
      mejor_actual=busqueda_local #O(1)
    camino_nuevo=romper(mejor_actual, data) #O(|V|^2) cambiamos de vecindario
  return mejor_actual #O(1)


####### 2nda versión ######

#Es una versión de ILS que swapea un 6% de las ciudades de cada instancia o mínimo 2 de ellas.

def swap_no_minimo2(camino, data, porcentaje=0.06): #O(|V|)
    camino_nuevo = (camino[0].copy(), camino[1]) #O(|V|)
    num_nodos = len(camino[0]) #O(1)
    # Calcular la cantidad de nodos a intercambiar basado en el porcentaje
    cantidad_nodos = max(2, int(porcentaje * num_nodos)) #O(1)
    # Asegurarse de que la cantidad de nodos a intercambiar no exceda el número de nodos disponibles
    cantidad_nodos = min(cantidad_nodos, num_nodos) #O(1)
    nodos_random = random.sample(range(num_nodos), cantidad_nodos) #O(1)
    # Realizar los intercambios en pares
    for i in range(0, len(nodos_random) - 1, 2): #O(|V|)
        camino_nuevo[0][nodos_random[i]], camino_nuevo[0][nodos_random[i + 1]] = camino_nuevo[0][nodos_random[i + 1]], camino_nuevo[0][nodos_random[i]] #O(1)
    # Calcular el nuevo costo
    nuevo_costo = bl.calcular_costo(data, camino_nuevo[0]) #O(|V|)
    camino_nuevo = (camino_nuevo[0], nuevo_costo) #O(1)  # Actualizar la tupla con el nuevo costo
    return camino_nuevo #O(1)

def romper2(camino, data): #O(|V|^2) Función que rompe el camino actual para cambiar de vecindario.
  nuevo_camino=(camino[0].copy(), camino[1]) #O(|V|)
  for i in range(len(camino[0])): #O(|V|)
    nuevo_camino=swap_no_minimo2(camino, data) #O(|V|)
  return nuevo_camino #O(1)

def ils_atsp_promedio(solucion, cant_iteraciones, data): #O(|V|) #Es semejante al anterior, solo cambia la manera en la que elegimos los nodos a swapear al perturbar el camino.
  mejor_actual=solucion[0].copy() #O(|V|)
  minimo_costo=solucion[1] #O(1)
  costo_nuevo=10e10 #O(1)
  camino_nuevo=(solucion[0].copy(),solucion[1]) #O(|V|)

  for iter in range(cant_iteraciones):
    busqueda_local=bl.relocate(camino_nuevo, data) #O(|V|^3)
    if busqueda_local[1]<minimo_costo: #O(1)
      minimo_costo=busqueda_local[1] #O(1)
      mejor_actual=busqueda_local #O(1)
    camino_nuevo=romper2(mejor_actual, data) #O(|V|^2)
  return mejor_actual #O(1)




############################################### SOLO LO USAMOS PARA LA EXPERIMENTACIÓN ########################################
def relocate_no_minimo(camino, data): #O(|V|*log(|V|))
    camino_nuevo = (camino[0].copy(), camino[1])  # O(|V|)
    longitud_camino = len(camino[0]) # O(1)
    # Seleccionar 3 nodos aleatorios
    nodos_random = random.sample(range(longitud_camino), 3)  # O(1)
    # Seleccionar 3 posiciones aleatorias
    posiciones_random = random.sample(range(longitud_camino), 3)  # O(1)
    # Extraer los nodos seleccionados
    nodos_seleccionados = [camino_nuevo[0][i] for i in nodos_random] # O(|V|)
    # Ordenar nodos_random en orden inverso para eliminar de manera segura
    nodos_random.sort(reverse=True) # O(|V|*log(|V|))
    # Eliminar los nodos seleccionados de sus posiciones originales
    for i in nodos_random: # O(|V|)
        del camino_nuevo[0][i] # O(1)
    # Asegurarse de que las posiciones_random estén en orden
    posiciones_random.sort() # O(|V|*log(|V|))
    # Insertar cada nodo en una de las posiciones aleatorias
    for i in range(3): 
        camino_nuevo[0].insert(posiciones_random[i], nodos_seleccionados[i]) # O(|V|)
    # Calcular el nuevo costo
    costo_nuevo = bl.calcular_costo(data, camino_nuevo[0])  # O(|V|)
    return (camino_nuevo[0], costo_nuevo)  # O(1)



def ils_atsp_relocate(solucion, cant_iteraciones, data): #O(|V|^4) Es la misma idea que el anterior nada mas que en vez de usar swap usamos relocate para buscar optimos
  mejor_actual=solucion[0].copy() #O(|V|)
  minimo_costo=solucion[1] #O(1)
  camino_nuevo=(solucion[0].copy(),solucion[1]) #O(|V|)
  for iter in range(cant_iteraciones):#O(|V|)
    busqueda_local=bl.relocate(camino_nuevo, data) #O(|V|^3)
    if busqueda_local[1]<minimo_costo: #O(1)
      minimo_costo=busqueda_local[1] #O(1)
      mejor_actual=busqueda_local #O(1)
    camino_nuevo=romper(mejor_actual, data) #O(|V|^2)
  return mejor_actual #O(1)


archivo = "br17.atsp"  # Reemplazar con la ruta de tu archivo

data = leer_archivo.leer_datos(archivo)
resultado_aproximado1 = res.ciudad_mas_cercana(0,data)
resultado_aproximado2 = res.llegada_mas_cercana(0,data)
resultado_aproximado3 = res.menor_promedio(0,data)
resultado_aproximado4 = res.minimo_de_distancias(0,data)
