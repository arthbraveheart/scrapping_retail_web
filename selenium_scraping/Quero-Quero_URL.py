# Automatically generated Python file from Quero-Quero 14.03.24.txt.txt

from   selenium import webdriver
from   selenium.webdriver.common.by import By
from   bs4 import BeautifulSoup
import time
import csv

from settings import  out_path #from the current package
from merged import load_pkl  #target as target_merged
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
guideshop = 'Quero-Quero ALL'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t 
target = load_pkl('Targets')['targets']
target = target[target[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link {guideshop}'].astype({f'Link {guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]

# Inicializar o driver do Selenium (certifique-se de ter o webdriver correspondente instalado, como o chromedriver)
driver = webdriver.Firefox()

# URL base da Quero Quero
base_url = "https://www.queroquero.com.br/"

# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    titulo = ['EAN', 'URL', 'Price', 'Title']
    csv_writer.writerow(titulo)

    for ean,url in zip(eans,urls):
    
        try:
           
            # Abrir o navegador e acessar a página principal
            driver.get(url)
            time.sleep(5)
            
    
            # Criar um objeto BeautifulSoup com o código fonte da página
            soup = BeautifulSoup(driver.page_source, 'html.parser')
    
            # Encontrar elementos de título e preço
            try:
                title = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[8]/div/div[3]/div/section/div/div[2]/div/div[3]/div/div/div/h1/span[1]').text
    
            except:
                title = ("Não encontrado")
            try:
                price = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div/div/div[8]/div/div[3]/div/section/div/div[2]/div/div[9]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div/span/span/span/span[1]').text
    
            except:
                price = ("Não encontrado")
                
            # Adicionar os dados à lista
            linha = [ean, url, price , title]
            print(linha)
            csv_writer.writerow(linha)
     
        except Exception as e:
            # Se ocorrer um erro, imprima a mensagem de erro e salve o DataFrame até esse ponto
            print(f"Erro: {e}")
            print("Salvando DataFrame até agora...")
            break  # Interrompe o loop em caso de erro    
           
    
            
# Fechar o navegador no final
driver.quit()

