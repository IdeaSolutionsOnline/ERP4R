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
__model_name__='turma.Turma'
#import base_models
from orm import *
from form import *

class Turma(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'turma'
        self.__title__= 'Turmas'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(turma.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Activar', 'Imprimir'], 'Activo':['Encerrar', 'Imprimir'], 'Encerrado':['Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Activar':['All'],
            'Encerrar':['All'],
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
            ('estado', ['Encerrado','Cancelado'])
            ]
        self.__get_options__ = ['numero']

        self.numero = string_field(view_order=1, name='Numero', size=60)
        self.estado = info_field(view_order=2, name='Estado', size=60, default='Rascunho')
        self.data_inicial = date_field(view_order=3, name='Data Inicial', size=60, args='required', default=datetime.date.today())
        self.data_final = date_field(view_order=4, name='Data Inicial', size=60, args='required')
        self.upload = upload_field(view_order = 5, name = 'Documento', size = 100)
        self.tac = list_field(view_order=6, name='TACs', condition="turma='{id}'", model_name='terceiro.Terceiro', list_edit_mode='inline', onlist=False)

    def get_turma(self):
        #print ('im in get_turma')
        def get_results():
            options = []
            opts = self.get(order_by='numero')
            for option in opts:
                options.append((str(option['id']), option['numero']))
            return options
        return erp_cache.get(key=self.__model_name__, createfunc=get_results)


    def Imprimir(self, key, window_id):
        template = 'turma'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()

    def Activar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Activo'
        self.put()
        return form_edit(window_id=window_id).show()

    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Encerrar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Encerrado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()
