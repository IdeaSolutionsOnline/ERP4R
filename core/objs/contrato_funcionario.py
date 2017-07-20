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
__model_name__ = 'contrato_funcionario.ContratoFuncionario'
import auth, base_models
from orm import *
from form import *

class ContratoFuncionario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'contrato_funcionario'
        self.__title__= 'Contrato Funcionário'
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

        #self.__tabs__ = [('Rendimentos',['rendimento_funcionario']),('Descontos',['retencao_funcionario'])]


        self.terceiro = parent_field(view_order=1 , name='Funcionário', hidden=True, size=130, onlist=False, model_name ='terceiro.Terceiro', column='nome')
        self.salario_base = currency_field(view_order=2,name='Salário', size=120)
        self.activo = boolean_field(view_order=3,name='Activo?', size=120,default=True)
        self.tipo = combo_field(view_order=4, name='Tipo',size=95, default='Permanente', options=[('Prestacao Servico','Prestacao Servico'),('Temporario','Temporario'),('Permanente','Permanente')])
        self.data_inicio = date_field(view_order=5, name="Data Início", size=120, default=datetime.date.today())
        self.data_fim = date_field(view_order=6, name="Data Fim", size=120)
        #self.rendimento_funcionario=list_field(view_order = 7, condition = "contrato_funcionario = '{id}'", model_name = 'rendimento_funcionario.RendimentoFuncionario', list_edit_mode = 'popup', search=True, onlist = False)
        #self.retencao_funcionario=list_field(view_order = 8, condition = "contrato_funcionario = '{id}'", model_name = 'retencao_funcionario.RetencaoFuncionario', list_edit_mode = 'popup', search=False, onlist = False)