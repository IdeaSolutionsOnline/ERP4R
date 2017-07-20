# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'compras.Compras'
import auth, base_models
from orm import *
from form import *

class Compras(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'compras'
        self.__title__ ='Compras' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'compras.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.valttl = string_field(view_order=1 , name='ValorTotal', size=80)
        self.desct = text_field(view_order=2 , name='Desconto', size=80)
        self.tppag = string_field(view_order=3 , name='TipoPagamento', size=80)
        self.descc = string_field(view_order=4 , name='Descricao', size=80)
        self.datrg = date_field(view_order=5 , name='DataRegisto', size=80)
        self.rfcontrat = list_field(view_order = 6, name = 'Cntratos', model_name = 'contrato.Contrato', condition = "rf='{id}'", list_edit_mode = 'popup', onlist = False)
       
        