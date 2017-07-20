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
__model_name__ = 'lista_precos.ListaPrecos'
import auth, base_models
from orm import *
from form import *
try:
    from my_terminal import Terminal
except:
    from terminal import Terminal

class ListaPrecos(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'lista_precos'
        self.__title__ = 'Listas de Preços'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Cancelar':['Gestor'],
            'Rascunho':['Gestor'],
            'full_access':['Gestor']
            }

        self.__no_edit__ = [
            ('estado', ['Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', args='autocomplete="on"', size=60)
        self.terminal = combo_field(view_order=2, name ='Terminal', args='required tabIndex="-1"', size=55, model='terminal', column='name', options='model.get_terminais()')
        self.data_inicial = date_field(view_order=3, name ='Data Inicial', args='required ', default=datetime.date.today())
        self.data_final = date_field(view_order=4, name ='Data Final', args='required ')
        self.estado = info_field(view_order=5, name ='Estado')
        self.linha_lista_precos = list_field(view_order=6, name ='Linhas de Lista de Preços', condition="lista_precos='{id}'", model_name='linha_lista_precos.LinhaListaPrecos', list_edit_mode='inline', onlist = False)

    def get_terminais(self):
        return Terminal().get_options()

    def Confirmar(self, key=None):
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Confirmado'
        ListaPrecos(**record).put()
        return form_edit(key = key, window_id = window_id)

    def cancelar(self, key, window_id):
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Cancelado'
        ListaPrecos(**record).put()
        return form_edit(key = key, window_id = window_id)

    def rascunho(self, key, window_id):
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Rascunho'
        ListaPrecos(**record).put()
        return form_edit(key = key, window_id = window_id)
