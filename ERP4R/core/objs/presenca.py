# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""ERP+"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'presenca.Presenca'
import base_models
from orm import *
from form import *

try:
    from my_turma import Turma
except:
    from turma import Turma


class Presenca(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'presenca'
        self.__title__ = 'Folha de Presença'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(presenca.numero) DESC'
        self.__workflow__ = (
            'estado', {
                'Rascunho': ['Confirmar', 'Inserir Formandos'],
                'Inserir Formandos': ['Confirmar'],
                'Confirmado': ['Imprimir', 'Cancelar'],
                'Cancelado': ['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar': ['All'],
            'Inserir Formandos':['All'],
            'Imprimir': ['All'],
            'Cancelar': ['All'],
            'Rascunho': ['All'],
            'full_access': ['All']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado', 'Cancelado'])
            ]
        self.__auth__ = {
            'read': ['All'],
            'write': ['All'],
            'create': ['All'],
            'delete': ['All'],
            'full_access': ['All']
            }
        self.__get_options__ = ['numero']

        self.numero = info_field(view_order=1, name='Número', args='readonly', size=30)
        self.estado = info_field(view_order=2, name='Estado', size=60, default='Rascunho')
        self.data = date_field(view_order=3, name='Data', args='required', default=datetime.date.today(), size=40)
        self.hora_inicial = time_field(view_order=4, name='Hora Inicial', size=60, args='required', default=time.strftime('%H:%M'))
        self.hora_final = time_field(view_order=5, name='Hora Final', size=60, args='required')
        self.turma = choice_field(view_order = 6, name = 'Turma', size = 80, model = 'turma', onlist = False, column = 'numero', options = "model.get_turma()")
        self.observacoes = text_field(view_order=7, name='Observações', size=100, args="rows=10", onlist=False, search=False)
        self.materias = text_field(view_order=8, name='Matérias', size=100, args="rows=10", onlist=False, search=False)
        self.linha_presenca = list_field(view_order=9, name='Presenças', condition="presenca='{id}'", model_name='linha_presenca.LinhaPresenca', list_edit_mode='inline', onlist=False)


    def get_turma(self):
        return Turma().get_turma()


    def Imprimir(self, key, window_id):
        template = 'presenca'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()


    def Inserir_Formandos(self,key,window_id):
        self.kargs = get_model_record(model=self, key=key)
        return form_edit(window_id=window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()


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