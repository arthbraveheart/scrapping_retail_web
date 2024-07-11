# Automatically generated Python file from Casa Mattos - 19.03.24.txt.txt

from unidecode import unidecode
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
guideshop = 'Casa Mattos'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls
target    = load_pkl('Targets')['targets']
#Lista para percorrer
#t 
target = target[target[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link {guideshop}'].astype({f'Link {guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

#Verification Price dict
priceDict = {85.09:0}

# Inicializa o ChromeDriver
driver = webdriver.Firefox()

def scrape_product_info(ean,url):
    driver.get(url)
    time.sleep(5)  # Aguardar 2 segundos para que os elementos sejam carregados

    soup = BeautifulSoup(driver.page_source, "html.parser")

    

    price_element = soup.find('span', class_='fbits-parcela')
    price = unidecode(price_element.text.strip()).replace("/", "").replace('R$','').replace('m2','').replace(' ','')\
                                                                            .replace('.','')\
                                                                            .replace(',','.') if price_element else 0
    price = np.float64(price)  
    price = priceDict.get(price,price)                                                                      
    linha = [ean, price, url]
    return linha



# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    
    titulo = ['EAN', 'URL', 'Title','Price', 'Avaliable', 'Unit']
    csv_writer.writerow(titulo)    
    for ean,url in zip(eans,urls):
        linha = scrape_product_info(ean,url)
        
        csv_writer.writerow(linha)
        print('='*50)
        print(linha)   
        

driver.quit()  # Fechar o navegador após concluir o scraping
#print(df)

