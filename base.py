# https://127.0.0.1:3030/api/BARRIO/INMUEBLE/TIPO

from bs4 import BeautifulSoup
import requests
from mongodb import client_mongo

num_pag = 1
hay_anuncios = True
list_of_dicts = []
dict_anuncios = {}
id_anuncio = 0
while hay_anuncios:
    url = "https://www.properati.com.ar/s/palermo/alquiler/?page={}".format(num_pag)
    print("Numero de pagina: ", num_pag)
    response = requests.get(url)
    response.encoding = "utf-8"
    html = response.text
    dom = BeautifulSoup(html, features = "html.parser")
    anuncios = dom.find_all( attrs = { 'class' : 'StyledCard-n9541a-1 ixiyWf' })
    # ¿hay una lista de 'anuncios'?
    if anuncios != []:
        for anuncio in anuncios:
            titulo_anuncio = anuncio.find(class_='StyledCardInfo-n9541a-2 ctwAhK').a.h2.text
            precio = anuncio.find(class_='StyledPrice-n9541a-5 eErRfd')
            moneda = anuncio.find(class_='StyledPrice-n9541a-5 eErRfd')
            expensas = anuncio.find(class_='StyledMaintenanceFees-n9541a-6 cRsmn')
            barrio = anuncio.find(class_='StyledLocation-n9541a-7 fqaBNm').text.split(',')[0] #Limpiar barrio
            tipo = anuncio.find(class_='StyledCardInfo-n9541a-2 ctwAhK').a.h2.text.split()[0]
            
            if expensas != None: 
                expensas = expensas.text.split('\xa0')[1].replace('.','') 
            else:
                expensas = None
                
            if precio != None:
                precio = precio.text.split()[1].replace('.','')
                moneda = moneda.text.split()[0]
            else:
                precio = None
                moneda = None
            
            if moneda == '$':
                moneda = 'ARS'
                
            dict_anuncios = {
                            "titulo": titulo_anuncio,
                            "moneda": moneda,
                            "expensas": expensas,
                            "barrio": barrio.lower(),
                            "tipo": tipo.lower(),
                            "precio": precio 
                            }
            id_anuncio +=1
            
            list_of_dicts.append(dict_anuncios)
            
        #
        #print(dict_anuncios)
        #ist_of_dicts = [dict_anuncio for dict_anuncio in dict_anuncios]
        
        #hay_anuncios = False
        num_pag += 1
    else:
        hay_anuncios = False
        
if list_of_dicts != []: 
    print('Insertando')
    client_mongo['worshop2']['properati'].insert_many(list_of_dicts)
else:
    print("No hay resultados")