from bs4 import BeautifulSoup
import requests
from mongodb import insertar_anuncios

tipos = ['venta', 'alquiler']
lista_de_anuncios = []
#anuncio_id = 0

#Cambiar variables en caso de actualizacion de la pagina
clase_lista_de_anuncios = 'StyledCard-n9541a-1 ixiyWf'
clase_titulo = 'StyledCardInfo-n9541a-2 ctwAhK'
clase_precio = 'StyledPrice-n9541a-5 eErRfd'
clase_expensas =  'StyledMaintenanceFees-n9541a-6 cRsmn'
clase_barrio = 'StyledLocation-n9541a-7 fqaBNm'
clase_inmueble = 'StyledCardInfo-n9541a-2 ctwAhK'
clase_fecha = 'StyledTooltip-n9541a-0 eeGwaF'
clase_vendedor = 'seller-name'

for tipo in tipos:
    hay_anuncios = True
    num_pag = 1
    while hay_anuncios and num_pag < 50:
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
                titulo_anuncio = anuncio.find(
                    class_= clase_titulo).a.h2.text
                precio = anuncio.find(class_=clase_precio)
                barrio = anuncio.find(
                    class_= clase_barrio).text.split(',')[0]  # Limpiar barrio
                inmueble = anuncio.find(
                    class_=clase_inmueble).a.h2.text.split()[0]
                fecha_publicacion = anuncio.find(
                    class_=clase_fecha).text
                vendedor = anuncio.find(class_=clase_vendedor)
                
                if precio != None:
                    precio = precio.text.split()[1].replace('.', '')
                    moneda = precio.text.split()[0]
                    
                expensas = expensas.text.split('\xa0')[1].replace('.', '') if expensas != None else expensas
                moneda = 'ARS' if moneda == '$' else 'USD'
                vendedor = vendedor.text if vendedor != None else vendedor
                #anuncio_id += 1
                
                dict_anuncios = {
                    #"id_anuncio": anuncio_id
                    "titulo": titulo_anuncio,
                    "moneda": moneda,
                    "expensas": expensas,
                    "barrio": barrio.lower(),
                    "inmueble": inmueble.lower(),
                    "precio": precio,
                    "fecha_publicacion": fecha_publicacion,
                    "vendedor": vendedor.lower(),
                    "tipo": tipo
                }

                lista_de_anuncios.append(dict_anuncios)
            num_pag += 1
        else:
            hay_anuncios = False

insertar_anuncios(lista_de_anuncios)