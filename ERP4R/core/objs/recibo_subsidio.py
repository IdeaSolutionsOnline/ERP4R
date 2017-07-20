
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
__model_name__ = 'recibo_subsidio.ReciboSubsidio'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class ReciboSubsidio(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'recibo_subsidio'
        self.__title__ = 'Recibos de Subsídio'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['periodo']
        self.__order_by__='periodo'


        self.funcionario = string_field(view_order=2, name ='Nome', size=100, args = 'readonly', onlist=True)

        self.nif = string_field(view_order=3, name ='Nif', args = 'readonly', onlist=True)                       

        self.periodo = string_field(view_order = 4, size=45, name ='Periodo', args = 'readonly')

        self.periodo_subsidio = string_field(view_order = 5, size=45, name ='Periodo Subsídio', args = 'readonly')

        self.tipo_oper = combo_field(view_order=6, name='Tipo Operação',size=100, onlist=True, default='N', options=[('N','Normal'),('O','Omissão'),('C','Correção Favor Contribuinto'),('E','Correção Favor Estado'),('A','Anulado')])

        self.tipologia = combo_field(view_order=7, name='Categoria',size=50, onlist=True, args='readonly', default='A.1', options=[('A.1','Trab. Dependente'),('A.2','Pensionista'),('A.3','Trab. Isento'),('A.4','Não Residente')])   
        
        self.salario_base = currency_field(view_order=8, name ='Rendimento Base', args = 'readonly', size=60, onlist=False, sum=True,onchange='base_or_aces_onchange')        
       
        self.salario_aces = currency_field(view_order=9, name ='Rend. Acessório',size=60, onlist=False,args = 'readonly', sum=True, onchange='base_or_aces_onchange')

        self.salario_isento = currency_field(view_order=10, name ='Rend. Isento', size=60, onlist=False,args = 'readonly', sum=False)

        self.salario_trib = currency_field(view_order=11, name ='Rend. Tributavel', size=60, args = 'readonly', sum=True, onlist=True)        

        self.valor_retido = currency_field(view_order=12, name ='Valor Retido', args = 'readonly', size=60, sum=True, onlist=True)
        
        self.inps_funcionario = currency_field(view_order=13, name ='INPS Funcionario', args = 'readonly', size=60, sum=True, onlist=True) 

        self.inps_entidade = currency_field(view_order=14, name ='INPS Entidade', args = 'readonly', size=60, sum=True, onlist=True)

        self.soat = currency_field(view_order=15, name ='SOAT', args = 'readonly', size=60, sum=True, onlist=True)

        self.sindicato = currency_field(view_order=16, name ='Sindicato', args = 'readonly', size=60, sum=True) 

        self.outros_retencoes = currency_field(view_order=17, name ='Outras Retenções', args = 'readonly', size=60, sum=True, onlist=False)        

        self.estado = info_field(view_order=18, name='Estado', size=60, default='Rascunho',args='readonly')

        self.salario = parent_field(view_order = 19, name = 'Salário', hidden=True, model_name = 'salario.Salario',nolabel=True, onlist = False, column = 'id')

        #self.terceiro = parent_field(view_order = 20, name = 'Terceiro', hidden=True, model_name = 'terceiro.Terceiro',nolabel=True, onlist = False, column = 'id')

       
    
    def base_or_aces_onchange(self, record):
        result = record.copy()
        result['trib'] = to_decimal(result['base']) + to_decimal(result['aces'])       
        return result

    def getPeriodo(self):
        options = []
        for ano in range(datetime.date.today().year-2,datetime.date.today().year+2):
            for mes in ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15'):
                valor = "{ano}-{mes}".format(ano=ano, mes=mes)
                options.append((str(valor), str(valor)))
        return options

    def getFuncionarios(self):
        return Terceiro().get_funcionarios()

