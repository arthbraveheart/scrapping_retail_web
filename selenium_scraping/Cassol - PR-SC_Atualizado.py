# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:16:59 2024

@author: arthur
"""

import time
import csv
import json
import warnings
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target


def setLocation(driver,cidade): 
    
    try:
        
            #driver.find_element(By.CSS_SELECTOR,'.cassol-region-id-5-x-wrapper > div:nth-child(1) > button:nth-child(1)').click()
            #driver.implicity_wait(2)
            toDigit = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.cassol-region-id-5-x-modalInput-container'))) #driver.find_element(By.CSS_SELECTOR,'.cassol-region-id-5-x-modalInput-container')
            ActionChains(driver).send_keys_to_element(toDigit, cepDict[cidade]).perform()
            #driver.implicity_wait(4)
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            driver.find_element(By.CSS_SELECTOR,'.cassol-region-id-5-x-button').click()
            #driver.implicity_wait(10)
        
    except Exception as e:
        ActionChains(driver).move_by_offset(6, 120).click().perform()
        print(f"Erro ao trocar a Localidade para {cidade} pelo seguinte motivo:\n", str(e))
        
        
def getPrice(soup):
   if getDisp(soup)==True: 
        try:
           
           price_element = soup.find('h2', class_="cassol-region-id-1-x-price") 
           price = unidecode(price_element.text.replace(' ','').replace('\n',' ').replace('R$','')).replace('/m2','').replace(' ','') #if price_element else '0'#"Não encontrado"
           #print(f"Preço: {price}")
        except:
            try:
               price_element = soup.find('span', class_='product-price__container')
               price = unidecode(price_element.text.replace(' ','').replace('\n',' ').replace('R$','')).replace('/m2','').replace(' ','') #if price_element else "Não encontrado"
               #print(f"Preço: {price}") 
            except:
               price_element = soup.find('p', class_='sc-iGgWBj cexvao')
               price = unidecode(price_element.text.replace(' ','').replace('\n',' ')).replace('ouemate','').replace('semjuros','').replace('R$','').replace(' ','') # if price_element else "Não encontrado"
               #print(f"Preço: {price}")
        price = price.replace('.','')       
        price = price.replace(',','.')
        if price.__contains__('x'):
            #price = price.replace(',','.')
            priceDot =  price.split('x')
            realPrice = int(priceDot[0])*float(priceDot[1])
            price = realPrice        
        return price
   else:
        return 0

def getDisp(soup):
    try:
        disp = soup.find('p',{'class':'lh-copy vtex-rich-text-0-x-paragraph vtex-rich-text-0-x-paragraph--productUnavailableTitle'}).text
        if 'retirado' in disp:
            return False
        else:
            return True
    except:    
        return True


def get_info_from_url(url, driver,loc,cidade):
        
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Espera até que o elemento de preço seja visível na página
        try:
            if soup.find('div',{'class':'cassol-region-id-5-x-wrapper'}).text == (loc + 'Alterar'):
                price = getPrice(soup)
            else:
                while soup.find('div',{'class':'cassol-region-id-5-x-wrapper'}).text != (loc + 'Alterar'):
                    setLocation(driver,cidade)
                    time.sleep(10)
                    soup      = BeautifulSoup(driver.page_source, 'html.parser')
                    time.sleep(8)
                try:    
                    price = getPrice(soup)  
                except:        
                    pass
        except:
            try:
                setLocation(driver,cidade)
                price = getPrice(soup)  
            except:
                price = 0
                pass
        #print(f"Preço: {price}")    
        return price
   
    
def process_data(uf, cidade, wait_time=15):
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
    driver.get('https://www.cassol.com.br/')
    time.sleep(5)
    setLocation(driver,cidade)
    time.sleep(5)
    loc = uf + '  /  ' + cidade 
    
    # Cria o arquivo CSV
    with open(out_path + f'Cassol_{uf}_{today}.csv', "w", newline="", encoding="utf-8") as f:
        # Especifica o separador como ponto e vírgula
        csv_writer = csv.writer(f, delimiter=';')
        titulo = ['EAN', 'Price', 'URL']
        csv_writer.writerow(titulo)
        
        for ean,url in zip(eans,urls):#df_excel['Link']:
            price= get_info_from_url(url, driver, loc, cidade)
            #data.append([ean,url, title, price])
            linha = [ean, price, url]
            print(linha)
            csv_writer.writerow(linha)
         
    
        driver.close()

UF      = 'SC' #'SC' 'PR'
CEP_SC  = '88010-020' #Floripa-SC
CEP_PR  = '80240-424' #Curitiba-PR

cepDict = {'Curitiba':'80240-424',
           'Florianópolis':'88010-020'}

# definitions
guideshop = 'Cassol'
today     = time.strftime("%d-%m-%Y")
i         = 0 #iterator for retrieves the right urls
target    = load_pkl('Updated2')
#Lista para percorrer
#t = 200
target = target[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[8:11]
eans   = target.loc[:,'EAN']#[8:11]

#df = process_data('PR', 'Curitiba')