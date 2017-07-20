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
__model_name__ = 'linha_leitura.LinhaLeitura'
import auth, base_models
from orm import *
from form import *
try:
    from my_contador import Contador
except:
    from contador import Contador

class LinhaLeitura(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_leitura'
        self.__title__ = 'Linhas de Folha de Leitura'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'linha_leitura.contador'#aqui penso que ainda temos a questão de que o order by que desejamos é o nome da relação e não o id por isso deveria ser contador.nome ou codigo e nao linha_leitura.contador
        self.__get_options__ = ['leitura']
        self.leitura_anterior_values = {}

        self.leitura = parent_field(view_order=1, name ='Leituras', args='style:visibility="hidden"', model_name='leitura.Leitura', nolabel=True, onlist=False, column='numero')
        self.contador = choice_field(view_order=2, name ='Contador', args='required tabIndex="-1"', model='contador', size=40, column='nome', options='model.get_contadores()')
        self.cliente = function_field(view_order=3, name ='Cliente', size=50)#, save=True
        self.leitura_anterior = function_field(view_order=4, name ='Leitura anterior', size=20, search=False)#, save=True
        self.leitura_actual = decimal_field(view_order=5, name ='Leitura actual', size=20, default=to_decimal(0), search=False)
        self.consumo = function_field(view_order=6, name ='Consumo', size=20, sum=True, search=False)#, save=True
        self.hora = time_field(view_order=7, name ='Hora')#, default=time.strftime('%H:%M:%S')
        self.factura = parent_field(view_order=8, name ='Factura', model_name='factura_cli.FacturaCliente', search=False, column='numero')

    def get_contadores(self):
        return Contador().get_options()

    def get_consumo(self, key):
        record = self.get(key=key)[0]
        #print (record)
        if not record['leitura_actual']:
            record['leitura_actual'] = to_decimal(0)
        #if not record['leitura_anterior']:
        #   record['leitura_anterior'] = to_decimal(0)
        #print (self.leitura_anterior_values)
        value = record['leitura_actual'] - self.leitura_anterior_values[key]
        return value

    def get_leitura_anterior(self, key):
        record = self.get(key=key)[0]
        sql = """
            SELECT max(linha_leitura.leitura_actual) as leitura_actual FROM linha_leitura 
            JOIN leitura
            ON leitura.id = linha_leitura.leitura
            WHERE leitura.data < (SELECT data FROM leitura WHERE id = '{leitura}') 
            AND leitura.zona = (SELECT zona FROM leitura WHERE id = '{leitura}')
            AND linha_leitura.contador = {contador}""".format(leitura = record['leitura'], contador = record['contador'])
        leitura_anterior = run_sql(sql)
        if leitura_anterior and leitura_anterior[0]['leitura_actual'] != None:
            value = leitura_anterior[0]['leitura_actual']
        else:
            value = 0
        self.leitura_anterior_values[key] = value
        return value

    def get_cliente(self, key):
        record = self.get(key=key)[0]
        sql = """
        SELECT terceiro.nome FROM terceiro 
        JOIN contrato
        ON contrato.cliente = terceiro.id
        JOIN contador_contrato
        ON contador_contrato.contrato = contrato.id
        WHERE contador_contrato.contador = '{contador}'
        """.format(contador=record['contador'])
        value = run_sql(sql)[0]['nome']
        return value

