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
                'EvByCaracteristics' : mp.newMap(numelements= 6, maptype= 'PROBING', loadfactor= 0.3, comparefunction= cmpByCarac)
                }

    analyzer['tracks'] = lt.newList('SINGLE_LINKED', compareIds)
    
    return analyzer

# Funciones para agregar informacion al catalogo

def addTracks(analyzer, track):
    lt.addLast(analyzer['tracks'], track)
    return None

def addCaracAsKey(analyzer, char):
    """
    Se añade cada característica del track como llave de un mapa y se inicializa un RBT por cada llave
    """
    nuevo_arbol = om.newMap(omaptype= 'RBT', comparefunction= cmpByRate)
    mp.put(analyzer['EvByCaracteristics'], char, nuevo_arbol)
    return None


def addTracksByCarac(analyzer, track):
    mapa = analyzer['EvByCaracteristics']
    keys = mp.keySet(mapa)
    for char in lt.iterator(keys):
        entry_1 = mp.get(mapa, char)
        arbol_RBT = me.getValue(entry_1)
        key = float(track[char])
        entry_2 = om.get(arbol_RBT, key)
        if entry_2 is not None:
            lista = me.getValue(entry_2)
            lt.addFirst(lista, track)
            om.put(arbol_RBT, key, lista)
        else:
            lista = lt.newList('SINGLE_LINKED', cmpfunction= compareIds)
            om.put(arbol_RBT, key, lista)
    return None

# Funciones para creacion de datos

# Funciones de consulta

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

