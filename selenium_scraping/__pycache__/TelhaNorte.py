# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:27:05 2024

@author: ArthurRodrigues
"""

# Automatically generated Python file from Telha Norte - 19.03.24.txt.txt

from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

from settings import  out_path #from the current package
from merged import target_merged
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions 
guideshop = 'Telha Norte MG SP'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t 
target = target_merged[target_merged[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link {guideshop}'].astype({f'Link {guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]


driver = webdriver.Firefox()
# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'URL', 'PriceUN', 'PriceUN']
    csv_writer.writerow(titulo)

    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
        i = i+1
        time.sleep (3)
        soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source

        # Encontre os elementos desejados usando BeautifulSoup
        try:
            valor2 = soup.select_one('.telhanorte-telha-store-app-1-x-preco-best-un').get_text(strip=True)
        except:
            valor2 = "Não encontrado"

        try:
            valor3 = soup.select_one('.telhanorte-telha-store-app-1-x-preco-m2').get_text(strip=True)
        except:
            valor3 = "Não encontrado"

        linha = str(ean) + ';' + url + ';' + valor2 + ';' + valor3 + ';' + '\n'
        print("="*50)
        print(linha)      
        f.write(linha)
        
driver.quit()        