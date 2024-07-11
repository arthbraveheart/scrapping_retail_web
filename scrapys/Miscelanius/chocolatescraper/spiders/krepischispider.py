# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:58:50 2024

@author: ArthurRodrigues
"""

import scrapy
from chocolatescraper.itemloaders import ChocolateProductLoader
from chocolatescraper.items import ChocolateProduct 
from pandas import read_pickle 
import re
import json

class ChocolateSpider(scrapy.Spider):

   # The name of the spider
   name = 'krepischispider'

   # These are the urls that we will start scraping
   #start_urls = ['https://www.krepischi.com.br','https://www.krepischi.com.br/pisos-e-revestimentos','https://www.krepischi.com.br/material-hidraulico']
   start_urls = read_pickle('C:/Users/ArthurRodrigues/Codes/Pricing/ScrapyTest/chocolatescraper/spiders/urlsKrep.pkl').iloc[:,0].to_list()
   
   
   def parse(self, response):
        product = ChocolateProductLoader(item=ChocolateProduct(), selector=response)
        product.add_value('tags', response.css('script::text').getall()[0])
        product.add_value('datas', response.css('script::text').getall()[1])
        yield product.load_item()
        
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
             next_page_url = next_page
             yield response.follow(next_page_url, callback=self.parse)    

   
   
   """def parse(self, response):
       
       products = response("script::text")
       
       for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=products)
            chocolate.add_css('name', "a.product__link::text")
            chocolate.add_css('price', 'strong::text')
            chocolate.add_css('url', 'a::attr(href)')
            yield chocolate.load_item()"""

   """# Extract all script tags content
   scripts = response.css('script::text').getall()

   for script in scripts:
       # Find JSON-like content inside the script
       data_layer = self.extract_data_layer(script)
       tags       = self.extract_tags(script)
   
   for product in products:
        chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=products)
        chocolate.add_css('name', "a.product__link::text")
        chocolate.add_css('price', 'strong::text')
        chocolate.add_css('url', 'a::attr(href)')
        yield chocolate.load_item()   """ 
"""

see = pd.read_json('C:/Users/ArthurRodrigues/Codes/Pricing/ScrapyTest/chocolatescraper/myscrapeddata.json')

see = see.dropna()

JSONS = []
for i in range(449):
    jsons = json.loads(see.iloc[:,1].iloc[i])
    JSONS.append(pd.DataFrame(jsons))
jsonsConcat_datas = pd.concat(JSONS)

"""