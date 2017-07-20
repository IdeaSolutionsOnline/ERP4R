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
__model_name__ = 'fornecedor.Fornecedor'
import auth, base_models
from orm import *
from form import *

class Fornecedor(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'fornecedor'
        self.__title__ ='Fornecedor' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        #self.__order_by__ = 'fornecedor.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__tabs__ = [
            ('Contatos do Sistema', ['contatos']),            
            ('Proposta do Sistema', ['proposta']),            
            ]
        self.nome = string_field(view_order=1 , name='Nome da Empresa ', size=80)
        self.nif = string_field(view_order=2 , name='NIF', size=80)
        self.tipo = combo_field(view_order=3 , name='Tipo', size=80, options=[('tipo1','Tipo1'), ('tipo2','Tipo2'), ('tipo3','Tipo3'), ('tipo4','Tipo4'), ('tipo5','Tipo5'), ('tipo6','Tipo6'), ('tipo7','Tipo7'), ('tipo8','Tipo8'), ('tipo9','Tipo9'), ('tipo10','Tipo10')])
        self.pais = combo_field(view_order=4 , name='Pais', size=80, options=[('pais1','Pais1'), ('pais2','Pais2'), ('pais3','Pais3'), ('pais4','Pais4'), ('pais5','Pais5'), ('pais6','Pais6'), ('pais7','Pais7'), ('pais8','Pais8'), ('pais9','Pais9'), ('pais10','Pais10')])
        self.repres = string_field(view_order=5 , name='Representante', size=80)
        self.estado = combo_field(view_order=6 , name='Estado', size=80, options=[('estado1','Estado1'), ('estado2','Estado2'), ('estado3','Estado3')])
        self.descc = text_field(view_order=7 , name='Descricao', size=80)
        self.contatos = list_field(view_order = 8, name = 'Contato Fornecedor', model_name = 'contatos.Contatos', condition = "rf='{id}'", list_edit_mode = 'popup', onlist = False)
        self.proposta = list_field(view_order = 9, name = 'Propostas Fornecedor', model_name = 'proposta.Proposta', condition = "rf2='{id}'", list_edit_mode = 'popup', onlist = False)
        self.rffpcv = parent_field(view_order=10, name ='Ref convite', model_name='conviteconcforn.Conviteconcforn', nolabel=True,  column='rffornecedcv')
        #self.localizacao = list_field(view_order = 13, name = 'Localização do Sistema:', model_name = 'localizacao.Localizacao', condition = "local='{id}'", list_edit_mode = 'inline', onlist = False)

    def get_opt(self, model):
        return eval(model + '().get_options()')