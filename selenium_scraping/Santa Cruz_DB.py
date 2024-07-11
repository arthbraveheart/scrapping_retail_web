# Automatically generated Python file from Santa Cruz - 19.03.24.txt.txt

from selenium import webdriver
import csv
import time
from bs4 import BeautifulSoup

from settings import  out_path #from the current package
from merged import load_pkl  #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions 
guideshop = 'StaCruz'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
t = 5 
target    = load_pkl('Updated2')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
target = target.loc[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})[:t]
eans   = target['EAN'][:t]


# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
   
    titulo = ['EAN', 'Produto', 'Price', 'URL', 'Seller','Date','Categoria','Date_Job']
    csv_writer.writerow(titulo)
    
    driver = webdriver.Firefox()
    
    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
    

        try:
            # Obtenha o conteúdo da página com BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Encontre o elemento desejado usando BeautifulSoup
            preco1_element = soup.find(class_='regular-price')
            
            # Extraia o texto do elemento
            try:
               preco1_full = preco1_element.text.strip()
               # Encontre a parte do texto até o caractere "/"
               preco1 = preco1_full.split('/')[0].strip().replace('/ m²','').replace('R$','')\
                                                                    .replace(' ','')\
                                                                    .replace('.','')\
                                                                    .replace(',','.')
            except:
                preco1 = 0
        except Exception as e:
            print(f"Erro ao processar a URL {url}: {str(e)}")
            preco1 = "Erro ao processar"
            
        product = url.split('/')[4]
        linha   = [ean, product ,preco1, url, guideshop, today, 'pricing', '27-05-2024']
        print(linha)
        csv_writer.writerow(linha)