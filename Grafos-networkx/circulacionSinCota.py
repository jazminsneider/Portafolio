import json
import networkx as nx
import matplotlib.pyplot as plt
import math
from typing import List


#Leemos los datos del archivo pasado por parámetro
def cargar_datos(archivo:str):
	filename = archivo
	with open(filename) as json_file:
		data = json.load(json_file)

	horariosRetiro:list[float]=[]
	horariosTigre:list[float]=[]
	demandaHorarios={}
	#Recorremos todos los trenes del día
	for service in data["services"]:
		#Por un lado nos gurdamos en variables los datos del tren en cuestión, es decir, su lugar de orgen (la salida), su lugar de destino (llegada), la demanda del mismo y la capacidad de sus vagones
		salida = data["services"][service]["stops"][0]
		llegada = data["services"][service]["stops"][1]
		demanda = data["services"][service]["demand"][0]
		capacidad = data["rs_info"]["capacity"]
		#Agregamos los horarios de salida/llegada a sus respectivas estaciones, es decir en las variables horariosRetiro y horariosTigre. Esto lo hacemos para luego ordenar los horarios en orden creciente.
		#Creamos un diccionario que tiene los datos de salida/llegada de un tren y los asocia con la cantidad de vagones necesarios para satisfacer la demanda del horario. Lo hacemos para guardarnos los imbalances que luego irán a los nodos
		#Aquella estación que recibe (nodo) tiene un valor negativo asociado y la que envía tiene uno positivo

		#Está más detallado en el informe. Pero también consideramos casos particulares en los que 2 trenes llegan y salen de una estación al mismo tiempo.
		#Pensamos que en la práctica no debería de tener sentido que los vagones de un tren que, por ejemplo, llega a las 9 a Retiro sean reutilizados para un tren que sale a las 9 de la estación. 
		#Para evitar este traspaso entre los nodos de la estación hicimos que los nodos de salida se posicionaran encima de los que son de llegada a la misma hora, restandoles un 0,1. O en el caso de que se guarde primero el nodo de salida, sumandole un 0,1 al de llegada.
		#De esta manera al hacer el sort en las listas nuestros nodos quedan ordenados como queremos
		#Si la estación de salida es Retiro
		if(salida["station"]=="Retiro"):

			#Si ya se agregó un nodo de llegada en ese horario
			if salida["time"] in horariosRetiro:
				#Le restamos 0,1 para que se posicione por encima del que llega a la misma hora y no reutilice esos vagones
				#se modifica el dato en la variable data pero no en el json
				salida["time"] = salida["time"] - 0.1
				horariosRetiro.append(salida["time"])
				#Asociamos el tren de salida a su catidad de vagones demandados
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)

			#Si no hay otro tren en ese horario entonces lo guarda normal
			else:
				horariosRetiro.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)

			#Si ya se agregó un nodo de salida en ese horario
			if llegada["time"] in horariosTigre:
				#le sumamos 0,1 al horario del tren de llegada para que se posicione por debajo del de salida
				#se modifica el dato en la variable data pero no en el json
				llegada["time"] = llegada["time"] + 0.1
				horariosTigre.append(llegada["time"])
				#Asociamos el tren a su cantidad de vagones demandados
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)
			#Si no hay otro tren en ese horario, lo guarda normal
			else:
				horariosTigre.append(llegada["time"])
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)

		#Si la estación de salida es Tigre
		
		else:
			#Los horarios se guardan igual que en retiro.
			if salida["time"] in horariosTigre:
				#se modifica el dato en la variable data pero no en el json
				salida["time"] = salida["time"] - 0.1
				horariosTigre.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)
			else:
				horariosTigre.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)

			if llegada["time"] in horariosRetiro:
				#se modifica el dato en la variable data pero no en el json
				llegada["time"] = llegada["time"] + 0.1
				horariosRetiro.append(llegada["time"])
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)
			else:
				horariosRetiro.append(llegada["time"])
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)

	#Ordenamos los horarios
	horariosRetiro.sort()
	horariosTigre.sort()
	return (horariosRetiro,horariosTigre,data,demandaHorarios)


