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
__model_name__ = 'linha_factura_forn.LinhaFacturaFornecedor'
import auth, base_models
from orm import *
from form import *
try:
    from produto import Produto
except:
    from produto import Produto
try:
    from unidade import Unidade
except:
    from unidade import Unidade

class LinhaFacturaFornecedor(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_factura_forn'
        self.__title__ = 'Linhas de Factura de Fornecedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['produto']

        self.factura_forn = parent_field(view_order=1, name ='Factura de Fornecedor', model_name='factura_forn.FacturaFornecedor', onlist=False, column='numero')
        self.ean = string_field(view_order=2, name ='EAN', size=45, onchange='ean_onchange')
        self.produto = choice_field(view_order=3, name ='Produto', args='required tabIndex="-1"', size=55, onchange='produto_onchange', model='produto', column='nome', options="model.get_opts('Produto', '_buyable()')")
        self.quantidade = decimal_field(view_order=4, name ='Quant.', size=20, sum=True, onchange='valores_onchange', default=1.0)
        self.unidade = combo_field(view_order=5, name ='Unid.Venda', size=30, args='required tabIndex="-1"', onchange='produto_onchange', model='unidade', column='nome', options="model.get_opts('Unidade','()')")
        self.valor_unitario = currency_field(view_order=6, name ='Valor Unitário', args='tabIndex="-1"', size=20, sum=True, onchange='valores_onchange', default=1.0)
        self.desconto = percent_field(view_order=7, name ='Desconto', args='tabIndex="-1"', size=20, onchange='valores_onchange')
        self.iva = percent_field(view_order=8, name ='IVA', args='readonly="readonly" tabIndex="-1"', size=20, nolabel=True, search=False)
        self.direito_deducao = percent_field(view_order=9, name ='Dedução IVA', args='readonly="readonly" tabIndex="-1"', size=20, nolabel=True, search=False,default=0)
        self.valor_total = currency_field(view_order=10, name ='Valor Total', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=1.0)

    def get_opts(self, model, tipo):
        return eval(model + '().get_options' + tipo)

    def ean_onchange(self, record):
        result = record.copy()
        product = Produto(where='referencia = {ean}'.format(ean=record['ean'])).get()
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
                unidade = product['unidade_medida_compra']
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=product['id'], quantidade=result['quantidade'], unidade=unidade, terminal = get_terminal('MiniMercado')))
            result['valor_total'] = to_decimal(result['quantidade']) * result['valor_unitario'] * desconto
            result['iva'] = to_decimal(product['iva'])
            result['unidade'] = product['unidade_medida_padrao']
            result['produto'] = product['id']
            #este
            result['direito_deducao'] = product['deducao']
        else:
            result = {}
        return result

    def valores_onchange(self, record):
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
        result['valor_total'] = to_decimal(record['quantidade']) * to_decimal(record['valor_unitario']) * desconto
        return result

    def produto_onchange(self, record):
        result = record.copy()
        product = Produto().get(key=record['produto'])
        if len(product) != 0:
            product = product[0]
            for key in ['quantidade', 'valor_unitario', 'valor_total']:
                record[key] = to_decimal(record[key])
                if record[key] <= to_decimal(0):
                    record[key] = to_decimal(1)
            if to_decimal(record['desconto']) > to_decimal(0):
                desconto = (100-to_decimal(record['desconto']))/100
            else:
                desconto = to_decimal(1)
            desconto = to_decimal(desconto)
            quantidade = to_decimal(record['quantidade'])
            unidade = record['unidade']
            if not record['unidade']:
                unidade = product['unidade_medida_compra']
            terminal = terminal_id
            result['valor_unitario'] = Produto().get_sale_price(product['id'], terminal, quantidade, unidade)#fazer a funcao de preço de compra
            result['valor_total'] = quantidade * result['valor_unitario'] * desconto
            result['iva'] = product['iva']
            result['unidade'] = unidade
            #este
            result['direito_deducao'] = product['deducao']
        else:
            result={}
        return result

