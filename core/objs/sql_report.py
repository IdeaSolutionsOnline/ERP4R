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
__model_name__ = 'sql_report.SQLReport'
import auth, base_models
from orm import *
from form import *

class SQLReport(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sql_report'
        self.__title__ = 'Reports Personalizados SQL'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'sql_report.name'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor Tesouro','Técnico DNRE','Gestor DNRE','Gestor de Formação','Formador'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar', 'Imprimir', 'Exportar'], 'Confirmado':['Alterar', 'Imprimir', 'Exportar']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Alterar':['Gestor'],
            'Imprimir':['All'],
            'Exportar':['All'],
            'full_access':['Gestor']
            }


        # self.__no_edit__ = [
        #     ('estado', ['Confirmado'])
        #     ]

        self.__get_options__ = ['name']

        self.name = string_field(view_order=1 , name='Nome', size=100)
        self.title = string_field(view_order=2 , name='Titulo', size=100)
        self.estado = info_field(view_order=3, name='Estado', size=40, default='Rascunho', dynamic_atrs = 'estado_dynamic_atrs', onlist=False)
        self.linha_sql_report = list_field(view_order=4, name='Variaveis', condition="sql_report='{id}'", model_name='linha_sql_report.LinhaSQLReport', list_edit_mode='inline', onlist = False)
        self.totais = string_field(view_order=5, name='Totais', size=150, onlist=False)
        self.ordem_dos_campos = string_field(view_order=6, name='Ordem dos Campos', size=150, onlist = False)
        self.sql = text_field(view_order=7 , name='SQL', search=False, args=" rows=20", size=200, onlist=False)


    def estado_dynamic_atrs(self, record, internal=False):
        #se inernal for igual a True é porque foi chamada internamente pelo forms
        #print('estou no estado_dynamic_atrs', record)
        result = {}
        from ujson import dumps
        if internal == False:
            bottle.response.content_type = 'application/json'
        #print(1)
        estado = record['estado']
        #print(estado)
        if estado == 'Confirmado':
            result = {'sql':{'nolabel':True, 'atrs':'style="visibility:hidden"'}, 'totais':{'nolabel':True, 'atrs':'style="visibility:hidden"'}, 'ordem_dos_campos':{'nolabel':True, 'atrs':'style="visibility:hidden"'}}
        #print(result)
        return dumps(result)


    def Imprimir(self, key, window_id):
        #print ('estou no imprimir do sql_report')
        template = 'sql_report'
        record = get_records_to_print(key=key, model=self)
        #print ('My record is', record, key)
        sql = record['sql']
        forbiden_terms = ['delete', 'DELETE', 'update', 'UPDATE', 'insert', 'INSERT']
        for forbiden in forbiden_terms:
            if forbiden in sql:
                return 'Proibido correr este comando!'
        variaveis = record['linha_sql_report']
        if variaveis:
            variaveis_dict = {}
            for variavel in variaveis:
                variaveis_dict[variavel['variavel']] = variavel['valor']
            sql = sql.format(**variaveis_dict)
        print(sql)
        result = run_sql(sql)
        print(result)
        ordem_dos_campos = record['ordem_dos_campos']
        totais = record['totais']
        title = record['title']
        record = {'result':result, 'totais':totais, 'ordem_dos_campos':ordem_dos_campos, 'title':title}
        return Report(record=record, report_template=template).show()

    def Exportar(self, key, window_id):
        record = get_records_to_print(key=key, model=self)
        #print (record, key)
        sql = record['sql']
        variaveis = record['linha_sql_report']
        if variaveis:
            variaveis_dict = {}
            for variavel in variaveis:
                variaveis_dict[variavel['variavel']] = variavel['valor']
            sql = sql.format(**variaveis_dict)
        result = run_sql(sql)
        return data_to_csv(result, self, 'Gravar')

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return ('form', form_edit(window_id = window_id).show())

    def Alterar(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return ('form', form_edit(window_id = window_id).show())

