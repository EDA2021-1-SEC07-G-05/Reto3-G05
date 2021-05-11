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
import datetime as dt
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
                'EvByPista': None,
                'EvByHour': None,
                'Genders': None,
                '#ByTrack': None,
                'VaderBy#': None}

    analyzer['tracks'] = mp.newMap(numelements= 100, maptype='PROBING')
    analyzer['EvByArtists'] = om.newMap(omaptype= 'RBT', comparefunction= compareIds)
    analyzer['EvByPista'] = om.newMap(omaptype= 'RBT', comparefunction= compareIds)
    analyzer['EvByCaracteristics'] = mp.newMap(numelements= 6, maptype= 'PROBING', loadfactor= 0.3, comparefunction= cmpByCarac)
    analyzer['EvByHour'] = om.newMap(omaptype='RBT', comparefunction=cmpInts)
    analyzer['Genders'] = mp.newMap(numelements= 9, maptype= 'PROBING')
    analyzer['#ByTrack'] = mp.newMap(numelements= 100, maptype= "PROBING")
    analyzer['VaderBy#'] = mp.newMap(numelements= 100, maptype= 'PROBING')
    return analyzer

# Funciones para agregar informacion al catalogo

def addVADERbyhashtag(analyzer, hashtag):
    mapa = analyzer['VaderBy#']
    key = hashtag['hashtag']
    if hashtag['vader_avg'] is not '':
        mp.put(mapa, key, hashtag['vader_avg'])
    else:
        mp.put(mapa, key, None)
    return None

def addHashByTrack(analyzer, track):
    mapa = analyzer['#ByTrack']
    key = track['track_id']
    entry = mp.get(mapa, key)
    if entry is not None:
        mapa_1 = me.getValue(entry)
        mp.put(mapa_1, track['hashtag'].lower(), 0)
        mp.put(mapa, key, mapa_1)
    else:
        mapa_1 =  mp.newMap(maptype= 'PROBING', comparefunction= cmpByCarac)
        mp.put(mapa_1, track['hashtag'].lower(), 0)
        mp.put(mapa,key,mapa_1)
    return None
    
def addGenders(analyzer):
    mapa = analyzer['Genders']
    mp.put(mapa, 'reggae', (60,90))
    mp.put(mapa, 'down-tempo', (70,100))
    mp.put(mapa, 'chill-out', (90,120))
    mp.put(mapa, 'hip-hop', (85,115))
    mp.put(mapa, 'jazz and funk', (120,125))
    mp.put(mapa, 'pop', (100,130))
    mp.put(mapa, 'R&B', (60,80))
    mp.put(mapa, 'rock', (110,140))
    mp.put(mapa, 'metal', (100,160))
    return None

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

def addTracksByHourTempo(analyzer, track):
    hora = hour_int(track)
    tempo = float(track['tempo'])
    arbol_hora = analyzer['EvByHour'] #arbol principal 
    entry_hora = om.get(arbol_hora, hora) #llave-valor con hora 
    if entry_hora is not None:
        arbol_tempo = me.getValue(entry_hora)
        entry_tempo = om.get(arbol_tempo, tempo)
        if entry_tempo is not None:
            estructura = me.getValue(entry_tempo)
            lt.addLast(estructura['mapa_completo'], track)
            mp.put(estructura['mapa_unicos'], track['track_id'], track)
            om.put(arbol_tempo, tempo, estructura)
        else:
            estructura = {'mapa_completo': lt.newList(datastructure= "SINGLE_LINKED", cmpfunction= compareTracks),
                          'mapa_unicos': mp.newMap(maptype= 'PROBING', comparefunction= cmpByCarac)}
            lt.addLast(estructura['mapa_completo'], track)
            mp.put(estructura['mapa_unicos'], track['track_id'], track)
            om.put(arbol_tempo, tempo, estructura)
    else:
        arbol_tempo = om.newMap(omaptype='RBT',comparefunction=cmpInts)
        estructura = {'mapa_completo': lt.newList(datastructure= "SINGLE_LINKED", cmpfunction= compareTracks),
                      'mapa_unicos': mp.newMap(maptype= 'PROBING', comparefunction= cmpByCarac)}
        lt.addLast(estructura['mapa_completo'], track)
        mp.put(estructura['mapa_unicos'], track['track_id'], track)
        om.put(arbol_tempo, tempo, estructura)
        om.put(arbol_hora, hora, arbol_tempo)
    return None

