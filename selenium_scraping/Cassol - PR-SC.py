# Automatically generated Python file from Cassol - PR-SC -14.03.24.txt.txt

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from unidecode import unidecode
import time
import csv

from settings import  out_path #from the current package
from merged import atualizado as target_merged #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
#t     = 4
UF     = 'SC' #'SC' 'PR'
CEP_SC = '89232-302' #Joinville-SC
CEP_PR = '83702-040' #Araucária-PR
today  = time.strftime("%d-%m-%Y")

#Lista para percorrer

target  = target_merged[target_merged[f'Link Cassol {UF}']!='Não encontrado']
urls    = target[f'Link Cassol {UF}'].astype({f'Link Cassol {UF}':'str'})#[:t]
eans    = target['EAN']#[:t] 



def get_info_from_url(url, driver):
    try:
        driver.get(url)
        time.sleep(5)  # Tempo de espera para garantir que a página seja carregada completamente
        
        # Verifica se a URL base foi carregada
        if driver.current_url == 'https://www.cassol.com.br/':
            print("URL base carregada. Preenchendo com 'Não encontrado'...")
            return "Não encontrado", "Não encontrado"
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        try: 
        
            title_element = soup.find('span', class_='vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--quickview ')
            title = unidecode(title_element.text.strip()) 
        
        except:
            title = "Não encontrado"
        
        try:    
            price_element = soup.find('div', class_='product-price')
            price = unidecode(price_element.text.strip())
        except:
            price = "Não encontrado"
        
        try: 
            price_element1 = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div/div[2]/section/div[1]/div[2]/div/div[9]/div/div/div/div/div[1]/div[2]/div/div[1]")
            price1 = unidecode(price_element1.text.replace('\n',' ')) 

        except:
            price1 = "Não encontrado"
        
        #print(f"Título: {title}")
        #print(f"Preço: {price}")
        
        return title, price, price1
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return "Não encontrado", "Não encontrado"


# Cria o arquivo CSV
with open(out_path + f'Cassol_{UF}_{today}.csv', "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN','URL', 'Price1','Price2', 'Title']
    csv_writer.writerow(titulo)
    manual_input_wait_time = 15
    
    driver = webdriver.Firefox()
    driver.get('https://www.cassol.com.br/')
    print(f"Aguarde {manual_input_wait_time} segundos para inserir o CEP manualmente...")
    time.sleep(manual_input_wait_time)
    
    #df_excel = pd.read_excel(file_path)
    #data = []
    
    for ean,url in zip(eans,urls):#df_excel['Link']:
        title, price, price1 = get_info_from_url(url, driver)
        #data.append([ean,url, title, price])
        linha = [ean, url, price, price1, title]
        print(linha)
        csv_writer.writerow(linha)
        
        

#df_result = pd.DataFrame(data, columns=['EAN','URL', 'Título', 'Preço'])
#df_result.to_csv(out_path + f'Cassol_{UF}_{today}.csv', sep=';', index=False, encoding='utf-8-sig')

driver.quit()

