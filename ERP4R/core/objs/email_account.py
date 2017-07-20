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
__model_name__='email_account.EmailAccount'
import auth, base_models
from orm import *
from form import *

class EmailAccount(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'email_account'
        self.__title__= 'Contas de Email'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'email_account.email'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['email']

        self.users = parent_field(view_order=1, name ='Utilizadores', args='style:visibility="hidden"', model_name='users.Users', nolabel=True, onlist=False, column='nome')
        self.email = string_field(view_order=2, name='Email', size=60)
        self.ssl = boolean_field(view_order=3, name ='SSL?', default=True, onlist=False)
        self.pop3_server = string_field(view_order=4, name='Servidor POP3', size=60)
        self.smtp_server = string_field(view_order=5, name='Servidor SMTP', size=60)
        self.pop_port = integer_field(view_order=6, name='Porta POP', size=40, onlist=False)
        self.smtp_port = integer_field(view_order=7, name='Porta SMTP', size=40, onlist=False)
        self.pop_user = string_field(view_order=8, name='Utilizador POP3', size=60)
        self.smtp_user = string_field(view_order=9, name='Utilizador SMTP', size=60, onlist=False)
        self.pop_pass = password_field(view_order=10, name='Password POP', size=40, onlist=False)
        self.smtp_pass = password_field(view_order=11, name='Password SMTP', size=40, onlist=False)

