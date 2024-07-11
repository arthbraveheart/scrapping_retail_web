# Automatically generated Python file from Sodimac - 19.03.24.txt.txt

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from unidecode import unidecode
import csv
import time
import re
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl  #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")


def get_price(driver):
    driver.get(url)
    
    time.sleep (5)
    soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source
    
    try:
        price = 1*(soup.find('div',{'data-testid':'out-of-stock-title'}).text == 'Produto sem estoque disponível') 
    except:
       try:
           preco1_element = soup.find('div',{'class':'jsx-116178131 primary jsx-338450109'})
           preco1_text    = unidecode(preco1_element.text).split('m2')[0]
           price          = preco1_text.replace('R$','').replace('pec','').replace('un','').replace('la','').replace('sac','').replace('gl','').replace(' ','')\
                                                                                           .replace('.','')\
                                                                                             .replace(',','.')   
       except:
           try:
               preco1_element = soup.find('div',{'class':'jsx-116178131 primary'})
               preco1_text    = unidecode(preco1_element.text).split('m2')[0]
               price          = preco1_text.replace('R$','').replace('pec','').replace('un','').replace('bd','').replace('la','').replace('sac','').replace('gl','').replace(' ','')\
                                                                                               .replace('.','')\
                                                                                                 .replace(',','.') 
           except:
               try:
                   preco1_element = soup.find('div',{'class':'jsx-116178131 primary'})
                   preco1_text    = unidecode(preco1_element.text).split('m2')[0]
                   price          = preco1_text.replace('R$','').replace('pec','').replace('un','').replace('bd','').replace('la','').replace('sac','').replace('gl','').replace(' ','')\
                                                                                                   .replace('.','')\
                                                                                                     .replace(',','.') 
               except:
                   price = 0
    return price
# definitions 
guideshop = 'Sodimac'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t = 5
target    = load_pkl('Updated3')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
target = target.loc[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#.loc[297:]
urls   = urls.str.split("&", expand=True,regex=False)[0]
eans   = target['EAN']#.loc[297:]


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
#driver = webdriver.Chrome() 

# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}2.csv", "w", newline="", encoding="utf-8") as f:
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)
    
    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        try:
           price = get_price(driver) 
        except:
           try: 
              price = get_price(driver) 
           except:
              price = 0 
        price = np.float64(price)
        linha = [ean, price, url]
        print(linha)
        csv_writer.writerow(linha)
    f.close()    
        
driver.quit()  # Fecha o navegador após cada iteração        