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
    fecha_publicacion: Optional[datetime] = datetime.now()
    inmueble: str = Field(...)
    expensas: float = Field(None)
    vendedor: str = Field(...)
    barrio: str = Field(None)
    tipo: str = Field(...)
    precio_peso: float = Field(...)
    #Buscar forma para autogestionar precio_dolar
    precio_dolar: float = Field(...)
    
    @validator('inmueble', 'barrio', 'tipo')
    def lowercase_strings(cls, v):
        return unidecode(v.lower())
    
    @validator('barrio')
    def verificar_barrio(cls, barrio):
        if barrio in lista_barrios:
            return barrio
        else:
            raise ValueError(f'{barrio} no corresponde')
    
    @validator('precio_peso', 'precio_dolar')
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
                "precio_peso": 14347190.0,
                "precio_dolar": 152321.8
        }}
        
class Anuncio_actualizar(BaseModel):
    titulo: Optional[str]
    fecha_publicacion: Optional[datetime] = datetime.now()
    inmueble: Optional[str]
    expensas: Optional[float]
    vendedor: Optional[str]
    barrio: Optional[str]
    tipo: Optional[str]
    precio_peso: Optional[float]
    precio_dolar: Optional[float]
    
    @validator('inmueble', 'barrio', 'tipo')
    def lowercase_strings(cls, v):
        return unidecode(v.lower())
    
    @validator('barrio')
    def verificar_barrio(cls, barrio):
        if barrio in lista_barrios:
            return barrio
        else:
            raise ValueError(f'{barrio} no corresponde')
    
    @validator('precio_peso', 'precio_dolar')
    def round_result(cls, v):
        return round(v, 2)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}