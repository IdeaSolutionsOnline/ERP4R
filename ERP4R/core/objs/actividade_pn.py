# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Registo de actividades policiais realizadas.
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'actividade_pn.ActividadePN'
import auth, base_models
from orm import *
from form import *

class ActividadePN(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'actividade_pn'
        self.__title__= 'Actividades Policiais'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(actividade_pn.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar', 'Cancelar'], 'Confirmado':['Imprimir', 'Encerrar', 'Cancelar'], 'Encerrado':['Cancelar'], 'Cancelado':['Rascunho']}
            )#imprimir, gerar queixa, gerar denuncia, imprimir queixa, etc...
        self.__workflow_auth__ = {
            'Confirmar':['Agente'],
            'Encerrar':['Agente'],
            'Rascunho':['Comandante'],
            'Cancelar':['Chefe'],
            'full_access':['Comandante']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }
        self.__get_options__ = ['numero']

        self.numero = info_field(view_order=1, name='Número', size=30)
        self.tipo = combo_field(view_order=2, name='Tipo', size=60, args='required', options=[('rusga','Rusga'), ('fiscalizacao','Fiscalização'), ('policiamento','Policiamento'), ('investigacao','Investigação'), ('notificação','Notificação'), ('patrulha','Patrulha'), ('operacao_stop','Operação Stop'), ('identificacao','Identificação')],)
        self.data_inicial = date_field(view_order=3, name='Data Inicial', size=60, args='required', default=datetime.date.today())
        self.data_final = date_field(view_order=4, name='Data Final', size=60, args='required', default=datetime.date.today())
        self.hora_inicial = time_field(view_order=5, name='Hora Inicial', size=60, args='required', default=time.strftime('%H:%M'))
        self.hora_final = time_field(view_order=6, name='Hora Final', size=60, args='required', default=time.strftime('%H:%M'))
        self.estado = info_field(view_order=7, name='Estado', size=60, default='Rascunho')
        self.descricao = text_field(view_order=8, name='Descrição', size=100, args="rows=20", colspan=3, onlist=False, search=False)
        #self.intervenientes = list_field(view_order=8, name ='Intervenientes', fields=['nome', 'estado'], condition="actividade='{id}'", model_name='terceiro.Terceiro', simple=True, show_footer=False, field_filter=("funcionario={value}",'True'))
        self.ocorrencia = list_field(view_order=9, name ='Ocorrências', fields=['numero', 'data_ocorrencia', 'metodo', 'esquadra', 'servico'], condition="actividade='{id}'", model_name='ocorrencia.Ocorrencia', list_edit_mode='edit')

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('actividade_pn')
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
