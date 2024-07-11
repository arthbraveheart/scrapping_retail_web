# Automatically generated Python file from Balarotti - PR-SC - 14.03.24.txt.txt

from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import numpy as np
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target as
import warnings
from selenium.webdriver.chrome.options import Options
# Suppress all warnings
warnings.filterwarnings("ignore")



def setEAN(driver,ean): 
    
    try:
        
            #driver.find_element(By.CSS_SELECTOR,'.cassol-region-id-5-x-wrapper > div:nth-child(1) > button:nth-child(1)').click()
            time.sleep(2)
            toDigit = driver.find_element(By.CSS_SELECTOR,'#linx-impulse-search-bar')
            time.sleep(2)
            toDigit.clear()
            time.sleep(2)
            ActionChains(driver).send_keys_to_element(toDigit, ean).perform()
            time.sleep(2)
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(4)
            toDigit.clear()
            #ActionChains(driver).move_by_offset(1, 1).click().perform()
            #driver.find_element(By.CSS_SELECTOR,'.cassol-region-id-5-x-button').click()
            #time.sleep(10)
        
    except Exception as e:
        ActionChains(driver).move_by_offset(6, 120).click().perform()
        print(f"Erro ao trocar a Localidade para {ean} pelo seguinte motivo:\n", str(e))


def get_info_from_url(url, driver):
    try:
        setEAN(driver,ean)
        time.sleep(3)         
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        price_element = soup.find('p', class_='balaroti-store-theme-2-x-Price')#price_element = soup.find('span', class_='balaroti-store-theme-2-x-currencyContainer')#vtex-product-price-1-x-sellingPriceValue')
        price = unidecode(price_element.text.replace(' ','').replace('\n',' ').replace('R$','')).replace('/m2','').replace(' ','')\
                                                                                                                .replace('.','')\
                                                                                                                .replace(',','.').replace('avista','') if price_element else 0
        price = np.float64(price)
        url   = driver.current_url 
        
        #toDigit = driver.find_element(By.CSS_SELECTOR,'#linx-impulse-search-bar')
        #toDigit.clear()
        #ActionChains(driver).move_by_offset(1, 1).click().perform()
        #time.sleep(3)
        #ActionChains(driver).move_by_offset(1, 1).click().perform()
        return price,url
    except Exception as e:
        print(f"Erro ao acessar {driver.current_url}: {e}")
        toDigit = driver.find_element(By.CSS_SELECTOR,'#linx-impulse-search-bar')
        toDigit.clear()
        url = driver.current_url
        time.sleep(3)
        return 0,url




# definitions
#t     = 4
UF      = 'SC' #'SC' 'PR'
CEP_SC = '88010-020' #Floripa-SC
CEP_PR = '80240-424' #Curitiba-PR
today = time.strftime("%d-%m-%Y")
target    = load_pkl('Targets')['targets']
#Lista para percorrer

target  = target[target[f'Link Balaroti {UF}']!='Não encontrado']
urls    = target[f'Link Balaroti {UF}'].astype({f'Link Balaroti {UF}':'str'})#[:t]
eans    = load_pkl('Eans')#target['EAN']#[:t] 


# Cria o arquivo CSV
with open(out_path + f'Balarotti_{UF}_{today}.csv', "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN','Price','URL']
    csv_writer.writerow(titulo)

    manual_input_wait_time = 15
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
    #driver = webdriver.Firefox()
    driver.get('https://www.balaroti.com.br/')
    print(f"Aguarde {manual_input_wait_time} segundos para inserir o CEP manualmente...")
    time.sleep(manual_input_wait_time)
        
    for ean in eans:#df_excel['Link']:
        #url = f"https://www.balaroti.com.br/busca?terms={ean}"
        driver.refresh()
        price,url = get_info_from_url(ean, driver)        
        linha = [ean, price, url]
        csv_writer.writerow(linha)
        print('='*50)
        print(linha)
        
        
#    df_result = pd.DataFrame(data, columns=['EAN','URL', 'Título', 'Preço'])
#    df_result.to_csv(out_path + f'Balarotti_{UF}_{today}.csv', sep=';', index=False, encoding='utf-8-sig')

driver.close()
 

