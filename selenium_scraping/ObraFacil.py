# Automatically generated Python file from ObraFacil - 19.03.24.txt.txt

import requests
from   bs4        import BeautifulSoup
import time
import csv 

from settings import  out_path #from the current package
from merged import target_merged #target_merged #strategy_target
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# definitions
guideshop = 'Obra Fácil'
today  = time.strftime("%d-%m-%Y")
i = 0 #iterator for retrieves the right urls

#Lista para percorrer
#t 
target = target_merged[target_merged[f'Link {guideshop}']!='Não encontrado']
urls   = target[f'Link {guideshop}'].astype({f'Link {guideshop}':'str'})#[:t]
eans   = target['EAN']#[:t]



# Função para extrair informações de título e preço de uma página
def extrair_informacoes(ean,url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        pass
    
    try:
        titulo = soup.select_one('#tab-description > h2').text.strip()
    except:
        titulo = "Titulo indisponivel"
    
    try:
        preco = soup.select_one('#content > div.column-main > div > div.col-md-7.col-sm-6.block-2.product-info-main > div:nth-child(5) > span > span').text.strip()
    except:
        preco = "Valor indisponivel"
    
    try:
        # Usar regex para extrair os 5 caracteres antes de "Preço por m²"
        m2 = soup.select_one ('#content > div.column-main > div > div.col-md-7.col-sm-6.block-2.product-info-main > div:nth-child(6) > span > span').text.strip()[:21].replace('Preço por m²','')


    except:
        m2 = "Valor indisponivel"
    
    linha = str(ean) + ';' + url + ';' + titulo + ';' + preco + ';' + m2 + ';'  + '\n'
    return linha

# Cria o arquivo CSV
with open(out_path + f"{guideshop}_{today}.csv", "w", newline="", encoding="utf-8") as f:
    # Especifica o separador como ponto e vírgula
    csv_writer = csv.writer(f, delimiter=';')
    
    titulo = ['EAN', 'URL', 'Title','Price', 'Avaliable', 'Unit']
    csv_writer.writerow(titulo)    
    for ean,url in zip(eans,urls):
        product_info = extrair_informacoes(ean,url)
        linha = product_info
        f.write(linha)
        print("="*50)
        print(linha)      



print('Dados salvos em '+ out_path + f'{guideshop}_{today}.csv')
