# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Gestão de ocorrencias que seguiram para o tribunal
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'tribunal.Tribunal'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class Tribunal(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'tribunal'
        self.__title__ = 'Emcaminhamento para o Tribunal'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'tribunal.data_inicial'
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }
        #self.__get_options__ = ['nome']

        self.ocorrencia = parent_field(view_order=1, name ='Ocorrencia', args='style:visibility="hidden"', model_name='ocorrencia.Ocorrencia', nolabel=True, onlist=False, column='numero')
        self.data = date_field(view_order=2, name='Data', size=60)
        self.hora = time_field(view_order=3, name='Hora', size=60)
        self.terceiro = choice_field(view_order=4, name ='Terceiro', size=60, model='terceiro', column='nome', options="model.get_terceiros()")
        self.descricao = text_field(view_order=5, name ='Descrição', args='rows=5', size=100, colspan=3)

    def get_terceiros(self):
        return Terceiro().get_options()
