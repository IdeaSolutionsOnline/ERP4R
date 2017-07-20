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
__model_name__ = 'sr_mulher.SRMulher'
import auth, base_models
from orm import *
from form import *
class SRMulher(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sr_mulher'
        self.__title__ ='Inscrição e Identificação da Mulher'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome'] # define tambem o campo a ser mostrado  no m2m, independentemente da descricao no field do m2m
        self.__order_by__ = 'sr_mulher.nome'
       

        #choice field com a estrutura de saude

        self.numero_inscricao = integer_field(view_order = 1, name = 'Nº de Inscrição', size = 40)
        self.nome = string_field(view_order = 2, name = 'Nome Completo', size = 70, onlist = True)
        self.data_nascimento = date_field(view_order = 3, name = 'Data Nascimento', size=40, args = 'required', onlist = True)
        self.escolaridade = combo_field(view_order = 4, name = 'Escolaridade', size = 40, default = '', options = [('analfabeta','Analfabeta'), ('primaria','Primária'), ('secundaria','Secundária'), ('mais','Mais')], onlist = True)
        self.telefone = string_field(view_order = 5, name = 'Telefone', size = 40, onlist = True)
        self.endereco_familia = text_field(view_order=6, name='Endereço Familia', size=70, args="rows=30", onlist=False, search=False) 
        self.endereco_actual = text_field(view_order=7, name='Endereço Fixo Actual', size=70, args="rows=30", onlist=False, search=False)
        self.observacoes = text_field(view_order=8, name='Observações', size=80, args="rows=30", onlist=False, search=False) 
        self.estado = combo_field(view_order = 9, name = 'Estado', size = 40, default = 'active', options = [('active','Activo'), ('canceled','Cancelado')], onlist = True) 
       

