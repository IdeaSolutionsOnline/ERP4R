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
__model_name__='tipo_documento.TipoDocumento'
import auth, base_models
from orm import *
from form import *

class TipoDocumento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'tipo_documento'
        self.__title__= 'Tipos de Documento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['descricao']

        self.nome = string_field(view_order=1 , name='Nome', size=60)
        self.descricao = string_field(view_order=2 , name='Descricao', size=60)

    def get_options(self):
        def get_results():
            options = []
            fields = []
            opts = self.get(order_by = self.__order_by__, fields = fields)
            for record in opts:
                options.append((str(record['nome']), record['descricao']))
            #print (options)
            return options
        return erp_cache.get(key=self.__model_name__ + '_options', createfunc=get_results)

