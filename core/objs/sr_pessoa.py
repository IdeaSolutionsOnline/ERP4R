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
__model_name__ = 'sr_pessoa.SRPessoa'
import auth, base_models
from orm import *
from form import *

class SRPessoa(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sr_pessoa'
        self.__title__ = 'Individuo'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order = 1, name = 'Nome', size = 80)
        self.sexo = combo_field(view_order = 2, name = 'Sexo', size = 50, default = ' ', options = [('masculino','Masculino'), ('feminino','Feminino')], onlist = True) 
        self.nr_inscricao = string_field(view_order = 3, name = 'Nº de Inscrição', size = 40)
        self.nome_pai = string_field(view_order = 4, name = 'Nome do Pai', size = 80)
        self.nome_mae = string_field(view_order = 5, name = 'Nome do Mãe', size = 80)
        self.p_consulta = date_field(view_order = 6, name = 'Primeira Consulta', size=50, args = 'required', default = datetime.date.today())
        self.d_nasc = date_field(view_order = 7, name = 'Data Nascimento', size=40, args = 'required')
        self.hora_nasc = time_field(view_order=8, name ='Hora Nascimento', size=40, onlist=True, args='required')
        self.endereco = text_field(view_order=9, name='Endereço Familia', size=100, args="rows=30", onlist=True, search=False)
        self.telefone = string_field(view_order = 10, name = 'Telefone', size = 40)
        self.email = string_field(view_order = 11, name = 'Email', size = 80)
        self.estado = combo_field(view_order = 12, name = 'Estado', size = 40, default = 'active', options = [('active','Activo'), ('canceled','Cancelado')], onlist = False)
        self.nr_registo = string_field(view_order = 15, name = 'Nº Registo', size = 40)
        self.data_registo = date_field(view_order = 16, name = 'Data Registo', size=40, args = 'required')
   
        
