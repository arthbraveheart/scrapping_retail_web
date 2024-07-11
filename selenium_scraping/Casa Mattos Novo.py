# Automatically generated Python file from Casa Mattos - 19.03.24.txt.txt

from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
target    = load_pkl('CMattos')
#Lista para percorrer
#t 
#target = target.query("Disponivel == 'Produto disponivel'")
urls   = target['URL'].astype('string')#[:t]
urls   = urls.replace('https://','', regex=True).apply(lambda x:'https://' + x )
eans   = target['EAN'].astype('string')#[:t]

#Verification Price dict
priceDict = {85.09:0}

# Inicializa o ChromeDriver
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
    
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)    
    for ean,url in zip(eans,urls):
        linha = scrape_product_info(ean,url)
        
        csv_writer.writerow(linha)
        print('='*50)
        print(linha)   
        

driver.close()#quit()  # Fechar o navegador após concluir o scraping
#print(df)

