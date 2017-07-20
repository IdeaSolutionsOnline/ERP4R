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
__model_name__ = 'rh_linha_recibo_salario.RHLinhaReciboSalario'
import auth, base_models
from orm import *
from form import *


class RHLinhaReciboSalario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_linha_recibo_salario'
        self.__title__= 'Linha Recibo Salário'
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

        self.rh_recibo_salario = parent_field(view_order=1 , name='Recibo', onlist=False, model_name ='rh_recibo_salario.RHReciboSalario')
        self.rh_tipo_rendimento = parent_field(view_order=2 , hidden=True, onlist=False, model_name ='rh_tipo_rendimento.RHTipoRendimento', column='nome')
        self.rh_tipo_desconto = parent_field(view_order=3 , hidden=True, onlist=False, model_name ='rh_tipo_desconto.RHTipoDesconto', column='nome')
        self.nome = string_field(view_order=4,name='Descrição',size=70)
        self.valor = currency_field(view_order=5,name='Valor',size=70, sum=True)
        self.parte_trib=currency_field(view_order=6,name='Parte Tributavel',size=45,args='readonly', sum=True, onlist=False)
        #recebe a origem do rendimento expresso na linha (salario, iur, inps, rendimento, desconto)
        self.origem =string_field(view_order=7, name='Origem', size=45, args='readonly',onlist=False)
        
        
        
