# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+

Este Objecto comporta-se como uma tabela de ligação entre os contadores e os contrato, não nos podemos esquecer que um contrato pode ter varios contadores, mas só um activo e um contador pode ter varios contratos mas apenas um activo
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'contador_contrato.ContadorContrato'
import auth, base_models
from orm import *
from form import *
try:
    from my_contador import Contador
except:
    from contador import Contador

class ContadorContrato(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'contador_contrato'
        self.__title__ = 'Contadores/Contratos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['contador']
        self.contrato = parent_field(view_order=1 , name='Contrato', model_name='contrato.Contrato', column='numero')
        self.contador = choice_field(view_order=2 , name='Contador', size=80, model='contador', column='nome',  options='model.get_contador()')
        self.data_inicio = date_field(view_order=3 , name='Data inicio', args='required', default=datetime.date.today())
        self.data_fim = date_field(view_order=4 , name='Data Fim')
        self.estado = combo_field(view_order=5 , name='Estado', args='required', default='activo', options=[('activo','Activo'), ('desactivo','Desactivo')])

    def get_contador(self):
        return Contador().get_options()
