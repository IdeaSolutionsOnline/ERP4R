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
__model_name__ = 'zona.Zona'
import auth, base_models
from orm import *
from form import *

class Zona(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'zona'
        self.__title__ = 'Zonas de Distribuição'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'zona.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1 , name='Nome', size=80)
        self.contratos = list_field(view_order=2 , name='Contratos', model_name='contrato.Contrato', condition="zona='{id}'", list_edit_mode='edit', onlist = False)

