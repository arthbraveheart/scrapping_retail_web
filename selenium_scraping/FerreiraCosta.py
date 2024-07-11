# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:29:49 2024

@author: ArthurRodrigues
"""

from unidecode import unidecode
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import csv
import time
import numpy as np
import pandas as pd
import warnings
from settings import out_path
from merged import load_pkl

# Suppress all warnings
warnings.filterwarnings("ignore")

# Definitions
guideshop = 'FerreiraCosta'
today = time.strftime("%d-%m-%Y")

target = load_pkl("Updated3")

# Filtra os links que não são 'Não encontrado'
filtered_df = target[target[f'Link{guideshop}'] != 'Não encontrado']
urls = filtered_df[f'Link{guideshop}'].astype(str)
eans = filtered_df['EAN']

# Configurar o navegador usando o driver correspondente
driver = webdriver.Chrome()
time1 = time.time()

# Cria o arquivo CSV
#out_path = r'C:\Users\Assis\\Documents\Sellers - 10.06.24'
with open(f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)

    for i, (ean, url) in enumerate(zip(eans, urls)):
        # Navegar para a página
        driver.get(url)
        
        # Espera 15 segundos na primeira URL
        
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source
        # Extrair as informações desejadas usando Selenium
        try:
            price_element = soup.find('h1', {'data-cy': 'box-price-product-price-value'})
            price = price_element.text.strip().replace('R$', '').replace(',', '.').replace('\xa0', '')

        except Exception as e:
            price = "Valor indisponível"
            print(f"Error extracting price for URL {url}: {e}")

        # Adicionar os dados à lista
        linha = [ean, price, url]
        print(linha)
        csv_writer.writerow(linha)

time2 = time.time()
print("Execution time:", time2 - time1)

driver.quit()  # Fecha o navegador após cada iteração
