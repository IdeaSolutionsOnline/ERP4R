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
__model_name__ = 'residencia.Residencia'
import auth, base_models
from orm import *
from form import *

class Residencia(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'residencia'
        self.__title__ ='Residencia' 
        self.__model_name__ = __model_name__
        self.__get_options__ = ['residecom']
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['DGPOG'],
            'full_access':['DGPOG']
            }

        self.residecom = string_field(view_order=1 , name='Reside com?', size=50)
        

    def get_self(self):
        return self.get_options()