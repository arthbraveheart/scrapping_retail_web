# Automatically generated Python file from Chatuba - 19.03.24.txt.txt

from unidecode import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import csv
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
guideshop = 'Chatuba'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t 
target =load_pkl('Updated3') #load_pkl('Strategics')['strategyTarget']#load_pkl('Updated2')#load_pkl('Targets')['targets']
target = target[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})
eans   = target['EAN']

options=Options()
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.disable_beforeunload', 1)

options.profile = firefox_profile

# inicia webdriver
driver = webdriver.Firefox(options=options)#firefox_profile=firefox_profile)

# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
   
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)


    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
        i = i+1
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source
        try:
            preco2_element = soup.find('span', {'class': 'vtex-product-price-1-x-currencyContainer'})
            preco2 = unidecode(preco2_element.text.strip().replace("un","")).replace('R$','').replace(' ','')\
                                                                .replace('.','')\
                                                                .replace(',','.')                                         
            preco2 = np.float64(preco2)
        except: #trying per EAN
        
            try: 
              ean     = target['EAN'][i]
              url_ean = f'https://www.chatuba.com.br/{ean}?_q={ean}&map=ft'
              driver.get(url_ean)
              time.sleep(5)
              preco2_element = soup.find('span', {'class': 'vtex-product-price-1-x-sellingPrice vtex-product-price-1-x-sellingPrice--summary-shelf vtex-product-price-1-x-sellingPrice--hasMeasurementUnit vtex-product-price-1-x-sellingPrice--summary-shelf--hasMeasurementUnit vtex-product-price-1-x-sellingPrice--hasUnitMultiplier vtex-product-price-1-x-sellingPrice--summary-shelf--hasUnitMultiplier'})
              preco2 = unidecode(preco2_element.text.strip().replace("un","")).replace('/m2','').replace('R$','').replace(' ','')\
                                                                  .replace('.','')\
                                                                  .replace(',','.')                                         
              preco2 = np.float64(preco2)
            except: 
              preco2 = 0   
        
        
        linha = [ean, preco2, url]
        print(linha)
        csv_writer.writerow(linha)
            
driver.quit()