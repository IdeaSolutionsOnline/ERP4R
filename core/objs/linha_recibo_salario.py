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
__model_name__ = 'linha_recibo_salario.LinhaReciboSalario'
import auth, base_models
from orm import *
from form import *


class LinhaReciboSalario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_recibo_salario'
        self.__title__= 'Linha Recibo Salário'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__='valor desc'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.recibo_salario = parent_field(view_order=1 , name='Recibo', onlist=False, model_name ='recibo_salario.ReciboSalario')
        self.tipo_rendimento = parent_field(view_order=2 , hidden=True, onlist=False, model_name ='tipo_rendimento.TipoRendimento', column='nome')
        self.tipo_desconto = parent_field(view_order=3 , hidden=True, onlist=False, model_name ='tipo_desconto.TipoDesconto', column='nome')
        self.nome = string_field(view_order=4,name='Descrição',size=70)
        self.valor = currency_field(view_order=5,name='Valor',size=70, sum=True)
        
        
