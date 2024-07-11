import scrapy

class ChocolateProduct(scrapy.Item):
    #name = scrapy.Field()
    #price = scrapy.Field()
    #url = scrapy.Field()
    tags = scrapy.Field()
    datas = scrapy.Field()

class CMattProduct(scrapy.Item):
    #name = scrapy.Field()
    #price = scrapy.Field()
    #url = scrapy.Field()
    #prodID = scrapy.Field()
    #urlAPI = scrapy.Field()
    jsons  = scrapy.Field()
    #datas = scrapy.Field()
    
class BalaProduct(scrapy.Item):
    #name = scrapy.Field()
    #price = scrapy.Field()
    url = scrapy.Field()
    eans = scrapy.Field()
    price = scrapy.Field()    