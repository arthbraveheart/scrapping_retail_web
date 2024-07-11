# Automatically generated Python file from Cnr - 19.03.24.txt.txt

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl  #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions 
guideshop = 'CNR'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t = 5 
target    = load_pkl('Updated3')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
target = target.loc[target[f'Link{guideshop}']!='Não encontrado']
urls   = target.loc[:,f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[:t]
eans   = target.loc[:,'EAN']#[:t]

# Cria o arquivo CSV
driver = webdriver.Firefox()
# Cria o arquivo CSV
time1 = time.time()


with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding='utf-8-sig') as f:

        # Especifica o separador como ponto e vírgula 
        csv_writer = csv.writer(f, delimiter=';')
       
        titulo = ['EAN', 'Price', 'URL']
        csv_writer.writerow(titulo)
        # Itera sobre cada URL
        for ean,url in zip(eans,urls):
            driver.get(url)
            time.sleep(2)
            soup      = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                preco = driver.find_element(By.XPATH, '//*[@id="content-product"]/div/div/div[3]/form/div[2]/div/p[1]/strong').text.replace('R$','').replace(' ','')\
                                                                   .replace('.','')\
                                                                    .replace(',','.')             
                preco = np.float64(preco)
            except:
                try:
                    preco = soup.find('p',{'class','sale-price'}).meta['content']
                    preco = np.float64(preco)
                except:    
                    preco = 0
            
           
            linha = [ean, preco, url]
            print(linha)
            csv_writer.writerow(linha)
driver.close()            
time2 =  time.time()
print("Execution time:",time2-time1)           