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
__model_name__ = 'tipo_rendimento.TipoRendimento'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas


class TipoRendimento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'tipo_rendimento'
        self.__title__= 'Tipos de Rendimento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__order_by__='nome'
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order = 1, name='Nome', size = 90)
        self.limite_isento = currency_field(view_order=2, name='Minimo Tributavel', size=90, default=0)        
        self.desconto_inps = boolean_field(view_order=3, name='Segurança Social?', size=90, default=True)
        self.percent_tribuavel = percent_field(view_order=4, name ='Percentagem Tributavel', size=90, search=False)
        self.conta_debito = choice_field(view_order = 5, name = 'Conta Debito', size = 90, model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_credito = choice_field(view_order = 6, name = 'Conta Credito', size = 90, model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        
    def get_opts(self, get_str):
        return eval(get_str)

    def get_options_buyable(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                options.append((option['id'], option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_buyable', createfunc = get_results)

        
