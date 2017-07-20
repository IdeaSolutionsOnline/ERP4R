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
__model_name__ = 'linha_presenca.LinhaPresenca'
#import base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro


class LinhaPresenca(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_presenca'
        self.__title__ = 'Presenças'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['tac']

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }

        self.presenca = parent_field(view_order=1, name ='Presenca', args='style:visibility="hidden"', model_name='presenca.Presenca', nolabel=True, onlist=False, column='numero')
        self.tac = choice_field(view_order=2 , name='TAC', size=100, model='terceiro', column='nome', options='model.get_tac()')
        self.observacoes = text_field(view_order=3, name='Observações', size=100, args="rows=10", onlist=False, search=False)


    def get_tac(self):
        return Terceiro().get_tac()


