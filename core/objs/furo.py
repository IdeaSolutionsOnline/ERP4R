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
__model_name__ = 'furo.Furo'
import auth, base_models
from orm import *
from form import *

class Furo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'furo'
        self.__title__ = 'Furo de Extracção de Água'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'furo.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=80)
        self.localizacao = string_field(view_order=2, name ='Localização', size=80)
        self.rede = many2many(view_order=3, name ='Redes', condition="furo='{id}'", model_name='rede.Rede')#, colspan=2
        self.conduta = list_field(view_order=4, name='Condutas', simple=True, show_footer=False, fields=['nome'], condition="furo='{id}'", model_name='conduta.Conduta', list_edit_mode='inline', onlist = False)#colspan=2, 
        self.contador = list_field(view_order=5, name='Contadores', simple=True, show_footer=False, fields=['nome'], condition="furo='{id}'", model_name='contador.Contador', list_edit_mode='inline', onlist = False)#colspan=2, 

