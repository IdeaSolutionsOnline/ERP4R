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
__model_name__ = 'tipo_desconto.TipoDesconto'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas


class TipoDesconto(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'tipo_desconto'
        self.__title__= 'Tipos de Descontos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order = 1, name='Nome',size = 90)
        self.taxa = boolean_field(view_order=2,name='Percentagem?',size=20)
        self.base = combo_field(view_order=3,name='Insidir sob', size=50, options=[('salario base','Salário Base'),('salario bruto','Salário Bruto')])
        self.conta_debito = choice_field(view_order = 4, name = 'Conta Debito', size = 90, model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_credito = choice_field(view_order = 5, name = 'Conta Credito', size = 90, model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        
    def get_opts(self, get_str):
        return eval(get_str)

        
