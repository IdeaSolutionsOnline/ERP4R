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
__model_name__ = 'linha_caixa.LinhaCaixa'
import auth, base_models
from orm import *
from form import *
try:
    from my_metodo_pagamento import MetodoPagamento
except:
    from metodo_pagamento import MetodoPagamento
try:
    from my_tipo_documento import TipoDocumento
except:
    from tipo_documento import TipoDocumento
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class LinhaCaixa(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_caixa'
        self.__title__ = 'Linhas de Movimento de Caixa'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'linha_caixa.metodo'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['descricao']

        #aqui pode vir a ser interesante acrescentar hora e data de movimento
        self.caixa = parent_field(view_order = 1, name = 'Caixa', model_name = 'caixa.Caixa', onlist = False, search = False, column = 'numero')
        self.descricao = string_field(view_order = 2, name = 'Descrição', size = 60)
        self.documento = combo_field(view_order = 3, name = 'Documento', size = 40, args = 'required', column = 'nome', options = "model.get_opts('TipoDocumento')")
        self.num_doc = integer_field(view_order = 4, name = 'Número Documento', args = 'required', size = 20)
        self.terceiro = choice_field(view_order = 5, name = 'Terceiro', size = 40, model = 'terceiro', column = 'nome', options= "model.get_opts('Terceiro')")
        self.metodo = combo_field(view_order = 6, name = 'Metodo Pagamento', args = 'required', size = 40, model = 'metodo_pagamento', column = 'nome', options = "model.get_opts('MetodoPagamento')")
        self.valor_documento = currency_field(view_order = 7, name = 'Valor Documento', size = 15)
        self.entrada = currency_field(view_order = 8, name = 'Entrada', size = 15, sum = True)
        self.saida = currency_field(view_order = 9, name = 'Saida', size = 15, sum = True)

    def get_opts(self, model):
        return eval(model + '().get_options()')

