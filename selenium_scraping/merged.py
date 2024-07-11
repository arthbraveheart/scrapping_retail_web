# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:12:48 2024

@author: ArthurRodrigues


O intuito é otimizar os processos de configuração dos códigos webscrapping
Basicamente é dividido em Input, Scripts e Output. 
Os trabalhos despendiosos de configuração como designação dos diretórios e bibliotecas vamos defini-los aqui. 
Assim, todos os cripts contidos nessa package serão atualizados automaticamente.  


*Descobri que já temos uma tabela concatenada
cloud = 'C:/Users/ArthurRodrigues/OneDrive - ABC ATACADO BRASILEIRO DA CONSTR LTDA/9. Pricing/0 . Input/'

"""
from settings import input_path, input_sheetname, monitoramento_path, monitoramento_sheetname,change,change2,strategy_path,strategy_sheetname, atualizado_path, db_path
from search import _replace, links_dict
import pandas as pd


def set_Targets():
    
    target        = pd.read_excel(input_path, sheet_name=input_sheetname)
    monitoramento = pd.read_excel(monitoramento_path, sheet_name=monitoramento_sheetname) 
    #what we have here
    target_cols               = target.columns
    monitoramento_cols        = monitoramento.columns
    #better views
    monitoramento_cols.rename('Colunas', inplace=True)
    target_cols.rename('Colunas', inplace=True)
    monitoramento_just       =  set(monitoramento_cols) - set(target_cols)
    just_monitoramento_links = pd.Series(list(monitoramento_just))
    just_monitoramento_links = just_monitoramento_links[just_monitoramento_links.str.contains('Link')]
    
    target_just       = set(target_cols) - set(monitoramento_cols)
    just_target_links = target_cols[target_cols.str.contains('Link')]
    #just_target_links = just_target_links[just_target_links.str.contains('Link')]
    target_links      = target[['SKU','EAN']+ list(just_target_links)]
    
    target_merged     = target.merge(monitoramento[['SKU']+list(just_monitoramento_links)], on='SKU' )
    
    
    #retirando links irrelevantes
    target_merged.replace({'Link Telha Norte MG SP': 'https://www.telhanorte.com.br/', 
                           'Link C&C SP':            'https://www.cec.com.br/',
                           'Link Mundial':           'https://www.mundialacabamentos.com.br/',
                           'Link Cassol  SC':        'https://www.cassol.com.br/',
                           'Link Cassol  PR':        'https://www.cassol.com.br/',
                           'Link Balaroti SC':       'https://www.balaroti.com.br/',
                           'Link Balaroti PR':       'https://www.balaroti.com.br/',
                           'Link Obra Fácil':        'https://lojaobrafacil.com.br/',},
                           'Não encontrado', inplace=True)
    targetsDict = {
        'curva':target,
        'monitoramento':monitoramento,
        'targets':target_merged,
        }
    return targetsDict

def get_TargetEANs(target):
    eans     = target['EAN'].to_list()
    chnge    = pd.read_excel(change)
    chnge2   = pd.read_excel(change2, sheet_name='Planilha1')
    novos    = pd.read_excel('C:/Users/ArthurRodrigues/Codes/Pricing/Target/Novos Eans Junho 2024.xlsx', sheet_name="EAN'S")
    new      = chnge[chnge['Situação']=='Entra']['EAN']
    new2     = chnge2['EAN']
    new_eans = list(new2) + list(new) + list(eans) + list(novos['EAN'])
    return new_eans


def get_Strategics(monitoramento):
    strategy             = pd.read_excel(strategy_path, sheet_name = strategy_sheetname)
    strategy_target      = strategy.merge(monitoramento, on='SKU')
    strategy_eans_target = strategy['EAN']
    strategyDict         = {
                            'strategyTarget':strategy_target,
                            'strategyEAN': strategy_eans_target 
                            } 
    return strategyDict


def to_Search(target):
    search_group                = target[['EAN','Descrição']]
    search_group['description'] = search_group['Descrição'].apply(lambda x: _replace(x))
    search_group['key']         = search_group['description'].str.split(r' ', expand = True)[1]
    guide_to_search = list(links_dict.keys())
    searchDict = {'searchGroup': search_group,
                  'guides': guide_to_search}
    return searchDict


def get_Updated():
    atualizado = pd.read_excel(atualizado_path)
    return atualizado


def save_pkl(obj, name='object', path=db_path):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
        file.close()
       
def load_pkl(name='object', path=db_path):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data    

def update_Pickles():
    
    Targets    = set_Targets()
    Eans       = get_TargetEANs(Targets['curva']) 
    Strategics = get_Strategics(Targets['monitoramento']) 
    Search     = to_Search(Targets['curva'])
    Updated    = get_Updated()
    ALL        = {
                'Targets'   :Targets, 
                'Eans'      :Eans, 
                'Strategics':Strategics, 
                'Search'    :Search, 
                'Updated'   :Updated
    }
    for each in ALL.keys():
        save_pkl(ALL[each], name=each)
    save_pkl(ALL, name='ALL_Targets')
    
def get_Pickles():
    pickles = load_pkl(name='ALL_Targets')
    return pickles    
    
def routine():
    update_Pickles()
    pickles = get_Pickles()
    return pickles    