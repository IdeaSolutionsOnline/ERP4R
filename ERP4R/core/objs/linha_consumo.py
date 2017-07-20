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
__model_name__ = 'linha_consumo.LinhaConsumo'
import auth, base_models
from orm import *
from form import *
try:
    from my_produto import Produto
except:
    from produto import Produto
try:
    from my_unidade import Unidade
except:
    from unidade import Unidade

class LinhaConsumo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_consumo'
        self.__title__ = 'Linhas de Talão de Consumo'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['descricao']

        self.consumo = parent_field(view_order=1, name ='Consumo', args='style:visibility="hidden"', model_name='consumo.Consumo', nolabel=True, onlist=False, column='numero')
        self.ean = string_field(view_order=2, name ='EAN', size=45, onchange='ean_onchange')
        self.produto = choice_field(view_order=3, name ='Produto', args='required tabIndex="-1"', size=55, onchange='produto_onchange', model='produto', column='nome', options="model.get_opts('Produto', '_sellable()')")
        self.quantidade = decimal_field(view_order=4, name ='Quant.', size=15, sum=True, onchange='valores_onchange', default=1.0)
        self.unidade = combo_field(view_order=5, name ='Unid.Venda', args='required tabIndex="-1"', onchange='produto_onchange', model='unidade', column='nome', options="model.get_opts('Unidade','()')")
        self.valor_unitario = currency_field(view_order=6, name ='Valor Unitário', args='tabIndex="-1"', size=20, sum=True, onchange='valores_onchange', default=1.0)
        self.iva = percent_field(view_order=7, name ='IVA', args='readonly="readonly" tabIndex="-1"', size=20, nolabel=True, search=False)
        self.valor_total = currency_field(view_order=8, name ='Valor Total', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=1.0)

    def get_opts(self, model, tipo):
        return eval(model + '().get_options' + tipo)

    def ean_onchange(self, record):
        result = record.copy()
        product = Produto(where='referencia = {ean}'.format(ean=record['ean'])).get()
        if len(product) != 0:
            product = product[0]
            for key in ['quantidade', 'valor_unitario', 'valor_total']:
                result[key] = to_decimal(result[key]) 
                if result[key] <= to_decimal(0):
                    result[key] = to_decimal(1)
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_venda']
            result['valor_unitario'] = to_decimal(product['preco_compra'])
            result['valor_total'] = to_decimal(result['quantidade']) * to_decimal(result['valor_unitario'])
            result['iva'] = to_decimal(product['iva'])
            result['unidade'] = unidade
            result['produto'] = product['id']
        else:
            result = {}
        return result

    def valores_onchange(self, record):
        result = record.copy()
        for key in ['quantidade', 'valor_unitario', 'valor_total']:
            result[key] = to_decimal(result[key]) 
            if result[key] <= to_decimal(0):
                result[key] = to_decimal(1)
        result['valor_total'] = result['quantidade'] * to_decimal(result['valor_unitario'])
        return result

    def produto_onchange(self, record):
        result = record.copy()
        product = Produto().get(key=record['produto'])
        if len(product) != 0:
            product = product[0]
            for key in ['quantidade', 'valor_unitario', 'valor_total']:
                result[key]= to_decimal(result[key]) 
                if result[key] <= to_decimal(0):
                    result[key] = to_decimal(1)
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_venda']
            result['valor_unitario'] = to_decimal(product['preco_compra'])
            result['valor_total'] = result['quantidade'] * result['valor_unitario']
            result['iva'] = to_decimal(product['iva'])
            result['ean'] = product['referencia']
            result['unidade'] = unidade
        else:
            result={}
        return result

