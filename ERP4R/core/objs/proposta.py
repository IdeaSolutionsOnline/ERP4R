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
__model_name__ = 'proposta.Proposta'
import auth, base_models
from orm import *
from form import *

class Proposta(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'proposta'
        self.__title__ ='Proposta' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'proposta.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.rf2 = parent_field(view_order=1, name ='Ref Fornecedor', model_name='fornecedor.Fornecedor', nolabel=True,  column='proposta')
        self.rfpp = parent_field(view_order=2, name ='Ref candidatura', model_name='candidatura.Candidatura', nolabel=True,  column='rfpropost')