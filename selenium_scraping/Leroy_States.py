# Automatically generated Python file from Leroy - Todos os estados - Cep autom�tico - 19.03.24.txt.txt
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import json
from multiprocessing import Process



from merged import target_merged #from current package
from settings import out_path    #from current package
import warnings


# Suppress all warnings
warnings.filterwarnings("ignore")


def urls_target(UF='MG'):    
    target      = target_merged[target_merged[f'Link Leroy {UF}']!=r'Nao encontrado'][f'Link Leroy {UF}']
    target      = target.astype({f'Link Leroy {UF}':'str'})
    #target_dict = dict(target)
    
    #Lista para percorrer
    urls        = target[:4]
    return urls
eans        = target_merged['EAN'][:4]

CEP_SC = '89780-000' #Xavantina-SC
CEP_PR = '83880-000' #Rio Negrinho-PR

today = time.strftime("%d-%m-%Y")

def process_data(uf,cidade,wait_time=15):
    print(cidade)
    #uf = dicionario['UF']
    #cidade = dicionario['cidade']
    #wait_time = dicionario['wait_time']
    try:
        # Extrair informações do data_set
        state_code = uf
        cidade = cidade

        # Lista para armazenar os dados
        data_list = []

        # Configuração do WebDriver (neste caso, usando Chrome)
        driver = webdriver.Firefox()

        # Abrir o link do Leroy Merlin
        driver.get("https://www.leroymerlin.com.br/")
        time.sleep(6)
        # Localizar e clicar no botão "Trocar"
        try:
            trocar_button = driver.find_element(By.XPATH, "//button[contains(@class, 'xR6Sx') and contains(@class, 't8Fay') and contains(@class, 'qBD95') and contains(@class, 'p0lUJ') and contains(@class, 'worgh') and contains(@class, 'Qi7lV') and contains(@class, 'MiBKH')]")
            trocar_button.click()
        except Exception as e:
            print("Erro ao clicar no botão 'Trocar':", str(e))

        # Aguardar um tempo para o modal carregar completamente (se necessário)
        time.sleep(5)

        # Localizar o campo de entrada para o CEP e inserir o CEP
        try:
            # Esperar até que o campo de entrada esteja visível e clicável
            cep_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@class='aE8V9 htek1']"))
            )
            cep_input.clear()  # Limpa qualquer valor pré-existente no campo
            cep_input.send_keys(cidade)
            time.sleep(4)# Insere o CEP desejado
            cep_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(4)# Simula o pressionamento da seta para baixo
            cep_input.send_keys(Keys.ENTER)
            time.sleep(1)
            cep_input.send_keys(Keys.ENTER)
        except Exception as e:
            print("Erro ao inserir o CEP:", str(e))

        # Esperar o tempo especificado para inserção manual do CEP
        time.sleep(wait_time)

        # Carregar os links do arquivo Excel usando pandas
        links = urls_target(UF=uf)

        # Iterar sobre os links
        for ean, link in zip(eans,links):
            
            state_code_upper = state_code.upper()

            try:
                # Neste bloco, obtemos as informações da página e as armazenamos
                driver.get(link)
                time.sleep(4)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Obter o título
                title_element = soup.find('span', {'class': 'name color-text'})
                if title_element:
                    title = title_element.text.strip()
                else:
                    title = "Título indisponível"

                # Obter o vendedor
                seller_element = soup.find('strong', {'data-seller-selected': 'true', 'data-cy': 'seller-name'})
                if seller_element:
                    seller = seller_element.text.strip()
                else:
                    seller = "Seller indisponível"

                # Se o vendedor não for Leroy Merlin, definir título e preço como indisponíveis
                if seller != "Leroy Merlin":
                    title = "Título indisponível"
                    price = "Preço indisponível"
                else:
                    price_tag = soup.find('div', {'class': 'price-tag-wrapper'})
                    if price_tag:
                        total_value = price_tag.get('data-branded-installments-total-value')
                        if total_value:
                            price = total_value
                        else:
                            price = "Preço indisponível"
                    else:
                        price = "Preço indisponível"
                        
                # Encontrar a disponibilidade do produto
                if price == "Preço indisponível":
                    disponibilidade = "Produto indisponível"
                else:
                    div_data = soup.find('div', {'data-postal-code': True})
                    if div_data:
                        data_purchase_buttons = div_data.get('data-purchase-buttons')
                        if data_purchase_buttons:
                            buttons_info = json.loads(data_purchase_buttons)
                            disponibilidade = buttons_info['ecommerce']['tooltip']
                            if not disponibilidade:
                                disponibilidade = "Produto disponível"
                        else:
                            disponibilidade = "Produto disponível"
                    else:
                        disponibilidade = "Produto disponível"

                # Adicionar os dados à lista
                data_list.append([ean, title, seller, price, disponibilidade, link])
                
                # Exibir informações na console
                print(f"EAN: {ean}")  # Exibir EAN na console
                print(f"Título: {title}")
                print(f"Vendedor: {seller}")
                print(f"Preço: {price}")
                print(f"Disponibilidade: {disponibilidade}")
                print(f"Link: {link}")
                print("=" * 50)

            except Exception as e:
                print(f"Erro ao processar link {link}: {str(e)}")
                data_list.append([ean, "Título indisponível", "Seller indisponível", "Preço indisponível", "Produto indisponível", link])
                continue

        # Criar DataFrame a partir da lista de dados
        columns = ['EAN', 'Título', f'Vendedor {state_code_upper}', f'Preço {state_code_upper}', f'Disponibilidade {state_code_upper}', f'Link {state_code_upper}']  # Nome das colunas
        df_result = pd.DataFrame(data_list, columns=columns)
        df_result.to_csv(out_path + f'Leroy_{uf}_{today}.csv', sep=';', index=False, encoding='utf-8-sig')
        
        return df_result

    except Exception as e:
        print("Ocorreu um erro:", str(e))

    finally:
        # Fechar o WebDriver
        driver.quit()

def process_data_parallel(data_sets):
    dfs = []
    for uf,cidade in zip(data_sets[0]['state_code'],data_sets[0]['cidade']):
        df = process_data(uf,cidade)
        dfs.append(df)
    return dfs


# Definindo os caminhos dos arquivos de entrada e saída para cada conjunto de dados
data_sets = [
    {
        'target': urls_target(),
        'state_code': ['MG','RJ','SP','ES','DF','MS','PR','SC','GO','BA'],
        'cidade': ['Juiz de Fora','Rio de Janeiro','Sao Paulo','Vitoria','Brasilia','Campo Grande','Curitiba','Florianopolis','Goiania','Salvador']
    },    # Adicione outras cidades aqui com seus respectivos estados
]


# Chama a função para processar os dados em paralelo
dfs = process_data_parallel(data_sets)

# Concatenar todos os DataFrames
merged_df = pd.concat(dfs, axis=1)

# Remover duplicatas das colunas EAN e Título, exceto para a primeira ocorrência
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# Caminho onde o arquivo final será salvo
output_folder = r'C:/Users/ArthurRodrigues/Downloads/Pricing/Results/CSV/'
#merged_file_path = os.path.join(output_folder, 'Leroy_Concatenado.19.03.24.csv')

# Save the merged DataFrame to a new CSV file

merged_df.to_csv(out_path + f'Leroy_Concatenado{today}.csv', sep=';', index=False, encoding='utf-8-sig')

print('Merged file saved to: ' + out_path + f'Leroy_Concatenado{today}.csv')
