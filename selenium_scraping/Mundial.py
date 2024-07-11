# Automatically generated Python file from Mundial - 19.03.24.txt.txt

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.chrome.options import Options
from settings import  out_path #from the current package
from merged import load_pkl  #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions 
guideshop = 'Mundial'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t = 5 
target    = load_pkl('Updated3')#load_pkl('Strategics')['strategyTarget']#load_pkl('Targets')['targets']
target = target.loc[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

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
# Cria o arquivo CSV
#driver = webdriver.Firefox()

# Cria o arquivo CSV
today = time.strftime("%d-%m-%Y")
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding='utf-8') as f:
    a0 = ("EAN")
    a1 = ("Url")
    a2 = ("Preço")
    a3 = ("Disponibilidade")
    
    titulo = a0 + ';' + a1 + ';' + a2 + ';' + a3 + '\n'
    f.write (titulo)
    
    # Itera sobre cada URL
    for ean,url in zip(eans,urls):
        driver.get(url)
        time.sleep(2)
        try:
            preco1 = driver.find_element(By.CLASS_NAME, 'skuBestPrice').text
        except:
            preco1 = "Não encontrado"
                
        try:
            disponibilidade = driver.find_element(By.CLASS_NAME, 'notifyme-title-div').text
        except:
            disponibilidade = "Não encontrado"
           
        linha = str(ean) + ';' + url + ';' + preco1 + ';' + disponibilidade + '\n'
        print(linha)
        f.write(linha)