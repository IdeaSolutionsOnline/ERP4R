# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_atendimento.GAPAtendimento'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPAtendimento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_atendimento'
        self.__title__ ='Fluxos de Atendimento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'int8(gap_atendimento.ordem)'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , args = 'required', name='Nome', size=80)
        self.ordem = integer_field(view_order=2, args = 'required', name='Ordem', size=30)
        self.servico = combo_field(view_order = 3, name  = 'Serviço', size = 50, args = 'required', model = 'gap_servico', search = False, column = 'nome', options = "model.get_opts('GAPServico().get_options()')")

    #Apanha todos os Fluxos de Atendimento
    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

    #Apanha todos os Fluxos
    def get_fluxos(self):
        options = []
        opts = self.get(order_by='int8(gap_atendimento.ordem)')
        for f in get_model_fields(self):
            if f[0] == 'servico':
                field=f
        for option in opts:
                servico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                options.append(option['nome']+";"+servico)
        return options
