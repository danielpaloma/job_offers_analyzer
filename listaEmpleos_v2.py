from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import requests
import pandas as pd
import numpy as np
import re


def leer_url(url):
	my_url = url
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	return page_soup


def lista_links_principales(numero_paginas):

	links_principales= [0 for _ in range(numero_paginas)] #10
	links_principales[0]= 'https://www.computrabajo.com.co/trabajo-de-electricista'

	for i in range(1,numero_paginas):
		links_principales[i]='https://www.computrabajo.com.co/trabajo-de-electricista?p=' + str(i) 

	del links_principales[1]

	return links_principales

def listaEmpleos(url):
	def isBlank (myString):
	    if myString and myString.strip():
	        #myString is not None AND myString is not empty or blank
	        return False
	    #myString is None OR myString is empty or blank
	    return True

	page_soup = leer_url(url)
	containers = page_soup.findAll("div",{"class":"iO"})
	k=len(containers)
	i=0
	#campos de la tabla
	id_oferta = [0 for _ in range(k)]
	fecha = [0 for _ in range(k)]
	cargo=[0 for _ in range(k)]
	link_oferta=[0 for _ in range(k)]
	
	#1. Extraer la informacion de los campos

	for i in range(k):
		#ID OFERTA
		try:
			id_oferta[i] = containers[i].find("a",{"class":"js-o-link"})['href'].split('-')[-1]
		except AttributeError:
			id_oferta[i]=""

		#FECHA
		try:
			fecha[i] = containers[i].find("span",{"class":"dO"}).get_text()
			
		except AttributeError:
			fecha[i]=""
		
		#CARGO
		try:
			cargo[i] = containers[i].find("a",{"class":"js-o-link"}).string
			cargo[i] = cargo[i].strip()
		except AttributeError:
			cargo[i]=""

		#link de la oferta
		try:
			link_oferta[i] = containers[i].find("a",{"class":"js-o-link"})['href']
		except AttributeError:
			link_oferta[i]=""

		i+=1
	
	#2. creando un Dataframe con las ofertas recopiladas
	tabla1 = pd.DataFrame(list(zip(id_oferta,fecha,cargo, link_oferta)),
               columns =['id_oferta','fecha','cargo','link_oferta']) 

	return tabla1

#Definir una ARAÑA --> funcion que tome como entrada la lista 'link_oferta'
# navega cada uno de los link y genera un DF con:
# id_oferta, cargo, descripcion, experiencia


def link_spider(links, cantidad_links):
	
	k= cantidad_links
	i=0

	#campos de la tabla2
	id_oferta = [0 for _ in range(k)]
	empresa=[0 for _ in range(k)]
	cargo=[0 for _ in range(k)]
	descripcion=[0 for _ in range(k)]
		
	#itera sobre todas las url guardadas en 'links'

	for i in range(k):

		page_soup = leer_url(links[i])
		
		container = page_soup.find("div",{"id":"MainContainer"})
		
	#1. Extraer la informacion de los campos
		#ID OFERTA
		try:
			id_oferta[i] = links[i].split('-')[-1]
		except AttributeError:
			id_oferta[i]=""

		#EMPRESA
		try:
			empresa[i] = container.find("a",{"id":"urlverofertas"}).get_text().strip()
		except AttributeError:
		 	empresa[i]=""

		#CARGO
		try:
			cargo[i] = container.find("h1",{"class":"m0"}).get_text().strip()
		except AttributeError:
			cargo[i]=""

		#DESCRIPCION
		try:
			descripcion[i] = container.find("section",{"class":"boxWhite fl w_100 detail_of mb20 bWord"}).get_text().strip()
			descripcion[i] = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', descripcion[i], flags=re.M)
		
		except AttributeError:
			descripcion[i]=""

		i+=1

	#2. creando un Dataframe con las ofertas recopiladas
	tabla2 = pd.DataFrame(list(zip(id_oferta,empresa, cargo, descripcion)), 
               columns =['id_oferta','empresa','cargo','descripcion']) 

	return tabla2



#1. Crear el listado de links principales
# recibe como parametro el numero de páginas principales a navegar

links_principales = lista_links_principales(10)


#2. Leer cada link principal y obtener la tabla de empleos (con sus links secundarios)
Tabla_empleos = pd.DataFrame(columns =['id_oferta','fecha','cargo','link_oferta'])

for link in links_principales:
	Tabla_empleos = Tabla_empleos.append(listaEmpleos(link), ignore_index = True)

Tabla_empleos.to_excel('Electricista_1_20210107.xls')

#3. Crear el listado de links secundarios, 

links_secundarios = Tabla_empleos.link_oferta.apply(lambda x: 'https://www.computrabajo.com.co' + x)
cantidad_links = len(links_secundarios)

#Tabla_descripcion = pd.DataFrame(columns =['id_oferta','empresa','cargo','descripcion'])

Tabla_descripcion = link_spider(links_secundarios,cantidad_links)
print(Tabla_descripcion.head())
Tabla_descripcion.to_excel('Electricista_2_20210107.xls')
