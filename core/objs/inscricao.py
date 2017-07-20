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
__model_name__='inscricao.Inscricao'
import base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro


class Inscricao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'inscricao'
        self.__title__= 'Fichas de Inscrição'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(inscricao.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar', 'Imprimir'], 'Confirmado':['Cancelar', 'Imprimir'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['All'],
            'Rascunho':['All'],
            'Imprimir':['All'],
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

        self.numero = string_field(view_order=1, name='Número', size=60)
        self.tac = choice_field(view_order=2, name='TAC', size=100, model='terceiro', column='nome', options='model.get_tac()')
        self.data = date_field(view_order=3, name='Data', size=60, args='required', default=datetime.date.today())
        self.estado = info_field(view_order=4, name='Estado', size=60, default='Rascunho')
        self.documento = list_field(view_order=5, name='Documentos', condition="inscricao='{id}'", model_name='documento.Documento', list_edit_mode='inline', onlist=False)


    def get_tac(self):
        return Terceiro().get_tac()


    def Imprimir(self, key, window_id):
        template = 'inscricao'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()


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
