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
__model_name__='funcionario_subsidio.FuncionarioSubsidio'
import auth, base_models
from orm import *
from form import *


class FuncionarioSubsidio(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'funcionario_subsidio'
        self.__title__= 'Subsídios Funcionarios'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['terceiro']     
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }       
        
        self.salario = parent_field(view_order=1 , name='Salario', size=150,hidden=False, nolabel=True, onlist=True, model_name ='salario.Salario', column='periodo')
        self.terceiro = combo_field(view_order=2, args='required', size=70, model='terceiro', column='nome', options='model.get_funcionarios()')
        
        

    def get_funcionarios(self):
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        return Terceiro().get_funcionarios()