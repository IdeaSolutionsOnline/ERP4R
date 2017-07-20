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
__model_name__ = 'linha_distribuicao.LinhaDistribuicao'
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

class LinhaDistribuicao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_distribuicao'
        self.__title__ = 'Linhas de Guia de Distribuição'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['produto']

        self.distribuicao = parent_field(view_order=1, name ='Distribuição', args='style:visibility="hidden"', model_name='distribuicao.Distribuicao', nolabel=True, onlist=False, column='numero')
        self.ean = string_field(view_order=2, name ='EAN', size=25)
        self.produto = choice_field(view_order=3, name ='Produto', args='required', size=40, onchange='produto_onchange', model='produto', column='nome', options="model.get_opts('Produto', '_sellable()')")
        self.quant_out = decimal_field(view_order=4, name ='Quant.Entregue', size=15, sum=True, onchange='valores_onchange', default=to_decimal(1))
        self.quant_in = decimal_field(view_order=5, name ='Quant.Devolvida', size=15, sum=True, onchange='valores_onchange', default=to_decimal(1))
        self.quant_vend = info_field(view_order=6, name ='Quant.Vendida', size=15, sum=True, default=to_decimal(1))
        self.quant_fact = function_field(view_order=7, name ='Quant.Facturada', size=15, sum=True, default=to_decimal(1))
        self.unidade = combo_field(view_order=8, name ='Unid.Venda', args='required tabIndex="-1"', onchange='produto_onchange', model='unidade', column='nome', options="model.get_opts('Unidade','()')")
        self.valor_unitario = currency_field(view_order=9, name ='Valor Unitário', size=15, sum=True, onchange='valores_onchange', default=to_decimal(1))
        self.iva = percent_field(view_order=10, name ='IVA', args=' readonly="readonly" ', size=15, nolabel=True, search=False)
        self.valor_total = currency_field(view_order=11, name ='Valor Total', size=15, sum=True, onchange='total_onchange', default=to_decimal(1))

    def get_opts(self, model, tipo):
        return eval(model + '().get_options' + tipo)

    def get_quant_fact(self, key):
        # ver aqui esta função
        value = to_decimal('0')
        #print (value)
        return round(value,0)

    def ean_onchange(self, record):
        result = record.copy()
        product = Produto(where='referencia = {ean}'.format(ean=record['ean'])).get()
        if len(product) != 0:
            product = product[0]
            for key in ['quant_in', 'quant_out', 'quant_vend', 'valor_unitario', 'valor_total']:
                result[key] = to_decimal(result[key]) 
                if result[key] <= to_decimal(0):
                    result[key] = to_decimal(1)
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_venda']
            quantidade = (to_decimal(result['quant_out']) - to_decimal(result['quant_in']))
            result['quant_vend'] = quantidade
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=product['id'], quantidade=quantidade, unidade=unidade, terminal = get_terminal('Distribuicao')))
            result['valor_total'] = quantidade * to_decimal(result['valor_unitario'])
            result['iva'] = to_decimal(product['iva'])
            result['unidade'] = unidade
            result['produto'] = product['id']
        else:
            result = {}
        return result

    def valores_onchange(self, record):
        result = record.copy()
        for key in ['quant_in', 'quant_out', 'quant_vend', 'valor_unitario', 'valor_total']:
            result[key] = to_decimal(result[key]) 
            if result[key] <= to_decimal(0):
                result[key] = to_decimal(1)
        quantidade = (to_decimal(result['quant_out']) - to_decimal(result['quant_in']))
        result['quant_vend'] = quantidade
        result['valor_total'] = quantidade * to_decimal(result['valor_unitario'])
        return result

    def produto_onchange(self, record):
        result = record.copy()
        product = Produto().get(key=record['produto'])
        if len(product) != 0:
            product = product[0]
            for key in ['quant_in', 'quant_out', 'quant_vend', 'valor_unitario', 'valor_total']:
                result[key]= to_decimal(result[key]) 
                if result[key] <= to_decimal(0):
                    result[key] = to_decimal(1)
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_venda']
            quantidade = (to_decimal(result['quant_out']) - to_decimal(result['quant_in']))
            result['quant_vend'] = quantidade
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=product['id'], quantidade=quantidade, unidade=unidade, terminal = get_terminal('Distribuicao')))
            result['valor_total'] = quantidade * to_decimal(result['valor_unitario'])
            result['iva'] = to_decimal(product['iva'])
            result['ean'] = product['referencia']
            result['unidade'] = unidade
        else:
            result={}
        return result

