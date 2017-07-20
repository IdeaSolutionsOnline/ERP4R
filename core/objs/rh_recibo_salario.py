
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
__model_name__ = 'rh_recibo_salario.RHReciboSalario'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro
from rh_tipo_rendimento import RHTipoRendimento


class RHReciboSalario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_recibo_salario'
        self.__title__ = 'Recibo de Salário'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['periodo']
        self.__order_by__='periodo'


        self.terceiro = choice_field(view_order=1, name ='Funcionário', args='required', size=70, model='terceiro', column='nome', options='model.get_funcionarios()')                       

        self.ano = combo_field(view_order = 2, size=45, name ='Ano', args = 'required', default = datetime.date.today().year, options='model.getAno()')

        self.periodo = combo_field(view_order = 3, size=45, name ='Periodo', default = datetime.date.today().strftime('%m'), options='model.getPeriodo()')
        
        self.tipo_funcionario = combo_field(view_order=4,name='Tipo Funcionario', size=45, onlist=False, options=[('dependente','Dependente'),('pensionista','Pensionista'),('isento','Isento'),('nao_residente','Não Residente')])

        self.estado = info_field(view_order=5, name='Estado', size=60, default='Rascunho',args='readonly')
        ########################
        self.rh_linha_recibo_salario = list_field(view_order=6, name='Rendimentos e Descontos', condition="rh_recibo_salario='{id}'", model_name='rh_linha_recibo_salario.RHLinhaReciboSalario', list_edit_mode='inline', onlist=False)
        
        self.rh_gasto_suportado = list_field(view_order=7, name='Gastos Suportados Pela Entidades', condition="rh_recibo_salario='{id}'", model_name='rh_gasto_suportado.RHGastoSuportado', list_edit_mode='popup', onlist=False)
        ########################
        self.rh_folha_salario = parent_field(view_order = 8, name = 'Salário', hidden=True, model_name = 'rh_folha_salario.RHFolhaSalario',nolabel=True, onlist = False, column = 'periodo')


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

    def record_lines(self, key):
        def get_results():            
            from rh_linha_recibo_salario import RHLinhaReciboSalario
            record_lines = RHLinhaReciboSalario(where="rh_recibo_salario = '{id}'".format(id=key)).get()
            return record_lines
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)
    
    def get_rendimentosAcessorios(self, key):
        total = to_decimal(0)
        linhas = self.record_lines(key=key)
        for linha in linhas:
            if linha['origem']=='rendimento':
                total+=to_decimal(linha['valor'])
        return total

    def get_rendimentosTributaveis(self, key):
        total = to_decimal(0)
        linhas = self.record_lines(key=key)
        for linha in linhas: 
            if linha['origem']=='rendimento':                
                total+=to_decimal(linha['parte_trib'])
        return total

    def get_rendimentosIsentos(self, key):
        total = to_decimal(0)
        linhas = self.record_lines(key=key)
        for linha in linhas: 
            if linha['origem']=='rendimento':                
                total+=to_decimal(linha['valor'])-to_decimal(linha['parte_trib'])
        return total

    def get_salario(self, key):
        linhas = self.record_lines(key=key)
        for linha in linhas: 
            if linha['origem']=='salario':
                return to_decimal(linha['valor'])
        return to_decimal(0)

    def get_retencao(self, key):
        linhas = self.record_lines(key=key)
        for linha in linhas: 
            if linha['origem']=='iur':
                return -to_decimal(linha['valor'])
        return to_decimal(0)

    def get_segurancaSocial(self, key):
        linhas = self.record_lines(key=key)
        for linha in linhas: 
            if linha['origem']=='inps':
                return -to_decimal(linha['valor'])
        return to_decimal(0)

    def get_outrosRetencoes(self, key):
        total = to_decimal(0)
        linhas = self.record_lines(key=key)
        for linha in linhas: 
            if ((linha['origem']=='desconto') or (linha['origem']=='outros_descontos')):
                total+=-to_decimal(linha['valor'])
        return total





    