def addGender(analyzer, gender, min_val, max_val):
    mp.put(analyzer['Genders'],gender,(min_val,max_val))
    return None

# Funciones para creacion de datos
def hour_int(track):
    hora = (track['created_at'].split(" ")[1])
    return (dt.datetime.strptime(hora, "%H:%M:%S")).time()

# Funciones de consulta

def consulta_auxiliar(analyzer):
    arbol_hora = analyzer['EvByHour']
    horas = om.keySet(arbol_hora)
    num_reproducciones = 0
    num_tracks = 0
    for hora in lt.iterator(horas):
        entry = om.get(arbol_hora, hora)
        arbol_tempo = me.getValue(entry)
        tempos = om.keySet(arbol_tempo)
        for tempo in lt.iterator(tempos):
            entry_tempo = om.get(arbol_tempo, tempo)
            estructura = me.getValue(entry_tempo)
            eventos = estructura['mapa_completo']
            mapa_tracks = estructura['mapa_unicos']
            tracks = mp.keySet(mapa_tracks)
            num_reproducciones += lt.size(eventos)
            num_tracks += lt.size(tracks)
    print(f"Reproducciones: {num_reproducciones}\nTracks: {num_tracks}")
    return None

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

#Funciones requerimiento #3
def consulta_req3(analyzer, mini_vali, max_vali, mini_valt, max_valt):

    entry_1 = mp.get(analyzer['EvByCaracteristics'], 'instrumentalness')
    entry_2 = mp.get(analyzer['EvByCaracteristics'], 'tempo')
    arbol_inst = me.getValue(entry_1)           
    arbol_temp = me.getValue(entry_2)
    estructuras_inst = om.values(arbol_inst, mini_vali, max_vali)
    estructuras_temp = om.values(arbol_temp, mini_valt, max_valt)
    mapa_trabajo = mp.newMap(numelements=20, maptype='PROBING')
    lista = lt.newList('ARRAY_LIST', cmpfunction= compareIds)
    unique_tracks = 0

    for estruc in lt.iterator(estructuras_inst):
        tracks = mp.keySet(estruc['mapa_unicos'])
        for track in lt.iterator(tracks): 
            entry = mp.get(analyzer['tracks'], track)
            value = me.getValue(entry)
            mp.put(mapa_trabajo, track, value)

    for estruc in lt.iterator(estructuras_temp):
        tracks = mp.keySet(estruc['mapa_unicos'])
        for track in lt.iterator(tracks):
            entry = mp.get(mapa_trabajo,track)
            if entry is not None:
                unique_tracks += 1
                value = me.getValue(entry)
                lt.addLast(lista, value)
    lista_final = lt.subList(lista, 1, 5)
    return unique_tracks, lista_final

#Funciones requerimiento 4

def consulta_req4(analyzer, list_gen):
    
    mapa_final = mp.newMap(numelements=10, maptype='PROBING')
    entry_2 = mp.get(analyzer['EvByCaracteristics'], 'tempo')
    arbol_tempo = me.getValue(entry_2)
    tot_eventos = 0
    for gender in list_gen:
        num_artistas = 0
        num_eventos = 0
        entry_1 = mp.get(analyzer['Genders'], gender)
        rango = me.getValue(entry_1)
        estructuras = om.values(arbol_tempo,rango[0],rango[1])
        lista_trabajo = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compareIds)
        for estruc in lt.iterator(estructuras):
            num_eventos += mp.size(estruc['mapa_completo'])
            for track in lt.iterator(mp.valueSet(estruc['mapa_completo'])):
                artista = track ['artist_id']
                if lt.isPresent(lista_trabajo, artista) == 0:
                    lt.addLast(lista_trabajo,artista)
                    num_artistas+=1
        tot_eventos += num_eventos
        top_artistas = lt.subList(lista_trabajo, 1, 10)
        info = (num_eventos,num_artistas,top_artistas)
        mp.put(mapa_final, gender, info)

    return tot_eventos, mapa_final 

