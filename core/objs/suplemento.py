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
__model_name__ = 'suplemento.Suplemento'
import auth, base_models
from orm import *
from form import *

class Suplemento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'suplemento'
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
        #self.__get_options__ = ['nome']


        self.terceiro = parent_field(view_order=1 , name='Terceiro', size=70,hidden=True, nolabel=True, onlist=False, model_name ='terceiro.Terceiro', column='nome')
        self.tipo = combo_field(view_order=2, name='Tipo Funcionario',size=70, default='A.1', options=[('A.1','Trabalhador Dependente'),('A.2','Pensionista'),('A.3','Trabalhador Isento'),('A.4','Não Residente')])
        self.rend_base = currency_field(view_order=3 , name='Rendimento Base', args='required', size=70)
        self.rend_acessorio = currency_field(view_order=4 , name='Rendimentos Acessórios', size=70)
        self.rend_isento = currency_field(view_order=5 , name='Rendimentos Isentos', size=70)
        self.rend_tributavel = function_field(view_order=6 , name='Rendimento Tributavel', size=70)
        self.pessoal_escritorio = boolean_field(view_order = 7, name = 'Funcionário de Escritório?', default = False)       
        



    def get_rend_tributavel(self, key):                     
        modelo = self.get(key=key)[0]
        soma = to_decimal(modelo['rend_base']) + to_decimal(modelo['rend_acessorio'])
        return int(soma)