def armar_grafo(horariosRetiro,horariosTigre,data,demandaHorarios):

	inf=10e10
	G=nx.DiGraph()
	#Esta lista va a contener todos los trenes que salen y llegan a Tigre en orden cronológico
	trenesRetiro = []
	#Esta lista va a contener todos los trenes que salen y llegan a Retiro en orden cronológico
	trenesTigre = []

	#Para todos los horarios busca su tren con la cantidad de vagones asociada.
	#Como los horarios de Retiro están en orden entonces se van a ir agregando en orden al grafo y a la lista de trenesRetiro
	for elem in horariosRetiro:
		for clave in demandaHorarios:
			if(str(elem) in clave and "Retiro" in clave):
				#Creamos el nodo con el tren y su demanda de vagones, el mismo va a tener el horario, la estación y el tipo del tren.
				G.add_node(clave,demand=demandaHorarios[clave])
				#Podría suceder que tenga más de 1 tren en retiro a la misma hora, por eso antes de agregarlo a la lista se fija si ya lo agregó para que no haya repetidos
				if(clave not in trenesRetiro):
					trenesRetiro.append(clave)


	#Agrego las aristas entre los nodos de los trenes de Retiro.
	#Les ponemos peso 0, capacidad infinito y cota inferior 0 (datos del enunciado)
	for tren in range(len(trenesRetiro)-1):
		G.add_edge(trenesRetiro[tren],trenesRetiro[tren+1],weight=0,capacity=inf,lower_bound=0)

	#Agregamos arista que va desde el ultimo nodo de retiro al 1ero de la misma estación
	#Le ponemos cota inferior 0, capacidad inifinito y peso 1. El peso nos va a ayudar a contabilizar la cantidad de  vagones que se necesitan en la cabecera al inicio del día
	G.add_edge(trenesRetiro[-1],trenesRetiro[0],weight=1,capacity=inf,lower_bound=0)

	#Agregamos los nodos de la estación de tigre
	for elem in horariosTigre:
		for clave in demandaHorarios:
			if(str(elem) in clave and "Tigre" in clave):
				G.add_node(clave,demand=demandaHorarios[clave])
				if(clave not in trenesTigre):
					trenesTigre.append(clave)


	#Agregamos aristas entre trenes de tigre
	for tren in range(len(trenesTigre)-1):
		G.add_edge(trenesTigre[tren],trenesTigre[tren+1],weight=0,capacity=inf,lower_bound=0)
	#Agregamos arista que va desde el ultimo nodo de tigre al 1ero de la misma estación
	G.add_edge(trenesTigre[-1],trenesTigre[0],weight=1,capacity=inf,lower_bound=0)

    #Agregamos aristas diagonales
	for service in data["services"]:
		#si tenemos nodos modificados (+/- 0.1) están guardados en data así que las aristas diagonales se hacen bien
		salida = data["services"][service]["stops"][0]
		llegada = data["services"][service]["stops"][1]
		#Les ponemos peso 0, cota inferior 0 y una cota superior que está en el archivo.json, esta es la cantidad máxima de vagones que se pueden enviar de una estación a otra
		G.add_edge(str(salida),str(llegada),weight=0,capacity=data["rs_info"]["max_rs"])
	#GRAFICAMOS
	pos={}
	for i in range(len(trenesRetiro)):
		pos[trenesRetiro[len(trenesRetiro)-i-1]]=(0,i)
		pos[trenesTigre[len(trenesTigre)-i-1]]=(1,i)
	nx.draw(G,pos, node_size=1000,node_color="green",with_labels=True,font_weight="bold")
	return G, trenesTigre,trenesRetiro

#Corremos el algoritmo de costo mínimo
def circulacionMaterialRodante(archivo:str):
	#Cargamos los datos y creamos el grafo
	datos=cargar_datos(archivo)
	grafo,trenesTigre,trenesRetiro=armar_grafo(datos[0],datos[1],datos[2],datos[3])

	#Corremos el algoritmo sobre el grafo
	flujoTotal,flujoAristas=nx.capacity_scaling(grafo, demand='demand', weight='weight')
	#Imprimimos la cantidad de vagones totales necesarios para satisfacer la demanda a lo largo del día
	print("Unidades requeridas en total: "+str(flujoTotal))
	#Agarramos los primeros y últimos nodos de las estaciones de Retiro y de Tigre:
	primerotigre = trenesTigre[0]
	ultimotigre =  trenesTigre[-1]
	primeroretiro = trenesRetiro[0]
	ultimoretiro = trenesRetiro[-1]
	#printeamos el flujo que corre por las aristas de trasnoche, esto son la cantidad de vagones que se necesitan por cabecera al inicio del día
	print("Unidades requeridas para Tigre: "+str(flujoAristas[ultimotigre][primerotigre]))
	print("Unidades requeridas para Retiro: " + str(flujoAristas[ultimoretiro][primeroretiro]))




