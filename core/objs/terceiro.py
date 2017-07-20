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
__model_name__='terceiro.Terceiro'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas
try:
    from my_codigo_pais import CodigoPais
except:
    from codigo_pais import CodigoPais

class Terceiro(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'terceiro'
        self.__title__= 'Terceiros (Clientes, Fornecedores, etc...)'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'terceiro.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.__tabs__ = [('Identificação',['nome','nif','origem','estado','desconto','credito',
            'a_receber','a_pagar','cliente','fornecedor','funcionario','sujeito_iva','retencao']),
        ('Contactos',['contacto']),
        ('Contrato ao Funcionário',['rh_contrato_funcionario']),
        ('Rendimento do Funcionário',['rh_rendimento_funcionario']),
        ('Desconto do Funcionário',['rh_desconto_funcionario'])]

        self.nome = string_field(view_order = 1, name = 'Nome', args = 'autocomplete = "on"', size = 70)
        self.nif = string_field(view_order = 3, name = 'Nif', size = 70, onlist = False)
        self.origem = combo_field(view_order = 2, name = 'Origem', size = 70, model = 'codigo_pais',args = 'required', column = 'codigo', default='CV', options = "model.get_opts('CodigoPais().get_options_buyable()')")
        self.estado = combo_field(view_order = 4, name = 'Estado', size = 70, default = 'activo', options = [('activo','Activo'), ('cancelado','Cancelado')])
        self.desconto = percent_field(view_order = 5, name = 'Desconto', size = 70)
        self.credito = currency_field(view_order = 6, name = 'Crédito', size = 70)
        self.a_receber = choice_field(view_order = 7, name = 'A Receber', size = 70, model = 'plano_contas', onlist = False, column = 'codigo nome', options = "model.get_plano_contas('devedora')")
        self.a_pagar = choice_field(view_order = 8, name = 'A Pagar', size = 70, model = 'plano_contas', onlist = False, column = 'codigo nome', options = "model.get_plano_contas('credora')")
        self.cliente = boolean_field(view_order = 9, name = 'Cliente?', default = True)
        self.fornecedor = boolean_field(view_order = 10, name = 'Fornecedor?', size = 60, default = False)
        self.funcionario = boolean_field(view_order = 11, name = 'Funcionário?', size = 60, default = False)
        self.sujeito_iva = boolean_field(view_order = 12, name = 'Sujeito a IVA?', size = 60, default = True, onlist = False)
        self.retencao = boolean_field(view_order = 13, name = 'Retenção Na Fonte?', size = 60, default = False, onlist = False)
        self.contacto = list_field(view_order = 14, condition = "terceiro = '{id}'", model_name = 'contacto.Contacto', list_edit_mode = 'edit', onlist = False)
        self.rh_contrato_funcionario = list_field(view_order = 15, condition = "terceiro = '{id}'", model_name = 'rh_contrato_funcionario.RHContratoFuncionario', list_edit_mode = 'inline', onlist = False)
        self.rh_rendimento_funcionario = list_field(size=200, view_order = 16, condition = "terceiro = '{id}'", model_name = 'rh_rendimento_funcionario.RHRendimentoFuncionario', list_edit_mode = 'inline', onlist = False)        
        self.rh_desconto_funcionario=list_field(size=200, view_order = 17, condition = "terceiro = '{id}'", model_name = 'rh_desconto_funcionario.RHDescontoFuncionario', list_edit_mode = 'inline', onlist = False)


    def get_opts(self, get_str):
        return eval(get_str)


    def get_plano_contas(self, tipo):
        return eval('PlanoContas().get_' + tipo + '()')


    def get_clientes(self):
        #print ('im in get_clientes')
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['cliente']:
                    #yield (str(option['id']), option['nome'])
                    options.append((str(option['id']), option['nome']))
            #print (options)
            return options
        return erp_cache.get(key=self.__model_name__ + '_clientes', createfunc=get_results)


    def get_fornecedores(self):
        #print('Im in get_fornecedores de terceiro')
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                #print(option)
                if option['fornecedor']:
                    #yield (str(option['id']), option['nome'])
                    options.append((str(option['id']), option['nome']))
            #print (options)
            return options
        return erp_cache.get(key=self.__model_name__ + '_fornecedores', createfunc=get_results)


    def get_funcionarios(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['funcionario']:
                    #yield (str(option['id']), option['nome'])
                    options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_funcionarios', createfunc=get_results)

