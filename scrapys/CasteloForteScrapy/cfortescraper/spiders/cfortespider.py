# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 14:03:37 2024

@author: ArthurRodrigues
"""

import scrapy
from cfortescraper.itemloaders import  CForteLoader
from cfortescraper.items import CForteProduct 
from scrapy_playwright.page import PageMethod


class CForteSpider(scrapy.Spider):

   # The name of the spider
   name = 'cfortespider'

   # These are the urls that we will start scraping
   #start_urls = ['https://www.casteloforte.com.br/pisos-e-revestimentos']
   #start_urls = read_pickle('C:/Users/ArthurRodrigues/Codes/Pricing/ScrapyTest/chocolatescraper/spiders/urlsCMatt.pkl').to_list()
   
   def start_requests(self):
       url = 'https://www.casteloforte.com.br/pisos-e-revestimentos'
       yield scrapy.Request(url, meta=dict(
               playwright = True,
               playwright_include_page = True, 
               playwright_page_methods =[
                   PageMethod('wait_for_selector', 'section.min'),
               ],
       errback=self.errback,
           ))
   
    
   async def parse(self, response):
        page = response.meta["playwright_page_methods "]
        await page.close()
    
        
        product = CForteLoader(item=CForteProduct(), selector=response)
        product.add_value('jsons', response.css('[type="application/ld+json"]::text').getall()[1])
        #product.add_value('datas', response.css('[id="__NEXT_DATA__"]::text').getall()[0])
        yield product.load_item()
        
        next_page = response.css('[rel="next"] ::attr(href)').get()
        if next_page is not None:
             next_page_url = next_page
             yield response.follow(next_page_url, callback=self.parse) 
   
   async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()             
             
             
             




             
             
             
             
             
             
             