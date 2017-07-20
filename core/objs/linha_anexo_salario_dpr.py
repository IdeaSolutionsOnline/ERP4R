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
__model_name__ = 'linha_anexo_salario_dpr.LinhaAnexoSalarioDPR'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class LinhaAnexoSalarioDPR(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_anexo_salario_dpr'
        self.__title__ = 'Linhas Anexo Salario'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['designacao']


        self.designacao = string_field(view_order=2, name ='Nome', size=45, args = 'required,readonly', onlist=True) 

        self.nif = string_field(view_order=3, name ='Nif', args = 'required,readonly', onlist=True)               

        self.periodo = string_field(view_order = 4, size=30, name ='Periodo', args = 'required,readonly')     
        
        self.base = currency_field(view_order=5, name ='Rend. Base', args = 'required,readonly',size=20, onlist=True, sum=True)        
       
        self.aces = currency_field(view_order=6, name ='Rend. Acessório', onlist=True,args = 'required,readonly', sum=True)

        self.isento = currency_field(view_order=7, name ='Rend. Isento', size=30, onlist=True,args = 'required,readonly', sum=True)

        self.trib = currency_field(view_order=8, name ='Rend. Tributavel', size=30, args = 'required,readonly', sum=True)
        
        self.tipologia = string_field(view_order=9, name ='Categoria', args = 'required,readonly')

        self.ir_teu = currency_field(view_order=10, name ='Valor Retido', args = 'required,readonly', size=20, sum=True)
        
        self.inps = currency_field(view_order=11, name ='Valor INPS', args = 'required,readonly', size=20, sum=True)        

        self.outros = currency_field(view_order=12, name ='Outras Retenções', args = 'required,readonly', size=20, sum=True)

        self.tp_oper = string_field(view_order=14, name ='Tipo Operação',args = 'required,readonly')

        self.anexo_salario_dpr = parent_field(view_order = 15, name = 'Anexo Salário DPR', hidden=True, model_name = 'anexo_salario_dpr.AnexoSalarioDPR',nolabel=True, onlist = False, column = 'id')

