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
__model_name__='linha_stock.LinhaStock'
import auth, base_models
from orm import *
from form import *
try:
    from armazem import Armazem
except:
    from armazem import Armazem
try:
    from produto import Produto
except:
    from produto import Produto

class LinhaStock(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_stock'
        self.__title__= 'Linhas de Stock'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['descricao']

        self.stock = parent_field(view_order=1, name ='Movimento de Stock', args='style:visibility="hidden"', model_name='stock.Stock', nolabel=True, onlist=False, column='numero')
        self.descricao = string_field(view_order=2, name ='Descrição', size=50)
        self.produto = choice_field(view_order=3, name ='Produto', args='required', size=50, model='produto', column='nome', options='model.get_produtos()')
        self.armazem = combo_field(view_order=4, name ='Armazém', args='required', size=50, model='armazem', column='nome', options='model.get_armazens()')
        self.quant_entrada = float_field(view_order=5, name ='Quant.Entrada', sum=True)
        self.quant_saida = float_field(view_order=6, name ='Quant.Saida', sum=True)

    def get_armazens(self):
        return Armazem().get_options()

    def get_produtos(self):
        return Produto().get_options()

