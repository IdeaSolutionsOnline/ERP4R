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
__model_name__='linha_lista_precos.LinhaListaPrecos'
import auth, base_models
from orm import *
from form import *
try:
    from my_produto import Produto
except:
    from produto import Produto
try:
    from my_unidade import Unidade
except:
    from unidade import Unidade

class LinhaListaPrecos(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_lista_precos'
        self.__title__= 'Linhas de Lista de Preços'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['produto']

        self.lista_precos = parent_field(view_order=1, name ='Lista de Preços', args='style:visibility="hidden"', model_name='lista_precos.ListaPrecos', nolabel=True, onlist=False, column='numero')#este args tem que desa+arecer ponho só hidden e converto no widget
        self.produto = choice_field(view_order=2, name ='Produto', args='required tabIndex="-1"', size=55, model='produto', column='nome', options="model.get_opts('Produto', '_sellable()')")
        self.categoria = string_field(view_order=3, name ='Categoria', args='tabIndex="-2"', size=55)
        self.quant_min = decimal_field(view_order=4, name ='Quant.Minima', default=0)
        self.quant_max = decimal_field(view_order=5, name ='Quant.Máxima', default=0)
        self.unidade = combo_field(view_order=6, name ='Unid.Venda', args='required tabIndex="-1"', model='unidade', column='nome', options="model.get_opts('Unidade','()')")
        self.preco = decimal_field(view_order=7, name ='Preço')

    def get_opts(self, model, tipo):
        return eval(model + '().get_options' + tipo)
