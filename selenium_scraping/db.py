# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:52:58 2024

@author: ArthurRodrigues
"""

from settings import db_path

def _routine():
    import time
    today    = time.strftime("%d-%m-%Y")
    DB_today = {
        'Leroys':[],
        'Others':[],
        'Base'  :[]
        }
    save_pkl(DB_today, name=f'DB_{today}')    

def save_pkl(obj, path = db_path, name = 'object'):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
        file.close()
       
def load_pkl(path = db_path, name = 'object'):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data 

      
      
      
      
      
      
      
