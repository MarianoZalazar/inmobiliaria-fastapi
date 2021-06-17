from fastapi import Query
from pydantic import BaseModel, validator
from typing import Optional, List

class CommonQueryModel(BaseModel):
    limit: int = Query(0, title="limit")
    sort_date: int = Query(1, title="Sort Date")
    moneda: str = Query(None, title="moneda")

    @validator('moneda')
    def check_moneda(cls, moneda):
        if moneda != None:
            return {"moneda": moneda}
        else:
            return {}
            