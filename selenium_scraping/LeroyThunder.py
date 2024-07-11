# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 21:01:24 2024

@author: ArthurRodrigues
"""

import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from io import StringIO
import psycopg2 ## Postgres

leroyHref = pd.read_pickle('C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/LeroyMap.pkl')

class LeroyWrap:

    

    def _walk(self):
        i=0
        while True:
            i+=1
            yield i


    def get_page_info(self,start_url):
        
        response = requests.get(start_url)#('https://www.leroymerlin.com.br/porcelanatos') # find all to get all
        soup     = BeautifulSoup(response.text, 'html.parser')
        jsons    = []
        
        # Collect all _minitables_ with precius information about product, such as EAN. 
        walk = self._walk()
        while True:
             try:
                 s         = soup.find_all('script')
                 json_dict = {True:s[5].text}
                 if s[5].text != '':
                     
                     jsons.append(json_dict.get('mpn' in s[5].text, s[4].text))
                     page = next(walk)
                     url  = (response.url + f'?page={page}') if page==0 else (response.url.split('?')[0] +f'?page={page}')
                     try:
                         
                        response = requests.get( url )#soup.find('link',{'rel':'next'})['href'])
                        soup = BeautifulSoup(response.text,'html.parser')
                     except:
                         jsons.append( "Null table")
                         break
                 else:
                     jsons.append( "Null table")
                     break
             except:
                 jsons.append( "Null table")
                 break
                 
        # Each row for each page with many products info
        # Here is an exemple:
        
        #page_info = json.loads(jsons[0]) # Dict containing many products info
        
        return jsons

    
    def _map(self):
        
        #hrefs = []
        
        for i in range(20):
            response = requests.get(f'https://www.leroymerlin.com.br/sitemap-{i}-p.html') if i>0 else requests.get(f'https://www.leroymerlin.com.br/sitemap-p.html')
            soup = BeautifulSoup(response.text,'html.parser')
            row = soup.find_all('div',{'row'})
            for h in row[2].find_all('a'):
                yield h['href']#hrefs.append(h['href']) 
        #return hrefs        
    
    def _crawl(self) -> list:
        """
        the output list is so big that may not support. 
        so we must implement an INSERT command in our database.

        """
        my_db = []
        while True:
            try:
                url_start = next(self._map())
                data      = self.get_page_info(url_start)
                my_db.append(data)    
            except:
                break
        return my_db

    def _Crawl(self) -> list:
        """
        the output list is so big that may not support. 
        so we must implement an INSERT command in our database.
 
        """
        store = DB().store_in_db #just the object
        data  = []
        l_it = iter(['https://www.leroymerlin.com.br/chuveiros--ver-todos-',''])#'https://www.leroymerlin.com.br/ver-todos-os-pisos'#,'https://www.leroymerlin.com.br/chuveiros--ver-todos-','https://www.leroymerlin.com.br/torneiras-para-banheiro','https://www.leroymerlin.com.br/vasos-sanitarios-convencioniais','https://www.leroymerlin.com.br/argamassas']#'https://www.leroymerlin.com.br/porcelanato'#iter(leroyHref.iloc[:,1])
        while True:
            try:
                url_start = next(l_it)#next(self._map())
                data      = self.get_page_info(url_start)
                for jsons in data:
                    store(jsons)    
            except:
                break
    
        
    def _get_rows(self):
        
        """
        Transform all string jsons stored at DB into a pandas.DataFrame.
        
        """
        
        conn     = DB().create_connection()
        JS       = pd.read_sql('SELECT * FROM public."leroy"',conn)
        products = JS.loc[JS.iloc[:,0].str.contains(':"Product"'),:] #get just the json string that have product info        
        Tables = []
        it     = iter(products.iloc[:,0]) #some laziness
        n      = products.shape[0]
        while n>0:
            jss    = pd.read_json(StringIO(next(it)))
            Tables.append(jss)
            n-=1
        leroyDF = pd.concat(Tables) #list with all jsons stored
        return leroyDF



class DB:

    """
    def __init__(self):
        self.create_connection()
    """    

    def create_connection(self):
        conn = psycopg2.connect(
            host="localhost",
            database="scrapys",
            user="postgres",
            password="123456")
        return conn    


    def process_item(self, item, spider):
        self.store_in_db(item)
        #we need to return the item below as scrapy expects us to!
        return item

    def store_in_db(self, item):
        conn = self.create_connection()
        curr = conn.cursor()
        curr.execute("""INSERT INTO public."leroy" (jsons) VALUES (%s);""", (item,))
        conn.commit()

w = LeroyWrap()

datas = w._Crawl()                