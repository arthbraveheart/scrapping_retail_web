# Automatically generated Python file from Santa Cruz - 19.03.24.txt.txt

from selenium import webdriver
import csv
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
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
#t = 5 
target    = load_pkl('Updated3')#load_pkl('Updated2')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
target = target.loc[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]


# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
   
    titulo = ['EAN', 'Price', 'URL',]
    csv_writer.writerow(titulo)
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
    
    #driver = webdriver.Chrome()#Firefox()
    
    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
    

        try:
            # Obtenha o conteúdo da página com BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Encontre o elemento desejado usando BeautifulSoup
            preco1_element = soup.find(class_='regular-price')
            
            # Extraia o texto do elemento
            preco1_full = preco1_element.text.strip() if preco1_element else "Não encontrado"
            
            # Encontre a parte do texto até o caractere "/"
            preco1 = preco1_full.split('/')[0].strip()
        except Exception as e:
            print(f"Erro ao processar a URL {url}: {str(e)}")
            preco1 = "Erro ao processar"

        linha = [ean, preco1, url]
        print(linha)
        csv_writer.writerow(linha)