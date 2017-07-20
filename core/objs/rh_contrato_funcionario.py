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
__model_name__ = 'rh_contrato_funcionario.RHContratoFuncionario'
import auth, base_models
from orm import *
from form import *

class RHContratoFuncionario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_contrato_funcionario'
        self.__title__= 'Contrato do Funcionário'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        
        self.terceiro = parent_field(view_order=1 , name='Funcionário', size=120,onlist=True, model_name ='terceiro.Terceiro', column='nome')
        self.salario_base = currency_field(view_order=2,name='Salário', size=120)
        self.activo = boolean_field(view_order=3,name='Activo?', size=120,default=True)
        self.tipo = combo_field(view_order=4, name='Tipo',size=120, default='dependente', options=[('dependente','Trabalhador Dependente'),('pensionista','Pensionista'),('isento','Trabalhador Isento'),('nao_residente','Não Residente')])
        self.vinculo = combo_field(view_order=5, name='Vínculo',size=120, default='efectivo', options=[('efectivo','Efectivo'),('prestacao_servico','Prestação Serviço'),('a_termo','A Termo')])
        self.data_inicio = date_field(view_order=6, name="Data Início", size=130, default=datetime.date.today())        
        self.data_fim = date_field(view_order=7, name="Data Fim", size=120)
        self.documento = image_field(view_order=8,name='Documento')
        