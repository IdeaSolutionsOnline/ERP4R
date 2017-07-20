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
__model_name__ = 'sr_pre_natal.SRPreNatal'
import auth, base_models
from orm import *
from form import *
try:
    from my_sr_crianca import SRCrianca
except:
    from sr_crianca import SRCrianca
class SRPreNatal(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sr_pre_natal'
        self.__title__ ='Periodo Pré-Natal'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['grupo_sanguineo'] # define tambem o campo a ser mostrado  no m2m, independentemente da descricao no field do m2m
        self.__order_by__ = 'sr_pre_natal.grupo_sanguineo'
       

        #choice field com a estrutura de saude

        self.duracao_gravidez = integer_field(view_order = 1, name = 'Duração Gravidez (semanas)', size = 30)
        self.numero_consultas = integer_field(view_order = 2, name = 'Consultas durante Gravidez', size = 30, onlist = True)
        self.grupo_sanguineo = combo_field(view_order = 3, name = 'Grupo Snaguineo e RH', size = 40, default = 'A', options = [('active','Activo'), ('canceled','Cancelado')], onlist = True) 
        self.tipo_gravidez = combo_field(view_order = 4, name = 'Tipo de Gravidez', size = 40, default = 'Normal', options = [('normal','Normal'), ('risco','De Risco')], onlist = True)       
        self.observacoes = text_field(view_order=5, name='Observações', size=50, onlist=True) 
        self.crianca = combo_field(view_order = 6, name  = 'Criança', size = 50, args = 'required', model = 'sr_criança', search = False, column = 'nome', options = "model.get_opts('SRCrianca().get_options()')", onlist=False)

    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

       

