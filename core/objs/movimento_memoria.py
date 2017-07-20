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
__model_name__ = 'movimento_memoria.MovimentoMemoria'
import auth, base_models
from orm import *
from form import *
try:
    from my_produto import Produto
except:
    from produto import Produto
try:
    from my_terminal import Terminal
except:
    from terminal import Terminal

class MovimentoMemoria(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'movimento_memoria'
        self.__title__ = 'Movimentos de Memória'
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

        self.memoria = parent_field(view_order=1, name ='Memória', args='style:visibility="hidden"', model_name='memoria.Memoria', nolabel=True, onlist=False, search=False, column='nome')
        self.descricao = string_field(view_order=2, name ='Descrição', size=60)
        self.produto = choice_field(view_order=3, name ='Produto', args='required', size=40, model='produto', column='nome', options="model.get_opts('Produto')")
        self.quantidade = decimal_field(view_order=4, name ='Quantidade', size=15)
        self.valor_unit = currency_field(view_order=5, name ='Val.Unit.')
        self.total = function_field(view_order=6, name ='Total', sum=True, search=False)
        self.vendedor = parent_field(view_order=7, name ='Vendedor', size=40, default="self.session['user']", model_name='users.Users', onlist=False, column='nome')
        self.terminal = combo_field(view_order=8, name ='Terminal', args='required', model='users', column='nome', options="model.get_opts('Terminal')")

    def get_opts(self, model):
        return eval(model + '().get_options()')

    def get_total(self, key):
        value = 0.0
        record = self.get(key=key)[0]
        value = to_decimal(record['valor_unit']) * to_decimal(record['quantidade'])
        return round(value,0)
