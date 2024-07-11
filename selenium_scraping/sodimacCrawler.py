# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:15:32 2024

@author: ArthurRodrigues
"""

import scrapy

            
class QuotesSpider(
        scrapy.Spider
        ):
        name = "sodimac"
        start_urls = [
            'https://www.sodimac.com.br/sodimac-br/product/888253',
            'https://www.sodimac.com.br/sodimac-br/product/888253/cuba-retangular-de-apoio-50cm-branco/888253/'
        ]
    
        def parse(self, response):
            # Extract the desired div elements
            out_of_stock_titles = response.xpath('//div[@data-testid="out-of-stock-title"]').get()
            
            for title in out_of_stock_titles:
                yield {'out_of_stock_title': title}
                

"""class SodimacSpider(scrapy.Spider):
    name = "sodimac"
    allowed_domains = ["sodimac.com.br"]
    start_urls = ["https://www.sodimac.com.br/sodimac-br/product/"]

    def parse(self, response):
        # Extract the desired div elements
        out_of_stock_titles = response.xpath('//div[@data-testid="out-of-stock-title"]').get()
        
        for title in out_of_stock_titles:
            yield {'out_of_stock_title': title}"""                