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
__model_name__ = 'rh_rendimento_funcionario.RHRendimentoFuncionario'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

from rh_tipo_rendimento import RHTipoRendimento

class RHRendimentoFuncionario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_rendimento_funcionario'
        self.__title__= 'Rendimento de Funcionarios'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['rh_tipo_rendimento']

        self.terceiro = parent_field(view_order=1, name='Funcionário', size=250, onlist=False, model_name ='terceiro.Terceiro', column='nome')
        self.rh_tipo_rendimento = combo_field(view_order = 2, name = 'Rendimento', size = 70, model = 'rh_tipo_rendimento',args = 'required', column = 'Nome', options = "model.get_opts('RHTipoRendimento().get_options()')")
        self.em_subsidio = boolean_field(view_order=3,name='Incluir em Subsídios?',size=280, default=True)
        self.valor = currency_field(view_order=4,name='Valor',size=60)
        
    
    def get_opts(self, get_str):
        return eval(get_str)