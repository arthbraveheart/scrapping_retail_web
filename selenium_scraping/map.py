# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 22:26:51 2024

@author: ArthurRodrigues
"""

import requests
from bs4 import BeautifulSoup

urls = 'https://www.construbel.com.br/'
grab = requests.get(urls)
soup = BeautifulSoup(grab.text, 'html.parser')

# opening a file in write mode
f = open("test2.txt", "w")
# traverse paragraphs from soup
for link in soup.find_all("a"):
   data = link.get('href')
   f.write(str(data))
   f.write("\n")

f.close()