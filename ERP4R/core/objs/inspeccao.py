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
__model_name__ = 'inspeccao.Inspeccao'
import auth, base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class Inspeccao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'inspeccao'
        self.__title__ = 'Inspecções'
        self.__model_name__ = __model_name__
        self.__auth__ = {
            'read':['All'],
            'write':['Inspector'],
            'create':['inspector'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['contrato']

        self.contrato = parent_field(view_order=1, name='Contrato', args='hidden', nolabel=True, onlist=False, model_name='contrato.Contrato', column='numero')
        self.data = date_field(view_order=2, name ='Data', default=datetime.date.today())
        self.inspector = combo_field(view_order=3, name ='Inspector', args='required tabIndex="-1"', size=55, model='terceiro', column='nome', options='model.get_terceiros()')
        self.notas = string_field(view_order=4, name ='Notas', args='autocomplete="on"', size=60, onlist=False)
        self.resultado = combo_field(view_order=5, name ='Resultado', args='required tabIndex="-1"', size=55, options=[('aprovado','Aprovado'), ('recusado','Recusado')])

    def get_terceiros(self):
        return Terceiro().get_funcionarios()
