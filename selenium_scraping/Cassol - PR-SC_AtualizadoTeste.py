# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:16:59 2024

@author: igor.dias
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from unidecode import unidecode
import time
import re
from settings import atualizado_path, out_path



UF      = 'SC' #'SC' 'PR'
CEP_SC = '88010-020' #Floripa-SC
CEP_PR = '80240-424' #Curitiba-PR

driver = webdriver.Firefox()
driver.get('https://www.cassol.com.br/')
time.sleep(15)
def get_info_from_url(url, driver):
    try:
        driver.get(url)
        #time.sleep(5)
        
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Espera até que o elemento de preço seja visível na página
        try:
           
           price_element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME,"cassol-region-id-1-x-price"))) 
           price = unidecode(price_element.text.replace(' ','').replace('\n',' ').replace('R$','')).replace('/m2','').replace(' ','') if price_element else '0'#"Não encontrado"
           #print(f"Preço: {price}")
        except:
            try:
               price_element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME,'product-price__container')))
               price = unidecode(price_element.text.replace(' ','').replace('\n',' ').replace('R$','')).replace('/m2','').replace(' ','') #if price_element else "Não encontrado"
               #print(f"Preço: {price}") 
            except:
               price_element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME,'sc-iGgWBj cexvao')))
               price = unidecode(price_element.text.replace(' ','').replace('\n',' ')).replace('ouemate','').replace('semjuros','').replace('R$','').replace(' ','') # if price_element else "Não encontrado"
               #print(f"Preço: {price}")
                
        price = price.replace(',','.')
        if price.__contains__('x'):
            #price = price.replace(',','.')
            priceDot =  price.split('x')
            realPrice = int(priceDot[0])*float(priceDot[1])
            price = realPrice
        print(f"Preço: {price}")    
        return price
    
    
    except Exception as e:
        
        print(f"Erro ao acessar {url}: {e}")
        return "0"

def main():
    file_path = atualizado_path
    today  = time.strftime("%d-%m-%Y")
    
    
    df_excel = pd.read_excel(file_path)
    df_excel = df_excel[df_excel['Link Cassol'].str.contains('cassol')]
    data = []
     
    for url,ean in zip(df_excel['Link Cassol'],df_excel['EAN']):
        
        price = get_info_from_url(url, driver)
        
        data.append([ean, price, url])

    df_result = pd.DataFrame(data, columns=['EAN', 'Preço', 'URL'])
    df_result.to_csv(out_path + f'Cassol_{UF}_{today}.csv', sep=';', index=False, encoding='utf-8-sig')

    driver.quit()

if __name__ == "__main__":
    main()



"""

try:
   price_element =WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.vtex-rich-text-0-x-paragraph--productUnavailableTitle')))
   price = '-1' if price_element else '0'
   #print(f"Preço: {price}")
except:
    
    return "0" 
"""