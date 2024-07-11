# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:46:12 2024

@author: ArthurRodrigues
"""


# Automatically generated Python file from Santa Cruz - 19.03.24.txt.txt
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
from unidecode import unidecode
from settings import  out_path #from the current package
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls


target = pd.read_excel('C:/Users/ArthurRodrigues/Codes/Pricing/Target/Curva A - Krepischi.xlsx', sheet_name='Curva A')
target = target.fillna('Não encontrado')

#Lista para percorrer
#t 
target = target.loc[target['LINK KREPISCHI']!='Não encontrado']#.str.contains('piso|porcelanato')][target['LINK KREPISCHI']!='Não encontrado']
urls   = target['LINK KREPISCHI'].astype({'LINK KREPISCHI':'str'})#[:t]
eans   = target['EAN']#[:t]


# Cria o arquivo CSV
with open(out_path + f"KREPISCHI_{today}.csv", "w", newline="", encoding="utf-8-sig") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
   
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)
    options = Options()
    #options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images":2,
        "profile.default_content_setting_values.notifications":2,
        "profile.managed_default_content_settings.stylesheets":2,
        #"profile.managed_default_content_settings.cookies":2,
        #"profile.managed_default_content_settings.javascript":1,
        #"profile.managed_default_content_settings.plugins":1,
        "profile.managed_default_content_settings.popups":2,
        #"profile.managed_default_content_settings.geolocation":2,
        #"profile.managed_default_content_settings.media_stream":2,


        }
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)#Firefox()
    
    #driver = webdriver.Firefox()
    
    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
        time.sleep(2)

        try:
            # Obtenha o conteúdo da página com BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                # Encontre o elemento desejado usando BeautifulSoup
                preco1_element = soup.find(class_='precoMetroAtual')
                preco         = unidecode(preco1_element.text.strip()).replace('\n','')\
                                                                    .replace('/M2','')\
                                                                     .replace('R$','')\
                                                                      .replace(' ','')\
                                                                       .replace('.','')\
                                                                        .replace(',','.') 
                preco = np.float64(preco)                                                        
            except:    
                # Extraia o texto do elemento
                try:
                    preco2_element = soup.find(class_='PrecoPrincipal color-tone-2')
                    preco = unidecode(preco2_element.text.strip()).replace('\n','')\
                                                                        .replace('/M2','')\
                                                                         .replace('R$','')\
                                                                          .replace(' ','')\
                                                                           .replace('.','')\
                                                                            .replace(',','.') 
                    preco = np.float64(preco)
                except:    
                    preco = 0
        except Exception as e:
            print(f"Erro ao processar a URL {url}: {str(e)}")
            preco1 = "Erro ao processar"

        linha = [ean,preco,url]
        print(linha)
        csv_writer.writerow(linha)


driver.quit()
