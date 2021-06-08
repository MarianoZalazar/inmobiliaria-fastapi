import motor.motor_asyncio as motor
import settings
from os import environ
from urllib.parse import urlencode
from pymongo import ReturnDocument

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

client = motor.AsyncIOMotorClient(f"mongodb+srv://{USER}:{PSWD}{SERVER}/{DB}?{urlencode(params)}")
bd = client[DB]
collection = bd['propiedades']


#Usar for loops en vez de list comprehension para mejor entendimiento

def insertar_varios_anuncios(lista_de_anuncios):
    collection.insert_many(lista_de_anuncios)


async def buscar_por_tipo(tipo):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'tipo': tipo}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def buscar_por_barrio(barrio):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'barrio': barrio}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def buscar_por_barrio_inmueble(barrio, inmueble):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'barrio': barrio, 'inmueble': inmueble}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def buscar_por_barrio_inmueble_tipo(barrio, inmueble, tipo):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'barrio': barrio, 'inmueble': inmueble, 'tipo': tipo}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def insertar_anuncio(anuncio):
    new_anuncio = await collection.insert_one(anuncio)
    anuncio_creado = await collection.find_one(filter={"_id": new_anuncio.inserted_id})
    return anuncio_creado


async def actualizar_anuncio(id, anuncio):
    anuncio_actualizado = await collection.find_one_and_update({'_id': id}, {'$set': anuncio}, return_document=ReturnDocument.AFTER)
    return anuncio_actualizado

async def eliminar_anuncio(id):
    anuncio_eliminado = await collection.delete_one({'_id': id})
    return anuncio_eliminado