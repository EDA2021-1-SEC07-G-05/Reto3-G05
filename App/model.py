﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():

    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'tracks': None,
                'EvByCaracteristics' : None,
                'EvByArtist': None,
                'EvByPista': None
                }

    analyzer['tracks'] = mp.newMap(numelements= 100, maptype='PROBING')
    analyzer['EvByArtists'] = om.newMap(omaptype= 'RBT', comparefunction= compareIds)
    analyzer['EvByPista'] = om.newMap(omaptype= 'RBT', comparefunction= compareIds)
    analyzer['EvByCaracteristics'] = mp.newMap(numelements= 6, maptype= 'PROBING', loadfactor= 0.3, comparefunction= cmpByCarac)
    return analyzer

# Funciones para agregar informacion al catalogo

def addTracks(analyzer, track):
    mp.put(analyzer['tracks'], track['track_id'], track)
    om.put(analyzer['EvByArtists'], track['artist_id'], track)
    om.put(analyzer['EvByPista'], track['id'], track)
    return None

def addCaracAsKey(analyzer, char):
    """
    Se añade cada característica del track como llave de un mapa y se inicializa un RBT por cada llave
    """
    nuevo_arbol = om.newMap(omaptype= 'RBT', comparefunction= cmpByRate)
    mp.put(analyzer['EvByCaracteristics'], char, nuevo_arbol)
    return None


def addTracksByCarac(analyzer, track, caract):
    for car in caract:
        rate = float(track[car])
        entry_1 = mp.get(analyzer['EvByCaracteristics'], car)
        arbol_RBT = me.getValue(entry_1)
        entry_2 = om.get(arbol_RBT, rate)
        if entry_2 is not None:
            est_datos = me.getValue(entry_2)
            mp.put(est_datos['mapa_completo'], int(track['id']), track)
            mp.put(est_datos['mapa_unicos'], track['track_id'], track)
            om.put(arbol_RBT, rate, est_datos)
        else:
            est_datos = {'mapa_completo': mp.newMap(numelements= 20, maptype= 'PROBING'),
                         'mapa_unicos': mp.newMap(numelements= 20, maptype= 'PROBING')}
            mp.put(est_datos['mapa_completo'], int(track['id']), track)
            mp.put(est_datos['mapa_unicos'], track['track_id'], track)
            om.put(arbol_RBT, rate, est_datos)    
    return None

# Funciones para creacion de datos

# Funciones de consulta

    #Apartado de funciones para consulta sobre la carga de datos
def consulta_propiedades(analyzer):
    mapa = analyzer['EvByCaracteristics']
    keys = mp.keySet(mapa)
    propiedades = lt.newList('SINGLE_LINKED')
    for i in lt.iterator(keys):
        entry = mp.get(mapa, i)
        arbol = me.getValue(entry)
        altura = om.height(arbol)
        elementos = om.size(arbol)
        lt.addFirst(propiedades, (altura,elementos))
    return propiedades

def consulta_propiedades_carga(analyzer):
    artistas = om.size(analyzer['EvByArtists'])
    pistas = om.size(analyzer['EvByPista'])
    size_lista = mp.size(analyzer['tracks'])
    keys = mp.keySet(analyzer['tracks'])
    primeros_5 = lt.subList(keys,1,5)
    ultimos_5 = lt.subList(keys,size_lista-4,5)
    lista_1 = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareIds)
    lista_2 = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareIds)
    for key in lt.iterator(primeros_5):
        entry = mp.get(analyzer['tracks'], key)
        track = me.getValue(entry)
        lt.addLast(lista_1, track)

    for key in lt.iterator(ultimos_5):
        entry = mp.get(analyzer['tracks'], key)
        track = me.getValue(entry)
        lt.addLast(lista_2, track)
    return artistas, pistas, size_lista, lista_1, lista_2

    #Apartado de funciones para consulta sobre el requerimiento 1
def consulta_req1(analyzer, car, sup, inf):
    #Número de artistas únicos
    mapa_caracs = analyzer['EvByCaracteristics']
    entry_1 = mp.get(mapa_caracs, car)
    arbol_RBT = me.getValue(entry_1)
    estructuras = om.values(arbol_RBT, inf, sup)
    mapa_trabajo = mp.newMap(numelements= 100, maptype= 'PROBING', loadfactor= 0.3)
    num_eventos = 0
    num_artistas = 0
    for ed in lt.iterator(estructuras):
        num_eventos += mp.size(ed['mapa_completo'])
        for track in lt.iterator(mp.valueSet(ed['mapa_completo'])):
            artista = track['artist_id']
            entry_2 = mp.get(mapa_trabajo, artista)
            if entry_2 is None:
                num_artistas += 1
                mp.put(mapa_trabajo, artista, 1)

    return num_eventos, num_artistas


#Apartado funciones req2
def consulta_req2(analyzer, inf_e, sup_e, inf_d, sup_d):
    """
    Ejecuta la consulta sobre los datos para responder al requerimiento 2
    """
    mapa_trabajo = mp.newMap(numelements=20, maptype='PROBING')
    lista_entregable = lt.newList(datastructure= 'ARRAY_LIST', cmpfunction= compareIds)
    mapa_caracs = analyzer['EvByCaracteristics']
    entry_1 = mp.get(mapa_caracs, 'energy')
    entry_2 = mp.get(mapa_caracs, 'danceability')
    arbol_energy = me.getValue(entry_1)
    arbol_dance = me.getValue(entry_2)
    #Vamos primero con energy
    estructuras = om.values(arbol_energy, inf_e, sup_e)
    for estructura in lt.iterator(estructuras):
        mapa = estructura['mapa_unicos']
        tracks = mp.keySet(mapa)
        for track in lt.iterator(tracks):
            mp.put(mapa_trabajo, track, 1)

    #Ahora vamos con danceability
    estructuras = om.values(arbol_dance, inf_d, sup_d)
    suma = 0
    for estructura in lt.iterator(estructuras):
        mapa = estructura['mapa_unicos']
        tracks = mp.keySet(mapa)
        for track in lt.iterator(tracks):
            entry = mp.get(mapa_trabajo, track)
            if entry is not None:
                entry_auxiliar = mp.get(analyzer['tracks'], track)
                track = me.getValue(entry_auxiliar) 
                lt.addLast(lista_entregable, track)
                suma += 1
    retorno = lt.subList(lista_entregable, 1, 5)
    return retorno, suma

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1, id2):
    """
    Compara dos id de cada pista
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def cmpByCarac(keyname, entry):
    key = me.getKey(entry)
    if keyname > key:
        return 1
    elif keyname < key:
        return -1
    else:
        return 0

def cmpByRate(key_1, key_2):
    if key_1 > key_2:
        return 1
    elif key_1 < key_2:
        return -1
    else:
        return 0
# Funciones de ordenamiento

