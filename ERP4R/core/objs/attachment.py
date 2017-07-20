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
__model_name__='attachment.Attachment'
import auth, base_models
from orm import *
from form import *

class Attachment(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'attachment'
        self.__title__= 'Anexos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'attachment.model'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        #esta parte terá que ser revista
#       self.__records_view__ = [
#           ('model', "context['model_name']", []),
#           ('model_id', "context['key']", []),
#           ]
        self.__get_options__ = ['model']

        self.model = string_field(view_order=1, name ='Modelo', size=60)
        self.model_id = string_field(view_order=2, name ='Id do Modelo', size=60)# ver como passar para parent
        self.attachment = string_field(view_order=3, name ='Anexo', size=60)
        self.description = string_field(view_order=4, name ='Descrição', size=60)


