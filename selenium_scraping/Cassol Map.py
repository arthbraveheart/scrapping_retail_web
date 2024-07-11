# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:31:51 2024

@author: ArthurRodrigues
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import csv
import numpy as np


def getURL(url,response):
    URL = []
    for resp in response:
        URL.append(url + resp['href'])
    return URL    

        
def getPrice(response):
    PRICE = []
    for resp in response:
        PRICE.append(resp.text.replace('\xa0','').replace('/m²','').replace('R$','').replace('.','').replace(',','.'))  
    return PRICE

    
def getTitle(response):
    TITLE = []
    for resp in response:
        TITLE.append(resp.text)
    return TITLE  


def Scrape(url):
    start = url
    driver = webdriver.Firefox()
    driver.get(start)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    one = soup.find('div',{'id':'gallery-layout-container'}) 
    urls =one.find_all('a')
    prices = one.find_all('span',{'class':'product-price__container'})
    titles = one.find_all('div',{'class':'vtex-product-summary-2-x-nameContainer flex items-start justify-center pv6'})
    
    dict_ = {
        'URL':getURL(start,urls),
        'PRICE':getPrice(prices),
        'TITLE':getTitle(titles),
        }
    
    return dict_   



start_url = 'https://www.cassol.com.br/pisos-e-revestimentos/pisos-ceramicos'
ALL = Scrape(start_url) 
df = pd.DataFrame.from_dict(ALL)   