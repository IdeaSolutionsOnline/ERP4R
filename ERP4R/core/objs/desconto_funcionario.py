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
__model_name__ = 'desconto_funcionario.DescontoFuncionario'
import auth, base_models
from orm import *
from form import *

from tipo_desconto import TipoDesconto

class DescontoFuncionario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'desconto_funcionario'
        self.__title__= 'Descontos ao Funcionario'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['tipo_desconto']


        self.terceiro = parent_field(view_order=1 , name='Funcionário', size=280, onlist=False, model_name ='terceiro.Terceiro', column='nome')
        self.tipo_desconto = combo_field(view_order = 2, name = 'Desconto', size = 70, model = 'tipo_desconto',args = 'required', column = 'Nome', options = "model.get_opts('TipoDesconto().get_options()')")
        self.em_subsidio = boolean_field(view_order=3,name='Em Subsídios?',size=280, default=True)
        self.valor = currency_field(view_order=4,name='Valor',size=70)
        
        

        #self.contrato_funcionario = parent_field(view_order=4, size=70,hidden=True, nolabel=True, onlist=False, model_name ='contrato_funcionario.ContratoFuncionario')
        
    def get_opts(self, get_str):
        return eval(get_str)