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
__model_name__ = 'conviteconcforn.Conviteconcforn'
import auth, base_models
from orm import *
from form import *

class Conviteconcforn(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'conviteconcforn'
        self.__title__ ='Convite Concurso Fornecedor' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'conviteconcforn.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }        
        self.tipo = date_field(view_order=1 , name='Dataconvite', size=80)
        self.rffornecedcv = list_field(view_order = 2, name = 'Fornecedor convidado', model_name = 'fornecedor.Fornecedor', condition = "rffpcv='{id}'", list_edit_mode = 'popup', onlist = False)
        self.rfconcurscv = list_field(view_order = 3, name = ' Referência concurso', model_name = 'concurso.Concurso', condition = "rfccv='{id}'", list_edit_mode = 'popup', onlist = False)