# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina', 'Abner Oliveira']
__credits__ = []
__version__ = "1.0"
__maintainer__ = ['António Anacleto', 'Jair Medina', 'Jair Medina', 'Abner Oliveira']
__status__ = "Development"
__model_name__ = 'sai_plano_conta.SaiPlanoConta'
#import auth, base_models
from orm import *
from form import *

class SaiPlanoConta(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sai_plano_conta'
        self.__title__ = 'Plano de Contas'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['codigo','nome']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'sai_plano_conta.codigo'
        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.codigo = string_field(view_order=1 , name='Código')
        self.nome = string_field(view_order=2 , name='Nome', size=150)
        #self.ascendente = choice_field(view_order=3 , name='Ascendente', size=80, model=self.__name__, column='nome', options='model.get_self()')
        self.tipo = combo_field(view_order=3 , name='Tipo', size=60, options=[('acumuladora','Acumuladora'),('dinheiro','Dinheiro'), ('credora','Credora'), ('devedora','Devedora'), ('receitas','Receitas'), ('gastos','Gastos'), ('resultados','Resultados'), ('compras','Compras'),('inventario','Inventário'), ('activos','Activos'), ('impostos','Impostos')])
        self.mapas = string_field(view_order=4, name='Mapas', size=100)