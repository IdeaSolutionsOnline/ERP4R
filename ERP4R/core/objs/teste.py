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
__model_name__='teste.Teste'
import base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro


class Teste(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'teste'
        self.__title__= 'Testes de Avaliação'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(teste.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['All'],
            'Rascunho':['All'],
            'Cancelar':['All'],
            'full_access':['All']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Cancelado'])
            ]
        self.__get_options__ = ['numero']

        self.numero = info_field(view_order=1, name='Número', args='readonly', size=30)
        self.data = date_field(view_order=2, name='Data', size=60, args='required', default=datetime.date.today())
        self.tac = choice_field(view_order=3 , name='TAC', size=60, model='terceiro', column='nome', options='model.get_tac()')
        self.nota = decimal_field(view_order=4, name='Avaliação', size=20, sum=True, default=to_decimal(1))
        self.observacoes = text_field(view_order=5, name='Observações', size=100, args="rows=5", onlist=False, search=False)
        self.teste = image_field(view_order=6, name = 'Teste', size = 100, onlist = False)
        self.estado = info_field(view_order=7, name='Estado', size=60, default='Rascunho')


    def get_tac(self):
        return Terceiro().get_tac()


    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id=window_id).show()


    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()


    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()
