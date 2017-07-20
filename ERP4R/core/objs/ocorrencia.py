# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Gestão de Ocorrencias Policiais, 
este é o Objecto base para toda a actividade policial, 
a partir daqui será gerada a informação estatistica necessária
"""
__author__ = 'António Anacleto'
__credits__ = ['Hugo Fonseca']
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__='ocorrencia.Ocorrencia'
import auth, base_models
from orm import *
from form import *
from esquadra import Esquadra
from terceiro import Terceiro

class Ocorrencia(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'ocorrencia'
        self.__title__= 'Gestão de Ocorrencias'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(ocorrencia.numero) DESC'
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
        self.__workflow_context__ = {
            }
        self.__tabs__ = [
            ('Envolvidos', ['identificacao']),
            ('Testemunhos', ['testemunho']),
            ('Crimes', ['crime']),
            ('Objectos', ['objecto']),
            ('Hospital', ['hospital']),
            ('Judicial', ['tribunal'])
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Encerrado','Cancelado'])
            ]
        self.__get_options__ = ['numero']

        self.numero = info_field(view_order=1, name='Número', size=30)#, default=self.new_number()
        self.data = date_field(view_order=2, name='Data', size=60, args='readonly', default=datetime.date.today())
        self.hora = time_field(view_order=3, name='Hora', size=60, args='readonly', default=time.strftime('%H:%M'), onlist=False, search=False)
        self.data_ocorrencia = date_field(view_order=4, name='Data Ocorrencia', args='required', size=60)
        self.hora_ocorrencia = time_field(view_order=5, name='Hora de Ocorrencia', args='required', size=60, onlist=False, search=False)
        self.metodo = combo_field(view_order=6, name='Metodo', size=60, args='required', onlist=False, search=False, options=[('denuncia','Denuncia'), ('noticia','Noticia'), ('queixa','Queixa'), ('participacao','Participação'), ('flagrante_delito','Flagrante Delito')])
        self.esquadra = combo_field(view_order=7, name='Esquadra/Posto', size=60, args='required', model='esquadra', options="model.get_esquadra()", column='nome')
        self.servico = combo_field(view_order=8, name='Serviço', size=60, options=[('esquadra','Esquadra'), ('piquete','Piquete'), ('transito','Trânsito'), ('fiscal','Fiscal'), ('maritima','Maritima'), ('investigacao','Investigação'), ('intervencao','Intervenção'), ('patrulha','Patrulha'), ('unid_especial','Unid.Especial'), ('prot_entidade','Prot.Entidade'), ('florestal','Florestal')])
        self.actividade = parent_field(view_order=9, name ='Actividade Pol.', model_name='actividade.Actividade', onlist=False, column='numero')
        self.estado = info_field(view_order=10, name='Estado', size=60, default='Rascunho')
        self.agente_detencao = combo_field(view_order=11, name='Agente/Detenção', size=60, model='terceiro',options="model.get_funcionarios()", column='nome')
        self.agente_servico = parent_field(view_order=12, name='Agente/Serviço', model_name='users.Users', size=40, default="context['user']", onlist=False, column='nome')
        self.local = string_field(view_order=13, name='Local', size=60)
        self.sucedido = text_field(view_order=14, name='Sucedido', size=100, args="rows=10 required", colspan=3, onlist=False, search=False)
        self.identificacao = list_field(view_order=15, name ='Envolvidos', condition="ocorrencia='{id}'", model_name='identificacao.Identificacao', list_edit_mode='inline', onlist = False)
        #(lista de terceiros do tipo vitima, testemunha, acusado, queixoso, etc. vindo de identificação com informações como nome, idade, profisão, morada, etc.)
        self.crime = list_field(view_order=16, name ='Crimes', condition="ocorrencia='{id}'", model_name='crime.Crime', list_edit_mode='inline', onlist = False)
        # lista de crimes agregados a esta ocorrencia
        self.objecto = list_field(view_order=17, name ='Objectos', condition="ocorrencia='{id}'", model_name='objecto.Objecto', list_edit_mode='inline', onlist = False)
        self.hospital = list_field(view_order=18, name ='Hospital', condition="ocorrencia='{id}'", model_name='hospital.Hospital', list_edit_mode='inline', onlist = False)
        self.tribunal = list_field(view_order=19, name ='Tribunal', condition="ocorrencia='{id}'", model_name='tribunal.Tribunal', list_edit_mode='inline', onlist = False)
        self.testemunho = list_field(view_order=20, name ='Testemunhos', condition="ocorrencia='{id}'", model_name='testemunho.Testemunho', list_edit_mode='inline', onlist = False)

    def get_esquadra(self):
        user_id = botle.request.session.get('user')
        return Esquadra().get_esquadra(user_id)

    def get_funcionarios(self):
        return Terceiro().get_funcionarios()

    def new_number(self):
        base_models.Sequence().get_sequence('ocorrencia')

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('ocorrencia')
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Encerrar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Encerrado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()
