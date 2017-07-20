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
__model_name__='email_category.EmailCategory'
import auth, base_models
from orm import *
from form import *

class EmailCategory(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'email_category'
        self.__title__= 'Categorias de Email'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }
        self.__get_options__ = ['name']

        self.name = string_field(view_order=1, name='Nome', size=40)
        self.emails = many2many(view_order=2, name='Emails', model_name='emails.Emails', condition="email_category='{id}'", fields = ['from', 'to', 'subject'])

