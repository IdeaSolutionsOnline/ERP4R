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
__model_name__ = 'linha_entrega.LinhaEntrega'
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

class LinhaEntrega(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_entrega'
        self.__title__ = 'Linhas de Entrega'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['produto']

        self.entrega = parent_field(view_order=1, name='Entrega', args='style:visibility="hidden"', model_name='entrega.Entrega', nolabel=True, onlist=False, column='numero')
        self.ean = string_field(view_order=2, name='EAN', size=45, onchange='ean_onchange')
        self.produto = choice_field(view_order=3, name='Produto', args='required tabIndex="-1"', size=60, onchange='produto_onchange', model='produto', column='nome', options="model.get_opts('Produto', '_sellable()')")
        self.quantidade = decimal_field(view_order=4, name='Quantidade', size=20, sum=True, onchange='valores_onchange', default=to_decimal(1))
        self.unidade = combo_field(view_order=5, name='Unidade', args='required tabIndex="-1"', size=40, onchange='produto_onchange', model='unidade', column='nome', options="model.get_opts('Unidade','()')")
        self.valor_unitario = currency_field(view_order=6, name='Valor Unitário', args='tabIndex="-1"', size=20, sum=True, onchange='valores_onchange', default=to_decimal(1))
        self.desconto = percent_field(view_order=7, name='Desconto', args='tabIndex="-1"', size=20, onchange='valores_onchange')
        self.iva = percent_field(view_order=8, name='IVA', args='readonly="readonly" tabIndex="-1"', size=20, nolabel=True, search=False)
        self.valor_total = currency_field(view_order=9, name='Valor Total', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=to_decimal(1))

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
            terminal = get_terminal(bottle.request.session['terminal'])
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(product['id'], terminal, result['quantidade'], unidade))
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
        result['valor_total'] = to_decimal(result['quantidade']) * to_decimal(result['valor_unitario'])
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
            terminal = get_terminal(bottle.request.session['terminal'])
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(product['id'], terminal, result['quantidade'], unidade))
            result['valor_total'] = result['quantidade'] * result['valor_unitario']
            result['iva'] = to_decimal(product['iva'])
            result['ean'] = product['referencia']
            result['unidade'] = unidade
        else:
            result={}
        return result

