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
__model_name__ = 'documento.Documento'
#import base_models
from orm import *
from form import *


class Documento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'documento'
        self.__title__ = 'Documentos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['descricao']

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }

        self.inscricao = parent_field(view_order=1, name ='Inscrição', args='style:visibility="hidden"', model_name='inscricao.Inscricao', nolabel=True, onlist=False, column='numero')
        self.nome = string_field(view_order = 2, name = 'Nome', size = 80)
        self.upload = upload_field(view_order = 3, name = 'Documento', size = 100)


