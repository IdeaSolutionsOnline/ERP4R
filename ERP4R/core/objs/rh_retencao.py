
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
__model_name__='rh_retencao.RHRetencao'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

class RHRetencao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_retencao'
        self.__title__= 'Taxas de Retenção'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__db_mode__ ='View'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.taxa_inps_func = percent_field(view_order = 1, name = 'Taxa INPS Funcionário', size = 70)
        self.conta_debito_inps_func = choice_field(view_order = 2, name = 'Conta Debito - INPS Funcionário', size = 90, onlist=False, model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_credito_inps_func = choice_field(view_order = 3, name = 'Conta Credito - INPS Funcionário', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")

        self.taxa_inps_entidade = percent_field(view_order = 4, name = 'Taxa INPS Entidade', size = 70)
        self.conta_debito_inps_entidade = choice_field(view_order = 5, name = 'Conta Debito - INPS Entidade', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_credito_inps_entidade = choice_field(view_order = 6, name = 'Conta Credito - INPS Entidade', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")     
        
        self.taxa_nao_residente = percent_field(view_order = 7, name = 'Taxa Funcionário Não Residente', size = 70)
        self.conta_debito_nao_residente = choice_field(view_order = 8, name = 'Conta Debito - Func. Não Residente', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_credito_nao_residente = choice_field(view_order = 9, name = 'Conta Credito - Func. Não Residente', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        
        self.taxa_prestacao_servico = percent_field(view_order = 10, name = 'Taxa Retenção Prest. Serviço', size = 70)
        self.conta_debito_prestacao_servico = choice_field(view_order = 11, name = 'Conta Debito - Prest. Serviço', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_credito_prestacao_servico = choice_field(view_order = 12, name = 'Conta Credito - Prest. Serviço', size = 90, onlist=False,  model = 'plano_contas', search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")


    def get_opts(self, get_str):
        return eval(get_str)