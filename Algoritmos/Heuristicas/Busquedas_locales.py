from typing import List
import random
import Heuristicas_golosas as resultado_inicial
import Leer_archivo as leer_archivo

#Esta es una función auxiliar que nos ayuda a calcular el costo del camino pasado por parámetro
def calcular_costo(data, camino): #O(|V|)
  costo=0 #O(1)
  for nodo in range(len(camino)-1): #O(|V|-1)=O(|V|)
    #Sumamos la distancia del nodo actual al siguiente 
    costo += data[camino[nodo]][camino[nodo+1]] #O(1)
  #Sumamos la distancia de la última ciudad a la primera
  costo+=data[camino[-1]][camino[0]] #O(1)
  return costo #O(1)

#######1era búsqueda local######## 

#swap. Swapeamos a todos los nodos con todos los nodos y nos quedamos con el camino menos costoso

#A esta función auxuliar le pasamos por parámetro el camino inicial junto con su costo, y el nodo a swapear proporcionado por la función swap junto con los datos de la instancia
def swap_aux(inicial, data,nodo_a_swapear): #O(|V|^2)
  camino_inicial=inicial[0] #O(1)
  costo=inicial[1] #O(1)
  camino_nuevo=camino_inicial.copy() #O(|V|)
  camino_mejor = camino_inicial.copy() #O(|V|)
  #Intercambiamos el nodo pasado por parámetro y nos quedamos con el camino de menos distancia
  for nodo in range(len(camino_inicial)): #O(|V|)
    #Intercambiamos los nodos
    camino_nuevo[nodo],camino_nuevo[nodo_a_swapear]=camino_nuevo[nodo_a_swapear],camino_nuevo[nodo] #O(1)
    #Si este nuevo camino tiene un costo menor, entonces me quedo con este,
    if(calcular_costo(data,camino_nuevo)<costo): #O(|V|)
      camino_mejor=camino_nuevo #O(1)
      costo=calcular_costo(data,camino_nuevo) #O(|V|)
    #Reiniciamos al camino original para intercambiar con otros nodos
    camino_nuevo=camino_inicial.copy() #O(|V|)
  #devolvemos el mejor camino encontrado
  return camino_mejor,costo #O(1)


def swap(inicial, data): #O(|V|^3)
  camino_nuevo=inicial[0] #O(1)
  costo_nuevo=inicial[1] #O(1)
  mejor_camino=inicial[0] #O(1)
  mejor_costo=inicial[1] #O(1)
  nodo = 0 #O(1)
  #Miro todas las ciudades del camino y las envío a swap aux para ser intercambiadas con todos los otros
  while nodo < len(inicial[0]): #O(|V|)
   camino_nuevo,costo_nuevo=swap_aux(inicial,data,nodo) #O(|V|^2)
   #Nos quedamos con aquel camino que tenga menor distancia
   if(costo_nuevo<mejor_costo): #O(1)
      mejor_camino=camino_nuevo #O(1)
      mejor_costo=costo_nuevo #O(1)
   nodo += 1 #O(1)
  #devolvemos el mejor camino encontrado
  return mejor_camino,mejor_costo #O(1)


#######2da búsqueda local######## 

#Relocate. Implementamos un algoritmo que hace relocate con todos los nodos en todas las posiciones del camino

#Esta función auxiliar se encarga de insertar al nodo pasado por parámetro en casa posición del camino y quedarse con la mejor respuesta, es decir aquella que de la menor distancia en general.
def relocate_aux(inicial, data, relocatear):#O(|V|^2)
  costo=inicial[1] #O(1)
  camino_nuevo=inicial[0].copy() #O(|V|)
  mejor_camino=inicial[0].copy() #O(|V|)
  costo_nuevo=costo #O(1)
  #insertamos a ese nodo en las posiciones disponibles
  for nodo in range(len(inicial[0])): #O(|V|)
    #eliminamos el nodo al que le vamos a hacer relocate
    camino_nuevo.pop(relocatear) #O(|V|)
    #insertamos a ese nodo en las posiciones disponibles, todas las otras ciudades se corren a la derecha en el camino nuevo
    camino_nuevo.insert(nodo,inicial[0][relocatear]) #O(|V|)
    costo_nuevo=calcular_costo(data,camino_nuevo) #O(|V|)
    #Si el costo del camino al que le hice relocate es menor, me quedo con este
    if costo_nuevo<costo: #O(1)
      costo=costo_nuevo #O(1)
      mejor_camino=camino_nuevo.copy() #O(|V|)
    #Reinicio al camino inicial para analizar qué sucede si pongo ese nodo en otra posición
    camino_nuevo=inicial[0].copy() #O(|V|)
  return mejor_camino, costo #O(1)

def relocate(inicial, data):#O(|V|^3)
  minimo = inicial[1] #O(1)
  mejor_camino = inicial[0] #O(1)
  nuevo_camino = inicial[0] #O(1)
  costo = 10e10 #O(1)
  nodo = 0 #O(1)
  #Hacemos relocate de todos los nodos de camino
  while nodo < len(inicial[0]): #O(|V|)
    nuevo_camino, costo  = relocate_aux(inicial,data,nodo) #O(|V|^2)
    #Comparo los distintos relocates mejores y me quedo con el que menor distancia tenga en total
    if(costo < minimo): #O(1)
      mejor_camino = nuevo_camino #O(1)
      minimo = costo #O(1)
    nodo += 1 # O(1)
  return mejor_camino, minimo #O(1)
