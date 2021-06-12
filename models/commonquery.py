from fastapi import Query


class CommonQueryModel():
    def __init__(self, limit: int = Query(0, title="Limita el valor por cantidad"),
                 sort_date: int = Query(
                     1, title="Ordenar por fecha: 1=Ascendente(Default) -1=Descendente"),
                 moneda: str = Query(
                     dict(), title="Tipo de moneda por la que se va a ordenar")):
        self.limit = limit
        self.sort_date = sort_date
        self.moneda = moneda
