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
__model_name__ = 'candidatura.Candidatura'
import auth, base_models
from orm import *
from form import *

class Candidatura(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'candidatura'
        self.__title__ ='Candidatura' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'candidatura.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }        
        self.tipo = date_field(view_order=1 , name='Datacandidatura', size=80)
        self.proposta = list_field(view_order = 2, name = 'Proposta Candidatura', model_name = 'proposta.Proposta', condition = "rfpp='{id}'", list_edit_mode = 'popup', onlist = False)
        self.rfcd = parent_field(view_order=3, name ='Ref Candidatura', model_name='concurso.Concurso', nolabel=True,  column='candidatura')