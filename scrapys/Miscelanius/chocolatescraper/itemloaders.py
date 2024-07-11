from itemloaders.processors import TakeFirst, MapCompose, Compose, Identity
from scrapy.loader import ItemLoader
import re

class ChocolateProductLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    
    
    
    def extract_data_layer(self, script_text):
         # Regex pattern to find dataLayer assignment
         pattern = re.compile(r'\"listProducts\":(\[.*?\])', re.DOTALL)#re.compile(r'\"listProducts\":(\[.*?\])', re.DOTALL)#(r'\"listProducts\":\[(\{.*?\})\]', re.DOTALL)#(r'dataLayer\s*=\s*(\[.*?\])', re.DOTALL)
         match = pattern.search(script_text)
         if match:
             return match.group(1)
         return None
    
    def extract_tags(self, script_text):
         # Regex pattern to find dataLayer assignment
         pattern = re.compile(r'gtag\(\s*\'event\',\s*\'view_item_list\',\s*(\{.*?\})\s*\);', re.DOTALL)
         match = pattern.search(script_text)
         if match:
             return match.group(1)
         return None
    
    #default_output_processor = TakeFirst()
    
    tags_in = MapCompose(lambda x :  ChocolateProductLoader().extract_tags(x) )
    datas_in = MapCompose(lambda x :  ChocolateProductLoader().extract_data_layer(x) )
    #price_in = MapCompose(lambda x: x.split("£")[-1])
    #url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x )
    
    
class SodimacLoader(ItemLoader):
      default_output_processor = TakeFirst()    
      
class CMattLoader(ItemLoader):
      default_output_processor = TakeFirst() 
      
      def extract_IDs(self, script_text):
           # Regex pattern to find dataLayer assignment
           pattern = re.compile(r'ecomm_prodid:\s*(\[.*?\])', re.DOTALL)
           match = pattern.search(script_text)
           if match:
               return match.group(1)
           return None
      
      
      prodID_in = MapCompose(lambda x: CMattLoader().extract_IDs(x))


class BalaProductLoader(ItemLoader):
    
    default_output_processor = Identity()
            
    def extract_ean(self, dumped_json):
         # Regex pattern to find dataLayer assignment
         pattern_ean   = re.compile(r'"ean":"(\d+)"')
         match         = re.findall(pattern_ean, dumped_json)
         if match:
             return match
         return None
    
    def extract_url(self, dumped_json):
         # Regex pattern to find dataLayer assignment
         pattern_link  = re.compile(r'"link":"(.*?)"')
         match         = re.findall(pattern_link, dumped_json)
         if match:
             return match
         return None
    
    def extract_price(self, dumped_json):
         # Regex pattern to find dataLayer assignment
         pattern_price = re.compile(r'"Price":(\d+\.\d+)')
         match         = re.findall(pattern_price, dumped_json)
         if match:
             return match
         return None
    #default_output_processor = TakeFirst()
    
    eans_in   = MapCompose(lambda x :  BalaProductLoader().extract_ean(x) )
    url_in   = MapCompose(lambda x : BalaProductLoader().extract_url(x) )
    price_in = MapCompose(lambda x: BalaProductLoader().extract_price(x))
    #url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x )


