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
__model_name__ = 'metodo_pagamento.MetodoPagamento'
import auth, base_models
from orm import *
from form import *
try:
    from plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

class MetodoPagamento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'metodo_pagamento'
        self.__title__ = 'Metodos de Pagamento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'metodo_pagamento.ordem'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['Caixa'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name='Nome', size=60)
        self.conta = choice_field(view_order=2, name='Conta', size=60, args='required', model='plano_contas', column='codigo nome', options='model.get_contas()')
        self.ordem = integer_field(view_order=3, name='Ordem', size=10)

    def get_contas(self):
        return PlanoContas().get_dinheiro()
