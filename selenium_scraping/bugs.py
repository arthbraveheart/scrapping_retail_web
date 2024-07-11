# -*- coding: utf-8 -*-
"""
Created on Thu May 30 23:34:27 2024

@author: ArthurRodrigues
"""

import merged
import numpy as np
from unidecode import unidecode


historico = merged.load_pkl('f_historico')

"""target = historico.query("  `Preço ABC Televendas`!='0' &  `Preço ABC Televendas`!=0 ")

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

"""

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
    'cincal':'cimcal',
    'ferreria costa':'ferreira costa',
    'forgacu':'forguacu',
    'leory':'leroy',
    'leroy merlin':'leroy',
    'mundial acabamentos':'mundial',
    'santa cruz acabamentos':'sta cruz',
    'telhanorte':'telha norte',
    'vimercat engera': 'vimercat',
    'vimercat mater':'vimercat',
    'wig construcao': 'wig'
    }
conc.replace(sellerDict, inplace=True)
conc = conc.str.strip()
historico['Nome do Concorrente'] = conc


