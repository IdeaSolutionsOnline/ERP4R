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
__model_name__ = 'outros_descontos_funcionario.OutrosDescontosFuncionario'
import auth, base_models
from orm import *
from form import *

from tipo_desconto import TipoDesconto

class OutrosDescontosFuncionario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'outros_descontos_funcionario'
        self.__title__= 'Outros Descontos ao Funcionario'
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


        self.terceiro = combo_field(view_order=1 , name='Funcionário', size=70, onlist=True, options='model.get_funcionarios()')
        self.tipo_desconto = combo_field(view_order = 2, name = 'Desconto', size = 70, model = 'tipo_desconto',args = 'required', column = 'Nome', options = "model.get_opts('TipoDesconto().get_options()')")
        self.valor = currency_field(view_order=3,name='Valor',size=70)
        self.salario = parent_field(view_order=4 , name='Salario', size=50,onlist=False, model_name ='salario.Salario', column ='periodo')
        
    def get_opts(self, get_str):
        return eval(get_str)
    def get_funcionarios(self):
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        return Terceiro().get_funcionarios()