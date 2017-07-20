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
__model_name__='certificacao.Certificacao'
#import base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro


class Certificacao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'certificacao'
        self.__title__= 'Certificações'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(certificacao.numero) DESC'
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

        self.numero = info_field(view_order=1, name='Número', size=60)
        self.estado = info_field(view_order=2, name='Estado', size=60, default='Rascunho')
        self.tac = choice_field(view_order=3 , name='TAC', size=100, model='terceiro', column='nome', options='model.get_tac()')
        self.data = date_field(view_order=4, name='Data', size=60, args='required', default=datetime.date.today())
        self.nota_final = function_field(view_order=5, name = 'Nota Final', size = 20, sum = True, search = False)
        self.presencas = function_field(view_order=6, name = '% de Presenças', size = 20, sum = True, search = False)
        self.certificado = image_field(view_order=7, name = 'Certificado', size = 100, onlist = False)
        self.avaliacao = text_field(view_order=8, name='Avaliação', size=100, args="rows=5", onlist=False, search=False)
        self.observacoes = text_field(view_order=9, name='Observações', size=100, args="rows=5", onlist=False, search=False)
        self.notas = list_field(view_order=10, name='Notas de Avaliação', model_name='teste.Teste', condition="tac='{tac}'", list_edit_mode='popup')


    def get_tac(self):
        return Terceiro().get_tac()


    def Imprimir(self, key, window_id):
        template = 'certificacao'
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
