# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Gestão de Esquadras e Postos Policiais bem como dos próprios comandos

"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'esquadra.Esquadra'
import auth, base_models
from orm import *
from form import *

class Esquadra(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'esquadra'
        self.__title__ = 'Esquadras e Postos Policiais'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'esquadra.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name ='Nome', size=60)
        self.localizacao = string_field(view_order=2, name ='Localização', size=60)
        self.telefone = string_field(view_order=3, name ='Telefone', size=30)
        self.tipo = combo_field(view_order=4, name ='Tipo', size=40, options=[('esquadra','Esquadra'), ('posto','Posto Policial'), ('comando','Comando'), ('unidade','Unidade')])
        self.users = many2many(view_order=5, name ='Funcionários', condition="esquadra='{id}'", model_name='users.Users')

    def get_esquadra(self, user_id):
        options = []
        sql = """
        SELECT e.id AS id, e.nome AS nome FROM esquadra AS e
        JOIN esquadra_users AS eu
        ON eu.esquadra = e.id
        JOIN users AS u
        ON eu.users = u.id
        where u.id = '{user_id}'
        """.format(user_id=user_id)
        opts = run_sql(sql)
        for option in opts:
            options.append((str(option['id']), option['nome']))
        return options

