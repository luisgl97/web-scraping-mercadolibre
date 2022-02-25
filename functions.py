import requests
from bs4 import BeautifulSoup
from lxml import etree

def todosProductos(url,producto):
        
    lista_titulos = []
    lista_urls = []
    lista_precios = []
    siguiente = url+producto
    
    while True:
    
        r=requests.get(siguiente)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            #Obtener titulos
            titulos = soup.find_all('h2',attrs={"class":"ui-search-item__title"})
            titulos = [i.text for i in titulos]
            lista_titulos.extend(titulos)
            
            #Obtener urls
            urls = soup.find_all('a',attrs={"class":"ui-search-item__group__element ui-search-link"})
            urls = [i.get ('href') for i in urls]
            lista_urls.extend(urls)
            
            #Obtener precios
            dom = etree.HTML(str(soup))
            precios = dom.xpath('//span[@class="price-tag ui-search-price__part"]//span[@class="price-tag-fraction"]')
            precios = [i.text for i in precios]
            lista_precios.extend(precios)
            
            ini = soup.find('span',attrs={'class':'andes-pagination__link'}).text
            #convertir string a entero
            ini= int(ini)
            
            paginador_final = soup.find('li',attrs={'class':'andes-pagination__page-count'})
            paginador_final = int (paginador_final.text.split(" ")[1])
        else:
            print("Respondio mal")
            break
        print(ini,paginador_final)  
        if ini==paginador_final:
            break
        siguiente = dom.xpath('//li[contains(@class,"--next")]/a')[0].get('href')
        
    return lista_titulos,lista_urls,lista_precios

def limiteProductos(url,producto,limite):
    lista_titulos = []
    lista_urls = []
    lista_precios = []
    siguiente = url+producto
    
    while True:
    
        r=requests.get(siguiente)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            #Obtener titulos
            titulos = soup.find_all('h2',attrs={"class":"ui-search-item__title"})
            titulos = [i.text for i in titulos]
            lista_titulos.extend(titulos)
            
            #Obtener urls
            urls = soup.find_all('a',attrs={"class":"ui-search-item__group__element ui-search-link"})
            urls = [i.get ('href') for i in urls]
            lista_urls.extend(urls)
            
            #Obtener precios
            dom = etree.HTML(str(soup))
            precios = dom.xpath('//span[@class="price-tag ui-search-price__part"]//span[@class="price-tag-fraction"]')
            precios = [i.text for i in precios]
            lista_precios.extend(precios)
            
            ini = soup.find('span',attrs={'class':'andes-pagination__link'}).text
            #convertir string a entero
            ini= int(ini)
            
            paginador_final = soup.find('li',attrs={'class':'andes-pagination__page-count'})
            paginador_final = int (paginador_final.text.split(" ")[1])
        else:
            print("Respondio mal")
            break
        print(ini,paginador_final)  
        
        if len(lista_titulos)>=int(limite):
            return lista_titulos[:limite],lista_urls[:limite],lista_precios[:limite]
        if ini==paginador_final:
            break
        
        siguiente = dom.xpath('//li[contains(@class,"--next")]/a')[0].get('href')
        
    return lista_titulos,lista_urls,lista_precios
