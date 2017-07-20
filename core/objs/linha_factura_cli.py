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
__model_name__ = 'linha_factura_cli.LinhaFacturaCliente'
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

class LinhaFacturaCliente(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_factura_cli'
        self.__title__ = 'Linhas de Factura a Cliente'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['produto']

        self.factura_cli = parent_field(view_order=1, name ='Factura Cliente', hidden=True, model_name='factura_cli.FacturaCliente', nolabel=True, onlist=False, column='numero')
        self.ean = string_field(view_order=2, name ='EAN', size=45, onchange='ean_onchange')
        self.produto = choice_field(view_order=3, name ='Produto', args='required tabIndex="-1"', size=55, onchange='produto_onchange', model='produto', column='nome', options="model.get_opts('Produto', '_sellable()')")
        self.quantidade = decimal_field(view_order=4, name ='Quant.', size=15, sum=True, onchange='valores_onchange', default=1.0)
        self.unidade = combo_field(view_order=5, name ='Unid.Venda', args='required tabIndex="-1"', onchange='produto_onchange', model='unidade', column='nome', options="model.get_opts('Unidade','()')")
        self.valor_unitario = currency_field(view_order=6, name ='Valor Unitário', args='tabIndex="-1"', size=20, sum=True, onchange='valores_onchange', default=1.0)
        self.desconto = percent_field(view_order=7, name ='Desconto', args='tabIndex="-1"', size=20, onchange='valores_onchange')
        self.iva = percent_field(view_order=8, name ='IVA',default = to_decimal(15.5), args='readonly="readonly" tabIndex="-1"', size=20, nolabel=True, search=False)
        self.valor_total = currency_field(view_order=9, name ='Valor Total', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=1.0)

    def get_opts(self, model, tipo):
        return eval(model + '().get_options' + tipo)

    def ean_onchange(self, record):
        result = record.copy()
        product = Produto(where='referencia = {ean}'.format(ean=record['ean'])).get()
        if len(product) != 0:
            product = product[0]
            for key in ['quantidade', 'valor_unitario', 'valor_total']:
                result[key]= to_decimal(result[key])
                if result[key] <= 0.0:
                    result[key]=1.0
            if result['desconto'] > 0.0:
                desconto = (100-to_decimal(result['desconto']))/100
            else:
                desconto = 1.0
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_venda']
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=product['id'], quantidade=result['quantidade'], unidade=unidade, terminal = get_terminal(bottle.request.session['terminal'])))
            result['valor_total'] = result['quantidade'] * result['valor_unitario'] * desconto
            result['iva'] = to_decimal(product['iva'])
            result['unidade'] = unidade
            result['produto'] = product['id']
        else:
            result = {}
        return result

    def produto_onchange(self, record):
        result = record.copy()
        #print ('estou em product_onchange', result)
        product = Produto().get(key=record['produto'])
        if len(product) != 0:
            product = product[0]
            for key in ['quantidade', 'valor_unitario', 'valor_total']:
                result[key]= to_decimal(result[key])
                if result[key] <= to_decimal(0):
                    result[key] = to_decimal(1)
            if to_decimal(result['desconto']) > to_decimal(0):
                desconto = to_decimal((100-to_decimal(result['desconto']))/100)
            else:
                desconto = to_decimal(1)
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_venda']
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=product['id'], quantidade=result['quantidade'], unidade=unidade, terminal = get_terminal(bottle.request.session['terminal'])))
            result['valor_total'] = result['quantidade'] * result['valor_unitario'] * desconto
            result['iva'] = to_decimal(product['iva'])
            result['ean'] = product['referencia']
            result['unidade'] = unidade
        else:
            result={}
        #print ('fim do produto_onchange')
        return result

    def valores_onchange(self, record):
        #O resultado é um dicionário com nomes de campos e valores que mudam consoante o valor do campo
        #Não confundir com atributos dinamicos que mudam atributos html
        result = record.copy()
        for key in ['quantidade', 'valor_unitario', 'valor_total']:
            if record[key] not in ['None', None, '']:
                record[key] = to_decimal(record[key])
            else:
                record[key] = to_decimal(0)
            if record[key] <= to_decimal(0):
                record[key] = to_decimal(1)
        if to_decimal(record['desconto']) > to_decimal(0):
            desconto = to_decimal((100-to_decimal(record['desconto']))/100)
        else:
            desconto = to_decimal(1)
        result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=result['produto'], quantidade=result['quantidade'], unidade=result['unidade'], terminal = get_terminal(bottle.request.session['terminal'])))
        result['valor_total'] = record['quantidade'] * result['valor_unitario'] * desconto
        return result
