# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde


Deverá funcionar pelo sistema de arvore tipo

Cabo verde
    Santiago
        Praia
            Achada de Santo António
                bla bla

"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'localizacao.Localizacao'
import auth, base_models
from orm import *
from form import *

class Localizacao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'localizacao'
        self.__title__ = 'Localizações'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'localizacao.codigo'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['codigo']

        self.codigo = string_field(view_order=1 , name='Codigo', size=80)
        self.nome = string_field(view_order=2 , name='Nome', size=80)
        self.ascendente = choice_field(view_order=3 , name='Ascendente', model=self.__name__, column='codigo', options='model.get_self()')

    def get_self(self):
        return self.get_options()
