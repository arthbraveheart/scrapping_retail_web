# Automatically generated Python file from viveza - 19.03.24.txt.txt

import time
from bs4 import BeautifulSoup
import unidecode
from selenium import webdriver
import csv
from settings import  out_path #from the current package
from merged import target_merged #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
guideshop = 'Viveza'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t 
target = target_merged[target_merged[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link {guideshop}'].astype({f'Link {guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

driver = webdriver.Firefox() 

# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    
    titulo = ['EAN', 'URL', 'Price', 'Title']
    csv_writer.writerow(titulo)

    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
        i = i+1
        time.sleep (3)
        soup = BeautifulSoup(driver.page_source, "html.parser") #driver.page_source
        
        try:
            title_element = soup.select_one('#area-a > div > div.right > div.wrapper.nome')
            title = unidecode.unidecode(title_element.text.strip()) 
        except:
            title = "Titulo indisponivel"
        try:
            price_element = soup.find('strong', 'skuPrice')
            price = price_element.text.strip().replace("/", "").replace("m²", "") 
        except:
            price = "Valor indisponivel"
    
    
    
    
    
        linha = str(ean) + ';' + url + ';' + price + ';' + title + ';' + '\n'
        print("="*50)
        print(linha)      
        f.write(linha)

driver.quit()