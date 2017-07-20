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
__model_name__ = 'bens.Bens'
import auth, base_models
from orm import *
from form import *

class Bens(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'bens'
        self.__title__ ='Bens' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'bens.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , name='Nome', size=80)
        self.cart = text_field(view_order=2 , name='Carateristica', size=80)
        self.marc = string_field(view_order=3 , name='Marca', size=80)
        self.logo = string_field(view_order=4 , name='Logo', size=80)
        self.tipo = combo_field(view_order=5 , name='Tipo', size=80)
        self.descc = text_field(view_order=6 , name='Descricao', size=80)
        self.datr = date_field(view_order=7 , name='DataRegisto', size=80)