# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:06:49 2024

@author: ArthurRodrigues
"""


links_dict = {
    """ "Leroy Merlin" """           :'www.leroymerlin.com.br',
    """ "Cassol" """                 :'www.cassol.com.br',
    """ "Balaroti" """               :'www.balaroti.com.br',
    """ "Mundial Acabamentos" """    :'www.mundialacabamentos.com.br',
    """ "Casa Mattos" """            :'www.casamattos.com.br',
    """ "Todimo" """                 :'www.todimo.com.br',
    """ "Telha Norte" """            :'www.telhanorte.com.br',
    """ "Castelo Forte" """          :'www.casteloforte.com.br',
    """ "C&C" """                    :'www.cec.com.br',
    """ "Chatuba" """                :'www.chatuba.com.br',
    """ "Construmarques" """         :'www.construmarques.com.br',
    """ "Krepischi" """              :'www.krepischi.com.br',
    """ "Alvorada" """               :'www.alvoradams.com.br',
    """ "Amoedo" """                 :'www.amoedo.com.br',
    """ "Lojas Quero-Quero" """      :'www.queroquero.com.br',
    """ "Santa Cruz Acabamentos" """ :'www.santacruzacabamentos.com.br',
    """ "Sodimac" """                :'www.sodimac.com.br',
    """ "Viveza" """                 :'www.casaviveza.com.br',
    #""" "Tanto Itaipava" """: 'www.tanto.com.br',
    #""" "Castellar Acabamentos" """: 'www.castellarbh.com.br',
    """ "Carajás" """: 'www.carajas.com.br',
    #""" "Horus Acabamentos" """: 'www.horusacabamentos.com.br',
    """ "Condec Premium" """: 'www.condec.com.br',
    }


def _replace(word):
    replaced = word.replace("POR ", "PORCELANATO ").replace("AC ", "ACETINADO ").replace("CX ", "CAIXA ").replace("VS ", "VASO ").replace("ARG ","ARGAMASSA ").replace("INT ","INTERNO ").replace("EXT ","EXTERNO ").replace("RET ","RETIFICADO ").replace("PSO ","PISO ").replace("EMBRA ","EMBRAMACO ").replace("COMP ","ACOPLADA ").replace("BCO ","BRANCO ").replace("AZJ","AZULEJO") \
                   .replace("LAM ","LAMINADO ") \
                   .replace("REV ","REVESTIMENTO ") \
                   .replace("REVEST ","REVESTIMENTO ") \
                   .replace('VINIL ', 'VINILICO ')    
    return replaced







