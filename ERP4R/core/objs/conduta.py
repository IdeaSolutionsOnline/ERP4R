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
__model_name__='conduta.Conduta'
import auth, base_models
from orm import *
from form import *
try:
    from my_rede import Rede
except:
    from rede import Rede
try:
    from my_furo import Furo
except:
    from furo import Furo
try:
    from my_chafariz import Chafariz
except:
    from chafariz import Chafariz
try:
    from my_contador import Contador
except:
    from contador import Contador

class Conduta(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'conduta'
        self.__title__= 'Condutas de Água'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name='Nome', size=60)
        self.diametro = decimal_field(view_order=2, name='Diametro(cm)', size=20)
        self.comprimento = decimal_field(view_order=3, name='Comprimento(m)', size=20)
        self.rede = choice_field(view_order=4, name='Rede', size=80, model='rede', column='nome', options="model.get_opt('Rede')")
        self.furo = choice_field(view_order=5, name='Furo', size=80, model='furo', column='nome', options="model.get_opt('Furo')")
        self.chafariz = choice_field(view_order=6, name='Chafariz', size=80, model='chafariz', column='nome', options="model.get_opt('Chafariz')")
        self.contador = choice_field(view_order=7, name='Contador', size=80, model='contador', column='nome', options="model.get_opt('Contador')")
        self.reservatorio = many2many(view_order=8, name='Reservatórios', fields=['nome'], model_name='reservatorio.Reservatorio', condition="conduta='{id}'")#, colspan=2
        self.estacao_bombagem = many2many(view_order=9, name='Estações de Bombagem', fields=['nome'], condition="conduta='{id}'", model_name='estacao_bombagem.EstacaoBombagem')#colspan=2, 

    def get_opt(self, model):
        return eval(model + '().get_options()')
