# Automatically generated Python file from Amoedo - 19.03.24.txt.txt

from unidecode import unidecode
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions

CEP_RJ = '20010-020'

target    = load_pkl('Updated3')#load_pkl('Strategics')['strategyTarget']#load_pkl('Updated') 
guideshop = 'Amoedo'
today     = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t 
target = target[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

driver = webdriver.Chrome() 
time.sleep(7)
# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8-sig") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)

    for ean,url in zip(eans,urls):
        
        driver.get(url)
        i = i+1
        time.sleep (2)
        soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source
        
        price = 0
        try: 
            if soup.find('span', {'class':'vtex-store-link-0-x-label vtex-store-link-0-x-label--btn-go-home w-100 tc ph6'}).text == 'Voltar a página inicial':
               continue
        except: 
            if soup.find('div', {'class':'vtex-flex-layout-0-x-flexRow vtex-flex-layout-0-x-flexRow--row-add-button'}).text == 'Indisponível': 
               continue
        

        try:
            preco2_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--summary')#'vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--product-price')
            price = unidecode(preco2_element.text.strip().replace("un","")).replace('R$','')\
                                                                 .replace(' ','')\
                                                                 .replace('.','')\
                                                                 .replace(',','.')
            price = np.float64(price)                                                #if preco2_element else "Valor indisponível"
            
        except:
            try:
                preco2_element = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--summary')#'vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--product-price')
                price = unidecode(preco2_element.text.strip().replace("un","")).replace('R$','')\
                                                                     .replace(' ','')\
                                                                     .replace('.','')\
                                                                     .replace(',','.')
                price = np.float64(price)                                                #if preco2_element else "Valor indisponível"
                
            except:
                price = 0 
        #priceDict = {1399.9:0} 
        #price = priceDict.get(price,price)
        #disponibilidade_element = soup.find('div', class_='vtex-store-components-3-x-title t-body mb3')
        #disponibilidade = "Produto disponível" if price!="Valor indisponível" else "Produto indisponível"
        # Adicionar os dados à lista
        linha = [ean, price, url]
        print(linha)
        csv_writer.writerow(linha)
        
driver.quit()        

