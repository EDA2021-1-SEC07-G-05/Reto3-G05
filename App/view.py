﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analyzer")
    print("2- Cargar información al analyzer")
    print("3- Requerimiento 1")
    print("70- Obtener propiedades de los árboles usados")
    print("0- Salir")

catalog = None

def init():
    return controller.init()

def execute_loadData(catalog): 
    answer = controller.loadData(catalog)
    return answer

def execute_consulta_propiedades(catalog):
    return controller.mediar_consulta_propiedades(catalog)

def execute_propiedades_carga(catalog):
    return controller.comunica_propiedades_carga(catalog)

def view_elementos_lista_carga(lista):
    contador = 1
    for evento in lt.iterator(lista):
        print(f"Eventp número {contador}")
        print(f"ID del evento: {evento['track_id']}")
        print(f"Instrumentalidad: {evento['instrumentalness']}")
        print(f"Acústica: {evento['acousticness']}")
        print(f"Liveness: {evento['liveness']}")
        print(f"Speechiness: {evento['speechiness']}")
        print(f"Energía: {evento['energy']}")
        print(f"Capacidad de baile: {evento['danceability']}")
        print(f"Valencia: {evento['valence']}\n")
        contador += 1

def view_propiedades(tuple):
    altura = tuple[0]
    elementos = tuple[1]
    return altura, elementos

def parametros_req1():
    car = input('Digite la característica de contenido: ')
    inf = input('Digite el valor mínimo de la característica: ')
    sup = input('Digite el valor máximo de la característica: ')
    return car,sup,inf

def execute_req1(catalog, car, sup, inf):
    """
    Ejecuta el requerimiento 1
    """
    return controller.comunica_req1(catalog, car, sup, inf)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        catalog = init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        answer = execute_loadData(catalog)
        propiedades = execute_propiedades_carga(catalog)
        print(f"Registros de eventos de escucha cargados: {propiedades[2]}\n")
        print(f"Resgistros de artistas únicos cargados: {propiedades[0]}\n")
        print(f"Registros de pistas únicas cargadas: {propiedades[1]}\n")
        print("Primeros 5 eventos cargados:")
        view_elementos_lista_carga(propiedades[3])
        print("Ultimos 5 eventos cargados: ")
        view_elementos_lista_carga(propiedades[4])

    elif int(inputs[0]) == 3:
        car,sup,inf = parametros_req1()
        result = execute_req1(catalog, car, sup, inf)
        print(f'Total de reproducciones = {result}')


    elif int(inputs[0]) == 70:
        result = execute_consulta_propiedades(catalog)
        contador = 0
        for i in lt.iterator(result):
            contador += 1
            altura, elementos = view_propiedades(i)
            print(f'\nArbol RBT {contador}:\naltura = {altura}\nelementos = {elementos}')

    else:
        sys.exit(0)
sys.exit(0)
