import json
import networkx as nx
import matplotlib.pyplot as plt
import math

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

		clave1:str = str(salida)
		clave2:str = str(llegada)

		#Agregamos los horarios de salida/llegada a sus respectivas estaciones. Esto lo hacemos para luego ordenar los horarios en orden creciente.
		#Creamos un diccionario que tiene los datos de salida/llegada de un tren y los asocia con la cantidad de vagones necesarios para satisfacer la demanda del horario. Lo hacemos para guardarnos los imbalances que luego irán a los nodos
		#Aquella estación que recibe (nodo) tiene un valor negativo asociado y la que envía tiene uno positivo
		#Si la estación de salida es Retiro

		if(salida["station"]=="Retiro"):
			if salida["time"] in horariosRetiro:
				salida["time"] = salida["time"] - 0.1
				horariosRetiro.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)
			else:
				horariosRetiro.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)

			if llegada["time"] in horariosTigre:
				horariosTigre.append(llegada["time"]+ 0.1)
				llegada["time"] = llegada["time"] + 0.1
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)
			else:
				horariosTigre.append(llegada["time"])
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)

		#Si la estación de salida es Tigre

		else:

			if salida["time"] in horariosTigre:
				salida["time"] = salida["time"] - 0.1
				horariosTigre.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)
			else:
				horariosTigre.append(salida["time"])
				demandaHorarios[str(salida)]=math.ceil(demanda/capacidad)

			if llegada["time"] in horariosRetiro:
				horariosRetiro.append(llegada["time"]+0.1)
				llegada["time"] = llegada["time"] + 0.1
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)
			else:
				horariosRetiro.append(llegada["time"])
				demandaHorarios[str(llegada)]=-math.ceil(demanda/capacidad)

	#Ordenamos los horarios
	horariosRetiro.sort()
	horariosTigre.sort()
	return (horariosRetiro,horariosTigre,data,demandaHorarios)


def armar_grafo(horariosRetiro,horariosTigre,data,demandaHorarios,cota,estacion):

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

    #Agregamos aristas diagonales
	for service in data["services"]:
		salida = data["services"][service]["stops"][0]
		llegada = data["services"][service]["stops"][1]
		#Les ponemos peso 0, cota inferior 0 y una cota superior que está en el archivo.json, esta es la cantidad máxima de vagones que se pueden enviar de una estación a otra
		G.add_edge(str(salida),str(llegada),weight=0,capacity=data["rs_info"]["max_rs"])

	#Por último agregamos las aristas que van desde la última parada de la estación a la primera.
	#Además, le ponemos a aquella estación solicitada por el usuario su cota en la arista que va del último nodo al primero de la misma.
	#Agregamos una arista que va desde la última estación pasada por parámetro hacia la cabecera de la otra con un costo superior a las otras. Esto lo hacemos para que el algortimo, que busca el costo mínimo elija esa ruta solamente si excede la capacidad de la arista.
	if(estacion=="Retiro"):
		G.add_edge(trenesRetiro[-1],trenesRetiro[0],weight=1,capacity=cota,lower_bound=0)
		G.add_edge(trenesRetiro[-1],trenesTigre[0],weight=2,capacity=inf,lower_bound=0)
		G.add_edge(trenesTigre[-1],trenesTigre[0],weight=1,capacity=inf,lower_bound=0)
	else:
		G.add_edge(trenesTigre[-1],trenesTigre[0],weight=1,capacity=cota,lower_bound=0)
		G.add_edge(trenesTigre[-1],trenesRetiro[0],weight=2,capacity=inf,lower_bound=0)
		G.add_edge(trenesRetiro[-1],trenesRetiro[0],weight=1,capacity=inf)
	#GRAFICAMOS
	pos={}
	for i in range(len(trenesRetiro)):
		pos[trenesRetiro[len(trenesRetiro)-i-1]]=(0,i)
		pos[trenesTigre[len(trenesTigre)-i-1]]=(1,i)
	nx.draw(G,pos, node_size=1000,node_color="green",with_labels=True,font_weight="bold")
	return G, trenesTigre,trenesRetiro,estacion


def circulacionMaterialRodanteCota(archivo:str,cota:int,estacion:str):
	#Cargamos los datos y creamos el grafo
	datos=cargar_datos(archivo)
	grafo,trenesTigre,trenesRetiro,estacion=armar_grafo(datos[0],datos[1],datos[2],datos[3],cota,estacion)
	#Corremos el algoritmo sobre el grafo
	flujoTotal,flujoAristas=nx.capacity_scaling(grafo, demand='demand', weight='weight')
	#Agarramos los primeros y últimos nodos de las estaciones de Retiro y de Tigre:
	primerotigre = trenesTigre[0]
	ultimotigre =  trenesTigre[-1]
	primeroretiro = trenesRetiro[0]
	ultimoretiro = trenesRetiro[-1]

	if(estacion == "Retiro"): #Si existe la arista de trasnoche entre retiro y tigre, retiro está acotado
		#Ahora el flujo total de vagones está mostrado por el flujo que corre por las 2 aristas de trasnoche y la última agregada para el ejercicio
		print("Unidades requeridas: "+str(flujoAristas[ultimotigre][primerotigre]+flujoAristas[ultimoretiro][primeroretiro]+ flujoAristas[ultimoretiro][primerotigre]))
		#Las unidades que se necesitan en Tigre al inicio del día ahora están marcadas por las aristas que van desde la última estación de tigre a la primera y la arista que los reacomoda a la noche (que va de la última parada de Retiro a la primera de Tigre)
		print("Unidades requeridas para Tigre: "+str(flujoAristas[ultimotigre][primerotigre]+flujoAristas[ultimoretiro][primerotigre]))
		#Las unidades que requiere Retiro al inicio del día con la cota es el flujo que corre por la arista que va desde la última parada de Retiro a la primera de Retiro
		print("Unidades requeridas para Retiro: " + str(flujoAristas[ultimoretiro][primeroretiro]))

	else: #Sino, Tigre está acotado
		#Ahora el flujo total de vagones está mostrado por el flujo que corre por las 2 aristas de trasnoche y la última agregada para el ejercicio
		print("Unidades requeridas: "+str(flujoAristas[ultimotigre][primerotigre]+flujoAristas[ultimoretiro][primeroretiro]+ flujoAristas[ultimotigre][primeroretiro]))
		#Las unidades que requiere Retiro al inicio del día con la cota es el flujo que corre por la arista que va desde la última parada de Tigre a la primera de Tigre
		print("Unidades requeridas para Tigre: "+str(flujoAristas[ultimotigre][primerotigre]))
		#Las unidades que se necesitan en Retiro al inicio del día ahora están marcadas por las aristas que van desde la última estación de Retiro a la primera y la arista que los reacomoda a la noche (que va de la última parada de Tigre a la primera de Retiro)
		print("Unidades requeridas para Retiro: " + str(flujoAristas[ultimoretiro][primeroretiro]+ flujoAristas[ultimotigre][primeroretiro]))



