# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
Registo de actividades enquanto aglomerador de tarefas.
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'actividade.Actividade'
import auth, base_models
from orm import *
from form import *

class Actividade(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'actividade'
        self.__title__= 'Actividades'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'actividade.codigo'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar', 'Cancelar'], 'Confirmado':['Imprimir', 'Encerrar', 'Cancelar'], 'Encerrado':['Cancelar'], 'Cancelado':['Rascunho']}
            )#imprimir, gerar queixa, gerar denuncia, imprimir queixa, etc...
        self.__workflow_auth__ = {
            'Confirmar':['All'],
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
        self.__get_options__ = ['numero']

        self.codigo = info_field(view_order=1, name='Código', size=30)
        self.nome = string_field(view_order = 2, name = 'Nome', size = 80)
        self.data_inicial = date_field(view_order=3, name='Data Inicial', size=60, args='required', default=datetime.date.today())
        self.data_final = date_field(view_order=4, name='Data Final', size=60, args='required', default=datetime.date.today())
        self.estado = info_field(view_order=5, name='Estado', size=60, default='Rascunho')#finalizada, cancelada, activa, em execução, em aberto, prevista,
        self.descricao = text_field(view_order=6, name='Descrição', size=100, args="rows=20", onlist=False, search=False)
        self.notas = text_field(view_order=7, name='Descrição', size=100, args="rows=20", onlist=False, search=False)
        self.anexos = list_field(view_order = 8, name = 'Anexos', condition = "users='{id}'", model_name = 'anexo.Anexo', show_footer = False, list_edit_mode = 'inline', onlist = False)



    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('actividade')
        self.kargs['estado'] = 'Confirmado'
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
