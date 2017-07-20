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
__model_name__ = 'chafariz.Chafariz'
import auth, base_models
from orm import *
from form import *
try:
    from my_rede import Rede
except:
    from rede import Rede
try:
    from my_contador import Contador
except:
    from contador import Contador

class Chafariz(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'chafariz'
        self.__title__ = 'Chafarizes'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'chafariz.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1 , name='Nome', size=80, args='required')
        self.localizacao = string_field(view_order=2 , name='Localização', size=80)
        self.tipo = combo_field(view_order=3 , name='Tipo', size=50, options=[('ligacao','Ligacao'),('autotanque','AutoTanque')])
        self.capacidade = decimal_field(view_order=4 , name='Capacidade M3', size=20)
        self.contador_in = choice_field(view_order=5 , name='Cont.Entrada', size=60, model='contador', column='nome', options="model.get_opts('Contador')")
        self.rede = choice_field(view_order=6 , name='Rede', size=60, model='rede', column='nome', options="model.get_opts('Rede')")
        self.contador_out = choice_field(view_order=7 , name='Cont.saida', size=60, model='contador', column='nome', options="model.get_opts('Contador')")
        self.conduta = list_field(view_order=8 , name='Condutas', fields=['nome', 'rede', 'diametro', 'comprimento'], condition="chafariz='{id}'", model_name='conduta.Conduta', show_footer=False, simple=True, list_edit_mode='inline')

    def get_opts(self, model):
        return eval(model + '().get_options()')

