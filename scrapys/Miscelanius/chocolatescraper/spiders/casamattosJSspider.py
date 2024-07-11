# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:33:46 2024

@author: ArthurRodrigues
"""

import scrapy
from chocolatescraper.itemloaders import ChocolateProductLoader, SodimacLoader, CMattLoader
from chocolatescraper.items import ChocolateProduct,CMattProduct 
from pandas import read_pickle 
import re
import json

class CMJsonSpider(scrapy.Spider):

   # The name of the spider
   name = 'casamattosJSspider'

   # These are the urls that we will start scraping
   #start_urls = ['https://www.casamattos.com.br/pisos-e-revestimentos']
   start_urls = read_pickle("C:/Users/ArthurRodrigues/Codes/Pricing/ScrapyTest/chocolatescraper/spiders/urlsCMattAPI.pkl").iloc[:,1].to_list()
   
   
   def parse(self, response):
        
        product = CMattLoader(item=CMattProduct(), selector=response)
        product.add_value('jsons', response.text)
        #product.add_value('datas', response.css('[id="__NEXT_DATA__"]::text').getall()[0])
        yield product.load_item()
        
        