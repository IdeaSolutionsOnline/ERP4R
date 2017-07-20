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
__model_name__='role.Role'
import auth, base_models
from orm import *
from form import *

class Role(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'role'
        self.__title__= 'Funções'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor','Gestor de Acessos'],
            'create':['Gestor','Gestor de Acessos'],
            'delete':['Gestor','Gestor de Acessos'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order = 1, name = 'Nome', size = 40)
        self.users = many2many(view_order = 2, name = 'Utilizadores', size = 200, model_name = 'users.Users', condition = "role='{id}'", fields = ['nome', 'login', 'email', 'estado'], onlist = False)

