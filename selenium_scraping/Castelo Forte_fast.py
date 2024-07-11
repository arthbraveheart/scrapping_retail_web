# Automatically generated Python file from Castelo Forte - 14.03.24.txt.txt

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import numpy as np
from merged import load_pkl #target_merged #strategy_target
from settings import out_path    #from current package
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")
cforte= load_pkl('UrlCForte').set_index('EAN')
eans  = load_pkl('UrlCForte')['EAN'].tolist()#load_pkl('Eans')#['EAN']#[:4]  #new_eans#[:5] 
urls  = load_pkl('UrlCForte')['Link Castelo Forte DF']
# Inicializar o navegador
driver = webdriver.Firefox()



#output formating
today = time.strftime("%d-%m-%Y")

# Cria o arquivo CSV
with open(out_path+ f'CasteloForte_{today}3.csv', "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    
    titulo = ['EAN', 'Price', 'URL']
    csv_writer.writerow(titulo)
    
    try:
        # Iterar sobre os EANs
        for ean in eans:#for ean,url in zip(eans,urls):#for ean in eans:
            try:
                # Limpar o campo de busca
                driver.get(cforte.loc[ean,'Link Castelo Forte DF'])#driver.get(f'https://www.casteloforte.com.br/busca?search={ean}')
                # Esperar o site carregar novamente
                time.sleep(4)
                
                
                # Obter o link atual da página
                current_url = driver.current_url
                
                # Agora, você precisa extrair as informações usando BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # Obter o preço
                try:
                    price_element = soup.find('h3',{'class':'price margint10'})
                except:
                    price_element = soup.find('div',{'class':'price margint10'})    
                price = price_element.text.strip().replace(r'à vista', '').replace('R$','').replace('/ m²','').replace(' ','')\
                                                                    .replace('.','')\
                                                                    .replace(',','.') 
                price = np.float64(price)  
                                                                     
            
                 
                # Adicionar os dados à lista
                linha = [ean, price, current_url]
                print(linha)
                csv_writer.writerow(linha)
                
               
                # Esperar alguns segundos antes de prosseguir para a próxima iteração
                #time.sleep(3)
            except:
                price = 0                                                    
                # Adicionar os dados à lista
                linha = [ean, price, current_url]
                print(linha)
                csv_writer.writerow(linha)
                
                
    finally:
        try:
            # Fechar o navegador ao finalizar
            driver.quit()
        except Exception as e:
            print("Erro ao fechar o navegador:", e)



print(f'Arquivo CSV salvo com sucesso em: {out_path}')
