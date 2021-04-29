"""
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

    analyzer['tracks'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['EvByArtists'] = om.newMap(omaptype= 'RBT', comparefunction= compareIds)
    analyzer['EvByPista'] = om.newMap(omaptype= 'RBT', comparefunction= compareIds)
    analyzer['EvByCaracteristics'] = mp.newMap(numelements= 6, maptype= 'PROBING', loadfactor= 0.3, comparefunction= cmpByCarac)
    return analyzer

# Funciones para agregar informacion al catalogo

def addTracks(analyzer, track):
    lt.addLast(analyzer['tracks'], track)
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
    size_lista = lt.size(analyzer['tracks'])
    primeros_5 = lt.subList(analyzer['tracks'],1,5)
    ultimos_5 = lt.subList(analyzer['tracks'],size_lista-4,5)
    return artistas, pistas, size_lista, primeros_5, ultimos_5

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
    mapa_caracs = analyzer['EvByCaracteristics']
    
    return None

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

