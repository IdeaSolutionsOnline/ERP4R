# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Linhas do Relatório SQL, é utilizado para carregar variaveis no SQL
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'linha_sql_report.LinhaSQLReport'
import auth, base_models
from orm import *
from form import *

class LinhaSQLReport(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_sql_report'
        self.__title__ = 'Variaveis de Relatório'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['campo']

        self.sql_report = parent_field(view_order=1, name ='Relatório SQL', args='style:visibility="hidden"', model_name='sql_report.SQLReport', nolabel=True, onlist=False, search=False, column='name')
        self.variavel = string_field(view_order=2, name ='Variavel', args='required', size=60)
        self.valor = string_field(view_order=3, name ='Valor', args='required', size=60)
