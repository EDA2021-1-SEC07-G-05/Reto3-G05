"""
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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
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
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("7- Requerimiento 5")
    print("70- Obtener propiedades de los árboles usados")
    print("0- Salir")

catalog = None

#Funciones relacionadas con la carga de datos

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
        print(f"Evento número {contador}")
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

#Funciones relacionadas con el requerimiento 1

def parametros_req1():
    """
    Pide los parámetros necesarios al usuario
    """
    car = input('Digite la característica de contenido: ')
    inf = float(input('Digite el valor mínimo de la característica: '))
    sup = float(input('Digite el valor máximo de la característica: '))
    return car,sup,inf

def execute_req1(catalog, car, sup, inf):
    """
    Ejecuta el requerimiento 1
    """
    return controller.comunica_req1(catalog, car, sup, inf)

def view_req_1(result):
    """
    Edita el view de los resultados del requerimiento 1
    """
    print("\nRESULTADOS ENCONTRADOS")
    print(f"Total de eventos de escucha: {result[0]}")
    print(f"Total de artistas únicos: {result[1]}\n")
    return None

#Funciones relacionadas con el requerimiento 2
def parametros_req2():
    """
    Pide al usuario los datos necesarios para realizar el requerimiento 2
    """
    inf_energy = float(input('Digite el valor mínimo de Energy que desea consultar: '))
    sup_energy = float(input('Digite el valor máximo de Energy que desea consultar: '))
    inf_dance = float(input('Digite el valor mínimo de Danceability que desea consultar: '))
    sup_dance = float(input('Digite el valor máximo de Danceability que desea consultar: '))
    return inf_energy, sup_energy, inf_dance, sup_dance

def execute_req2(catalog,a,b,c,d):
    """
    Ejecuta el requerimiento 2
    """
    return controller.comunica_req2(catalog, a, b, c, d)

def view_req_2(lista):
    """
    Edita el view de los resultados del requerimiento 2
    """
    print('\nRESULTADOS ENCONTRADOS')
    print(f'\nPistas encontradas: {lista[1]}')
    for track in lt.iterator(lista[0]):
        t_id = track['track_id']
        e = track['energy']
        d = track['danceability']
        print(f'Track id: {t_id}, energy: {e}, danceability: {d}')

    print("\n")
    
#Funciones requerimiento #3
def parametros_req3():

    mini_vali = float(input('Digite el valor mínimo para instrumentalness que desea consultar: '))
    max_vali = float(input('Digite el valor máximo para instrumentalness que desea consultar: '))
    mini_valt = float(input('Digite el valor mínimo para el tempo que desea consultar: '))
    max_valt = float(input('Digite el valor máximo para el tempo que desea consultar: '))
    return mini_vali, max_vali, mini_valt, max_valt

def execute_req3(catalog, mini_vali, max_vali, mini_valt, max_valt):
    return controller.execute_req3(catalog, mini_vali, max_vali, mini_valt, max_valt)

def view_req_3(result):

    print('\nRESULTADOS ENCONTRADOS')
    print(f'Número de pistas únicas: {result[0]}')
    n = 0
    for track in lt.iterator(result[1]):
        n +=1
        track_id= track['track_id']
        inst= track['instrumentalness']
        temp = track['tempo']
        print(f'Track {n}: {track_id}, instrumentalness: {inst}, tempo: {temp}')

#Funciones requerimiento #4

def parametros_req4():
    genders = input('Digite los géneros musicales que desea consultar: ')
    return genders

def execute_req4(catalog, genders):
    return controller.execute_req4(catalog, genders)

def view_req_4(result):

    print('\nRESULTADOS ENCONTRADOS')
    print(f'Total de reproducciones: {result[0]}')
    print(result[1]) #aqui imprimo el mapa final completo, aún no he pasado los datos para que se vean lindos 
    
#Funciones relacionadas con el requerimiento 5
def parametros_req5():
    init = input("Digite el valor mínimo de la hora del día: ")
    end = input("Digite el valor máximo de la hora del día: ")
    return init, end

def execute_req5(catalog, init, end):
    """
    Inicia el proceso de ejecución del requerimiento 5
    """
    return controller.comunica_req5(catalog, init, end)

def view_req_5_part1(lista):
    """
    Edita el view de los resultados del requerimiento 5
    """
    total = 0
    for tupla in lt.iterator(lista):
        total += tupla[1]
        print(f'Número de reproducciones de {tupla[0]}: {tupla[1]}')
    print(f"\nEl total de reproducciones de todas las categorías (con repetición) encontradas en el rango dado es de: {total}")
    return None   

def view_req_5_part2(lista_top_of_the_world):
    print('\nTOP TRACKS POR HASHTAGS')
    i = 1
    for track in lt.iterator(lista_top_of_the_world):
        print(f"Track {i}: {track[0]}, Hashtags: {track[1]}, VADER promedio: {track[2]}")
        i+=1
    print("\n")
    return None
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
        print(f"Registros de eventos de escucha cargados: {propiedades[1]}\n")
        print(f"Resgistros de artistas únicos cargados: {propiedades[0]}\n")
        print(f"Registros de pistas únicas cargadas: {propiedades[2]}\n")
        print("Primeros 5 eventos cargados:")
        view_elementos_lista_carga(propiedades[3])
        print("Ultimos 5 eventos cargados: ")
        view_elementos_lista_carga(propiedades[4])

    elif int(inputs[0]) == 3:
        car,sup,inf = parametros_req1()
        result = execute_req1(catalog, car, sup, inf)
        view_req_1(result)

    elif int(inputs[0]) == 4: 
        inf_e, sup_e, inf_d, sup_d = parametros_req2()
        result = execute_req2(catalog, inf_e, sup_e, inf_d, sup_d)
        view_req_2(result)

    elif int(inputs[0]) == 5: 
        mini_vali, max_vali, mini_valt, max_valt = parametros_req3()
        result = execute_req3(catalog, mini_vali, max_vali, mini_valt, max_valt)
        view_req_3(result)
    
    elif int(inputs[0]) == 6: 
        genders = parametros_req4()
        result = execute_req4(catalog, genders)
        view_req_4(result)

    elif int(inputs[0]) == 7:
        init, end = parametros_req5()
        result = execute_req5(catalog, init, end)
        print('\nRESULTADOS ENCONTRADOS')
        print(f'\nReproducciones encontradas en el rango de horas dado: {result[2]}')
        view_req_5_part1(result[0])
        view_req_5_part2(result[1])

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
