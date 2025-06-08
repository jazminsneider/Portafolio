from funciones_auxiliares import *

#función auxiliar solo para programación dinámica
def minimo(superdict, x: int, largo_y, k: int):
  min = 10e10
  y_ultima: int = 0
  for y in range(largo_y): #dado que sabemos que la solución óptima está en el diccionario guardada con la clave x=len(grilla_x)-1 y breakpoints=(breakpoints pedidos)-1, busca la mínima por todo el rango y.
    if superdict[(x, y, k)][0] < min:
      min = superdict[(x, y, k)][0]
      y_ultima = y
  return min, superdict[(x, y_ultima, k)][1], y_ultima


def breakpointsAuxPD(breakpoints, grillax, grillay, superdiccionario, npuntos):
  #Para poder acceder a los errores anteriores inicialmente cargamos los errores que genera ubicar un único breakpoint al principio de la grilla_x. 
  #Consideramos que al ser un único punto, el error del mismo es la diferencia entre el primer punto y el y de la grilla que elegí
  reconstruir_aux = []
  for y in range(len(grillay)):
    errorInicial = abs(npuntos[1][0] - grillay[y])
    superdiccionario[(0, y, 0)][0] = errorInicial
  #creamos a y b como auxiliares. Ahí vamos a guardar los valores de las posiciones de las grillas que generan el mínimo error en cada caso
  a = 0
  b = 0
  #La idea de estos ciclos es generar una manera de comparar una x e y donde estamos parados, y para esos valores, comparar el error que generan estos puntos si se lo agregamos a los anteriores ya calculados
  #X e Y representarían un nuevo punto del cual no conozco el error al agregarlo coomo breakpoint, pero sí conozco los anteriores, representados por xi e yi.
  #Esto lo hacemos para cada breakpoint
  for k in range(1, breakpoints):
    for x in range(1, len(grillax)):
      for y in range(len(grillay)):
        #Luego de encontrar el (x;y) optimo para xi yi, volvemos a cambiar el error para encontrar el próximo minimo
        min_error = 1e10
        #Generamos un xi que representa todos los puntos de la grillax ya recorridos, con un valor agregado. Con este queremos trazar una función lineal entre (xi;yi) y (x,y) y encontrar aquella que genere el minimo error entre todas
        for xi in range(0, x):
          for yi in range(len(grillay)):
            #Calculamos el error de unir el punto (xi;yi) con (x;y)
            error_aux = error((grillax[xi], grillay[yi]), (grillax[x], grillay[y]), npuntos)
            #Encontramos el error de llegar a este nuevo punto en base a todos los puntos anteriores a ese.
            #Es decir, sumamos los errores anteriores + el nuevo error de unir el punto x;y
            error_total = error_aux + superdiccionario[(xi, yi, k - 1)][0]
            #ahora que tenemos el error total del nuevo camino que contiene el punto (x;y) vemos si este trazo es el que genera un mínimo error
            #Si hay un camino que tiene menor error que aquel encontrado anteriormente como mínimo, lo actualizamos
            if error_total < min_error:
              #Nos guardamos el nuevo error mínimo y además la posición en la que fue encontrado
              min_error, a, b = error_total, xi, yi
              #A su vez buscamos el camino para llegar a ese mínimo
              reconstruir_aux = superdiccionario[(xi, yi, k - 1)][1]
              
          #Una vez recorridas todas las xi anteriores y encontrada la que genera un trazo de error mínimo. Agregamos este nuevo valor mínimo a nuestro diccionario junto con el camino hacia ella, es decir, el camino hacia el anterior + los puntos del nuevo mínimo.
          superdiccionario[(x, y, k)] = [min_error, reconstruir_aux[:] + [(a, b)]]
  #Buscamos el mínimo del superdiccionario. Sabemos que el mínimo optimo tiene que estar en la posición x = len(grillax)-1 ya que si o si debe haber un breakpoint en la ultima posicion de la grillax. Además, sabemos que ese valor debe estar en breakpoints-1 (el -1 ya que consideramos breakpoints como posiciones) dentro del diccionario ya que significa que es el valor donde tengo todos mis breakpoints y también estoy al final de la grilla x. Entonces solo debemos iterar en las ys para encontrar cuál es la que contiene el ultimo breakpoint.
  #Buscamos el mínimo de nuestro diccionario. Sabemos que este resultado tiene que estar en el último punto de la grilla x y en el último breakpoint. (hacemos breakpoints-1 ya que los contamos desde 0 hasta breakpoints-1). Lo que nos falta recuperar es la y que genera ese valor mínimo. Mínimo nos va a devolver el error mínimo encontrado al final del map, el camino recorrido para llegar hasta ese punto (indicado por posiciones en grilla_x y grilla_y), y la posición de la y del último breakpoint
  posiciones_solucion = minimo(superdiccionario,len(grillax) - 1, len(grillay), breakpoints - 1)
  
  solucion = []
  #Como tenemos el camino marcado por posiciones en la grilla, ahora reconstruimos la solución con sus respectivos valores.
  for elem in posiciones_solucion[1]:
    solucion.append((grillax[elem[0]], grillay[elem[1]]))
  #Agregamos el último breakpoint, ya que si bien teníamos el camino hacia el mismo, no está agregado en el for.
  solucion.append((grillax[-1], grillay[posiciones_solucion[2]]))
  #Devolvemos el error y su respectiva solución
  return posiciones_solucion[0], solucion

#esta función llena todas las posiciones que vamos a usar del diccionario con un error muy grande y listas vacias
def inicializar(breakpoints: int, m1: int, m2: int):
  superdiccionario = {}
  inf: float = 10e10
  for k in range(breakpoints):
    for i in range(m1):
      for j in range(m2):
        superdiccionario[(i, j, k)] = [inf, []]
  return superdiccionario


def breakpointsPD(archivo: str, breakpoints: int, m1: int, m2: int):
  puntosEnX: List[float] = leer_datos(archivo)[0]
  puntosEnY: List[float] = leer_datos(archivo)[1]
  grilla_x: List[float] = armar_grilla(puntosEnX, puntosEnY, m1, m2)[0]
  grilla_y: List[float] = armar_grilla(puntosEnX, puntosEnY, m1, m2)[1]
  superdiccionario = inicializar(breakpoints, m1, m2)

  return breakpointsAuxPD(breakpoints, grilla_x, grilla_y, superdiccionario,
               (puntosEnX, puntosEnY))
