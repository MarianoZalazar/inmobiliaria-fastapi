from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from unidecode import unidecode
from barrios import lista_barrios
#from pyobjectid import PydanticObjectId

class Anuncio(BaseModel):
    titulo: str = Field(...)
    fecha_publicacion: Optional[datetime] = datetime.now()
    inmueble: str = Field(...)
    expensas: float = Field(None)
    #Implementar tipo User
    vendedor: str = Field(...)
    barrio: str = Field(...)
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
            raise ValueError('Barrio no corresponde')
    
    @validator('precio_peso', 'precio_dolar')
    def round_result(cls, v):
        return round(v, 2)