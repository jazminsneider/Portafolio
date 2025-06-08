import json
from typing import List
from typing import Tuple
import time
from typing import Dict


#función que lee los datos y retorna una tupla con 2 listas (las coordenadas en x y las coordenadas en y de cada punto)
def leer_datos(datos:str)-> tuple[list[float],list[float]]:
  instance_name = datos
  
  filename = "../../data/" + instance_name
  with open(filename) as f:
      instance = json.load(f)
  
  
  puntosenX:List[float]=instance["x"]
  puntosenY:List[float]=instance["y"]
  return(puntosenX,puntosenY)


def armar_grilla(puntosEnX: list[float], puntosEnY: list[float], m1: int, m2: int) -> tuple[list[float], list[float]]:
   grid_x = np.linspace(min(puntosEnX), max(puntosEnX), num=m1, endpoint=True)
   grid_y = np.linspace(min(puntosEnY), max(puntosEnY), num=m2, endpoint=True)
   
   return list(grid_x), list(grid_y)

#Función que calcula el error entre dos puntos
def error(BP_inicial:tuple[float,float], BP_final:tuple[float,float] , Puntos:tuple[List[float],List[float]])->float:
  suma_de_errores:float = 0
  #Recuperamos las coordenadas en x y en y de los breakpoints para calcular la función lineal que une a los puntos
  x1:float = BP_inicial[0]
  x2:float = BP_final[0]
  y1:float = BP_inicial[1]
  y2:float = BP_final[1]
  pendiente:float = (y2-y1)/(x2-x1)
  ordenada:float = y2-pendiente*x2
  i:int = 0
  #Buscamos aquellos puntos que se encuentran entre los breakpoints
  while(i < len(Puntos[0]) and Puntos[0][i]<=x2):
       #Si el punto se encuentra dentro del rango de los breakpoint entonces calcula su error
       if x1 < Puntos[0][i]:
           yFuncion:float=pendiente*Puntos[0][i]+ordenada
           suma_de_errores+=abs(Puntos[1][i]-yFuncion)
       i+=1
  return suma_de_errores

#calcula el error de una solucion con varios puntos
def errorSolucion(solucion:list[tuple[float,float]],Puntos:tuple[List[float],List[float]])->float:
   i:int=0
   errorTotal:float=0
  #Si la solucion no tiene breakpoints, el error total es inf
   if(len(solucion) == 0):
      errorTotal = 10e10
     
  #si la solucion tiene solo un punto, el error es el valor absoluto entre el punto calculado por la solucion y el punto pasado por parámetro.
   elif(len(solucion) == 1): 
       errorTotal+=abs(Puntos[1][0] - solucion[0][1])
     
 
   else:
    errorTotal+=Puntos[1][0] - solucion[0][1] #calcula el error del primer punto
    while(i<len(solucion)-1): #calcula los errores de a pares
        errorTotal+=error(solucion[i],solucion[i+1],Puntos)
        i+=1
   return errorTotal

#esta funcion es para poder filtrar despues las soluciones en la recursion segun las x que contiene
def lista_x(coordenadas:list[tuple[float,float]]):
   res:list[float] = []
   i:int = 0 
   while i< len(coordenadas):
       res.append(coordenadas[i][0])
       i +=1
   return res
