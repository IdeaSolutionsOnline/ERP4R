# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Registo de Identificações realizadas no decorrer de uma ocorrencia.
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__='identificacao.Identificacao'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class Identificacao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'identificacao'
        self.__title__= 'Identificação de Intervenientes'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        #self.__order_by__ = 'identificacao.terceiro'
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }

        #self.__get_options__ = ['terceiro']

        self.ocorrencia = parent_field(view_order=1, name='Ocorrencia', args='style:visibility="hidden"', model_name='ocorrencia.Ocorrencia', nolabel=True, onlist=False, column='numero')
        self.terceiro = choice_field(view_order=2, name='Individuo', size=60, model='terceiro', column='nome', options="model.get_terceiros()")
        self.condicao = combo_field(view_order=3, name='Condição', size=40, options=[('vitima','Vitima'), ('queixoso','Queixoso'), ('acusado','Acusado'), ('testemunha','Testemunha'), ('informador','Informador')])
        self.categoria = combo_field(view_order=4, name='Categoria', size=40, options=[('nacional','Nacional'), ('residente','Residente'), ('emigrante','Emigrante'), ('turista','Turista'), ('negocios','Negócios')])
        self.idade_terceiro = function_field(view_order=5, name='Idade')#ocorrencia.data_ocorrencia-terceiro.data_nascimento
        self.resultado = combo_field(view_order=6, name='Resultado', size=40, options=[('detencao','Detenção'), ('outro','Outro')])

    def get_terceiros(self):
        return Terceiro().get_options()

    def get_idade_terceiro(self, key):
        import dateutil
        value = 0
        self.kargs = get_model_record(model=self, key=key)
        #print (self.kargs)
        from terceiro import Terceiro
        pessoa = Terceiro(where="id='{terceiro}'".format(terceiro=self.kargs['terceiro'])).get()[0]
        #print (pessoa)
        return dateutil.relativedelta.relativedelta(datetime.date.today(), pessoa['data_nascimento']).years
