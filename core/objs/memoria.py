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
__model_name__ = 'memoria.Memoria'
import auth, base_models
from orm import *
from form import *

class Memoria(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'memoria'
        self.__title__ = 'Memórias'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Vendedor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=40)
        self.descricao = string_field(view_order=2, name ='Descrição', size=40)
        self.posicao = integer_field(view_order=3, name ='Posição', size=40)
        self.foto = image_field(view_order=4, name ='Foto', size=100)
        self.impressa = boolean_field(view_order=5, name ='Impressa?', default=False)
        self.valor_pago = decimal_field(view_order=6, name ='Valor Pago', size=40, sum=True, default=0.0)
        self.terminal = many2many(view_order=7, name ='Terminais', condition="memoria='{id}'", model_name='terminal.Terminal')
        self.movimento_memoria = list_field(view_order=8, name ='Movimentos de Memória', condition="memoria='{id}'", model_name='movimento_memoria.MovimentoMemoria', list_edit_mode='inline', onlist = False)


