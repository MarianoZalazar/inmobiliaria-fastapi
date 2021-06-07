import settings
from os import environ
from urllib.parse import urlencode
from pymongo import MongoClient

params = {'retryWrites': 'true',
          'w': 'majority',
          'ssl': 'true',
          'ssl_cert_reqs': 'CERT_NONE'
         }

USER = environ['USER']
PSWD = environ['PSWD']
SERVER = environ['SERVER']
DB = environ['DB']
PORT = environ['PORT']

client_mongo = MongoClient('mongodb+srv://' + USER + ':' + PSWD + SERVER + '/' + DB + '?' + urlencode(params))
collection = client_mongo[DB]['propiedades']

def insertar_anuncios(lista_de_anuncios):
    if lista_de_anuncios != []:
        print('Insertando')
        collection.insert_many(lista_de_anuncios)
    else:
        print("No hay resultados")

def buscar_por_barrio(barrio):
    result = [objeto for objeto in collection.find(filter={'barrio':(barrio)}, projection={'_id': 0})]
    return result

def buscar_por_barrio_inmueble(barrio, inmueble):
    result = [objeto for objeto in collection.find(filter={'barrio':(barrio), 'inmueble':(inmueble)}, projection={'_id': 0})]
    return result

def buscar_por_barrio_inmueble_tipo(barrio, inmueble, tipo):
    result = [objeto for objeto in collection.find(filter={'barrio':(barrio), 'inmueble':(inmueble), 'tipo':(tipo)}, projection={'_id': 0})]
    return result

    