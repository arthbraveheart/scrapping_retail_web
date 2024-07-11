# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:26:57 2024

@author: ArthurRodrigues
"""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.io import write_html
import re
import merged

"""
historico = merged.load_pkl('f_historico')

conc = historico['Nome do Concorrente'].nunique()
concorrentes = historico['Nome do Concorrente'].drop_duplicates()
n1   = historico['n1'].nunique()

group2 = historico.groupby(['Nome do Concorrente'])['n1'].value_counts()
group2 = group2.to_frame().reset_index()

fig = make_subplots(rows=conc, cols=1)

i=1
for c in concorrentes:
    
    fig.add_trace(
        go.Scatter(x=group2.query("`Nome do Concorrente`==@c").n1, y=group2['count']),
        row=i, col=1
    )
    i=i+1


fig.update_layout( title_text="Side By Side Subplots") #height=600, width=800,
write_html(fig,'C:/Users/ArthurRodrigues/Codes/Expansion/Visuals/subplots.html')
"""
#fig.show()
stacked = merged.load_pkl('stacked')
uf = ['MG','RJ','SP','ES','DF','MS','PR','SC','GO','BA']
stacked['Seller Exclusivo'] = '-'
summed = stacked[stacked['Share+1']!=0][stacked['Share+1']!=9].loc[:,'Share+1'].apply(lambda x: x+1)
stacked.loc[list(summed.index),'Share+1'] = summed
sku = list(set(stacked['SKU']))
for u in uf:    
    for s in sku:
        ll = stacked.query("SKU==@s & UF==@u ").loc[:,'Share+1']
        if len(re.findall('0',str(list(ll)))) == len(ll)-1:
            stacked.loc[list(ll.index),'Exclusivo'] = 1
            stacked.loc[list(ll.index),'Seller Exclusivo'] = len(ll)*list(stacked.loc[list(ll[ll!=0].index),'Seller'])
        else:    
            stacked.loc[list(ll.index),'Exclusivo'] = 0




