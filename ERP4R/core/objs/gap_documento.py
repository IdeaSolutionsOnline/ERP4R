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
__model_name__ = 'gap_documento.GAPDocumento'
import auth, base_models
from orm import *
from form import *

class GAPDocumento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_documento'
        self.__title__ ='Documentos'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__order_by__ = 'gap_documento.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , name='Nome', size=40)
        self.data = date_field(view_order = 2, name = 'Data', size=40, args='readonly', default = datetime.date.today())
        self.documento = image_field(view_order=3, name='Upload Documento', size=50, onlist=False)
        self.gap_servico = many2many(view_order=4, name='Serviço', fields=['nome'], size=50, model_name='gap_servico.GAPServico', condition="gap_documento='{id}'", onlist=False)
        self.tipo = combo_field(view_order = 5, name = 'Tipo', size = 50, onlist = False, args = 'required', search = False, options = [('legislacao','Legislação'),('manual','Manual'),('outros','Outros')])


    def get_self(self):
        return self.get_options()


     #Apanha todos os documentos
    def get_documentos(self):
        def get_results():
            self.kargs['join'] = ",gap_documento_gap_servico"
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id"
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                options.append(str(option['nome'])+";"+str(option['documento'])+";"+str(option['tipo'])+";"+str(option['gap_servico'])+";")
            return options
        return erp_cache.get(key=self.__model_name__ + '_documentos', createfunc=get_results)


    #Apanha todos os documentos tipo legislacao
    def get_legislacao(self,servicoId=None,ascendenteId=None):
        options = []
        self.kargs['join'] = ",gap_documento_gap_servico"
        if(ascendenteId == None):
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id  and  gap_documento_gap_servico.gap_servico ='{servicoId}' ".format(servicoId=str(servicoId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'legislacao') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")
        else:
            #procura pelos documentos do seu ascendente caso existirem
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id and  gap_documento_gap_servico.gap_servico ='{servicoId}'".format(servicoId=str(ascendenteId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'legislacao') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")

            #procura pelos documentos do servico
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id and  gap_documento_gap_servico.gap_servico ='{servicoId}'".format(servicoId=str(servicoId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'legislacao') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")
        return options

    #Apanha todos os documentos tipo manual
    def get_manual(self,servicoId=None,ascendenteId=None):
        options = []
        self.kargs['join'] = ",gap_documento_gap_servico"
        if(ascendenteId == None):
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id  and  gap_documento_gap_servico.gap_servico ='{servicoId}' ".format(servicoId=str(servicoId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'manual') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")
        else:
            #procura pelos documentos do seu ascendente caso existirem
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id and  gap_documento_gap_servico.gap_servico ='{servicoId}'".format(servicoId=str(ascendenteId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'manual') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")

            #procura pelos documentos do servico
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id and  gap_documento_gap_servico.gap_servico ='{servicoId}'".format(servicoId=str(servicoId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'manual') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")
        return options


    #Apanha todos os documentos tipo outros
    def get_outros(self,servicoId=None,ascendenteId=None):
        options = []
        self.kargs['join'] = ",gap_documento_gap_servico"
        if(ascendenteId == None):
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id  and  gap_documento_gap_servico.gap_servico ='{servicoId}' ".format(servicoId=str(servicoId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'outros') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")
        else:
            #procura pelos documentos do seu ascendente caso existirem
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id and  gap_documento_gap_servico.gap_servico ='{servicoId}'".format(servicoId=str(ascendenteId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'outros') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")

            #procura pelos documentos do servico
            self.where ="gap_documento_gap_servico.gap_documento = gap_documento.id and  gap_documento_gap_servico.gap_servico ='{servicoId}'".format(servicoId=str(servicoId))
            opts = self.get(order_by='nome')
            for option in opts:
                if(option['tipo'] == 'outros') and (option['active'] == True):
                        options.append(str(option['nome'])+";"+str(option['documento'])+";")
        return options