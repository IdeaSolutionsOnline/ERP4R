# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina']
__credits__ = []
__version__ = "1.0"
__maintainer__ =  ['António Anacleto', 'Jair Medina']
__status__ = "Development"
__model_name__= 'sai_rf.SaiRF'
#import base_models#auth,
from orm import *
from form import *
try:
    from my_users import Users
except:
    from users import Users

class SaiRF (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_rf'
        self.__title__= 'Repartições de Finanças'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir','Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Rascunho':['Gestor'],
            'Imprimir':['All'],
           }
        self.__auth__ = {
            'read':['All'],
            'write':['Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso'])
            ]

        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name='Nome', size=100,onlist=True )
        self.localizacao = string_field(view_order=2, name='Localização', size=100,onlist=True)
        self.estado = info_field(view_order=3, name ='Estado', default='Rascunho', onlist=True, hidden=True, nolabel=True,)
        self.users = list_field(view_order = 4, name = 'Funcionários', fields=['nome','email'], model_name = 'users.Users', condition = "rf='{id}'", list_edit_mode = 'popup', onlist = False)



    def Imprimir(self, key, window_id):
        template = 'alerta_for'
        record =self.prepare_data()#get_records_to_print(key=key, model=self)
        #print (template)
        return Report(record=record, report_template=template).show()


    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id = window_id).show()


    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()
