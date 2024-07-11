from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from chocolatescraper.spiders import casamattosJSspider as cm
import requests
import pandas as pd

## Storing to DB
#import mysql.connector ## MySQL
import psycopg2 ## Postgres

class PriceToUSDPipeline:

    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):

            #converting the price to a float
            floatPrice = float(adapter['price'])

            #converting the price from gbp to usd using our hard coded exchange rate
            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item
        else:
            raise DropItem(f"Missing price in {item}")
            
class ProdIDToListPipeline:

    #gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('prodID'):

            
            _locals = dict()
            exec('prodList =' + adapter['prodID'], _locals)

            adapter['prodID'] = _locals['prodList']

            return item
        else:
            raise DropItem(f"Missing price in {item}")            


class UrlAPIPipeline:

    #gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('prodID'):

            root = 'https://www.casamattos.com.br/produto/api/'
            urls = []
            if adapter['prodID'] is not None:
                for pid in adapter['prodID']:
                    urls.append(root+pid)
                    
            adapter['urlAPI'] = urls
            return item
        else:
            raise DropItem(f"Missing price in {item}") 
            
class JsonsPipeline:

    #gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('urlAPI'):

            
            JSONS = []
            for url in adapter['urlAPI']:
                cmjson = requests.get(url).json()
                jsonOut = pd.DataFrame(cmjson['Variantes']).astype({col:'string' for col in ['Nome','SKU','EAN']}).select_dtypes(exclude=['object']).T.to_dict()[0]
                JSONS.append(jsonOut)           
            adapter['jsons'] = JSONS
            return item
        else:
            raise DropItem(f"Missing price in {item}") 

class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['datas'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['datas'])
            return item




class SavingToPostgresPipelineKP(object):

    def __init__(self):
        self.create_connection()
        

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
        curr.execute("""INSERT INTO public.krepe (name, fornecedor, url) VALUES (%s, %s, %s);""", (
            item["name"],#[0],
            item["price"],#[0],
            item["url"],#[0]
        ))
        conn.commit()
        
  
class MyPipeline:
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if spider.name == 'casamattosspider':
            # Trigger the second spider
            self.crawler.engine.crawl(cm.CMJsonSpider(), spider)
        return item        
  
    
class SavingToPostgresPipelineCM(object):

    def __init__(self):
        self.create_connection()
        

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
        curr.execute("""INSERT INTO public.cmattos ("jsons") VALUES (%s);""", ( #, urlAPI, jsons) VALUES (%s, %s, %s);""", (
            #item["prodID"],#[0],
           # item["urlAPI"],#[0],
            item["jsons"],#[0]
        ))
        conn.commit()  
        
class SavingBala(object):

    def __init__(self):
        self.create_connection()
        

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
        for e,p,u in zip(item["eans"],item["price"],item["url"]):
            curr.execute("""INSERT INTO public."Balaroti" ("ean", "price", "url") VALUES (%s,%s,%s);""", ( #, urlAPI, jsons) VALUES (%s, %s, %s);""", (
                e,#item["eans"],#[0],
                p,#item["price"],#[0],
                u,#item["url"],#[0]
            ))
            conn.commit()  
        
        
        
"""

run cmattosspider
run cmattosJSspider

import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="scrapys",
    user="postgres",
    password="123456")
import pandas as pd
CMjsons = pd.read_sql(' SELECT "jsons" FROM public."cmattos" OFFSET 1206  ', con=conn)
df1 = pd.read_json(CMjspons[0])
df1 = pd.read_json(CMjsons[0])
df1 = pd.read_json(CMjsons.iloc[0])
CMjsons.iloc[0]
CMjsons.iloc[0][0]
df1 = pd.read_json(CMjsons.iloc[0][0])
import json
df1 = json.loads(CMjsons.iloc[0][0])
CMjsons.iloc[0][1]
CMjsons.iloc[1][0]
df2 = json.loads(CMjsons.iloc[1][0])
df1 | df2
{**df1 , **df2}
df2 = json.loads(CMjsons.iloc[1][0])['Variantes']
df2 = json.loads(CMjsons.iloc[1][0])['Variantes'][0]
df3 = json.loads(df2)
df3 = json.loads(str(df2))
str(df2)
df3 = pd.DataFrame.from_dict(df2)
df3 = pd.DataFrame(df2)
df3 = pd.DataFrame.from_dict(df2)
df2 = json.loads(CMjsons.iloc[1][0])['Variantes']
df3 = pd.DataFrame.from_dict(df2)
df3 = pd.DataFrame.from_dict(df2).astype({col:'string' for col in ['Nome','SKU','EAN']}).select_dtypes(exclude=['object']).T.to_dict()[0]
lines = []
CMjsons.iloc[1][0]
CMjsons.iloc[0][0]
CMjsons.iloc[2][0]
CMjsons.iloc[3][0]
CMjsons.iloc[4][0]
df3 = pd.DataFrame.from_dict(df2).astype({col:'string' for col in ['Nome','SKU','EAN']}).select_dtypes(exclude=['object'])
for i in range(3424):
    df1 = json.loads(CMjsons.iloc[i][0])['Variantes']
    df2 = pd.DataFrame.from_dict(df1).astype({col:'string' for col in ['Nome','SKU','EAN']}).select_dtypes(exclude=['object'])
    lines.append(df2)
    
CMall = pd.concat(lines)
df2 = json.loads(CMjsons.iloc[1][0])
json.loads(CMjsons.iloc[1][0])['Alias']
url = 'www.casamattos.com.br/produto/'
url + json.loads(CMjsons.iloc[1][0])['Alias']
alias = []
for i in range(3424):
    ref = json.loads(CMjsons.iloc[i][0])['Alias']
    site = url + ref
    lines.append(site)
for i in range(3424):
    ref = json.loads(CMjsons.iloc[i][0])['Alias']
    site = url + ref
    alias.append(site)
CMall['URL'] = alias
CMall['EAN'].str.strip()
CMall['EAN'][0]
CMall['EAN'][0][0]
CMall['EAN']
CMall['EAN'].iloc[0]
int(CMall['EAN'].iloc[0])
CMall['EAN'] = CMall['EAN'].str.strip()
CMall['EAN'] = CMall['EAN'].astype('int64')
CMall = CMall.fillna(0).copy()
CMall = CMall.fillna('0')
CMall['EAN'] = CMall['EAN'].astype('int64')
CMall['EAN'] = CMall['EAN'].str.replace('','0')
lines = []
for i in range(3424):
    ref = json.loads(CMjsons.iloc[i][0])['Alias']
    site = url + ref
    lines.append(site)
lines = []
for i in range(3424):
    df1 = json.loads(CMjsons.iloc[i][0])['Variantes']
    df2 = pd.DataFrame.from_dict(df1).astype({col:'string' for col in ['Nome','SKU','EAN']}).select_dtypes(exclude=['object'])
    lines.append(df2)
CMall = pd.concat(lines)
CMall['URL'] = alias
CMall['EAN'].iloc[0]
''.replace(r'$','3')
f_ean = pd.read_pickle('file:///C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/f_ean.pkl')
f_ean.dtypes
f_ean = f_ean.astype({'EAN':'string'})
f_ean.dtypes
CMall.dtypes
weHave = CMall.merge(f_ean, right_on='EAN', left_on='EAN')
weHave.to_pickle('C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/CMattos.pkl')
eans = pd.read_pickle('file:///C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/Eans.pkl')
CMall.query("EAN in @eans")
Eans = eans.astype("string")
CMall.query("EAN in @Eans")

"""        