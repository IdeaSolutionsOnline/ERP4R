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
__model_name__ = 'area_fiscal.AreaFiscal'
import auth, base_models
from orm import *
from form import *

class AreaFiscal(Model, View):
    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'area_fiscal'
        self.__title__ = 'Área Fiscal'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__db_mode__ = 'None'
        self.__get_options__ = ['local']
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }


        self.codigo = string_field(view_order = 1, name = 'Código', size = 30)
        self.local = string_field(view_order = 2, name = 'Local', size = 80)

    def get_options_buyable(self):
        def get_results():
            options = []
            opts = self.get()
            for option in opts:
                options.append((str(option['codigo']), option['local']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_buyable', createfunc = get_results)


    def get_options_local(self):
        def get_results():
            options = []
            opts = self.get()
            for option in opts:
                options.append((str(option['local']), option['local']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_local', createfunc = get_results) 	