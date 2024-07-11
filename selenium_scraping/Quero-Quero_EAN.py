# Automatically generated Python file from Quero-Quero 14.03.24.txt.txt

from   selenium import webdriver
from   selenium.webdriver.common.by import By
from   selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from   bs4 import BeautifulSoup


from merged import load_pkl #from current package
from   settings   import out_path    #from current package
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")


guideshop = 'Quero-Quero ALL'

target = load_pkl('Targets')['targets']
target = target[target[f'Link {guideshop}']!='Não encontrado']
target      = target.astype({f'Link {guideshop}':'str'})
#target_dict = dict(target)

#Lista para percorrer
urls        = target
eans        = target['EAN']

today = time.strftime("%d-%m-%Y")

# Ler o arquivo CSV
#csv_path = r'C:\Users\IgorSilva\Desktop\Lista Itens Estratégicos Março 24.xlsx'
#df = pd.read_excel(csv_path, usecols=['EAN'], dtype={'EAN': str})
df = eans.to_frame()
# Adicionar novas colunas ao DataFrame
df['Link Quero Quero'] = ''
df['Title'] = ''
df['Price'] = ''
#df['SKU'] = '' #está considerando que o sku é igual ao EAN, equivocado?

# Inicializar o driver do Selenium (certifique-se de ter o webdriver correspondente instalado, como o chromedriver)
driver = webdriver.Firefox()

# URL base da Quero Quero
base_url = "https://www.queroquero.com.br/"


# Loop através dos EANs
for index, row in df.iterrows():
    try:
        ean = str(row['EAN']).split('.')[0]  # Remover parte decimal, se houver

        # Abrir o navegador e acessar a página principal
        driver.get(f'https://www.queroquero.com.br/{ean}?_q={ean}&map=ft')
        time.sleep(5)
        

        # Criar um objeto BeautifulSoup com o código fonte da página
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Encontrar o elemento <a> correspondente ao produto
        product_link = soup.find('a', {'class': 'vtex-product-summary-2-x-clearLink'})

        # Obter o HREF do elemento <a> e adicionar o prefixo se encontrado
        if product_link:
            product_url = product_link.get('href')
            product_url = "https://www.queroquero.com.br" + product_url
        else:
            product_url = "Link indisponível"

        # Adicionar a URL ao DataFrame
        df.at[index, 'Link Quero Quero'] = product_url

        # Encontrar elementos de título e preço
        title_element = soup.find('span', {'class': 'vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body'})
        price_container = soup.find('span', {'class': 'vtex-product-price-1-x-currencyContainer vtex-product-price-1-x-currencyContainer--summary'})

        # Obter o título
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Título indisponível"

        # Obter o preço
        if price_container:
            price_elements_integer = price_container.find_all('span', {'class': 'vtex-product-price-1-x-currencyInteger'})
            price_integer = ''.join(element.text for element in price_elements_integer)
            price_elements_fraction = price_container.find_all('span', {'class': 'vtex-product-price-1-x-currencyFraction'})
            price_fraction = ''.join(element.text for element in price_elements_fraction)
            price = f"{price_integer}.{price_fraction}"
        else:
            price = "Preço indisponível"

        # Adicionar os resultados ao DataFrame
        df.at[index, 'Title'] = title
        df.at[index, 'Price'] = price

        # Adicionar SKU ao DataFrame
        #sku = str(row['EAN']).split('.')[0]  # Assuming SKU is same as EAN
        #df.at[index, 'SKU'] = sku

        print(product_url, title, price)

    except Exception as e:
        # Se ocorrer um erro, imprima a mensagem de erro e salve o DataFrame até esse ponto
        print(f"Erro: {e}")
        print("Salvando DataFrame até agora...")
        
        df.to_csv(out_path + f'{guideshop}_{today}.csv', sep=';')
        #df.to_excel(r'C:/Users/IgorSilva/Desktop/200_QueroQuero_Parcial_14.03.xlsx', index=False, engine='openpyxl')
        break  # Interrompe o loop em caso de erro

# Fechar o navegador no final
driver.quit()

# Salvar o DataFrame completo em um novo arquivo Excel
df.to_csv(out_path + f'{guideshop}_{today}.csv', sep=';')
#df.to_excel(r'C:/Users/IgorSilva/Desktop/200_Quero_Quero_14.03.24.xlsx', index=False, engine='openpyxl')

# Exibir o DataFrame final
print(df.head(7))
