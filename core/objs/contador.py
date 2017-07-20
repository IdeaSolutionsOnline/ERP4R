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
__model_name__ = 'contador.Contador'
import auth, base_models
from orm import *
from form import *
try:
    from my_rede import Rede
except:
    from rede import Rede
try:
    from my_furo import Furo
except:
    from furo import Furo

class Contador(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'contador'
        self.__title__ = 'Contadores de Água'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'contador.nome'
        self.__tabs__ = [('Estação de Bombagem',['estacao']),
        ('Reservatório',['reservatorio']),
        ('Conduta',['conduta']),
        ('Contratos',['contrato']),
        ('Chafarizes',['chafariz'])]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1 , name='Código', size=60)
        self.tipo = combo_field(view_order=2 , name='Tipo', size=50, options=[('consumo','Consumo'), ('rede','Rede')])
        self.rede = choice_field(view_order=3 , name='Rede de Distribuição', size=80, model='rede', column='nome', options="model.get_opt('Rede')")
        self.furo = choice_field(view_order=4 , name='Furo de extracção', size=80, model='furo', column='nome', options="model.get_opt('Furo')")
        self.estacao = list_field(view_order=5 , name='', fields=['nome'], simple=True, show_footer=False, model_name='estacao_bombagem.EstacaoBombagem', condition="contador_in='{id}' OR contador_out='{id}'", list_edit_mode='inline')#, colspan=2
        self.reservatorio = list_field(view_order=6 , name='', fields=['nome'], simple=True, show_footer=False, model_name='reservatorio.Reservatorio', condition="contador_in='{id}' OR contador_out='{id}'", list_edit_mode='inline')#colspan=2,
        self.conduta = list_field(view_order=7 , name='', fields=['nome'], simple=True, show_footer=False, model_name='conduta.Conduta', condition="contador='{id}'", list_edit_mode='inline')#colspan=2, 
        self.contrato = list_field(view_order=8 , name='', fields=['contrato', 'estado'], show_footer=False, model_name='contador_contrato.ContadorContrato', condition="contador='{id}'", list_edit_mode='inline')#colspan=2, 
        self.chafariz = list_field(view_order=9, name='', fields=['nome'], simple=True, show_footer=False, model_name='chafariz.Chafariz', condition="contador_in='{id}' OR 'contador_out'='{id}'", list_edit_mode='inline')#colspan=2, 

    def get_opt(self, model):
        return eval(model + '().get_options()')

