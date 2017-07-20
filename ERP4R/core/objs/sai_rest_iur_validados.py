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
__model_name__= 'sai_rest_iur_validados.SaiRestIURValidados'
import auth, base_models
from orm import *
from form import *

class SaiRestIURValidados(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sai_rest_iur_validados'
        self.__title__= 'Restituição de IUR, Lista Validados'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'sai_rest_iur_validados.nome'
        self.__workflow__ = (
            'estado', {'Em Pagamento':[], 'Reprovado':[], 'Pago':[], 'Validado':['Pagar', 'Reprovar'], 'NIB Invalido':[], 'Valores no GRE e no SIGOF diferentes':[], 'Dados Diferentes no SIGOF e no GRE': []}
            )
        self.__workflow_auth__ = {
            'Pagar':['Técnico Tesouro'],
            'Reprovar':['Técnico Tesouro'],
            'full_access':['Gestor Tesouro','Administrador']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Técnico Tesouro','Gestor Tesouro','Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }
        # self.__no_edit__ = [
        #     ('estado', ['Em Pagamento','Reprovado', 'Pago', 'Dados Diferentes no SIGOF e no GRE', 'Valores no GRE e no SIGOF diferentes', 'NIB Invalido', 'Validado', ])
        #     ]
        self.__records_view__ = [
            ('utilizador', 'get_records_view_values', ['Gestor Tesouro', 'Técnico DNRE', 'Gestor DNRE'], 'in'),
            ]
        self.__get_options__ = ['nome']

        self.ano = info_field(view_order=1, name='Ano', size=60)
        self.liquidacao = info_field(view_order=2, name='Liquidação', size=60)
        self.cabimento = info_field(view_order=3, name='Cabimento', size=60)
        self.nome = info_field(view_order=4, name='Nome', size=100)
        self.nif = info_field(view_order=5, name='NIF', size=60)
        self.valor = info_field(view_order=6, name='Valor', size=60, sum=True)
        self.estado = info_field(view_order=7, name='Estado', size=60)
        self.utilizador = info_field(view_order=8, name='Utilizador', size=60)
        self.nib = info_field(view_order=9, name='NIB', size=60)
        self.nib_a_corrigir = string_field(view_order=10, name='NIB a Corrigir', size=60)
        self.comprovativo = upload_field(view_order=11, name='Comprovativo', onlist=False)
        self.historico = text_field(view_order=12, name='Histórico', search=False, args=" rows=30 readonly", size=150, onlist=False)
        self.nota = text_field(view_order=13, name='Motivo  do Extorno \ Reprovação', search=False, args=" rows=5 ", size=150, onlist=False)

    # exemplo de utilização de __records_view com função em vez de tuple directo
    def get_records_view_values(self, window_id):
        print('im in get_records_view_values')
        ctx_dict = get_context(window_id)
        #print(ctx_dict)
        return ctx_dict['user_name']

    def Pagar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Em Pagamento'
        self.kargs['historico'] = self.kargs['historico'] + 'Aprovado para pagamento pelo tesouro em ' + str(datetime.datetime.today())
        self.put()
        return form_edit(window_id=window_id).show()

    def Reprovar(self, key, window_id):
        nota1 = bottle.request.forms.get('nota')
        if nota1== ''  :
            print(2)
            bottle.response.status = 500
            return '<span style="color: #FFFFFF; font-size: 20px; font-weight: bold;">O campo  Motivo  do Extorno \ Reprovação é obrigatório ser preenchido! Por favor insira-o para prosseguir!</span> \n'
        else:
            self.kargs = get_model_record(model=self, key=key)


            self.kargs['estado'] = 'Reprovado'
            self.kargs['historico'] = self.kargs['historico'] + 'Reprovado para pagamento pelo tesouro em ' + str(datetime.datetime.today())
            self.put()
            return form_edit(window_id=window_id).show()
