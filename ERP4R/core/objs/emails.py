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
__model_name__='emails.Emails'
import base_models #auth, 
from orm import *
from form import *

class Emails(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'emails'
        self.__title__= 'Emails'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'emails.date DESC, emails.time DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Enviar'], 'Enviado':['Arquivar'], 'Lido':['Reencaminhar', 'Responder', 'Arquivar', 'Spam', 'Marcar Não Lido'], 'Novo':['Reencaminhar', 'Responder', 'Arquivar', 'Spam', 'Marcar Lido'],}
            )
        self.__workflow_auth__ = {
            'Enviar':['All'],
            'Reencaminhar':['All'],
            'Responder':['All'],
            'Arquivar':['All'],
            'Spam':['All'],
            'Marcar Lido':['All'],
            'Marcar Não Lido':['All'],
            'full_access':['Gestor']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['Gestor']
            }
        self.__record_colors__ = [
            ('estado',{'Novo':'bold', 'Enviado':'green'}),
            ]
        self.__records_view__ = [
            ('users', "context['user']", []),
            ]
        self.__get_options__ = ['date']

        self.estado = info_field(view_order = 1, name = 'Estado', default = 'Rascunho')# , colspan=3
        self.users = parent_field(view_order = 2, name = 'Utilizador', size = 40, default = "context['user']", model_name = 'users.Users', search = False, args = 'style:visibility="hidden"', nolabel = True, onlist = False, column = 'nome')
        self.date = date_field(view_order = 3, name = 'Data', default = datetime.date.today())
        self.time = time_field(view_order = 4, name = 'Hora', default = time.strftime('%H:%M'))
        self.msg_from = email_field(view_order = 5, name = 'De', size = 60)
        self.msg_to = email_field(view_order = 6, name = 'Para', size = 60) 
        self.cc = email_field(view_order = 7, name = 'CC', size = 60, onlist = False)
        self.bcc = email_field(view_order = 8, name = 'BCC', size = 60, onlist = False)
        self.subject = string_field(view_order = 9, name = 'Assunto', size = 150)# , colspan=3
        self.message = message_field(view_order = 10, name = 'mensagem', onlist = False, search = False, size = 90)# , colspan=4
        self.email_category = many2many(view_order = 11, name = 'Categorias', model_name = 'email_category.EmailCategory', condition = "emails = '{id}'", fields = ['name'])# , colspan=2
        self.attachment = list_field(view_order = 12, name = 'Anexos', condition = "model = 'emails.Emails' And model_id='{id}'", model_name = 'attachment.Attachment', fields = ['description'], show_footer = False, list_edit_mode = 'inline', onlist = False)#, colspan=2

    def Marcar_Lido(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Lido'
        self.put()
        return form_edit(window_id=window_id).show()

    def Marcar_Nao_Lido(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Novo'
        self.put()
        return form_edit(window_id=window_id).show()

    def Spam(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Spam'
        self.put()
        return form_edit(window_id=window_id).show()

    def Enviar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Enviado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Reencaminhar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Enviado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Responder(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Enviado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Arquivar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Arquivado'
        self.put()
        return form_edit(window_id=window_id).show()

