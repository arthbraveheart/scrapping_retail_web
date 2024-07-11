# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:13:28 2024

@author: ArthurRodrigues
"""
from db import load_pkl,save_pkl
from settings import out_path
import pandas as pd
import numpy as np
import time
import re

today = time.strftime("%d-%m-%Y")



def _wizard(base,guideshops,folder, date):
    glued  =  _concat_shops(guideshops, date)
    Base   =  _procWizX(base,glued)
    Base   =  _concat_Leroy(Base,folder)
    DB     =  load_pkl(name=f'DB_{date}') 
    DB['Base'].append(Base)
    DB['Others'].append(glued)
    
    save_pkl(DB, name=f'DB_{date}')      

def _updateDB(DBname,KEY,FILE):
    DB     =  load_pkl(name=DBname) 
    DB[KEY].append(FILE)
    save_pkl(DB, name=DBname)


def _procWizX(base,guides_glued):
    
    gg = guides_glued
    
    not_in = set(base['EAN']) - set(gg['EAN'])
    not_in_dict = {idx:'Não encontrado' for idx in not_in}
    
    gg.set_index('EAN', inplace=True)
    gg_dict = gg.to_dict()
    
    
    
    for key in gg_dict.keys():
        base[key] = base['EAN'].replace(gg_dict[key])
    for key in gg_dict.keys():
        base[key] = base[key].replace(not_in_dict)
    
    return base



def _concat_shops(guideshops, date):
    R = []
    for guideshop in guideshops:
        result = pd.read_csv(out_path + f"{guideshop}_{date}.csv",sep=';')
        R.append(result)
    R = pd.concat(R)    
    return R


def _concat_Leroy(base,folder):
    
    state_code = ['MG','RJ','SP','ES','DF','MS','PR','SC','GO','BA']
    L = []
    for estado in state_code:
       l = pd.read_excel(f"C:/Users/ArthurRodrigues/OneDrive - ABC ATACADO BRASILEIRO DA CONSTR LTDA/9. Pricing/1. Output/{folder}/Leroy_{estado}_{today}.xlsx")
       L.append(l)
    L_cat = pd.concat(L, join='inner', axis=1)
    
    
    
    
    #L_cat = pd.read_excel("C:/Users/ArthurRodrigues/OneDrive - ABC ATACADO BRASILEIRO DA CONSTR LTDA/9. Pricing/1. Output/leroys.xlsx")
    
    eans = L_cat['EAN']#L[1]['EAN']
    
    #L_cat = pd.concat(L, join='inner', axis=1)
    """L_cat_cols = L_cat.columns
    for d in [5*i for i in range(1,10)]:
        L_cat.drop(L_cat_cols[d], axis=1, inplace=True)
    L_cat['EAN'] = eans
    """
    
    for estado in state_code:
        L_cat.rename(columns={f'Vendedor {estado}':f'Vendedor Leroy {estado}',f'Preço {estado}':f'Preço Leroy {estado}',f'Disponibilidade {estado}':f'Disponibilidade Leroy {estado}',f'Link {estado}':f'Link Leroy {estado}'},inplace=True)
    
    base = _procWizX(base, L_cat)
        
    return base    


def getBugs(target,colTargetID):

    right = []
    err = []
    
    for i in range(target.shape[0]):
        see = target.iloc[i,colTargetID]
        try:
            right.append(np.float64(see))
        except:
            err.append(i)
    bugDict = {
        'right':right,
        'err':err
        }    
    return    bugDict 


def getSeller():
    concorrentes = historico['Nome do Concorrente']
    conc = concorrentes.copy()

    conc = conc.str.split('-',expand=True,regex=False)[0]
    conc = conc.apply(lambda x: unidecode(x).lower())
    conc = conc.apply(lambda x: x.replace('.',''))
    conc = conc.str.strip()

    states = ['sp','mg','pr','sc','es','ba','ms','df','rj','go']

    for state in states:
        pattern = fr' {state}$'
        conc    = conc.str.split(pattern, expand=True, regex=True)[0]

    conc    = conc.str.split(' (', expand=True, regex=False)[0]

    sellerDict = {
        'balarotti':'balaroti',
        'belaroti':'balaroti',
        'cimcal':'cincal',
        'ferreria costa':'ferreira costa',
        'forgacu':'forguacu',
        'leory':'leroy',
        'leroy merlin':'leroy',
        'munidal acabamentos':'mundial',
        'santa cruz acabamentos':'sta cruz',
        'telhanorte':'telha norte',
        'vimercat engera': 'vimercat',
        'vimercat mater':'vimercat',
        'wig construcao': 'wig'
        }
    conc.replace(sellerDict, inplace=True)
    conc = conc.str.strip()
    historico['Nome do Concorrente'] = conc



def f_histMagic():
    historico = pd.read_excel('C:/Users/ArthurRodrigues/Codes/Pricing/Target/f_historicoprecos.xlsx')
    histCols  = historico.columns 
    prices    = histCols[17:] 
    trues     = [historico.dtypes == 'O']
    historico = historico.astype({col: 'string' for col in trues[0][trues[0] == True].index})
    
    
    dates_bool   = historico['Data'].str.contains('/', regex=True)
    dates_trueID = dates_bool[dates_bool == True].index
    dates_true   = historico.iloc[dates_trueID,1]
    formated     = pd.to_datetime(dates_true, format='%d/%m/%Y')
    
    historico.loc[list(dates_trueID),'Data'] = formated
    historico['Data']   = pd.to_datetime(historico['Data'], format='%Y-%m-%d %H:%M:%S').copy()
    
    historico.astype({cols:'string' for cols in prices})
    
    for price in prices:
        
        clean2           = [re.sub(r'[^0-9,.]', '',historico.loc[i,price]) for i in range(0,historico.shape[0])]
        historico[price] = clean2
    
    for price in prices: 
        work = historico.loc[historico[price].str.contains(',')].copy()
        work.loc[:,price] = work.loc[:,price].apply(lambda x: x.replace('.','').replace(',','.'))
        work.loc[work.index,price]
        historico.loc[work.index,:] = work.copy()
    
    historico.astype({cols:np.float64 for cols in prices})    
    
    
    getSeller()
    
#base = pd.read_excel("C:/Users/ArthurRodrigues/Codes/Pricing/Target/PRICING SEMANAL (ARQUIVO BASE).xlsx", sheet_name='Monit. ShP Digital ALL')
#_concat_Leroy(base,'CurvaA_25_03_2024')

#f_histMagic()




























