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
__model_name__ = 'rendimento_funcionario.RendimentoFuncionario'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

from tipo_rendimento import TipoRendimento

class RendimentoFuncionario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rendimento_funcionario'
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
        self.__get_options__ = ['rendimento']

        self.terceiro = parent_field(view_order=1, name='Funcionário', size=250, onlist=False, model_name ='terceiro.Terceiro', column='nome')
        self.tipo_rendimento = combo_field(view_order = 2, name = 'Rendimento', size = 70, model = 'tipo_rendimento',args = 'required', column = 'Nome', options = "model.get_opts('TipoRendimento().get_options()')")
        self.em_subsidio = boolean_field(view_order=3,name='Em Subsídios?',size=280, default=True)
        self.valor = currency_field(view_order=4,name='Valor',size=60)
        
        #self.contrato_funcionario = parent_field(view_order=4,hidden=True, nolabel=True, onlist=False, model_name ='contrato_funcionario.ContratoFuncionario')

    
    def get_opts(self, get_str):
        return eval(get_str)