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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    suma = 0
    tracksfile = cf.data_dir + 'context_content_features-small.csv'
    input_file = csv.DictReader(open(tracksfile, encoding="utf-8"),
                                delimiter=",")
    caract = input_file.fieldnames[0:5] + input_file.fieldnames[7:9]
    for char in caract:
        model.addCaracAsKey(analyzer, char)
    id_a = 1
    for track in input_file:
        track['id'] = id_a
        id_a += 1
        model.addTracks(analyzer, track)
        model.addTracksByCarac(analyzer, track, caract)
        model.addTracksByHourTempo(analyzer, track)
    model.addGenders(analyzer)
    print(suma)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def mediar_consulta_propiedades(analyzer):
    return model.consulta_propiedades(analyzer)

def comunica_propiedades_carga(catalog):
    return model.consulta_propiedades_carga(catalog)

def comunica_req1(catalog, car, sup, inf):
    """
    Comunica al model la petición del view del requerimiento 1
    """
    return model.consulta_req1(catalog,car,sup,inf)

def comunica_req2(catalog, inf_e, sup_e, inf_d, sup_d):
    """
    Comunica al model la petición del view del requerimiento 2
    """
    return model.consulta_req2(catalog, inf_e, sup_e, inf_d, sup_d)

def comunica_req5(analyzer, init, end):
    """
    Comunica al model la petición del view del requerimiento 5
    """
    return model.cosulta_req5(analyzer, init, end)