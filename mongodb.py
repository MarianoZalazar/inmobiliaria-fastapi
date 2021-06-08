import motor.motor_asyncio as motor
import settings
from os import environ
from urllib.parse import urlencode

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

async def buscar_por_tipo(tipo):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'tipo': tipo},projection={'_id': 0}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def buscar_por_barrio(barrio):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'barrio': barrio},
                                         projection={'_id': 0}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def buscar_por_barrio_inmueble(barrio, inmueble):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'barrio': barrio, 'inmueble': inmueble},
                                         projection={'_id': 0}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def buscar_por_barrio_inmueble_tipo(barrio, inmueble, tipo):
    lista_de_anuncios = []
    async for anuncio in collection.find(filter={'barrio': barrio, 'inmueble': inmueble, 'tipo': tipo},
                                         projection={'_id': 0}):
        lista_de_anuncios.append(anuncio)
    return lista_de_anuncios

async def insertar_anuncio(anuncio):
    new_anuncio = await collection.insert_one(anuncio)
    anuncio_creado = await collection.find_one(filter={"_id": new_anuncio.inserted_id}, projection={'_id': 0})
    return anuncio_creado