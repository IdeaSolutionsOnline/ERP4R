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
__model_name__ = 'linha_leitura_chafariz.LinhaLeituraChafariz'
import auth, base_models
from orm import *
from form import *
try:
    from my_contador import Contador
except:
    from contador import Contador

class LinhaLeituraChafariz(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_leitura_chafariz'
        self.__title__ = 'Linhas de Folha de Leitura de Chafariz'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['chafariz']

        self.leitura_chafariz = parent_field(view_order=1, name ='Leitura Chafariz', args='style:visibility="hidden"', model_name='leitura_chafariz.LeituraChafariz', nolabel=True, onlist=False, column='numero')
        self.contador = choice_field(view_order=2, name ='Contador', args='required tabIndex="-1"', onchange='contador_onchange', model='contador', column='nome', options='model.get_contadores()')
        self.chafariz = parent_field(view_order=3, name ='Chafariz', size=50, model_name='terceiro.Terceiro', column='nome')
        self.leitura_anterior = decimal_field(view_order=4, name ='Leitura anterior', args='readonly="readonly" tabIndex="-1"', size=20, default=1.0)
        self.leitura_actual = decimal_field(view_order=5, name ='Leitura actual', size=20, default=1.0)
        self.hora = time_field(view_order=6, name ='Hora Leitura', args='required ', default=time.strftime('%H:%M:%S'))
        self.factura = parent_field(view_order=7, name ='Factura', model_name='factura_cli.FacturaCliente', search=False, column='numero')

    def get_contadores(self):
        return Contador().get_options()

    def contador_onchange(self, record):
        result = record.copy()
        product = Produto().get(key=record['produto'])
        if len(product) != 0:
            product = product[0]
            for key in ['quantidade', 'valor_unitario', 'valor_total']:
                result[key]= to_decimal(result[key]) 
                if result[key] <= to_decimal(0):
                    result[key]= to_decimal(0)
            if to_decimal(result['desconto']) > to_decimal(0):
                desconto = (100-to_decimal(result['desconto']))/100
            else:
                desconto = to_decimal(0)
            result['valor_unitario'] = to_decimal(Produto().get_sale_price(produto=product['id'], quantidade=result['quantidade'], unidade=product['unidade_medida_padrao'], terminal = get_terminal('Loja')))
            result['valor_total'] = result['quantidade'] * result['valor_unitario'] * desconto
            result['iva'] = to_decimal(product['iva'])
            result['unidade'] = product['unidade_medida_padrao']
        else:
            result={}
        return result

