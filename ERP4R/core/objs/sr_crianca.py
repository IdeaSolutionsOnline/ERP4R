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
__model_name__ = 'sr_crianca.SRCrianca'
import auth, base_models
from orm import *
from form import *
class SRCrianca(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sr_crianca'
        self.__title__ ='Inscrição e Identificação da Criança'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome'] # define tambem o campo a ser mostrado  no m2m, independentemente da descricao no field do m2m
        self.__order_by__ = 'sr_crianca.nome'
        self.__tabs__ = [
            ('Pré-Natal', ['sr_pre_natal']),
            ('Neo-Natal', ['sr_neo_natal']),
            ('Irmãos', ['sr_crianca']),
            ]  
       

        #choice field com a estrutura de saude

        self.numero_inscricao = integer_field(view_order = 1, name = 'Nº de Inscrição', size = 40)
        self.primeira_consulta = date_field(view_order = 2, name = 'Primeira Consulta', size=40, args = 'required', default = datetime.date.today(), onlist = False)
        self.nome = string_field(view_order = 3, name = 'Nome', size = 70, onlist = True)
        self.sexo = combo_field(view_order = 4, name = 'Sexo', size = 40, default = 'Feminino', options = [('feminino','Feminino'), ('masculino','Masculino')], onlist = True) 
        self.data_nascimento = date_field(view_order = 5, name = 'Data Nascimento', size=40, args = 'required', onlist = True)
        self.hora_nascimento = time_field(view_order=7, name ='Hora Nascimento', size=40, onlist=False, args='required')
        self.numero_registo = string_field(view_order = 8, name = 'Nº Registo', size = 40, onlist = False)
        self.data_registo = date_field(view_order = 9, name = 'Data Registo', size=40, args = 'required')
        self.nome_pai = string_field(view_order = 10, name = 'Nome do Pai', size = 60, onlist=False)
        self.nome_mae = string_field(view_order = 11, name = 'Nome do Mãe', size = 60)  
        self.endereco_familia = text_field(view_order=12, name='Endereço Familia', size=70, args="rows=30", onlist=False, search=False) 
        self.telefone = string_field(view_order = 13, name = 'Telefone', size = 40, onlist = True)
        self.estado = combo_field(view_order = 14, name = 'Estado', size = 40, default = 'active', options = [('active','Activo'), ('canceled','Cancelado')], onlist = True) 
        self.sr_pre_natal = list_field(view_order=15, name = 'Informações Pré-Natal', fields=['duracao_gravidez'], condition="crianca='{id}'",  model_name='sr_pre_natal.SRPreNatal', list_edit_mode='inline', onlist = False)      
        self.sr_neo_natal = list_field(view_order=16,  name = 'Informações Neo-Natal', column='local_parto', condition="sr_crianca='{id}'", model_name='sr_neo_natal.SRNeoNatal', list_edit_mode='inline', onlist = False)