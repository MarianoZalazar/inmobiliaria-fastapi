from fastapi import FastAPI, HTTPException, Body, status
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.anuncio import Anuncio
import mongodb as db

app = FastAPI()

@app.get('/')
async def root():
    return {"msg": "Root"}

@app.get('/api/{barrio_o_tipo}', response_model=List[Anuncio])
async def get_by_hood_or_type(barrio_o_tipo: str):
    if barrio_o_tipo == 'venta' or barrio_o_tipo == 'alquiler':
        lista_anuncios = await db.buscar_por_tipo(barrio_o_tipo)
    else:
        lista_anuncios = await db.buscar_por_barrio(barrio_o_tipo)
        
    if len(lista_anuncios) >= 1:
        return lista_anuncios
    
    raise HTTPException(status_code=404, detail=f"{barrio_o_tipo} not found")

@app.get('/api/{barrio}/{inmueble}', response_model=List[Anuncio])
async def get_by_property_type(barrio: str, inmueble: str):
    lista_anuncios = await db.buscar_por_barrio_inmueble(barrio.lower(), inmueble.lower())
    if len(lista_anuncios)>=1:
        return lista_anuncios
    
    raise HTTPException(status_code=404, detail=f"Resource not found")
    
@app.get('/api/{barrio}/{inmueble}/{tipo}', response_model=List[Anuncio])
async def get_by_property_type_and_rent_sold(barrio: str, inmueble: str, tipo: str):
    lista_anuncios = await db.buscar_por_barrio_inmueble_tipo(barrio.lower(), inmueble.lower(), tipo.lower())
    if len(lista_anuncios)>=1:
        return lista_anuncios
    
    raise HTTPException(status_code=404, detail=f"Resource not found")

@app.post('/api/propiedades', response_model=Anuncio)
async def post_property(anuncio: Anuncio = Body(...)):
    anuncio = jsonable_encoder(anuncio)
    new_anuncio = await db.insertar_anuncio(anuncio)
    return JSONResponse(content=new_anuncio, status_code=status.HTTP_201_CREATED)



#Fix ruta api/barrio_o_tipo (probable error en scrapeo)
#Añadir campo ID (ObjectdID o UUID)
#PUT-DELETE Methods
#Añadir query parameters (limits, dates)