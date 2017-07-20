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
__model_name__='diario.Diario'
import base_models#auth, 
from orm import *
from form import *

class Diario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'diario'
        self.__title__= 'Diários'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1 , name='Nome', size=60)
        self.tipo = combo_field(view_order=2 , name='Tipo', size=60, options=[('abertura','Abertura'), ('vendas','Vendas'), ('stock', 'Stock'), ('compras','Compras'), ('caixa','Caixa'), ('bancos','Bancos'), ('outros','Outros'), ('apuramento','Apuramento'), ('encerramento','Encerramento')])

    def get_diario(self, diario):
        self.kargs['where'] = "tipo='{diario}'".format(diario=diario)
        return self.get()[0]['id']


