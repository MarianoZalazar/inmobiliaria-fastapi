from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from unidecode import unidecode
from barrios import lista_barrios
from models.pyobjectid import PydanticObjectId
from bson import ObjectId


class Anuncio(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    titulo: str = Field(...)
    fecha_publicacion: datetime = Field(datetime.now())
    inmueble: str = Field(...)
    vendedor: str = Field(...)
    barrio: str = Field(...)
    tipo: str = Field(...)
    moneda: str = Field(...)
    precio: float = Field(..., gt=0)
    expensas: float = Field(None)

    @validator('inmueble', 'barrio', 'tipo')
    def lowercase_strings(cls, v):
        return unidecode(v.lower())

    @validator('barrio')
    def verificar_barrio(cls, barrio):
        if barrio in lista_barrios:
            return barrio
        else:
            raise ValueError(f'{barrio} no corresponde')

    @validator('moneda')
    def verificar_moneda(cls, moneda):
        if moneda == 'ARS' or moneda == 'USD':
            return moneda
        else:
            raise ValueError(f'{moneda} no corresponde')

    @validator('precio')
    def round_result(cls, v):
        return round(v, 2)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "60bf5114071947dsa145d46bb2",
                "titulo": "Departamento en Caballito",
                "fecha_publicacion": "2021-06-07T00:00:00",
                "inmueble": "departamento",
                "expensas": 10000,
                "vendedor": "cortese propiedades",
                "barrio": "caballito",
                "tipo": "venta",
                "moneda": "ARS",
                "precio": 14347190.0
            }}


class Anuncio_actualizar(BaseModel):
    titulo: Optional[str]
    inmueble: Optional[str]
    expensas: Optional[float]
    vendedor: Optional[str]
    barrio: Optional[str]
    tipo: Optional[str]
    moneda: Optional[str]
    precio: Optional[float]

    @validator('inmueble', 'barrio', 'tipo')
    def lowercase_strings(cls, v):
        return unidecode(v.lower())

    @validator('barrio')
    def verificar_barrio(cls, barrio):
        if barrio in lista_barrios:
            return barrio
        else:
            raise ValueError(f'{barrio} no corresponde')

    @validator('moneda')
    def verificar_moneda(cls, moneda):
        if moneda == 'ARS' or moneda == 'USD':
            return Moneda
        else:
            raise ValueError(f'{moneda} no corresponde')

    @validator('precio')
    def round_result(cls, v):
        if v > 0:
            return round(v, 2)
        else:
            raise ValueError('Precio debe ser mayor a 0')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
