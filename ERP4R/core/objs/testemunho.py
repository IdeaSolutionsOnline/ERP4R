# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Gestão de Testemunhos

"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'testemunho.Testemunho'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class Testemunho(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'testemunho'
        self.__title__ = 'Testemunhos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'testemunho.testemunha'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar', 'Cancelar'], 'Confirmado':['Imprimir', 'Cancelar'], 'Cancelado':['Rascunho']}
            )#imprimir, gerar queixa, gerar denuncia, imprimir queixa, etc...
        self.__workflow_auth__ = {
            'Imprimir':['Agente'],
            'Confirmar':['Agente'],
            'Rascunho':['Comandante'],
            'Cancelar':['Chefe'],
            'full_access':['Comandante']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }
        #self.__get_options__ = ['testemunha']

        self.ocorrencia = parent_field(view_order = 1, name = 'Ocorrencia', args = 'style:visibility="hidden"', model_name = 'ocorrencia.Ocorrencia', nolabel = True, onlist = False, column = 'numero')
        self.terceiro = choice_field(view_order = 2, name = 'Testemunha', size = 80, model = 'terceiro', column = 'nome', options = "model.get_terceiros()")
        self.estado = info_field(view_order = 3, name = 'Estado', size = 60, default = 'Rascunho')
        self.descricao = text_field(view_order = 4, name = 'Descrição', args = 'rows=20', size = 100, colspan = 3)

    def get_terceiros(self):
        return Terceiro().get_options()

    def Imprimir(self, key, window_id):
        template = 'testemunho'
        record = get_records_to_print(key = key, model = self)
        return Report(record = record, report_template = template).show()

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()
