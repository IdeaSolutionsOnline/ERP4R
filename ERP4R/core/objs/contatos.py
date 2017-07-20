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
__model_name__ = 'contatos.Contatos'
import auth, base_models
from orm import *
from form import *

class Contatos(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'contatos'
        self.__title__ ='Contatos' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ ='edit'
        #self.__order_by__ = 'contatos.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.telfn = string_field(view_order=1 , name='Telefone', size=80)
        self.telmv = string_field(view_order=2 , name='Telemovel', size=80)
        self.fax = string_field(view_order=3 , name='Fax', size=80)
        self.email = string_field(view_order=4 , name='Email', size=80)
        self.email2 = string_field(view_order=5 , name='Email2', size=80)
        self.site = string_field(view_order=6 , name='Site', size=80)
        self.datrg = string_field(view_order=7 , name='Dateregisto', size=80)
        self.rf = parent_field(view_order=8, name ='Ref Fornecedor', model_name='fornecedor.Fornecedor', nolabel=True,  column='contatos')