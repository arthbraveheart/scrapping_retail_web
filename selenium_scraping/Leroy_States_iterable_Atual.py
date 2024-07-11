# Automatically generated Python file from Leroy - Todos os estados - Cep automático - 19.03.24.txt.txt

import time
import csv
import json
import warnings
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from settings import  out_path #from the current package
from merged import load_pkl #target_merged #strategy_target

# Suppress all warnings
warnings.filterwarnings("ignore")

def setLocation(driver,cidade):   
    try:
        driver.find_element(By.CSS_SELECTOR,'span.hover\:underline:nth-child(1)').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,'button.text-primary-700').click()
        toDigit = driver.find_element(By.CSS_SELECTOR,'#downshift-0-input')
        ActionChains(driver).send_keys_to_element(toDigit, cidade).perform()
        time.sleep(4)
        
        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()

        ActionChains(driver).send_keys(Keys.ENTER).perform()
        toConfirm = driver.find_element(By.CSS_SELECTOR,'button.border-transparent:nth-child(3)')
        ActionChains(driver).send_keys_to_element(toConfirm, Keys.ENTER).perform()
    except Exception as e:
        ActionChains(driver).move_by_offset(6, 120).click().perform()
        print(f"Erro ao trocar a Localidade para {cidade} pelo seguinte motivo:\n", str(e))


def getDisp(soup,*TAGS):
    
    # Obter o vendedor
    seller_element = soup.find(*sellerTag)
    seller         = seller_element.text.strip()
    #verification
    # Encontrar a disponibilidade do produto
    seller_verification = {'Leroy Merlin':'Produto disponivel'}
    disp_verification   = {True:'Produto disponivel'}
    disponibilidade     = seller_verification.get(seller,'Produto indisponivel')
    if disponibilidade == 'Produto disponivel':
        try:
            div_data = soup.find(*dispTag)
            try:
                data_purchase_buttons = div_data.get('data-purchase-buttons')
                buttons_info = json.loads(data_purchase_buttons)
                disponibilidade = disp_verification.get( buttons_info['ecommerce']['enabled'], 'Produto indisponivel')
                #verification
            except:
                 disponibilidade = "Produto disponi­vel"
        except:
            disponibilidade = "Produto indisponi­vel"
    return disponibilidade

    
def getPrice(soup):
    #Ready to get the Price!        
    try:
        price_tag = soup.find(*priceTag).get('data-branded-installments-total-value').replace(' ','')\
                                                                                        .replace('.','')\
                                                                                          .replace(',','.') 
        price = np.float64(price_tag)
    except:
        price = 0
    return price


def whilesh(soup, condition, driver, cidade):
    if condition==False:
        return 0 
    else:
        setLocation(driver,cidade)
        time.sleep(10)
        soup      = BeautifulSoup(driver.page_source, 'html.parser')
        if condition==False:
            return 0
        
        return whilesh(soup, condition, driver, cidade)

    
def write(linha,csv_writer):
    # Adicionar os dados a  lista
    linha = linha
    csv_writer.writerow(linha)
    # Exibir informaÃ§Ãµes na console
    print(f"EAN: {linha[0]}\nPreço: {linha[1]}\nLink: {linha[2]}")  # Exibir EAN na console
    print("=" * 50)

    
