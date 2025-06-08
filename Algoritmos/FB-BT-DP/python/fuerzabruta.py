from funciones_auxiliares import *

def breakpointsAuxFB(archivo:str,breakpoints:int,x:int,y:int,grilla_x,grilla_y,npuntos,solucion:list[tuple[float,float]],optima:list[tuple[float,float]],errorMinimo:float):
   
#si no contiene a la posicion 0 de la grilla x en la solucion, no es una solución factible por lo que ni se fija si esa es mejor que óptima
   if breakpoints==0 and x==len(grilla_x) and (grilla_x[0] not in lista_x(solucion)):
       return errorMinimo, optima
   
   #si tengo una solucion factible y con la cantidad de breakpoints adecuada, se fija si tiene menor error que la ultima calculada como óptima. Si es mejor, optima se actualiza.
   elif (breakpoints==0 and x==len(grilla_x)):
        if (errorSolucion(solucion,npuntos)<errorMinimo):
            optima=solucion.copy()
            errorMinimo=errorSolucion(optima,npuntos)
        return errorMinimo, optima
    
   #Este if es para que no repita puntos de x
   elif x<len(grilla_x)and grilla_x[x] in lista_x(solucion):
       return errorMinimo, optima
   
   #para que no haya soluciones que no lleguen al punto final
   elif (breakpoints==0 and x!=len(grilla_x)):
        return errorMinimo, optima
     
   #para que no haya soluciones con menos puntos que los pedidos
   elif(breakpoints!=0 and x==len(grilla_x)):
       return errorMinimo, optima

  #paso recursivo
   for j in range(0,len(grilla_y)+1): #el +1 es para que pueda tomar como breakpoint todas las opciones disponibles en la grilla Y, y además una opción extra que es no tomar ninguno

       
       if j==len(grilla_y): #caso que no toma el punto como breakpoint
            errorMinimo,optima=breakpointsAuxFB(archivo,breakpoints,x+1,j,grilla_x,grilla_y,npuntos,solucion,optima,errorMinimo)
     
       else:  #tomo el punto como breakpoint
        errorMinimo,optima=breakpointsAuxFB(archivo,breakpoints-1,x+1,j,grilla_x,grilla_y,npuntos,solucion+[(grilla_x[x],grilla_y[j])],optima,errorMinimo)
       
   return errorMinimo,optima

def breakpointsFB(archivo:str,breakpoints:int,m1:int,m2:int)->list[tuple[float,float]]:
  #procesar los datos ingresados y armar grillas
    puntosEnX:list[float]=leer_datos(archivo)[0]
    puntosEnY:list[float]=leer_datos(archivo)[1]
    grilla_x:list[float]=armar_grilla(puntosEnX,puntosEnY,m1,m2)[0]
    grilla_y:list[float]=armar_grilla(puntosEnX,puntosEnY,m1,m2)[1]
    error:float=10e10

#llamamos a una funcion auxiliar que va a usar atributos adicionales además de los que el usuario ingresa:
  #solucion empieza como una lista vacia para poder ir rellenándola con todos los breakpoints posibles
  #optima inicia como vacía y se llenará con la mejor de todas las soluciones, a medida que las vaya encontrando
  #error arranca siendo muy alto para poder ir comparando
    return breakpointsAuxFB(archivo,breakpoints,-1,-1,grilla_x,grilla_y,(puntosEnX,puntosEnY),[],[],error)



