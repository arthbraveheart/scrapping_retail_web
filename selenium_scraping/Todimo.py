
# -*- coding: utf-8 -*-
"""
]Created on Tue Apr  2 16:13:21 2024

@author: ArthurRodrigues
"""

# Automatically generated Python file from Todimo 19.03.24.txt.txt

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
import csv
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions 
guideshop = 'Todimo MS E PR'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls
CEP = '79002-010'
#Lista para percorrer
#t 
target    = load_pkl('Targets')['targets']
target = target[target[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link {guideshop}'].astype({f'Link {guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

driver = webdriver.Firefox()

# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8-sig") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)


    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
        i = i+1
        time.sleep (3)
        soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source
        
       
        
        try:
            price_element = soup.find('span',{'class':'vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--product__price'})
            price = unidecode(price_element.text).strip().replace("/", "").replace("m²", "").replace('M2','').replace('R$','').replace(' ','').replace('.','')\
                                                                                          .replace(',','.')
            price = np.float64(price)
        except:
            price = 0
    
    
        
    
    
        linha = [ean, price, url]
        print("="*50)
        print(linha)      
        csv_writer.writerow(linha)
        
driver.quit()
