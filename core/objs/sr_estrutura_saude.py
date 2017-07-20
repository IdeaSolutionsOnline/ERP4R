# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CvTek'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CvTek"
__status__ = "Development"
__model_name__ = 'sr_estrutura_saude.EstruturaSaude'
import auth, base_models
from orm import *
from form import *

class EstruturaSaude(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sr_estrutura_saude'
        self.__title__ = 'Estrutura de Saúde'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']




