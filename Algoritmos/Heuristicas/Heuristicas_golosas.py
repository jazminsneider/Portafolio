from typing import List
import random
import Leer_archivo as leer_archivo

#Esta función busca la ciudad más cercana no visitada a la última visitada
def minimo(vecinos, camino): # Peor de los casos O(|V|^2)
  min = 9999999 # O(1)
  pos = 0 # O(1)
  #Mira para todos los vecinos de la ciudad su distancia
  for nodo in range(len(vecinos)): #O(|V|)
    #Se queda con aquel más cercano que no perteneza a las ciudades ya visitadas, estas se encuentran en camino
    if(nodo not in camino and min > vecinos[nodo]): #O(|V|) en realidad es longitud de camino pero en el peor caso O(V), + O(1) = O(V)
      min = vecinos[nodo] #O(1)
      pos = nodo # O(1)
  #Devuelve la posicion del minimo
  return pos #O(1)


#En esta primera heuristica golosa implementamos el algoritmo de ciudad más cercana
#Nos paramos en un nodo inicial S y de ahí vamos buscando la ciudad más cercana no visitada a esta. Luego de encontrarla, esta nueva ciudad se agrega al camino recorrido y se vuelve nuestro nuevo actual
#Buscamos aquella ciudad no visitada más cercana a la última visitada y la guardamos en el recorrido.
def ciudad_mas_cercana(s:int, data): # En el peor caso O(|V|^4)
  #En la variable camino nos guardamos todads las ciudades ya visitadas
  camino = [s] #O(1)
  actual = s #O(1)
  costo=0 #O(1)
  #Iterar hasta que se hayan recorrido todas las ciudades
  while(len(camino) != len(data[actual])):#O(|V|)
    #Miro las ciudades
    for nodo in range(len(data)): #O(|V|)
        #si no fue visitada, evalúo la distancia de llegar hasta ahí desde actual
        if(nodo not in camino): #O(|V|)
          pos = minimo(data[actual],camino) #O(|V|^2)
          camino.append(pos) #O(1)
          costo+=data[actual][pos] #O(1)
          actual = pos  #O(1)
  #Sumamos el costo de la última arista 
  costo += data[actual][s] #O(1)
  return camino, costo #O(1)


#######2nda heuristica golosa########

#En llegada más cercana buscamos hacer lo mismo que ciudad más cercana pero a la inversa, estamos parados sobre un nodo actual y busco cuál es aquel nodo que llega hacia este con menor distancia y no fue visitado.
#Esto se nos ocurrió ya que ASTP es asimétrico

def llegada_mas_cercana(s:int, data): # En el peor caso O(|V|^3)
  #En la variable camino nos guardamos todads las ciudades ya visitadas
  camino = [s] #O(1)
  actual = s #O(1)
  costo=0 #O(1)
  #Mientras que hayan ciudades sin visitar
  while(len(camino) != len(data[actual])):#O(|V|)
    #reiniciamos el mínimo para que mire la distancia hacia otras ciudades
    min = 10e10 #O(1)
    pos = 0 #O(1)
    for nodo in range(len(data)): #O(|V|)
        #Si la ciudad no fue visitada y el nodo es distinto al actual evalúo su distancia hacia la ciudad actual.
        if(nodo not in camino and nodo != actual): #O(|V|)
           #Me quedo con aquella ciudad que llegue con menor distancia a mi actual
           if(data[nodo][actual] < min): #O(1)
              min = data[nodo][actual] #O(1)
              pos = nodo #O(1)
    actual = pos #O(1)
    #Como se va haciendo a la inversa, tenemos que poner los nodos al revés. Al principio de la lista, pero como en el 0 está la ciudad inicial, insertamos en la 1era posición
    camino.insert(1,pos) #O(|V|) en el peor caso
    costo += min #O(1)
  costo += data[s][pos] #O(1)
  return camino, costo #O(1)


 #######3er heuristica golosa########