#######3era búsqueda local########
#2opt común
def _2opt(inicial, data,i,k): #O(|V|^2)
  # asignamos j y l como los proximos nodos de i y k respectivamente
  if(i == len(inicial[0])-1): #O(1)
  # si i es el ultimo el proximo tiene que ser el primer nodo
    j = 0 #O(1)
  else:

    j=i+1 #O(1)

  if(k == len(inicial[0])-1): #O(1)
  # si i es el ultimo el proximo tiene que ser el primer nodo
    l = 0 #O(1)
  else:
    l=k+1 #O(1)

  camino=inicial[0] #O(1)
  costo=inicial[1] #O(1)
  camino_nuevo=[] #O(1)
  mejor=inicial[0] #O(1)
  if i > k: #O(1)
        i, k = k, i #O(1)
        j, l = l, j #O(1)
  # nos aseguramos que i y k no sean consecutivos y si lo son no es valido y devuelvo el resultado inicial
  if(k == j or i==k-1 or (inicial[0][0]==inicial[0][i] and inicial[0][-1] ==inicial[0][k])): #O(1)
      return inicial #O(1)
  else: #O(1)
    camino_nuevo = camino[:i + 1] #O(|V|)
    curr=k #O(1)
    #recorro los nodos del k al i para invertir su dirrección
    while curr!=j-1: #O(|V|)
      camino_nuevo.append(camino[curr]) #O(1)
      curr-=1 #O(1)
    camino_nuevo = camino_nuevo + camino[l:] #O(|V|)
    costo_nuevo = calcular_costo(data, camino_nuevo) #O(|V|)
    #veo si el costo de este nuevo resultado es menor al inicial, si lo es, lo devuelvo si no devuelvo el resultado inicial
    if costo_nuevo < inicial[1]: #O(1)
          return camino_nuevo, costo_nuevo #O(1)
    return camino, inicial[1] #O(1)

def _2opt_global(inicial, data): #O(|V|^4)
    #guardo como mi mejor solucion a mi solucion inicial
    mejor_camino = inicial[0].copy() #O(|V|)
    costo = inicial[1] #O(1)
    mejor_costo = inicial[1] #O(1)
    #recorro todos los posibles pares de nodos
    for i in range(len(mejor_camino)): #O(|V|)
        for k in range(len(mejor_camino)): #O(|V|)
          if(k != i): #O(1)
            #siempre hacemos _2opt2 sobre la solución inicial cambiando solo los pares de nodos a usar
            nuevo_camino, nuevo_costo = _2opt((inicial[0], costo), data, i, k) #O(|V|^2)
            #veo si al usar el operador _2opt2 me devuelve un costo menor o no
            if nuevo_costo < mejor_costo: #O(1)
                mejor_camino, mejor_costo = nuevo_camino, nuevo_costo #O(1)

    return mejor_camino, mejor_costo #O(1)


#######4ta búsqueda local######## 

#2opt mejorado
def _2opt2(inicial, data,i,k): #O(|V|^2)
  if(i == len(inicial[0])-1): #O(1)
    j = 0 #O(1)
  else:
    j=i+1 #O(1)

  if(k == len(inicial[0])-1): #O(1)
    l = 0 #O(1)
  else:
    l=k+1 #O(1)

  camino=inicial[0] #O(1)
  costo=inicial[1] #O(1)
  camino_nuevo=[] #O(1)
  mejor=inicial[0] #O(1)
  if i > k: #O(1)
        i, k = k, i #O(1)
        j, l = l, j #O(1)
  if(k == j or i==k-1 or (inicial[0][0]==inicial[0][i] and inicial[0][-1] ==inicial[0][k])): #O(1)
      return inicial #O(1)
  else:
    camino_nuevo = camino[:i + 1] #O(|V|)
    curr=k #O(1)
    while curr!=j-1: #O(|V|)
      camino_nuevo.append(camino[curr]) #O(1)
      curr-=1 #O(1)
    camino_nuevo = camino_nuevo + camino[l:] #O(|V|)
    costo_nuevo = calcular_costo(data, camino_nuevo) #O(|V|)
    if costo_nuevo < inicial[1]: #O(1)
          return camino_nuevo, costo_nuevo #O(1)
    return camino, inicial[1] #O(1)

#Se hace 2 opt con la solución mejorada
def _2opt_global_mejorado(inicial, data): #O(|V|^4) Este operador funciona muy parecido al anterior salvo por una diferencia.
    mejor_camino = inicial[0].copy() #O(|V|)
    costo = inicial[1] #O(1)
    mejor_costo = inicial[1] #O(1)
    for i in range(len(mejor_camino)): #O(|V|)
        for k in range(len(mejor_camino)): #O(|V|)
          if(k != i): #O(1)
            #Esta es la diferencia clave. Vamos mejorando siempre la mejor solución encontrada en lugar de mejorar la inicial, lo que potencialmente la vuelve mas eficiente.
            nuevo_camino, nuevo_costo = _2opt2((mejor_camino, mejor_costo), data, i, k) #O(|V|^2)
            if nuevo_costo < mejor_costo: #O(1)
                mejor_camino, mejor_costo = nuevo_camino, nuevo_costo #O(1)

    return mejor_camino, mejor_costo #O(1)



#PARA CORRER LAS DISTINTAS BÚSQUEDAS LOCALES CON LAS INSTANCIAS Y RESULTADOS DE LOS GOLOSOS
archivo1 = "ft70.atsp"  # Reemplazar con la ruta de tu archivo
datos = leer_archivo.leer_datos(archivo1)
camino1 = resultado_inicial.ciudad_mas_cercana(0,datos)
camino2 = resultado_inicial.llegada_mas_cercana(0,datos)
camino3 = resultado_inicial.menor_promedio(0,datos)
camino4 = resultado_inicial.minimo_de_distancias(0,datos)

