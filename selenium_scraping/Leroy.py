import time
import csv
import json
import warnings
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from settings import out_path # from the current package
from merged import load_pkl # target_merged # strategy_target

# Suppress all warnings
warnings.filterwarnings("ignore")

def setLocation(driver, cidade):
    try:
        driver.find_element(By.CSS_SELECTOR, 'span.hover\:underline:nth-child(1)').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'button.text-primary-700').click()
        toDigit = driver.find_element(By.CSS_SELECTOR, '#downshift-0-input')
        ActionChains(driver).send_keys_to_element(toDigit, cidade).perform()
        time.sleep(4)

        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        toConfirm = driver.find_element(By.CSS_SELECTOR, 'button.border-transparent:nth-child(3)')
        ActionChains(driver).send_keys_to_element(toConfirm, Keys.ENTER).perform()
    except Exception as e:
        ActionChains(driver).move_by_offset(6, 120).click().perform()
        print(f"Erro ao trocar a Localidade para {cidade} pelo seguinte motivo:\n", str(e))

def getDisp(soup, *TAGS):
    seller_element = soup.find(*sellerTag)
    seller = seller_element.text.strip()
    seller_verification = {'Leroy Merlin': 'Produto disponivel'}
    disp_verification = {True: 'Produto disponivel'}
    disponibilidade = seller_verification.get(seller, 'Produto indisponivel')
    if disponibilidade == 'Produto disponivel':
        try:
            div_data = soup.find(*dispTag)
            try:
                data_purchase_buttons = div_data.get('data-purchase-buttons')
                buttons_info = json.loads(data_purchase_buttons)
                disponibilidade = disp_verification.get(buttons_info['ecommerce']['enabled'], 'Produto indisponivel')
            except:
                disponibilidade = "Produto disponi­vel"
        except:
            disponibilidade = "Produto indisponi­vel"
    return disponibilidade

def getPrice(soup):
    try:
        price_tag = soup.find(*priceTag).get('data-branded-installments-total-value').replace(' ', '') \
                                                                                     .replace('.', '') \
                                                                                     .replace(',', '.')
        price = np.float64(price_tag)
    except:
        price = 0
    return price

def getDiscount(soup):
    try:
        discount_price_tag = soup.find('span', {'data-cy': 'product-price-integer'}).text
        discount_price = discount_price_tag.strip()
        discount_price = np.float64(discount_price.replace('R$', '').replace('.', '').replace(',', '.'))
    except:
        discount_price = 0
    return discount_price

def whilesh(soup, condition, driver, cidade):
    if not condition:
        return 0
    else:
        setLocation(driver, cidade)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if not condition:
            return 0
        return whilesh(soup, condition, driver, cidade)

def write(linha, csv_writer):
    csv_writer.writerow(linha)
    print(f"EAN: {linha[0]}\nPreço: {linha[1]}\nDesconto: {linha[2]}\nLink: {linha[3]}")  # Exibir EAN na console
    print("=" * 50)

def process_data(uf, cidade, wait_time=15):
    time1 = time.time()
    state_code_upper = uf.upper()
    cidade = cidade
    loc = cidade + ' - ' + uf
    with open(out_path + f'Leroy_{uf}_{today}.csv', "w", newline="", encoding="utf-8-sig") as f:
        csv_writer = csv.writer(f, delimiter=';')
        titulo = ['EAN', 'Price', 'Discount', 'URL']  # Nome das colunas
        csv_writer.writerow(titulo)
        try:
            # Inicializar o navegador
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
            #params = {
            #"latitude": -20.4435,
            #"longitude": -54.6478,
            #"accuracy": 100
            #}
        
        
            #driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
            options.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome( options=options)
            #driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
            #driver = webdriver.Firefox()
            #driver = webdriver.Firefox()
            driver.get("https://www.leroymerlin.com.br/")
            time.sleep(6)
            setLocation(driver, cidade)
            time.sleep(8)
    
            for ean, url in zip(eans, urls):
                link = url
                try:
                    driver.get(link)
                    time.sleep(8)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    time.sleep(2)
                    if soup.find(*locTag).text == loc:
                        try:
                            disponibilidade = getDisp(soup, *TAGS)
                            if disponibilidade == 'Produto disponivel':
                                price = getPrice(soup)
                                discount = getDiscount(soup)
                                write([ean, price, discount, link], csv_writer)
                            else:
                                continue
                        except:
                            continue
                    else:
                        while soup.find(*locTag).text != loc:
                            setLocation(driver, cidade)
                            time.sleep(10)
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            time.sleep(8)
                        try:
                            disponibilidade = getDisp(soup, *TAGS)
                            if disponibilidade == 'Produto disponivel':
                                price = getPrice(soup)
                                discount = getDiscount(soup)
                                write([ean, price, discount, link], csv_writer)
                            else:
                                continue
                        except:
                            continue
                except Exception as e:
                    try:
                        setLocation(driver, cidade)
                        disponibilidade = getDisp(soup, *TAGS)
                        if disponibilidade == 'Produto disponivel':
                            price = getPrice(soup)
                            discount = getDiscount(soup)
                            write([ean, price, discount, link], csv_writer)
                        else:
                            continue
                    except:
                        print(f"Erro ao processar link {link}: {str(e)}")
                        continue
            f.close()
            df_result = pd.read_csv(out_path + f'Leroy_{uf}_{today}.csv', sep=';')
            return df_result
        except Exception as e:
            print("Ocorreu um erro:", str(e))
        finally:
            driver.quit()
            time2 = time.time()
            print("Execution time:", time2 - time1)

def process_data_parallel(toGet):
    dfs = []
    for uf, cidade in zip(toGet['state_code'], toGet['cidade']):
        df = process_data(uf, cidade)
        dfs.append(df)
    return dfs

guideshop = 'Leroy'
today = time.strftime("%d-%m-%Y")
target = load_pkl('Updated2')
target = target[target[f'Link{guideshop}'] != 'Não encontrado']
urls = target[f'Link{guideshop}'].astype({f'Link{guideshop}': 'str'})
eans = target.loc[:, 'EAN']

locTag = ('span', {'data-testid': 'location-region-name'})
sellerTag = ('strong', {'data-seller-selected': 'true', 'data-cy': 'seller-name'})
priceTag = ('div', {'class': 'price-tag-wrapper'})
dispTag = ('div', {'data-postal-code': True})
TAGS = (locTag, sellerTag, priceTag, dispTag)

data_sets = {
    'state_code': ['MG', 'RJ', 'SP', 'ES', 'DF', 'MS', 'PR', 'SC', 'GO', 'BA'],
    'cidade': ['Juiz de Fora', 'Rio de Janeiro', 'São Paulo', 'Vitória', 'Brasília', 'Campo Grande', 'Curitiba', 'Florianópolis', 'Goiânia', 'Salvador']
}

toGet = pd.DataFrame.from_dict(data_sets)
