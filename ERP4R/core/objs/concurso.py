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
__model_name__ = 'concurso.Concurso'
import auth, base_models
from orm import *
from form import *

class Concurso(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'concurso'
        self.__title__ ='Concurso' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'concurso.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.desig = string_field(view_order=1 , name='Designacao', size=80)
        self.logo = string_field(view_order=2 , name='Logo', size=80)
        self.descc = string_field(view_order=3 , name='Descricao', size=80)
        self.tipo = combo_field(view_order=3 , name='Tipo', size=80, options=[('tipo1','Tipo1'), ('tipo2','Tipo2'), ('tipo3','Tipo3'), ('tipo4','Tipo4'), ('tipo5','Tipo5'), ('tipo6','Tipo6'), ('tipo7','Tipo7'), ('tipo8','Tipo8'), ('tipo9','Tipo9'), ('tipo10','Tipo10')])
        self.datainic = date_field(view_order=5 , name='Data Inicial', size=40, args = 'required', default = datetime.date.today())
        self.datafin = date_field(view_order=6 , name='Data Final', size=40, args = 'required', default = datetime.date.today())
        self.cart = text_field(view_order=7 , name='Caracteristica', size=80)
        self.candidatura = list_field(view_order = 8, name = 'Candidatura concurso', model_name = 'candidatura.Candidatura', condition = "rfcd='{id}'", list_edit_mode = 'popup', onlist = False)
        self.rfccv = parent_field(view_order=9, name ='Ref convite', model_name='conviteconcforn.Conviteconcforn', nolabel=True,  column='rfconcurscv') 