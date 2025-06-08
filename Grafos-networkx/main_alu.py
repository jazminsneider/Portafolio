from circulacionConCota import *
from circulacionSinCota import *


#Ejecutar el main_alu y escribirle el tipo de algoritmo a utilizar. Luego ingresar el archivo .json a analizar.
def pedido_terminal():
    while True:
        comando = input("Ingrese comando: S ejecuta el algoritmo sin cota, C ejecuta con cota: ").strip().upper()
        
        if comando == 'S':
            archivo = input("Ingrese el nombre del archivo JSON: ").strip()
            circulacionMaterialRodante(archivo)
            break
        elif comando == 'C':
            archivo = input("Ingrese el nombre del archivo JSON: ").strip()
            while True:
                try:
                    cota = int(input("Ingrese la cota (un número entero): ").strip())
                    break
                except ValueError:
                    print("Por favor, ingrese un número entero válido.")
            
            while True:
                estacion = input("Ingrese el nombre de la estación a limitar (Retiro o Tigre): ").strip()
                if estacion in ["Retiro", "Tigre"]:
                    break
                else:
                    print("Estación inválida. Por favor, ingrese 'Retiro' o 'Tigre'.")
            
            circulacionMaterialRodanteCota(archivo, cota, estacion)
            break
        else:
            print("Comando inválido. Por favor, intente nuevamente.")

# Llamada a la función para solicitar el comando
pedido_terminal()


