# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:26:03 2024

@author: ArthurRodrigues
"""

# Automatically generated Python file from Alvorada - 14.03.24.txt.txt

from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
#import pandas as pd
import csv
import numpy as np
from merged import load_pkl
from settings import out_path    #from current package
import warnings
from unidecode import unidecode
# Suppress all warnings
warnings.filterwarnings("ignore")

guideshop = 'São Geraldo DF'

eans  = load_pkl('Eans')#target#['EAN']#[:4] #new_eans #target_merged['EAN'][:t]  #.tolist()

# Inicializar o navegador
driver = webdriver.Chrome()#Firefox()

# Lista para armazenar os dados
#data_list = []
today = time.strftime("%d-%m-%Y")
# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
   

    titulo = ['EAN','Price', 'URL']
    csv_writer.writerow(titulo)
    
    try:
        # Iterar sobre os EANs
        for ean in eans:
            # Limpar o campo de busca
            driver.get(f'https://www.saogeraldo.com/{ean}?_q={ean}&map=ft')
            # Esperar o site carregar novamente
            #time.sleep(3)
            
            # Esperar alguns segundos para a página carregar
            time.sleep(3)
            
            # Obter o link atual da página
            current_url = driver.current_url
            # Agora, você precisa extrair as informações usando BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Obter o preço
            try:
                
                price_element = soup.find('span',{'class','vtex-product-price-1-x-sellingPriceValue vtex-product-price-1-x-sellingPriceValue--shelf'})
            
                price = unidecode(price_element.text).strip().replace('/ m²','').replace('R$','')\
                                                                     .replace(' ','')\
                                                                     .replace('.','')\
                                                                     .replace(',','.')
                price = np.float64(price)  
                # Adicionar os dados à lista
                #data_list.append([ean, title, price, current_url])
                linha = [ean, price, current_url]
                print(linha)
                csv_writer.writerow(linha)                                                   
            except:
                pass
 
    
    finally:
        f.close()
        try:
            # Fechar o navegador ao finalizar
            driver.quit()
        except Exception as e:
            print("Erro ao fechar o navegador:", e)

# Criar um DataFrame com os dados coletados
#df_output = pd.DataFrame(data_list, columns=['EAN', 'Título', 'Preço', 'URL'])

# Salvar o DataFrame em um arquivo CSV
#output_csv_path = os.path.join(desktop_path, 'Alvorada_200_14.03.24.csv')
#today = time.strftime("%d-%m-%Y")
#df_output.to_csv(out_path+ f'ShopAlvorada_{today}.csv', index=False)

print(f'Arquivo CSV salvo com sucesso em: {out_path}')
