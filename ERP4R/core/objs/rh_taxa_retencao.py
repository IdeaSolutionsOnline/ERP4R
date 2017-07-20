
# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVTek'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek"
__status__ = "Development"
__model_name__ = 'rh_taxa_retencao.RHTaxaRetencao'
import auth, base_models
from orm import *
from form import *


class RHTaxaRetencao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_taxa_retencao'
        self.__title__ = 'Taxa de Retenção'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['taxa']
        self.__order_by__='taxa'



        self.minimo = currency_field(view_order = 1, size=70, name ='(De)Renumeração Mensal Minimo', args = 'required')

        self.maximo = currency_field(view_order = 2, size=70, name ='(A)Renumeração Mensal Maximo', args = 'required')
        
        self.taxa = percent_field(view_order = 3, name='Taxa', size=45, args = 'required')