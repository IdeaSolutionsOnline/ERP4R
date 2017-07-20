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
__model_name__ = 'periodo.Periodo'
import auth, base_models
from orm import *
from form import *
try:
    from my_ano_fiscal import AnoFiscal
except:
    from ano_fiscal import AnoFiscal

class Periodo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'periodo'
        self.__title__ = 'Periodos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'periodo.data_inicial'
        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Contabilista'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=50)
        self.tipo = combo_field(view_order=2, name ='Tipo', size=40, options=[('normal','Normal'), ('abertura','Abertura'), ('apuramento','Apuramento'), ('encerramento','Encerramento')])
        self.ano_fiscal = combo_field(view_order=3, name ='Ano Fiscal', size=40, model='ano_fiscal', options='model.get_anos_fiscais()', column='nome')
        self.data_inicial = date_field(view_order=4, name ='Data Inicial')
        self.data_final = date_field(view_order=5, name ='Data Final')

    def get_anos_fiscais(self):
        return AnoFiscal().get_options()

    def get_periodo(self, data):
        #print('im in get_periodo')
        periodo = None
        periodos = self.get()
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(data)) in lista_datas:
                periodo = p['id']
        #print('o periodo encontrado pelo get_periodo e', periodo, type(periodo))
        return str(periodo)
