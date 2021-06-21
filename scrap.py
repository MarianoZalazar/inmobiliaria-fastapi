from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from unidecode import unidecode
from models.anuncio import Anuncio
import pprint
from mongodb import insertar_anuncios


lista_de_anuncios = []
#anuncio_id = 0

# Cambiar variables en caso de actualizacion de la pagina
clase_lista_de_anuncios = 'StyledCard-n9541a-1 ixiyWf'
clase_titulo = 'StyledCardInfo-n9541a-2 ctwAhK'
clase_precio = 'StyledPrice-sc-1wixp9h-0 bZCCaW'
clase_expensas = 'StyledMaintenanceFees-n9541a-6 cRsmn'
clase_barrio = 'StyledLocation-n9541a-7 fqaBNm'
clase_fecha = 'StyledTooltip-n9541a-0 eeGwaF'
clase_vendedor = 'seller-name'

for tipo in ['venta', 'alquiler']:
    hay_anuncios = True
    num_pag = 1
    while hay_anuncios and num_pag <= 25:
        print("Numero de pagina: ", num_pag, " de ", tipo)
        url = f"https://www.properati.com.ar/s/capital-federal/{tipo}/?page={num_pag}"
        response = requests.get(url)
        response.encoding = "utf-8"
        html = response.text
        dom = BeautifulSoup(html, features="html.parser")

        # ¿hay una lista de 'anuncios'?
        if ((anuncios := dom.find_all(class_=clase_lista_de_anuncios)) != []):
            for anuncio in anuncios:
                titulo_anuncio = anuncio.find(class_=clase_titulo).a.h2.text
                precio = anuncio.find(class_=clase_precio)
                expensas = anuncio.find(class_=clase_expensas)
                barrio = anuncio.find(class_=clase_barrio).text.split(
                    ',')[0].replace(' / ', '-').replace(' ', '-')  # Limpiar barrio
                inmueble = titulo_anuncio.split()[0]
                vendedor = anuncio.find(class_=clase_vendedor)
                fecha_publicacion = datetime.strptime(
                    anuncio.find(class_=clase_fecha).text, '%d/%m/%Y')

                if precio != None:
                    moneda = precio.text.split()[0]
                    moneda = 'ARS' if moneda == '$' else moneda
                    precio = float(precio.text.split()[
                                   1].replace('.', '').replace(',', '.'))

                expensas = expensas.text.split('\xa0')[1].replace(
                    '.', '') if expensas != None else expensas
                vendedor = vendedor.text if vendedor != None else vendedor

                anuncio = Anuncio(
                    titulo=titulo_anuncio,
                    expensas=expensas,
                    barrio=barrio,
                    inmueble=inmueble,
                    precio=precio,
                    moneda=moneda,
                    fecha_publicacion=fecha_publicacion,
                    vendedor=vendedor.lower(),
                    tipo=tipo)

                lista_de_anuncios.append(anuncio.dict())
            num_pag += 1
        else:
            hay_anuncios = False


# pprint.pprint(lista_de_anuncios)
insertar_anuncios(lista_de_anuncios)
