# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Registo de Crimes
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'crime.Crime'
import auth, base_models
from orm import *
from form import *

class Crime(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'crime'
        self.__title__ = 'Tipos de Crime'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'data_inicial'
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }
        #self.__get_options__ = ['nome']

        self.ocorrencia = parent_field(view_order=1, name ='Ocorrencia', args='style:visibility="hidden"', model_name='ocorrencia.Ocorrencia', nolabel=True, onlist=False, column='numero')
        self.tipo = combo_field(view_order=2, name ='Tipo', size=40, options=[('assalto','Assalto'), ('roubo','Roubo'), ('agressao','Agressão'), ('electronico','Electrónico'), ('fiscal','Fiscal'), ('burla','Burla'), ('propriedade','Contra Propriedade'), ('economico','Económico'), ('droga','Drogas'), ('vbg','VBG'), ('atentado_pudor', 'Atentado ao Pudor'), ('sexual','Sexual'), ('abuso_confianca','Abuso de Confiança'), ('porte_ilegal_arma','Porte Ilegal de Arma')])
        self.descricao = text_field(view_order=3, name ='Descrição', size=100, colspan=3, args='rows=10')

