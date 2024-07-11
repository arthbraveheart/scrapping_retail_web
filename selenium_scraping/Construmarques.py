# Automatically generated Python file from Construmarques - 14.03.24.txt.txt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import csv
import numpy as np
from settings import   out_path # monitoramento_path, monitoramento_sheetname, input_path, out_path #from the current package
from merged import load_pkl # strategy_eans_target  # new_eans #eans  # from current package #strategy 
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

UF          = 'Construmarques SP' #'SC' 'PR'

#Lista para percorrer
#t           = 4
#urls        = target#[:t]
eans  = load_pkl('Eans')#[9:15]#['EAN']#[:4]  #new_eans#target_merged[target_merged[f'Link {UF}']!='Não encontrado']['EAN']#[:t]
# Inicializar o navegador
driver = webdriver.Chrome()

# Lista para armazenar os dados
data_list = []

# Cria o arquivo CSV
today = time.strftime("%d-%m-%Y")
# Cria o arquivo CSV
with open(out_path + f"{UF}_{today}.csv", "w", newline="", encoding="utf-8-sig") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)

    

    try:
        # Iterar sobre os EANs
       for ean in eans:
            # Limpar o campo de busca
            driver.get(f"https://www.construmarques.com.br/busca?busca={ean}")
            # Esperar o site carregar novamente
            time.sleep(5)
            # Obter o link atual da página
            url = driver.current_url
            # Agora, você precisa extrair as informações usando BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Obter o título
            title_element = soup.find('span', {'class': 'text-lg my-2 text-[#1E1E1E]'})
            if title_element:
                title = title_element.text.strip()
            else:
                title = "Título indisponível"
            
            # Obter o preço
            price_element = soup.find('h2', {'class': 'preco'})
            if price_element:
                price = price_element.text.strip().replace('/ m²','')\
                                                                     .replace('R$','')\
                                                                      .replace(' ','')\
                                                                       .replace('.','')\
                                                                        .replace(',','.') 
                price = np.float64(price)                                                        
            else:
                price = 0
            
            linha = [ean, price, url]
            print(linha)
            csv_writer.writerow(linha)
    
    finally:
        try:
            # Fechar o navegador ao finalizar
            driver.quit()
        except Exception as e:
            print("Erro ao fechar o navegador:", e)

