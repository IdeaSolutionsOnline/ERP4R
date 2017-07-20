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
__model_name__='gap_terceiro.GAPTerceiro'
import auth, base_models
from orm import *
from form import *

class GAPTerceiro(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_terceiro'
        self.__title__= 'Terceiros'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'terceiro.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order = 1, name = 'Nome', args = 'autocomplete = "on"', size = 80)
        self.nif = string_field(view_order = 2, name = 'Nif', size = 40, onlist = False)
        self.estado = combo_field(view_order = 3, name = 'Estado', size = 40, default = 'activo', options = [('activo','Activo'), ('cancelado','Cancelado')])
        #self.desconto = percent_field(view_order = 4, name = 'Desconto', size = 50)
        #self.credito = currency_field(view_order = 5, name = 'Crédito', size = 50)
        #self.a_receber = choice_field(view_order = 6, name = 'A Receber', size = 80, model = 'plano_contas', onlist = False, column = 'codigo nome', options = "model.get_plano_contas('devedora')")
        #self.a_pagar = choice_field(view_order = 7, name = 'A Pagar', size = 80, model = 'plano_contas', onlist = False, column = 'codigo nome', options = "model.get_plano_contas('credora')")
        self.cliente = boolean_field(view_order = 8, name = 'Cliente?', default = True)
        #self.fornecedor = boolean_field(view_order = 9, name = 'Fornecedor?', default = False)
        self.funcionario = boolean_field(view_order = 10, name = 'Funcionário?', default = False)
        #self.sujeito_iva = boolean_field(view_order = 11, name = 'Sujeito a IVA?', size = 50, default = True, onlist = False)
        #self.contacto = list_field(view_order = 12, name = 'Contactos', condition = "terceiro = '{id}'", model_name = 'contacto.Contacto', list_edit_mode = 'popup', onlist = False)
    '''
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

    '''
