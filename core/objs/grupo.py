# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+

Gestão de outras tarefas enquanto aglomerador de tarefas, no essencial tarefas pessoais

"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__='grupo.Grupo'
import auth, base_models
from orm import *
from form import *

class Grupo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'grupo'
        self.__title__= 'Grupos/Equipas'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'grupo.nome'
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

        self.nome = string_field(view_order=1, name='Nome', size=80)
        self.utilizadores = many2many(view_order = 2, name = 'Utilizadores', size = 200, model_name = 'users.Users', condition = "role='{id}'", fields = ['nome', 'login', 'email', 'estado'], onlist = False)


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
