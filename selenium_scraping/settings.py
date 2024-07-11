# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:12:39 2024

@author: ArthurRodrigues

O intuito é otimizar os processos de configuração dos códigos webscrapping
Basicamente é dividido em Input, Scripts e Output. 
Os trabalhos despendiosos de configuração como designação dos diretórios e bibliotecas vamos defini-los aqui. 
Assim, todos os cripts contidos nessa package serão atualizados automaticamente.


"""
#input
path = 'C:/Users/ArthurRodrigues/Codes/Pricing/Target/'

input_path              = path + 'Pricing - 20 Março 2024 - CURVA A.xlsx'  #Cesta CURVA A - De Linha 06-MAR-2024.xlsx
input_sheetname         = 'Monit. ShP Digital ALL'     

monitoramento_path      = path + '01.11.23 - Monitoramento Concorrência digital (1).xlsx'
monitoramento_sheetname = 'Monitoramento compilado'

change                  = path + 'Mudanças Curva A Abril - 2024 1.xlsx'
change2                 = path + 'itens_adicionais_curvaA_maio2024.xlsx'

strategy_path           = path + 'Itens Estratégicos ABC ABRIL 24.xlsx'
strategy_sheetname      = 'Planilha2'

#output
out_path                = 'C:/Users/ArthurRodrigues/OneDrive - ABC ATACADO BRASILEIRO DA CONSTR LTDA/9. Pricing/1. Output/'#'C:/Users/ArthurRodrigues/Downloads/Pricing/Results/CSV/'

#atualizado
atualizado_path = path + 'Banco de Dados ATUALIZADO - 19.04.24.xlsx'

#dataBase
db_path = 'C:/Users/ArthurRodrigues/Codes/Variables/pricing_variables/'


