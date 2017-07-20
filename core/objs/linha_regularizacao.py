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
__model_name__ = 'linha_regularizacao.LinhaRegularizacao'
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

class LinhaRegularizacao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_regularizacao'
        self.__title__ = 'Linhas de Regularizacao'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['produto']

        self.regularizacao = parent_field(view_order=1, name ='Regularizacao', args='style:visibility="hidden"', model_name='regularizacao.Regularizacao', nolabel=True, onlist=False, column='numero')
        self.produto = choice_field(view_order=2, name ='Produto', args='required', size=60, onchange='produto_onchange', model='produto', column='nome', options="model.get_opts('Produto')")
        self.unidade = combo_field(view_order=3, name ='Unidade', args=' tabIndex="-1"', size=40, model='unidade', column='nome', options="model.get_opts('Unidade')")
        self.quant_sistema = decimal_field(view_order=4, name ='Quant.Sistema', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=to_decimal(0))
        self.quant_real = decimal_field(view_order=5, name ='Quant.Real', size=20, sum=True, onchange='valores_onchange', default=to_decimal(0))
        self.diferenca = decimal_field(view_order=6, name ='Diferença', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=to_decimal(0))
        self.valor_unitario = currency_field(view_order=7, name ='Valor Unitário', args='readonly="readonly" tabIndex="-1"', size=20, sum=True, default=to_decimal(0))
        self.valor_total = currency_field(view_order=8, name ='Valor Total', args=' readonly="readonly" tabIndex="-1"', size=20, sum=True, default=to_decimal(0))

    def get_opts(self, model):
        return eval(model + '().get_options()')

    def valores_onchange(self, record):
        for key in ['valor_unitario', 'valor_total', 'quant_real']:
            record[key]= to_decimal(record[key])
            if record[key] <= to_decimal(0):
                record[key] = to_decimal(0)
        result = record.copy()
        result['diferenca'] = to_decimal(result['quant_real']) - to_decimal(result['quant_sistema'])
        result['valor_total'] = to_decimal(result['diferenca']) * result['valor_unitario']
        return result

    def produto_onchange(self, record):
        for key in ['valor_unitario', 'valor_total', 'quant_real', 'quant_sistema']:
            record[key]= to_decimal(record[key]) 
            if record[key] <= to_decimal(0):
                record[key] = to_decimal(0)
        result = record.copy()
        #print (record)
        sql = """
            SELECT p.id, p.nome, p.unidade_medida_compra, p.preco_compra, ls.armazem, 
            sum(ls.quant_entrada) as quant_entrada, sum(quant_saida) as quant_saida
            FROM produto AS p 
            LEFT JOIN linha_stock AS ls
            ON ls.produto = p.id
            LEFT JOIN armazem AS a
            ON a.id = ls.armazem
            WHERE p.id = '{produto}'
            GROUP BY ls.armazem, p.id, p.nome
            ORDER BY p.nome
            """.format(produto=record['produto'])
        #print (sql)
        products = run_sql(sql)
        #print(products)
        result['unidade'] = products[0]['unidade_medida_compra']
        #o preço unitario tem que vir da função do produto
        result['valor_unitario'] = to_decimal(products[0]['preco_compra'])
        for product in products:
            if str(product['armazem']) == str(record['armazem']):
                result['quant_sistema'] = to_decimal(product['quant_entrada'])-to_decimal(product['quant_saida'])
                result['diferenca'] = to_decimal(result['quant_real']) - to_decimal(result['quant_sistema'])
                result['valor_total'] = to_decimal(result['diferenca']) * result['valor_unitario']
        #print (result)
        return result

