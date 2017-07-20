# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_servico.GAPServico'
import auth, base_models
from orm import *
from form import *
class GAPServico(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_servico'
        self.__title__ ='Serviço'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome'] # define tambem o campo a ser mostrado  no m2m, independentemente da descricao no field do m2m
        self.__order_by__ = 'gap_servico.letra'
        self.__tabs__ = [
            ('Fluxo de Atendimento', ['gap_atendimento']),
            ('FAQ´s', ['gap_faq']),
            ('Checklist', ['gap_checklist']),
            ('Senha', ['gap_senha']),
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , name='Nome', size=50)
        self.ascendente = choice_field(view_order=2 , name='Ascendente', size=60, model='gap_servico', column='nome', options="model.get_self()", onlist = False)
        self.letra = string_field(view_order=3, name='Letra', size=15)
        self.gap_turno = many2many(view_order=4, name='Turno', fields=['nome'], size=50, model_name='gap_turno.GAPTurno', condition="gap_servico='{id}'", onlist=False)
        self.gap_documento = many2many(view_order=5, name='Documento', fields=['nome'], size=50, model_name='gap_documento.GAPDocumento', condition="gap_servico='{id}'", onlist=False)
        self.gap_senha_config = many2many(view_order = 6, name = 'Configurador de Senha', size = 50, fields=['descricao'], model_name = 'gap_senha_config.GAPSenhaConfig', condition = "gap_servico='{id}'", onlist=False)
        self.descricao = text_field(view_order=7, name='Descricao', size=90, args="rows=20", onlist=True, search=False)
        self.gap_atendimento = list_field(view_order=8, name ='Fluxo de Atendimento', condition="servico='{id}'",fields=['nome','ordem'], model_name='gap_atendimento.GAPAtendimento', list_edit_mode = 'popup', onlist = False)
        self.gap_faq = list_field(view_order=9, name ='FAQ´s', condition="servico='{id}'",fields=['pergunta','resposta'], model_name='gap_faq.GAPFaq', list_edit_mode='popup', onlist = False)
        self.gap_checklist = list_field(view_order=10, name ='Checklist', condition="servico='{id}'",fields=['nome','servico'], model_name='gap_checklist.GAPChecklist', list_edit_mode='popup', onlist = False)
        self.gap_senha = list_field(view_order=11, name ='Senha', condition="servico='{id}'",fields=['nr_senha','servico'], model_name='gap_senha.GAPSenha', list_edit_mode='inline', onlist = False)


    #Apanha todos os Serviços
    def get_self(self):
        return self.get_options()

    #Apanha o id do Serviço
    def get_servico_id(self, nome=None):
         try:
            self.where = "nome = '{nome}'".format(nome=str(nome))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return str(self.kargs['id'])
            return None
         except:
            return None

    #Apanha o id do Serviço e subservico (caso existir)
    def get_servico_Subid(self, nome=None):
         try:
            self.where = "nome = '{nome}'".format(nome=str(nome))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return str(self.kargs['id'])+";"+str(self.kargs['ascendente'])
            return None
         except:
            return None

    #Apanha os Serviços
    def get_servico(self):
        #Essa funçao apanha todos os serviços
        options = []
        opts = self.get(order_by='letra')
        for option in opts:
                options.append(str(option['id'])+";"+str(option['letra'])+";"+option['nome']+";"+str(option['ascendente']))
        return options


    #Apanha os Serviços (nome apenas)
    def get_servico_nome(self):
        #Essa funçao apanha todos os serviços
        options = []
        opts = self.get(order_by='letra')
        for option in opts:
                if options:
                    options.append(";"+option['nome'])
                else:
                    options.append(option['nome'])
        return options

    #Apanha os 4 primeiros Serviços (nome apenas) para preencher a TV :D
    def get_servico_tv(self):
        #Essa funçao apanha 4 primeiros serviços e os envia para a TV
        options = None
        count = 0
        opts = self.get(order_by='letra')
        for option in opts:
                if(count == 4):
                        break
                else:
                    if(option['ascendente'] == None):
                            if(options == None):
                                    options = str(option['nome'])
                            else:
                                options=str(options)+";"+str(option['nome'])
                            count+=1
        return options


    #Apanha o nome do serviço associado a essa id :)
    def get_letra_servico(self,keyservico=None):
        #Essa funçao apanha a letra do servico xpto
        try:
            self.where = "id = '{id}'".format(id=str(keyservico))
            self.kargs = self.get(order_by='letra')
            if self.kargs:
                self.kargs = self.kargs[0]
                return str(self.kargs['nome'])
            return None
        except:
            return None


    #verificar se o serviço encontra-se disponivel para a chamada
    def check_turnoServico(self,servico_id=None):
        try:
             from gap_turno import GAPTurno
             self.kargs['join'] = ",gap_servico_gap_turno"
             self.where ="gap_servico_gap_turno.gap_servico ='{servico_id}'".format(servico_id=servico_id)
             opts = self.get()
             options = []
             for option in opts:
                if(option['active']==True):
                     if(GAPTurno().check_turno(turno_id=option['gap_turno'])):
                            return True
             return False
        except:
            return False