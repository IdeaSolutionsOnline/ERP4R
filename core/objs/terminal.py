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
__model_name__ = 'terminal.Terminal'
import auth, base_models
from orm import *
from form import *

class Terminal(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'terminal'
        self.__title__= 'Terminais de Trabalho'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
        }
        self.__get_options__ = ['name']

        self.name = string_field(view_order=1 , name='Nome', size=40)
        self.users = many2many(view_order=2 , name='Utilizadores', condition="terminal='{id}'", model_name='users.Users', fields = ['nome', 'login', 'email', 'estado'], onlist = False)
#pela lógica o get_terminal deveria ser um metodo aqui e não uma função no utils

