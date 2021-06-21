from fastapi import FastAPI, HTTPException, Body, status,  Path, Query, Depends
from starlette.responses import RedirectResponse
from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import examples
from models.anuncio import Anuncio, Anuncio_actualizar
from models.commonquery import CommonQueryModel
import mongodb as db

def check_list_len(lista_anuncios, resource="Resource"):
    if len(lista_anuncios) >= 1:
        return True
    else:
        raise HTTPException(status_code=404, detail=f"{resource} not found")

app = FastAPI(title="Inmobiliaria API",
              description="API para disponibilizacion de datos sobre propiedades en CABA. Informacion conseguida a traves de Properati"
              )


@app.get('/', include_in_schema=False)
async def root():
    response = RedirectResponse('/docs')
    return response

##############################################################################

@app.get('/api/{barrio_o_tipo}',
         response_description='Obtener lista de anuncios por barrio o tipo de operacion',
         response_model=List[Anuncio])
async def get_by_barrio_o_tipo(barrio_o_tipo: str = Path(..., title="Un barrio o tipo de operacion",
                                                         examples={
                                                             "Barrio": {"value": "las-canitas"},
                                                             "Tipo": {"value": "venta"}
                                                         }),
                               q: CommonQueryModel = Depends(CommonQueryModel)
                               ):
    if barrio_o_tipo == 'venta' or barrio_o_tipo == 'alquiler':
        lista_anuncios = await db.buscar_anuncios({"tipo": barrio_o_tipo.lower(), **q.moneda}, q)
    else:
        lista_anuncios = await db.buscar_anuncios({"barrio": barrio_o_tipo.lower(), **q.moneda}, q)
        
    if check_list_len(lista_anuncios, barrio_o_tipo):
        return lista_anuncios

##############################################################################


@app.get('/api/{barrio}/{inmueble}',
         response_description='Obtener lista de anuncios por barrio e inmueble',
         response_model=List[Anuncio])
async def get_by_barrio_inmueble(barrio: str = Path(...,
                                                    title="Nombre del barrio, intercambiar espacios con '-' ",
                                                    example="nunez"),
                                 inmueble: str = Path(..., title="Tipo de inmueble",
                                                      example="departamento"),
                                 q: CommonQueryModel = Depends(CommonQueryModel)):
    lista_anuncios = await db.buscar_anuncios({'barrio': barrio.lower(), 'inmueble': inmueble.lower(), **q.moneda}, q)
    if check_list_len(lista_anuncios):
        return lista_anuncios

##############################################################################


@app.get('/api/{barrio}/{inmueble}/{tipo}',
         response_description='Obtener lista de anuncios por barrio, inmueble y tipo de operacion',
         response_model=List[Anuncio])
async def get_by_barrio_inmueble_tipo(barrio: str = Path(...,
                                                         title="Nombre del barrio, intercambiar espacios con '-' ",
                                                         example="san-nicolas"),
                                      inmueble: str = Path(
                                          ..., title="Tipo de inmueble", example="casa"),
                                      tipo: str = Path(
                                          ..., title="Tipo de operacion alquiler/venta", example="alquiler"),
                                      q: CommonQueryModel = Depends(CommonQueryModel)):
    lista_anuncios = await db.buscar_anuncios({'barrio': barrio.lower(), 
                                               'inmueble': inmueble.lower(), 
                                               'tipo': tipo.lower(),
                                               **q.moneda}, q)
    if check_list_len(lista_anuncios):
        return lista_anuncios 

##############################################################################


@app.post('/api/propiedades',
          response_description='Publicar un anuncio',
          response_model=Anuncio)
async def publicar_anuncio(anuncio: Anuncio = Body(..., example=examples.post_example)):
    anuncio = jsonable_encoder(anuncio)
    new_anuncio = await db.insertar_anuncio(anuncio)
    return JSONResponse(content=new_anuncio, status_code=status.HTTP_201_CREATED)

##############################################################################


@app.put('/api/propiedades/{id}',
         response_description='Actualizar un anuncio',
         response_model=Anuncio)
async def actualizar_anuncio(id: str = Path(..., example='fd23114h2y0719d46ba9'),
                             anuncio: Anuncio_actualizar = Body(..., example=examples.put_example)):
    anuncio = {k: v for k, v in anuncio.dict().items() if v is not None}
    if check_list_len(lista_anuncios, f"Anuncio {id}"):
        anuncio_actualizado = await db.actualizar_anuncio(id, anuncio)
        if anuncio_actualizado is not None:
            return anuncio_actualizado

##############################################################################


@app.delete('/api/propiedades/{id}',
            response_description='Eliminar un anuncio')
async def borrar_anuncio(id: str = Path(..., example='fd23114h2y0719d46ba9')):
    anuncio_eliminado = await db.eliminar_anuncio(id)
    if anuncio_eliminado.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Anuncio {id} not found")
