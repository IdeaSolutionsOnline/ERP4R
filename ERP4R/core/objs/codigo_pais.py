# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'codigo_pais.CodigoPais'
import auth, base_models
from orm import *
from form import *

class CodigoPais(Model, View):
    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'codigo_pais'
        self.__title__ = 'Codigo dos Países'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']


        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }
            
        self.codigo = string_field(view_order = 1, name = 'Código', size = 30)
        self.nome = string_field(view_order = 2, name = 'Nome', size = 80)


    def get_options_buyable(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                options.append((str(option['codigo']), option['codigo']+' - '+option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_buyable', createfunc = get_results)
