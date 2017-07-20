# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina']
__credits__ = []
__version__ = "1.0"
__maintainer__ =  ['António Anacleto', 'Jair Medina']
__status__ = "Development"
__model_name__= 'sai_contribuinte.SaiContribuinte'
#import base_models#auth,
from orm import *
from form import *


class SaiContribuinte (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_contribuinte'
        self.__title__= 'Contribuinte'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir','Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Rascunho':['Gestor'],
            'Imprimir':['All'],
           }

        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }


        self.__tabs__ = [
            ('Dados do Contribuinte', ['nu_nif','nm_contribuinte','nm_dcomercial','tp_contribuinte','ds_area_fiscal','nu_bi','dt_nascimento','nm_pai','nm_mae','tp_sexo','estado_empresa','ds_estado_civil','ds_morada']),
            ('contato', ['nu_telefone','nu_telemovel','email','nu_fax','cae']),
            ('IUR', ['dt_inicio_actividade','ds_classificacao','tp_regime_iur','ds_tp_regime_iur','tp_isencao_iur','dt_ini_isencao_iur','dt_fim_isencao_iur','ds_tp_isencao_iur']),
            ('IVA', ['ds_tp_operacao_iva','ds_tp_afeccao_real_iva','tp_regime_iva','ds_tp_deducao_iva','ds_tp_isencao_iva','pro_rata_iva','ds_tp_regime_iva']),
            ('Outros', ['nu_trabalhador','nu_viatura','nat_freguesia','tp_estado_fiscal','ds_estado_fiscal','nif_portal','dt_nif_portal','importador','exportador','gc','nu_inps'])
            ]

        self.nu_nif= string_field(view_order = 1, name ='Nif', size = 80)
        #print('1')
        self.nm_contribuinte = string_field(view_order = 2, name ='Nome',size = 150)
        self.nm_dcomercial = string_field(view_order = 3, name = 'Nome Comercial', size = 50, onlist=False)
        self.tp_contribuinte = string_field(view_order = 4, name = 'tipo', size = 20, onlist=False)
        self.ds_area_fiscal = string_field(view_order = 5, name = 'Área Fiscal', size = 50)
        self.nu_bi = integer_field(view_order = 6, name = 'Nr BI',  size = 80)
        self.dt_nascimento = string_field(view_order = 7, name = 'Data Nascimento', size = 2, onlist=False)
        self.nm_pai = string_field(view_order = 8, name = 'Nome Pai',  size = 150, onlist=False)
        self.nm_mae = string_field(view_order = 9, name = 'Nome Mãe',  size = 150, onlist=False)
        self.tp_sexo= string_field(view_order = 10, name = 'Sexo', size = 2, onlist=False)
        #print('2')
        self.estado_empresa = string_field(view_order = 11, name = 'Estado Empresa',  size = 40, onlist=False)
        self.ds_estado_civil = string_field(view_order = 12, name = 'Estado Civil', size = 40, onlist=False)
        self.ds_morada = string_field(view_order = 13, name = 'Morada', size = 140, onlist=False)
        self.nu_telefone = string_field(view_order = 14, name = 'Telefone', size = 40, onlist=False)
        self.nu_telemovel  = string_field(view_order = 15, name = 'Telemovel ', size = 40, onlist=False)
        self.email = string_field(view_order=16 , name='Email', onlist=False, size=100)
        self.nu_fax = string_field(view_order=17 , name='Fax', onlist=False, size=40)
        self.cae = string_field(view_order=18 , name='CAE', onlist=False, size=40)
        self.dt_inicio_actividade = string_field(view_order = 19, name = 'Data de Inicio de Atividade', size = 40, onlist=False)
        self.ds_classificacao = string_field(view_order=20 , name='Classificacão', size=40, onlist=False)
        self. tp_regime_iur = string_field(view_order=21 , name=' tp_regime_iur', size=40, onlist=False)
       # print('3')
        self.ds_tp_regime_iur = string_field(view_order=22 , name='ds_tp_regime_iur ', size=40, onlist=False)
        self.tp_isencao_iur = string_field(view_order=23 , name=' tp_isencao_iur ', size=40, onlist=False)
        self.dt_ini_isencao_iur = string_field(view_order=24 , name=' dt_ini_isencao_iur ', size=40, onlist=False)
        self.dt_fim_isencao_iur = string_field(view_order=25 , name=' dt_fim_isencao_iur ', size=40, onlist=False)
        self.ds_tp_isencao_iur = string_field(view_order=26 , name=' ds_tp_isencao_iur ', size=40, onlist=False)
        #print('4')
        self.ds_tp_operacao_iva = string_field(view_order=27 , name='  ds_tp_operacao_iva ', size=40, onlist=False)
        self.ds_tp_afeccao_real_iva= string_field(view_order=28 , name=' ds_tp_afeccao_real_iva ', size=40, onlist=False)
        self.tp_regime_iva= string_field(view_order=29 , name='  tp_regime_iva ', size=40, onlist=False)
        self.ds_tp_regime_iva= string_field(view_order=30 , name='ds_tp_regime_iva ', size=40, onlist=False)
        self.ds_tp_deducao_iva= string_field(view_order=31 , name='ds_tp_deducao_iva ', size=40, onlist=False)
        self.ds_tp_isencao_iva= string_field(view_order=32 , name='ds_tp_isencao_iva ', size=40, onlist=False)
        self.pro_rata_iva = integer_field(view_order = 33, name = 'pro_rata_iva',  size = 40, onlist=False)
        self.nu_trabalhador = integer_field(view_order = 34, name = 'Nrº Trabalhador',  size = 40, onlist=False)
        self.nu_viatura = integer_field(view_order = 35, name = 'Nrº Viatura',  size = 40, onlist=False)
        self.nat_freguesia= string_field(view_order=36 , name='Freguesia ', size=40, onlist=False)
        #print('5')
        self.tp_estado_fiscal = integer_field(view_order = 37, name = 'Tipo Estado fiscal',  size = 40, onlist=False)
        self.ds_estado_fiscal= string_field(view_order=38 , name='Estado fiscal ', size=40, onlist=False)
        self.nif_portal= string_field(view_order=39 , name='Nif no portal ', size=40, onlist=False)
        self.dt_nif_portal = date_field(view_order=40, name ='Data do nif no portal', onlist=False)
        self.importador= string_field(view_order=41 , name='importador', size=40, onlist=False)
        self.exportador= string_field(view_order=42 , name='exportador', size=40, onlist=False)
        self.gc= string_field(view_order=43 , name='gc', size=40, onlist=False)
        #print('6')
        self.nu_inps= string_field(view_order=44 , name='nu_inps', size=40, onlist=False)
        self.estado = info_field(view_order=45, name ='Estado', default='Rascunho', onlist=False, hidden=True, nolabel=True)









