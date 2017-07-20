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
__model_name__ = 'security_log.SecurityLog'
import auth, base_models
from orm import *
from form import *
try:
    from my_terminal import Terminal
except:
    from terminal import Terminal

class SecurityLog(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'security_log'
        self.__title__ = 'Log de Segurança'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'security_log.date, security_log.time'
        self.__auth__ = {
            'read':['all'],
            'write':['all'],
            'create':['all'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['name']

        self.name = string_field(view_order=1, name ='Nome', size=80)
        self.event = string_field(view_order=2, name ='Evento', size=80)
        self.description = string_field(view_order=3, name ='Descrição', size=200)
        self.terminal = combo_field(view_order=4, name ='Posto', args='required', model='terminal', column='name', options='model.get_terminais()')
        self.date = date_field(view_order=5, name ='Data', args='required', default=datetime.date.today())
        self.time = time_field(view_order=6, name ='Hora', args='required', default=time.strftime('%H:%M:%S'))

    def get_terminais(self):
        return Terminal().get_options()
