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
__model_name__= 'sub_familia_produto.SubFamiliaProduto'
import auth, base_models
from orm import *
from form import *

class SubFamiliaProduto(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sub_familia_produto'
        self.__title__= 'Sub Familias de Produtos'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'sub_familia_produto.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.nome = string_field(view_order=1, name ='Nome', size=60)


    def get_options_buyable(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                options.append((str(option['nome']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_buyable', createfunc = get_results)