def process_data(uf,cidade, wait_time=15):
    time1            = time.time()
    state_code_upper = uf.upper()
    cidade           = cidade
    loc              = cidade + ' - ' + uf 
    with open(out_path + f'Leroy_{uf}_{today}2.csv', "w", newline="", encoding="utf-8-sig") as f:
        # Especifica o separador como ponto e vírgula
        csv_writer = csv.writer(f, delimiter=';')
        titulo = ['EAN', 'Price','URL']  # Nome das colunas
        csv_writer.writerow(titulo)
        try:
            # Configurção do WebDriver (neste caso, usando Chrome)
            options=Options()
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference('permissions.default.stylesheet', 2)
            firefox_profile.set_preference('permissions.default.image', 2)
            options.profile = firefox_profile
            driver = webdriver.Firefox(options=options)#firefox_profile=firefox_profile)
            # Abrir o link do Leroy Merlin
            driver.get("https://www.leroymerlin.com.br/localizacao")
            time.sleep(6)
            # Localizar e clicar no botÃ£o "Trocar"
            setLocation(driver,cidade)
            time.sleep(8)
    
            # Iterar sobre os links
            for ean,url in zip(eans,urls):
                link = url
                try:
                     # Neste bloco, obtemos as informaÃ§Ãµes da pÃ¡gina e as armazenamos
                     driver.get(link)
                     time.sleep(8)
                     soup      = BeautifulSoup(driver.page_source, 'html.parser')
                     time.sleep(2)
                     if soup.find(*locTag).text == loc:                          
                            try:
                                     disponibilidade = getDisp(soup, *TAGS)
                                     if disponibilidade == 'Produto disponivel':
                                        price = getPrice(soup)
                                        write([ean, price, link],csv_writer)
                                     else:
                                        continue
                            except:
                                     continue #seller = "Seller indisponi­vel"
                     else:
                            while soup.find(*locTag).text != loc:
                                     setLocation(driver,cidade)
                                     time.sleep(10)
                                     soup      = BeautifulSoup(driver.page_source, 'html.parser')
                                     time.sleep(8)
                            try:
                                    disponibilidade = getDisp(soup, *TAGS)
                                    if disponibilidade == 'Produto disponivel':
                                       price = getPrice(soup)
                                       write([ean, price, link],csv_writer)
                                    else:
                                       continue
                            except:
                                     continue #seller = "Seller indisponi­vel"
                except Exception as e:
                     try:
                            setLocation(driver,cidade)
                            disponibilidade = getDisp(soup, *TAGS)
                            if disponibilidade == 'Produto disponivel':
                               price = getPrice(soup)
                               write([ean, price, link],csv_writer)
                            else:
                               continue
                            
                     except:    
                            print(f"Erro ao processar link {link}: {str(e)}")
                            continue
            # Criar DataFrame a partir da lista de dados
            f.close()
            df_result = pd.read_csv(out_path + f'Leroy_{uf}_{today}.csv', sep=';')
            
            return df_result
    
        except Exception as e:
            print("Ocorreu um erro:", str(e))
    
        finally:
            # Fechar o WebDriver
            driver.quit()
            time2 =  time.time()
            print("Execution time:",time2-time1) 

def process_data_parallel(toGet):
    dfs = []
    for uf,cidade in zip(toGet['state_code'],toGet['cidade']):
        df = process_data(uf,cidade)
        dfs.append(df)
    return dfs 

# definitions
guideshop = 'Leroy'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls
target    = load_pkl('Updated3')
#Lista para percorrer
#t = 200
target = target[target[f'Link{guideshop}']!='Não encontrado']
urls   = target[f'Link{guideshop}'].astype({f'Link{guideshop}':'str'})#.loc[[376,375,371,369,367,366,365,357,354,347,344,330,329,324,298,296,291,269,169,160,159,158,146,142,135,63]]
eans   = target.loc[:,'EAN']#.loc[:376]#.loc[[376,375,371,369,367,366,365,357,354,347,344,330,329,324,298,296,291,269,169,160,159,158,146,142,135,63]]#[:t]

#Tags to scrape
locTag    = ('span', {'data-testid':'location-region-name'})
sellerTag = ('strong', {'data-seller-selected': 'true', 'data-cy': 'seller-name'})
priceTag  = ('div', {'class': 'price-tag-wrapper'})
dispTag   = ('div', {'data-postal-code': True})
TAGS      = (locTag,sellerTag,priceTag, dispTag)                

#  I N P U T  #
data_sets = {
                'state_code': ['MG','RJ','SP','ES','DF','MS','PR','SC','GO','BA'],
                'cidade': ['Juiz de Fora','Rio de Janeiro','São Paulo','Vitória','Brasília','Campo Grande','Curitiba','Florianópolis','Goiânia','Salvador']
            }   

toGet = pd.DataFrame.from_dict(data_sets)

#df = process_data('PR','Curitiba')