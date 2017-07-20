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
__model_name__ = 'users.Users'
import auth, base_models
from orm import *
from form import *

class Users(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'users'
        self.__title__ = 'Utilizadores'
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

        self.nome = string_field(view_order = 1, name = 'Nome', size = 50)
        self.login = string_field(view_order = 2, name = 'Login', size = 40)
        self.password = password_field(view_order = 3, name = 'Password', size = 40, onlist = False)
        self.email = string_field(view_order = 4, name = 'Email', size = 80)
        self.estado = combo_field(view_order = 5, name = 'Estado', size = 40, default = 'active', options = [('active','Activo'), ('canceled','Cancelado')], onlist = False)
        self.foto = image_field(view_order = 6, name = 'Foto', size = 100, onlist = False)
        self.frontoffice = boolean_field(view_order = 7, name = 'FrontOffice?')

        self.role = many2many(view_order = 8, name = 'Função', size = 40, model_name = 'role.Role', condition = "users='{id}'")
        self.terminal = many2many(view_order = 9, name = 'Terminais POS', size = 40, model_name = 'terminal.Terminal', condition = "users='{id}'")
        self.email_account = list_field(view_order = 10, name = 'Contas de Email', condition = "users='{id}'", model_name = 'email_account.EmailAccount', show_footer = False, list_edit_mode = 'inline', onlist = False)
