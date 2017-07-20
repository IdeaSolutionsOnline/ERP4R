# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVtek dev"
__status__ = "Development"
__model_name__ = 'gap_localizacao.GAPLocalizacao'
import auth, base_models
from orm import *
from form import *

class GAPLocalizacao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_localizacao'
        self.__title__ ='Localização'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_localizacao.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.codigo = string_field(view_order=1 , name='Codigo', size=40)
        self.nome = string_field(view_order=2 , name='Nome', size=80)
        self.ilha = combo_field(view_order = 3, name = 'Ilha', size = 35, options = [('SA','Santo Antão'), ('SV','São Vicente'), ('SN','São Nicolau'), ('SL','Sal'), ('BV','Boa Vista'), ('MAIO','Maio'), ('ST','Santiago'), ('FG','Fogo'), ('BR','Brava')], onlist = True)

    #Apanha as localizaçoes disponiveis
    def get_self(self):
        return self.get_options()

    #Apanha as localizaçoes por nome
    def get_localizacao_nome(self, nome=None):
        #Essa funçao apanha localizaçao por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['nome'] == nome:
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']+ ' - ' + option['ilha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_localizacao_nome', createfunc=get_results)

    #Apanha as localizaçoes por codigo
    def get_localizacao_codigo(self, codigo=None):
        #Essa funçao apanha localizaçao por codigo
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['codigo'] == codigo:
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']+ ' - ' + option['ilha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_localizacao_codigo', createfunc=get_results)


    def get_localizacao(self, localizacaoId=None):
        try:
            self.where = "id = '{id}'".format(id=str(localizacaoId))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return str(self.kargs['nome'])+";"+str(self.kargs['ilha'])
            return None
        except:
            return None