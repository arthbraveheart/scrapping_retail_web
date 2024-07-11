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
      
      
class CForteLoader(ItemLoader):
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

       