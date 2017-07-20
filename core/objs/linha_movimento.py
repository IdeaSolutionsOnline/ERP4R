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
__model_name__ = 'linha_movimento.LinhaMovimento'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

class LinhaMovimento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_movimento'
        self.__title__ = 'Linhas de Movimento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['descricao']

        self.movimento = parent_field(view_order=1, name ='Movimento', args='style:visibility="hidden"', model_name='movimento.Movimento', nolabel=True, onlist=False, search=False, column='numero')
        self.descricao = string_field(view_order=2, name ='Descrição', size=60)
        self.conta = choice_field(view_order=3, name ='Conta', args='required', size=50, model='plano_contas', column='codigo nome', options='model.get_contas()')
        self.quant_debito = decimal_field(view_order=4, name ='Quant.Débito', sum=True)
        self.debito = currency_field(view_order=5, name ='Débito', sum=True)
        self.quant_credito = decimal_field(view_order=6, name ='Quant.Crédito', sum=True)
        self.credito = currency_field(view_order=7, name ='Crédito', sum=True)

    def get_contas(self):
        return PlanoContas().get_lancamento()