#Apartado de funciones relacionadas con el requerimiento 5
def cosulta_req5(analyzer, init, end):
    """
    Apartado de la primera parte de la consulta
    """
    mapa_trabajo = mp.newMap(maptype='PROBING', comparefunction=cmpByCarac)
    hora_1 = (dt.datetime.strptime(init, "%H:%M:%S")).time()
    hora_2 = (dt.datetime.strptime(end, "%H:%M:%S")).time()
    arbol_hora = analyzer['EvByHour']
    mapa_genders = analyzer['Genders']
    genders = mp.keySet(mapa_genders)
    for gender in lt.iterator(genders):
        mp.put(mapa_trabajo, gender, 0)
    arboles_tempo = om.values(arbol_hora, hora_1, hora_2)
    reproducciones = 0
    for arbol_tempo in lt.iterator(arboles_tempo):
        for gender in lt.iterator(genders):
            entry_tempos = mp.get(mapa_genders, gender)
            tempo = me.getValue(entry_tempos)
            piso = om.floor(arbol_tempo, tempo[0])
            techo = om.ceiling(arbol_tempo, tempo[1])
            print(piso,techo)
            estructuras = om.values(arbol_tempo, piso, techo)
            contador = 0
            for estructura in lt.iterator(estructuras):
                reproducciones = lt.size(estructura['mapa_completo'])
                contador += reproducciones
            entry_num_reproducciones = mp.get(mapa_trabajo, gender)
            num_reproducciones = me.getValue(entry_num_reproducciones)
            num_reproducciones += contador
            mp.put(mapa_trabajo, gender, num_reproducciones)


    """
    mapa_hashtag = analyzer['#ByTrack']
    mapa_VADER = analyzer['VaderBy#']
    keys = mp.keySet(mapa_trabajo)
    mayor = ('aletoso',0)
    for key in lt.iterator(keys):
        entry = mp.get(mapa_trabajo, key)
        conteo = me.getValue(entry)
        if conteo > mayor[1]:
            mayor = (key, conteo)

    entry = mp.get(analyzer['Genders'], mayor[0])
    tempo = me.getValue(entry)
    lista_trabajo = lt.newList(datastructure= 'ARRAY_LIST', cmpfunction= cmpByNumhashtags)
    
    
    for arbol_tempo in lt.iterator(lista_mapas):
        estructuras = om.values(arbol_tempo, tempo[0], tempo[1])
        for estructura in lt.iterator(estructuras):
            mapa = estructura['mapa_unicos']
            for key in lt.iterator(mp.keySet(mapa)):
                entry = mp.get(mapa_hashtag, key)
                mapa_otra_vez = me.getValue(entry)
                num_hashtags = lt.size(mp.keySet(mapa_otra_vez))
                prom = 0
                for hashtag in lt.iterator(mp.keySet(mapa_otra_vez)):
                    entry = mp.get(mapa_VADER, hashtag)
                    if entry is not None:
                        value = me.getValue(entry)
                        if value is not None:
                            prom += float(value)
                tres_tupla = (key, num_hashtags, prom/num_hashtags)
                lt.addLast(lista_trabajo, tres_tupla)

    sort_list = sa.sort(lista_trabajo, cmpByNumhashtags)
    sublist = lt.subList(sort_list, 1, 10)

    print(mayor)
    """
    
    return mapa_trabajo, None

# Funciones utilizadas para comparar elementos dentro de una lista

def compareTracks(track_1, track_2):
    if (track_1['id'] == track_2['id']):
        return 0
    elif track_1['id'] > track_2['id']:
        return 1
    else:
        return -1

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

def cmpInts(int_1, int_2):
    """
    Compara dos valores enteros en el orden de los enteros
    """
    if int_1 > int_2:
        return 1
    elif int_1 < int_2:
        return -1
    else:
        return 0

def cmpByNumhashtags(tuple_1, tuple_2):
    v_1 = tuple_1[1]
    v_2 = tuple_2[1]
    if v_1 > v_2:
        return 1
    elif v_1 < v_2:
        return -1
    else:
        return 0


# Funciones para eliminar informacion del catalogo

def removeGender(analyzer,name_gen):
    mp.remove(analyzer['Genders'], name_gen)
    return None
