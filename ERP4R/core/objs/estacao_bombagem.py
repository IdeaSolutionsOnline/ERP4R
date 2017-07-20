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
__model_name__ = 'estacao_bombagem.EstacaoBombagem'
import auth, base_models
from orm import *
from form import *
try:
    from my_contador import Contador
except:
    from contador import Contador

class EstacaoBombagem(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'estacao_bombagem'
        self.__title__ = 'Estação de Bombagem'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'estacao_bombagem.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=80)
        self.localizacao = string_field(view_order=2, name ='Localizacao', size=80)
        self.contador_in = choice_field(view_order=3, name ='Cont.Entrada', size=80, model='contador', column='nome', options='model.get_contadores()')
        self.contador_out = choice_field(view_order=4, name ='Cont.saida', size=80, model='contador', column='nome', options='model.get_contadores()')
        self.rede = many2many(view_order=5, name ='Redes', fields=['nome'], condition="estacao_bombagem='{id}'", model_name='rede.Rede')#, colspan=2
        self.conduta = many2many(view_order=6, name ='Condutas', fields=['nome', 'rede', 'diametro', 'comprimento'], condition="estacao_bombagem='{id}'", model_name='conduta.Conduta')

    def get_contadores(self):
        return Contador().get_options()
