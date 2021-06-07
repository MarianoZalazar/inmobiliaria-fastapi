from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from unidecode import unidecode
from mongodb import insertar_anuncios
#import pprint


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

# Obtener valor del dolar a traves de una API
response_dolar_api = requests.get('https://api-dolar-argentina.herokuapp.com/api/dolarpromedio')
valor_dolar = json.loads(response_dolar_api.text)
valor_compra = float(valor_dolar["compra"])
valor_venta = float(valor_dolar["venta"])


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

        anuncios = dom.find_all(class_=clase_lista_de_anuncios)
        # ¿hay una lista de 'anuncios'?
        if anuncios != []:
            for anuncio in anuncios:
                titulo_anuncio = anuncio.find(class_=clase_titulo).a.h2.text
                precio = anuncio.find(class_=clase_precio)
                expensas = anuncio.find(class_=clase_expensas)
                barrio = anuncio.find(class_=clase_barrio).text.split(',')[0].split('/')[0].replace(' ', '-')  # Limpiar barrio
                inmueble = titulo_anuncio.split()[0]
                vendedor = anuncio.find(class_=clase_vendedor)
                fecha_publicacion = datetime.strptime(anuncio.find(class_=clase_fecha).text, '%d/%m/%Y')

                if precio != None:
                    moneda = precio.text.split()[0]
                    precio = float(precio.text.split()[1].replace('.', '').replace(',', '.'))
                    precio_peso = round(precio * valor_venta, 2) if moneda == 'USD' else precio
                    precio_dolar = round(precio_peso / valor_compra, 2)

                expensas = expensas.text.split('\xa0')[1].replace('.', '') if expensas != None else expensas
                vendedor = vendedor.text if vendedor != None else vendedor

                dict_anuncios = {
                    "titulo": titulo_anuncio,
                    "expensas": expensas,
                    "barrio": unidecode(barrio.lower()),
                    "inmueble": inmueble.lower(),
                    "precio_dolar": precio_dolar,
                    "precio_peso": precio_peso,
                    "fecha_publicacion": fecha_publicacion,
                    "vendedor": vendedor.lower(),
                    "tipo": tipo
                }

                lista_de_anuncios.append(dict_anuncios)
            num_pag += 1
        else:
            hay_anuncios = False

insertar_anuncios(lista_de_anuncios)
