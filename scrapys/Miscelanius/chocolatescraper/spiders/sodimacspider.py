# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:33:46 2024

@author: ArthurRodrigues
"""

import scrapy
from chocolatescraper.itemloaders import ChocolateProductLoader, SodimacLoader
from chocolatescraper.items import ChocolateProduct 
from pandas import read_pickle 
import re
import json

class ChocolateSpider(scrapy.Spider):

   # The name of the spider
   name = 'sodimacspider'

   # These are the urls that we will start scraping
   start_urls = ['https://www.sodimac.com.br/sodimac-br/category/cat170729/porcelanato/']
   #start_urls = read_pickle('C:/Users/ArthurRodrigues/Codes/Pricing/ScrapyTest/chocolatescraper/spiders/urlsKrep.pkl').iloc[:,0].to_list()
   
   
   def parse(self, response):
        product = SodimacLoader(item=ChocolateProduct(), selector=response)
        product.add_value('tags', response.css('[data-rh="true"]::text').getall()[0])
        product.add_value('datas', response.css('[id="__NEXT_DATA__"]::text').getall()[0])
        yield product.load_item()
        
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
             next_page_url = next_page
             yield response.follow(next_page_url, callback=self.parse) 