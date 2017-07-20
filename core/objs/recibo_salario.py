
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
__model_name__ = 'recibo_salario.ReciboSalario'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class ReciboSalario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'recibo_salario'
        self.__title__ = 'Recibos de Salários'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['periodo']
        self.__order_by__='periodo'


        self.terceiro = choice_field(view_order=1, name ='Funcionário', args='required', size=70, model='terceiro', column='nome', options='model.get_funcionarios()')                       

        self.ano = combo_field(view_order = 2, size=45, name ='Ano', args = 'required', default = datetime.date.today().year, options='model.getAno()')

        self.periodo = combo_field(view_order = 3, size=45, name ='Periodo', default = datetime.date.today().strftime('%m'), options='model.getPeriodo()')
        
        self.estado = info_field(view_order=4, name='Estado', size=60, default='Rascunho',args='readonly')
        ########################
        self.linha_recibo_salario = list_field(view_order=5, name='Rendimentos e Descontos', condition="recibo_salario='{id}'", model_name='linha_recibo_salario.LinhaReciboSalario', list_edit_mode='inline', onlist=False)
        ########################
        self.salario = parent_field(view_order = 6, name = 'Salário', hidden=True, model_name = 'salario.Salario',nolabel=True, onlist = False, column = 'periodo')


    def get_opts(self, get_str):
        return eval(get_str)

    def getPeriodo(self):
        return [('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Nuvembro'),('12','Dezembro'),('13','Subsídio Natal'),('14','Prémio Produtividade'),('15','Subsídio Féria')]

    def getAno(self):
        options = []
        for ano in range(2014,datetime.date.today().year+2):
            options.append((str(ano), str(ano)))
        return options

    def get_funcionarios(self):
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        return Terceiro().get_funcionarios()
    
    def base_or_aces_onchange(self, record):
        result = record.copy()
        result['trib'] = to_decimal(result['base']) + to_decimal(result['aces'])       
        return result



    