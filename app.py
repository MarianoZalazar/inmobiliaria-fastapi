from fastapi import FastAPI, HTTPException, Body, status
from pydantic import Field
from starlette.responses import RedirectResponse
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import examples
from models.anuncio import Anuncio, Anuncio_actualizar
import mongodb as db

app = FastAPI(title="Inmobiliaria API",
              description="API para disponibilizacion de datos sobre propiedades en CABA. Informacion conseguida a traves de Properati"
              )


@app.get('/', include_in_schema=False)
async def root():
    response = RedirectResponse('/docs')
    return response

##############################################################################

@app.get('/api/{barrio_o_tipo}', 
         response_description = 'Obtener lista de anuncios por barrio o tipo de operacion', 
         response_model=List[Anuncio])
async def get_by_barrio_o_tipo(barrio_o_tipo: str):
    if barrio_o_tipo == 'venta' or barrio_o_tipo == 'alquiler':
        lista_anuncios = await db.buscar_por_tipo(barrio_o_tipo.lower())
    else:
        lista_anuncios = await db.buscar_por_barrio(barrio_o_tipo.lower())
        
    if len(lista_anuncios) >= 1:
        return lista_anuncios
    
    raise HTTPException(status_code=404, detail=f"{barrio_o_tipo} not found")

##############################################################################

@app.get('/api/{barrio}/{inmueble}', 
         response_description = 'Obtener lista de anuncios por barrio e inmueble', 
         response_model=List[Anuncio])
async def get_by_barrio_inmueble(barrio: str, inmueble: str):
    lista_anuncios = await db.buscar_por_barrio_inmueble(barrio.lower(), inmueble.lower())
    if len(lista_anuncios)>=1:
        return lista_anuncios
    
    raise HTTPException(status_code=404, detail=f"Resource not found")

##############################################################################
    
@app.get('/api/{barrio}/{inmueble}/{tipo}', 
         response_description = 'Obtener lista de anuncios por barrio, inmueble y tipo de operacion', 
         response_model=List[Anuncio])
async def get_by_barrio_inmueble_tipo(barrio: str, inmueble: str, tipo: str):
    lista_anuncios = await db.buscar_por_barrio_inmueble_tipo(barrio.lower(), inmueble.lower(), tipo.lower())
    if len(lista_anuncios)>=1:
        return lista_anuncios
    
    raise HTTPException(status_code=404, detail=f"Resource not found")

##############################################################################

@app.post('/api/propiedades', 
          response_description = 'Publicar un anuncio', 
          response_model=Anuncio,)
async def publicar_anuncio(anuncio: Anuncio = Body(..., example=examples.post_example)):
    anuncio = jsonable_encoder(anuncio)
    new_anuncio = await db.insertar_anuncio(anuncio)
    return JSONResponse(content=new_anuncio, status_code=status.HTTP_201_CREATED)

##############################################################################

@app.put('/api/propiedades/{id}', 
         response_description = 'Actualizar un anuncio', 
         response_model=Anuncio)
async def actualizar_anuncio(id: str = Field(..., example='fd23114h2y0719d46ba9'), 
                             anuncio: Anuncio_actualizar = Body(..., example=examples.put_example)):
    anuncio = {k: v for k, v in anuncio.dict().items() if v is not None}
    if len(anuncio) >= 1:
        anuncio_actualizado = await db.actualizar_anuncio(id, anuncio)
        if anuncio_actualizado is not None:
            return anuncio_actualizado

    raise HTTPException(status_code=404, detail=f"Anuncio {id} not found")

##############################################################################

@app.delete('/api/propiedades/{id}', 
            response_description = 'Eliminar un anuncio')
async def borrar_anuncio(id: str = Field(..., example='fd23114h2y0719d46ba9')):
    anuncio_eliminado = db.eliminar_anuncio(id)
    if anuncio_eliminado.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Anuncio {id} not found")


#Añadir query parameters (limits, dates)