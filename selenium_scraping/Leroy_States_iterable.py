# Automatically generated Python file from Leroy - Todos os estados - Cep automático - 19.03.24.txt.txt

import time
import csv
import json
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from merged import new_eans as target  # strategy # strategy_eans_target  # new_eans #eans  # from current package
from settings import out_path    #from current package


# Suppress all warnings
warnings.filterwarnings("ignore")

#get target ready
eans  =  target # ['EAN'][:4]

#output formating
today = time.strftime("%d-%m-%Y")

def process_data(uf,cidade, wait_time=15):
    time1 = time.time()
    state_code_upper = uf.upper()
    cidade           = cidade
    
    with open(out_path + f'Leroy_{uf}_{today}.csv', "w", newline="", encoding="utf-8") as f:
        # Especifica o separador como ponto e vírgula
        csv_writer = csv.writer(f, delimiter=';')
        titulo = ['EAN', 'Tí­tulo', f'Vendedor {state_code_upper}', f'Preço {state_code_upper}', f'Disponibilidade {state_code_upper}', f'Link {state_code_upper}']  # Nome das colunas
        csv_writer.writerow(titulo)
        try:
            
    
           
            # Configurção do WebDriver (neste caso, usando Chrome)
            driver = webdriver.Firefox()
    
            # Abrir o link do Leroy Merlin
            driver.get("https://www.leroymerlin.com.br/")
            time.sleep(6)
            # Localizar e clicar no botÃ£o "Trocar"
            try:
                trocar_button = driver.find_element(By.XPATH, "//button[contains(@class, 'xR6Sx') and contains(@class, 't8Fay') and contains(@class, 'qBD95') and contains(@class, 'p0lUJ') and contains(@class, 'worgh') and contains(@class, 'Qi7lV') and contains(@class, 'MiBKH')]")
                trocar_button.click()
            except Exception as e:
                print("Erro ao clicar no botão 'Trocar':", str(e))
    
            # Aguardar um tempo para o modal carregar completamente (se necessÃ¡rio)
            time.sleep(5)
    
            # Localizar o campo de entrada para o CEP e inserir o CEP
            try:
                # Esperar atÃ© que o campo de entrada esteja visÃ­vel e clicÃ¡vel
                cep_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@class='aE8V9 htek1']"))
                )
                cep_input.clear()  # Limpa qualquer valor prÃ©-existente no campo
                cep_input.send_keys(cidade)
                time.sleep(4)# Insere o CEP desejado
                cep_input.send_keys(Keys.ARROW_DOWN)
                time.sleep(4)# Simula o pressionamento da seta para baixo
                cep_input.send_keys(Keys.ENTER)
                time.sleep(1)
                cep_input.send_keys(Keys.ENTER)
            except Exception as e:
                print("Erro ao inserir o CEP:", str(e))
    
            # Esperar o tempo especificado para inserÃ§Ã£o manual do CEP
            time.sleep(wait_time)
    
            # Carregar os links do arquivo Excel usando pandas
            #links = urls_target(UF=uf)
    
            # Iterar sobre os links
            for ean in eans:
                link = f"https://www.leroymerlin.com.br/search?term={ean}"
               
    
                try:
                    # Neste bloco, obtemos as informaÃ§Ãµes da pÃ¡gina e as armazenamos
                    driver.get(link)
                    time.sleep(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    try:
                        # Obter o tí­tulo
                        title_element = soup.find('span', {'class': 'name color-text'})
                        title         = title_element.text.strip()
                    except:
                        title = "Título indisponí­vel"
    
                    try:
                        # Obter o vendedor
                        seller_element = soup.find('strong', {'data-seller-selected': 'true', 'data-cy': 'seller-name'})
                        seller         = seller_element.text.strip()
                    except:
                        seller = "Seller indisponí­vel"
    
                    try:
                        price_tag = soup.find('div', {'class': 'price-tag-wrapper'})
                        try:
                            price = price_tag.get('data-branded-installments-total-value')
                        except:    
                            price = "Preço indisponí­vel"
                    except:
                        price = "Preço indisponí­vel"
                        
                    # Encontrar a disponibilidade do produto
                    seller_verification = {'Leroy Merlin':'Produto disponível'}
                    disponibilidade = seller_verification.get(seller,'Produto indisponível')
                    if disponibilidade == 'Produto disponível':
 
                        try:
                            div_data = soup.find('div', {'data-postal-code': True})
                            try:
                                data_purchase_buttons = div_data.get('data-purchase-buttons')
                                buttons_info = json.loads(data_purchase_buttons)
                                disponibilidade = buttons_info['ecommerce']['tooltip']
                            except:
                                 disponibilidade = "Produto disponí­vel"
                        except:
                            disponibilidade = "Produto indisponí­vel"
                            
     
                    # Adicionar os dados Ã  lista
                    #data_list.append([ean, title, seller, price, disponibilidade, link])
                    linha = [ean, title, seller, price, disponibilidade, link]
                    csv_writer.writerow(linha)
                    # Exibir informaÃ§Ãµes na console
                    print(f"EAN: {ean}\nTí­tulo: {title}\nVendedor: {seller}\nPreço: {price}\nDisponibilidade: {disponibilidade}\nLink: {link}")  # Exibir EAN na console
                    print("=" * 50)
    
                except Exception as e:
                    print(f"Erro ao processar link {link}: {str(e)}")
                    #data_list.append([ean, "Título indisponÃ­vel", "Seller indisponí­vel", "Preço indisponí­vel", "Produto indisponí­vel", link])
                    linha = [ean, "Título indisponí­vel", "Seller indisponí­vel", "Preço indisponí­vel", "Produto indisponí­vel", link]
                    csv_writer.writerow(linha)
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

def process_data_parallel(data_sets):
    dfs = []
    for uf,cidade in zip(data_sets[0]['state_code'],data_sets[0]['cidade']):
        df = process_data(uf,cidade)
        dfs.append(df)
    return dfs 


#  I N P U T  #

data_sets = [
    {
  #      'target': urls_target(),
        'state_code': ['MG','RJ','SP','ES','DF','MS','PR','SC','GO','BA'],
        'cidade': ['Juiz de Fora','Rio de Janeiro','Sao Paulo','Vitoria','Brasilia','Campo Grande','Curitiba','Florianopolis','Goiania','Salvador']
    },    # Adicione outras cidades aqui com seus respectivos estados
]



