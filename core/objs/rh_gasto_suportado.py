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
__model_name__ = 'rh_gasto_suportado.RHGastoSuportado'
import auth, base_models
from orm import *
from form import *


class RHGastoSuportado(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_gasto_suportado'
        self.__title__= 'Gatos Suportados em Salario'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__='valor desc'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.rh_recibo_salario = parent_field(view_order=1 , name='Recibo', size=70,onlist=True, column='periodo', model_name ='rh_recibo_salario.RHReciboSalario')
        self.nome = string_field(view_order=2,name='Descrição',size=100)
        self.valor = currency_field(view_order=3,name='Valor',size=70, sum=True)
        
        
        
