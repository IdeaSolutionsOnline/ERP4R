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
__model_name__= 'sai_rest_iur_global.SaiRestIURGlobal'
import auth, base_models
from orm import *
from form import *

class SaiRestIURGlobal(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sai_rest_iur_global'
        self.__title__= 'Restituição de IUR, Lista Global'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'sai_rest_iur_global.nome_sigof'
        self.__auth__ = {
            'read':['All'],
            'write':['Técnico Tesouro', 'Gestor Tesouro','Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }
        self.__get_options__ = ['cabimento']

        self.ano_referencia = info_field(view_order=1, name='Ano Referência', size=60, search=True)
        self.ano_cabimento = info_field(view_order=2, name='Ano Cabimento', size=60, onlist=False)
        self.conh_fixacao = info_field(view_order=3, name='Conh.Fixação', size=60, onlist=False)
        self.estado = info_field(view_order=4, name='Estado GRE', size=60)
        self.liquidacao = info_field(view_order=5, name='Liquidação', size=60)
        self.cabimento_sigof = info_field(view_order=6, name='Cab. Sigof', size=60)
        self.cabimento_gre = info_field(view_order=7, name='Cab. Gre', size=60, onlist=False)
        self.nome_sigof = info_field(view_order=8, name='Nome Sigof', size=100, onlist=False)
        self.nome_gre = info_field(view_order=9, name='Nome Gre', size=100)
        self.nif_sigof = info_field(view_order=10, name='NIF Sigof', size=60, onlist=False)
        self.nif_gre = info_field(view_order=11, name='NIF GRE', size=60)
        self.valor_bruto = info_field(view_order=12, name='Valor Imposto', size=60, onlist=False)
        self.credito = info_field(view_order=13, name='Crédito', size=60, onlist=False)
        self.valor_a_pagar = info_field(view_order=14, name='V. A Pagar', size=60)
        self.valor_cabimento = info_field(view_order=15, name='V. Cabimento', size=60, onlist=False)
        self.valor_pago = info_field(view_order=16, name='V. Pago', size=60)
        self.nib_sigof = info_field(view_order=17, name='NIB Sigof', size=60, onlist=False)
        self.nib_gre = info_field(view_order=18, name='NIB Gre', size=60, onlist=False)
        self.data_compensacao = info_field(view_order=19, name='Data Compensação', size=60, onlist=False)
