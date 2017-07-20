# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+

Gestão de processos enquanto aglomerador de tarefas

"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__='processo.Processo'
import auth, base_models
from orm import *
from form import *

class Processo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'processo'
        self.__title__= 'Processos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'processo.codigo'
        self.__workflow__ = (
            'estado', {'Rascunho':['Activar'], 'Activo':['Encerrar', 'Cancelar'], 'Encerrado':['Cancelar'], 'Cancelado':['Rascunho']}
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
        self.__get_options__ = ['nome']

        self.codigo = info_field(view_order=1, name='Número', size=30)
        self.nome = string_field(view_order=2, name='Nome', size=80)
        self.estado = info_field(view_order=3, name='Estado', size=60, default='Rascunho')
        self.descricao = text_field(view_order=4, name='Descrição', size=100, args="rows=20", onlist=False, search=False)
        self.notas = text_field(view_order=5, name='Descrição', size=100, args="rows=20", onlist=False, search=False)
        self.grupos = many2many(view_order = 6, name = 'Utilizadores', size = 200, model_name = 'users.Users', condition = "role='{id}'", fields = ['nome', 'login', 'email', 'estado'], onlist = False)
        self.recursos = many2many(view_order = 7, name = 'Utilizadores', size = 200, model_name = 'users.Users', condition = "role='{id}'", fields = ['nome', 'login', 'email', 'estado'], onlist = False)
        self.anexos = list_field(view_order = 8, name = 'Anexos', condition = "users='{id}'", model_name = 'anexo.Anexo', show_footer = False, list_edit_mode = 'inline', onlist = False)


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
