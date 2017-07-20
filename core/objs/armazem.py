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
__model_name__ = 'armazem.Armazem'
import auth, base_models
from orm import *
from form import *

class Armazem(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'armazem'
        self.__title__ = 'Armazens'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'armazem.nome'
        
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor de Stocks'],
            'create':['Gestor de Stocks'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.nome = string_field(view_order=1 , name='Nome', size = 60)
        self.tipo = combo_field(view_order=2 , name='Tipo', size = 60, options=[('cliente','Cliente'), ('fornecedor','Fornecedor'), ('fisico','Fisico'), ('regularizacoes','Regularizações')])
        self.estado = combo_field(view_order=3 , name='Estado', size = 60, options=[('activo','Activo'), ('cancelado','Cancelado')])
