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
__model_name__ = 'rede.Rede'
import auth, base_models
from orm import *
from form import *

class Rede(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rede'
        self.__title__ = 'Redes de Distribuição'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'rede.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=60)
        self.contador = list_field(view_order=2, name ='Contadores', simple=True, show_footer=False, fields=['nome'], condition="rede='{id}'", model_name='contador.Contador', list_edit_mode='inline', onlist = False)# colspan=2,
        self.chafariz = list_field(view_order=3, name ='Chafarizes', simple=True, show_footer=False, fields=['nome'], condition="rede='{id}'", model_name='chafariz.Chafariz', list_edit_mode='inline', onlist = False)#colspan=2, 
        self.conduta = list_field(view_order=4, name ='Condutas', simple=True, show_footer=False, fields=['nome', 'rede', 'diametro', 'comprimento'], condition="rede='{id}'", model_name='conduta.Conduta', list_edit_mode='inline', onlist = False)#colspan=2, 
        self.furo = many2many(view_order=5, name ='Furos', condition="rede='{id}'", model_name='furo.Furo', onlist = False)#, colspan=2
        self.estacao_bombagem = many2many(view_order=6, name ='Estações', fields=['nome', 'localizacao'], condition="rede='{id}'", model_name='estacao_bombagem.EstacaoBombagem', onlist = False)#, colspan=2
        self.reservatorio = many2many(view_order=7, name ='Reservatórios', fields=['nome', 'localizacao'], condition="rede='{id}'", model_name='reservatorio.Reservatorio', onlist = False)#, colspan=2

