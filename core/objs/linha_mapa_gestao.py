# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina', 'Abner Oliveira']
__credits__ = []
__version__ = "1.0"
__maintainer__ = ['António Anacleto', 'Jair Medina', 'Jair Medina', 'Abner Oliveira']
__status__ = "Development"
__model_name__ = 'linha_mapa_gestao.LinhaMapaGestao'
#import auth, base_models
from orm import *
from form import *


class LinhaMapaGestao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        
        self.__name__ = 'linha_mapa_gestao'
        self.__title__ = 'Valores'
        self.__model_name__ = __model_name__
        #self.__list_edit_mode__ = 'inline'
    
        self.mapg = parent_field(view_order=1, name ='Mapa Gestao', args='style:visibility="hidden"', model_name='mapa_gestao.MapaGestao', nolabel=True, onlist=False, column='numero')
        self.cod_conta = choice_field(view_order=2, name ='Codigo de Conta', size=30, onchange='ean_onchange')
        self.conta = string_field(view_order=3, name ='Conta', size=45, onchange='ean_onchange')
        self.debito = currency_field(view_order = 4, name = 'Débito', sum = True, args = 'readonly')
        self.credito = currency_field(view_order = 5, name = 'Crédito', sum = True, args = 'readonly')