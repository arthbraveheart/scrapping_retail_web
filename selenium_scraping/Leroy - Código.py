# Automatically generated Python file from Leroy - C�digo - 14.03.24.txt.txt

import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import tkinter as tk
from tkinter import messagebox
from selenium.webdriver.common.by import By



from merged import target_merged #from current package
from settings import out_path    #from current package
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

UF          = 'PR' #'SC'
target      = target_merged[target_merged[f'Link Cassol {UF}']!='N�o encontrado'][f'Link Cassol {UF}']
target      = target.astype({f'Link Cassol {UF}':'str'})
target_dict = dict(target)

#Lista para percorrer
urls        = target[:4]
eans        = target_merged['EAN'][:4]

CEP_SC = '89780-000' #Xavantina-SC
CEP_PR = '83880-000' #Rio Negrinho-PR



def get_title(link):
    try:
        driver = webdriver.Firefox()
        response = driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title_element = soup.find('span', {'class': 'name color-text'})
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Título indisponível"
        driver.quit()
        return title
    except Exception as e:
        print(f"Erro ao obter título: {str(e)}")
        return "Título indisponível"

def process_data(links_file_path, state_code, wait_time=15):
    try:
        # Lista para armazenar os dados
        data_list = []

        # Configuração do WebDriver (neste caso, usando Chrome)
        driver = webdriver.Chrome()

        # Abrir o link do Leroy Merlin
        driver.get("https://www.leroymerlin.com.br/")

        # Esperar o tempo especificado para inserção manual do CEP
        time.sleep(wait_time)

        # Carregar os links do arquivo Excel usando pandas
        df_links = pd.read_excel(links_file_path)

        # Iterar sobre os links
        for index, row in df_links.iterrows():
            link = row['Links']
            ean = row['EAN']  # EAN
            state_code_upper = state_code.upper()

            try:
                # Fazer requisição GET para obter o conteúdo da página
                time.sleep(5)
                response = driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                price_tag = soup.find('div', {'class': 'price-tag-wrapper'})

                if price_tag:
                    # Obter o valor do atributo data-branded-installments-total-value
                    total_value = price_tag.get('data-branded-installments-total-value')
                    if total_value:
                        price = total_value   # Price com sigla do estado
                    else:
                        price = "Preço indisponível"
                else:
                    price = "Preço indisponível"
                    
                

                # Adicionar os dados à lista
                data_list.append([ean, price, link])  # Adicionando EAN, preço e link

                # Exibir informações na console
                print(f"EAN: {ean}")  # Exibir EAN na console
                print(f"Preço: {price}")
                print(f"Link: {link}")
                print("=" * 50)

            except Exception as e:
                print(f"Erro ao processar link {link}: {str(e)}")
                data_list.append([ean, "Preço indisponível", link])
                continue

        # Criar DataFrame a partir da lista de dados
        columns = ['EAN', f'Valor {state_code_upper}', f'Link {state_code_upper}']  # Nome das colunas
        df_result = pd.DataFrame(data_list, columns=columns)

        # Exibir pop-up
        root = tk.Tk()
        root.withdraw()  # Esconder a janela principal
        messagebox.showinfo("Conclusão", "Processamento concluído. Por favor, insira o CEP manualmente.")
        root.destroy()  # Fechar a janela pop-up

        return df_result

    except Exception as e:
        print("Ocorreu um erro:", str(e))

    finally:
        # Fechar o WebDriver
        driver.quit()

# Definindo os caminhos dos arquivos de entrada e saída para cada conjunto de dados
data_sets = [
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'MG'
    },
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'RJ'
    },
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'SP'
    },  
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'ES'
    },
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'DF'
    },    
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'GO'
    },
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'PR'
    },
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'SC'
    },
    {
        'links_file_path': r'C:\Users\IgorSilva\Desktop\ColetaLinks_LeroyMerlin_CURVA_A_08.03.24.xlsx',
        'state_code': 'BA'
    }] 

dfs = []


for data_set in data_sets:
    df = process_data(data_set['links_file_path'], data_set['state_code'])
    dfs.append(df)


merged_df = dfs[0]
for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on='EAN', how='outer')

# Save the merged DataFrame to a new CSV file
#merged_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Leroy_Concatenado.csv')
today = time.strftime("%d-%m-%Y")
merged_df.to_csv(out_path + f'Leroy_{UF}_{today}.csv', sep=';', index=False, encoding='utf-8-sig')

print(f"Merged file saved to: {out_path}Leroy_Concatenado_{today}.csv")
