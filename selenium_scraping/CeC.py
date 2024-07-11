# Automatically generated Python file from CeC - 19.03.txt.txt
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
guideshop = 'C&CSP'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t=5 
target    = load_pkl('Updated3')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
target = target[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

# Configurar o navegador usando o driver correspondente
driver = webdriver.Chrome()
time1 = time.time()
# Itera sobre cada URL
i = 0 #iterator for retrieves the right urls


# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}2.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)

    for ean,url in zip(eans,urls):
         # Navegar para a página
        driver.get(url)
        i = i+1
        time.sleep(2)
    
        # Extrair as informações desejadas
        try:
            preco2_element = driver.find_element(By.XPATH, '//*[@id="Body_Body_divCard"]/div/div[1]/div[1]/span[3]/strong').text
            preco2 = unidecode(preco2_element.strip().replace('R$','').replace(" m²","")).replace(' ','')\
                                                                .replace('.','')\
                                                                .replace(',','.')
            preco2 = np.float64(preco2)                                               
        except:
           try:
            preco2_element = driver.find_element(By.XPATH, '//*[@id="Body_Body_divCard"]/div/div[1]/div[1]/span[2]/strong').text
            preco2 = unidecode(preco2_element.strip().replace('R$','').replace(" un","")).replace(' ','')\
                                                                .replace('.','')\
                                                                .replace(',','.') 
            preco2 = np.float64(preco2)                                           
           except:
            preco2 = 0
        
        
        # Adicionar os dados à lista
        linha = [ean, preco2, url]
        print(linha)
        csv_writer.writerow(linha)
                
time2 =  time.time()
print("Execution time:",time2-time1)  
