from fastapi import Query


class CommonQueryModel():
    def __init__(self, limit: int = Query(0, title="Limita el valor por cantidad"),
                 sort_date: int = Query(
                     1, title="Ordenar por fecha: 1=Ascendente(Default) -1=Descendente"),
                 moneda: str = Query(
                     dict(), title="Tipo de moneda por la que se va a ordenar"),
                 sort_precio: int = Query(
                     1, title="Ordenar por precio: 1=Ascendente(Default) -1=Descendente")
                 ):
        self.limit = limit
        self.sort_date = sort_date
        self.moneda = moneda
        self.sort_precio = sort_precio
