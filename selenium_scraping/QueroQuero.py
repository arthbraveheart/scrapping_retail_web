# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:47:08 2024

@author: ArthurRodrigues
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target
import csv
from unidecode import unidecode
import numpy as np
# definitions
guideshop = 'Quero-Quero'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls
target    = load_pkl('Updated2')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
#Lista para percorrer
#t = 200
#target = target[target[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[t:210]
eans   = target.loc[:,'EAN']#[:t]





# Inicializar o driver do Selenium (certifique-se de ter o webdriver correspondente instalado, como o chromedriver)
driver = webdriver.Firefox()

# URL base da Quero Quero
base_url = 'https://www.queroquero.com.br' 
time1            = time.time()
with open(out_path + f'QueroQuero_{today}.csv', "w", newline="", encoding="utf-8-sig") as f:
     # Especifica o separador como ponto e vírgula
     csv_writer = csv.writer(f, delimiter=';')
     titulo = ['EAN', 'Price','URL']  # Nome das colunas
     csv_writer.writerow(titulo)
     try:
         
         driver.get(base_url)
         time.sleep(5)
         # Iterar sobre os links
         for ean,url in zip(eans,urls):
             link = url
             try:
                # Abrir o navegador e acessar a página principal
                
                
                driver.get(f"https://www.queroquero.com.br/{ean}?_q={ean}&map=ft")
        
                time.sleep(5)
        
                # Criar um objeto BeautifulSoup com o código fonte da página
                soup = BeautifulSoup(driver.page_source, 'html.parser')
        
                # Obter o preço
                try:
                    
                    price_element = soup.find('span',{'class':'vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--summary'})
                    price = unidecode(price_element.text).strip().replace("/", "").replace("m²", "").replace('M2','').replace('R$','').replace(' ','').replace('.','')\
                                                                                                  .replace(',','.')
                    price = np.float64(price)
                    # Adicionar os resultados ao DataFrame
                    linha = [ean, price, driver.current_url]
                    print(linha)
                    csv_writer.writerow(linha)
                except:
                    if url!='Não encontrado':
                       driver.get(url)
                       time.sleep(5)
                       soup = BeautifulSoup(driver.page_source, 'html.parser')
                       # Obter o preço
                       try:
                           
                           price_element = soup.find('span',{'class':'vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--product-price'})
                           price = unidecode(price_element.text).strip().replace("/", "").replace("m²", "").replace('M2','').replace('R$','').replace(' ','').replace('.','')\
                                                                                                         .replace(',','.')
                           price = np.float64(price)
                           # Adicionar os resultados ao DataFrame
                           linha = [ean, price, url]
                           print(linha)
                           csv_writer.writerow(linha)
                       except:
                           continue
                    else:
                        continue
                        
                
        
             except Exception as e:
                # Se ocorrer um erro, imprima a mensagem de erro e salve o DataFrame até esse ponto
                print(f"Erro: {e}")
                
     except Exception as e:
         print("Ocorreu um erro:", str(e))

     finally:
         # Fechar o WebDriver
         driver.quit()
         time2 =  time.time()
         print("Execution time:",time2-time1) 
         
         
# Fechar o navegador no final
driver.quit()


