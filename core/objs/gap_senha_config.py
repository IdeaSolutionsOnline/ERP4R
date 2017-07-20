# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVTek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_senha_config.GAPSenhaConfig'
import auth, base_models
from orm import *
from form import *


class GAPSenhaConfig(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_senha_config'
        self.__title__ = 'Configurador de Senha'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_senha_config.loja'
        self.__get_options__ = ['descricao']
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.descricao = string_field(view_order = 1, name = 'Descrição', size = 40, search=True)
        self.mensagem_cabecalho = text_field(view_order = 2, name = 'Mensagem de Cabeçalho', size = 50, search=True)
        self.mensagem_rodape = text_field(view_order = 3, name = 'Mensagem de Rodapé', size = 50, search=True)
        self.terminal = many2many(view_order = 4, name = 'Loja', size = 50, fields=['name'], model_name = 'terminal.Terminal', condition = "gap_senha_config='{id}'", onlist=False)
        self.gap_servico = many2many(view_order = 5, name = 'Servico', size = 50, fields=['nome'], model_name = 'gap_servico.GAPServico', condition = "gap_senha_config='{id}'", onlist=False)



    #Apanha toda a configuraçao disponivel :)
    def get_self(self):
        return self.get_options()

    #Apanhar configurasao para uma senha
    def get_config_servico(self, servico=None):
        from gap_servico import GAPServico
        #Primeiro procuro por serviço (caso existir retorno os respectivos valores)
        self.kargs['join'] = ",gap_senha_config_gap_servico"
        self.where ="gap_senha_config_gap_servico.gap_servico = '{id}' and gap_senha_config_gap_servico.gap_senha_config= gap_senha_config.id".format(id=str(servico))
        self.kargs = self.get()
        if self.kargs:
            self.kargs = self.kargs[0]
            return str(self.kargs['mensagem_cabecalho'])+";"+str(self.kargs['mensagem_rodape'])
        return ";;"


    def get_config_loja(self, loja=None):
        self.kargs['join'] = ",gap_senha_config_terminal"
        self.where ="gap_senha_config_terminal.terminal = '{id}' and gap_senha_config_terminal.gap_senha_config=gap_senha_config.id".format(id=str(loja))
        self.kargs = self.get()
        if self.kargs:
            self.kargs = self.kargs[0]
            return str(self.kargs['mensagem_cabecalho'])+";"+str(self.kargs['mensagem_rodape'])
        return ";;" #em caso da senha ainda nao for configurada