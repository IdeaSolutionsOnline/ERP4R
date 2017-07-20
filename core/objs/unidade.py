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
__model_name__ = 'unidade.Unidade'
import auth, base_models
from orm import *
from form import *

class Unidade(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'unidade'
        self.__title__ = 'Unidades de Medida'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['simbolo']
        self.__order_by__ = 'unidade.nome'
        #def get_options_convert(self): ver como fazer no futuro, hoje não tenho tempo
        self.simbolo = string_field(view_order=1, name='Simbolo', size=40)
        self.nome = string_field(view_order=2, name='Nome', size=60)
        self.linha_unidade = list_field(view_order=3, name='Conversões', model_name='linha_unidade.LinhaUnidade', condition="unidade='{id}'", list_edit_mode='inline', onlist = False)


