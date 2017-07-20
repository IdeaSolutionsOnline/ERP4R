# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina', 'Abner Oliveira']
__credits__ = []
__version__ = "1.0"
__maintainer__ =  ['António Anacleto', 'Jair Medina', 'Jair Medina', 'Abner Oliveira']
__status__ = "Development"
__model_name__= 'mapa_gestao.MapaGestao'
#import base_models#auth,
from orm import *
from form import *


class MapaGestao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'mapa_gestao'
        self.__title__= 'Mapa Gestão'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__workflow__ = (
            'estado', {'Rascunho':['Imprimir', 'Valores0', 'Imp.Excel', 'Imp.Primavera', 'Imp.PHC'], 'Confirmado':['Imprimir']}
            )
        self.__workflow_auth__ = {
            'Imprimir':['All'],
            'Valores0':['All'],
            'Imp.Excel':['All'],
            'Imp.PHC':['All'],
            'Imp.Primavera':['All'],
            'Rascunho':['Gestor'],
           }
           


        self.nif = string_field(view_order=1, name='Nif', size=80)
        self.ano_fiscal = string_field(view_order=2, name='Ano Fiscal', size=5)
        self.estado = info_field(view_order=3, name ='Estado', default='Rascunho', onlist=False, hidden=True, nolabel=True,)
        self.mapa = combo_field(view_order=4, name ='Mapa', options=[('balancete','Balancete'), ('balanco','Balanço'), ('demonst_resul','Demonstração de Resultado'), ('fluxoCaixa','Fluxo de Caixa')], onlist=False, default='Praia')
        self.linha_mapa_gestao = list_field(view_order = 5, name = 'Valores', model_name = 'linha_mapa_gestao.LinhaMapaGestao', condition = "factura_cli='{id}'", list_edit_mode = 'inline', onlist = False)


    












