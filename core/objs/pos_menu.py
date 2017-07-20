# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""ERP+"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__= 'pos_menu.POSMenu'
import auth, base_models
from orm import *
from form import *

class POSMenu(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'pos_menu'
        self.__title__= 'Menus POS'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'pos_menu.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=40)
        self.descricao = string_field(view_order=2, name ='Descrição', size=60)
        self.tipo = combo_field(view_order=3, name ='Tipo', args='required', options=[('comida','Comida'), ('bebida','Bebida'), ('diversos','Diversos')])
        self.terminal = many2many(view_order=4, name ='Postos', condition="pos_menu='{id}'", model_name='terminal.Terminal')
        self.produto = many2many(view_order=5, name ='Produtos', condition="pos_menu='{id}'", model_name='produto.Produto')