def promedio(data, nodo, camino):  #O(|V|^2)
  res = 0 #O(1)
   #Miro los vecinos del candidato
  for n in range(len(data[nodo])): #O(|V|)
     #Si no visité esa ciudad, la sumo al costo de ese nodo. 
    if(n not in camino and n!=nodo):  #O(|V|) en el peor caso
      res += data[nodo][n] #O(1)
   #Realizamos un promedio del costo
  res = res/(len(data)-len(camino)) #O(1)
  return res #O(1)

 #En esta heuristica golosa hicimos un algoritmo que elije la ciudad que tenga la menor suma de su distancia a la actual sumada al promedio de su distancia a todas las no visitadas
 #La ciudad actual es la última visitada
def menor_promedio(s:int, data): #O(|V|^4)
  camino = [s] #O(1)
  actual = s #O(1)
  costo=0 #O(1)
  while(len(camino) != len(data[actual])): #O(|V|)
    #Reiniciamos el promedio para los próximos candidatos
    menor_promedio = 1100000000 #O(1)
    menor_nodo = 0 #O(1)
    for nodo in range(len(data)): #O(|V|)
      #si la ciudad no fue visitada la evalúo como posible próxima
      if nodo not in camino: #O(V) en el peor caso
        #miro el promedio de distancias hacia todas las otras
        prom_actual = promedio(data,nodo,camino) #O(|V|^2)
        if( prom_actual + data[actual][nodo] < menor_promedio): #O(1)
          menor_nodo = nodo #O(1)
          menor_promedio = prom_actual + data[actual][nodo] #O(1)
    camino.append(menor_nodo) #O(1)
    costo += data[actual][menor_nodo] #O(1)
    actual = menor_nodo #O(1)
  costo += data[actual][s] #O(1)
  return camino,costo #O(1)


#######4ta heuristica golosa########
#En esta heiuristica buscamos visitar aquella ciudad cuya distancia sumada al visitar una ciudad no vista antes más cercana
#Mira 2 ciudades a futuro

#Esta función nos ayuda a encontrar la distancia hacia la ciudad más cercana no visitada desde un nodo
def min_aux(data, nodo, camino): #O(|V|^2)
    minimo = 10e10 #O(1)
    for i in range(len(data)): #O(|V|)
        if i not in camino and i != nodo: #O(|V|)
            minimo = min(minimo, data[nodo][i]) #O(1)
    return minimo #O(1)

def minimo_de_distancias(s, data): #O(|V|^4)
    #El camino recorrido
    camino = [s] #O(1)
    actual = s #O(1)
    costo = 0 #O(1)
    ultimo_nodo = 0 #O(1)
    #Mientras que no se hayan visitado todas las ciudades
    while len(camino) < len(data): #O(|V|)
        min_costo = 10e10 #O(1)
        proximo_nodo = -1 #O(1)
        for nodo in range(len(data)): #O(|V|)
            #Si la ciudad todavía no se visitó entonces evalúo su distancia
            if nodo not in camino: #O(|V|)
                # Calcula el costo del nodo actual al nodo candidato y su mínimo costo a otras ciudades no visitadas
                costo_parcial = data[actual][nodo] + min_aux(data, nodo, camino) #O(1)+O(V^2)=O(V^2)
                #Si encontré un nodo de menor distancia me lo quedo
                if costo_parcial < min_costo: #O(1)
                    min_costo = costo_parcial #O(1)
                    proximo_nodo = nodo #O(1)
                #Nos guardamos la última ciudad visitada
                ultimo_nodo = nodo #O(1)
        #Si ya todas las ciudades fueron visitadas entonces me queda el último nodo
        if proximo_nodo == -1: #O(1)
            proximo_nodo = ultimo_nodo #O(1)
        camino.append(proximo_nodo) #O(1)
        #Sumamos el costo del próximo nodo
        costo += data[actual][proximo_nodo] #O(1)
        actual = proximo_nodo #O(1)
    #Sumamos el costo de la última arista
    costo += data[actual][s] #O(1)
    return camino, costo #O(1)



#PARA CORRER LOS DISTINTOS ALGORITMOS GOLOSOS CON LAS INSTANCIAS
archivo = "ft70.atsp"  # Reemplazar con la ruta de tu archivo

data = leer_archivo.leer_datos(archivo)
resultado_aproximado1 = ciudad_mas_cercana(0,data)
resultado_aproximado2 = llegada_mas_cercana(0,data)
resultado_aproximado3 = menor_promedio(0,data)
resultado_aproximado4 = minimo_de_distancias(0,data)
