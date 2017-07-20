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
__model_name__='linha_unidade.LinhaUnidade'
import auth, base_models
from orm import *
from form import *
try:
    from my_unidade import Unidade
except:
    from unidade import Unidade

class LinhaUnidade(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_unidade'
        self.__title__= 'Conversões'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['formula']

        self.unidade = parent_field(view_order=1, name ='Unidade', args='style:visibility="hidden"', model_name='unidade.Unidade', nolabel=True, onlist=False, column='nome')
        self.para_unidade = combo_field(view_order=2, name ='Unidade', args='required', size=60, model='unidade', column='nome', options='model.get_unidades()')
        self.formula = string_field(view_order=3, name ='Formula', size=60)

    def get_unidades(self):
        return Unidade().get_options()
