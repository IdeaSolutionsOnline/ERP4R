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
__model_name__ = 'caixa.Caixa'
import auth, base_models
from orm import *
from form import *
try:
    from my_terminal import Terminal
except:
    from terminal import Terminal

class Caixa(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'caixa'
        self.__title__ = 'Movimentos de Caixa'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(caixa.numero) DESC'
        self.__workflow__ = (
            'estado', {'Aberta':['Fechar','Imprimir'], 'Impresso':['Fechar','Imprimir','Cancelar'], 'Fechada':['Cancelar','Imprimir'], 'Cancelada':['Aberta']}
            )
        self.__workflow_auth__ = {
            'Fechar':['Caixa'],
            'Imprimir':['All'],
            'Rascunho':['Gestor'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__no_edit__ = [
            ('estado', ['Fechada','Cancelada'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Caixa'],
            'create':['Caixa'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data_inicial = date_field(view_order = 1, name = 'Data Inicial', default = datetime.date.today(), args = 'required')
        self.data_final = date_field(view_order = 2, name = 'Data Final')
        #self.hora_inicial = time_field(view_order = 3, name = 'Hora Inicial', default = time.strftime('%H:%M'), args = 'required')
        self.hora_final = time_field(view_order = 4, name = 'Hora Final')
        self.valor_inicial = currency_field(view_order = 5, name = 'Valor Inicial')
        self.valor_final = currency_field(view_order = 6, name = 'Valor Final', search = False)
        self.numero = info_field(view_order = 7, name = 'Número')
        self.estado = info_field(view_order = 8, name = 'Estado', default = 'Aberta')
        self.saldo = function_field(view_order = 9, name = 'Saldo', size = 20, sum = True, search = False)
        self.total = function_field(view_order = 10, name = 'Total Em Caixa', size = 20, sum = True, search = False)
        self.vendedor = parent_field(view_order = 11, name='Vendedor', size = 40, onlist = False, default = "session['user']", model_name = 'users.Users', column = 'nome')
        self.terminal = combo_field(view_order = 12, name = 'Terminal', args = 'required', model = 'terminal', column = 'name', options = 'model.get_terminal()')
        self.linha_caixa = list_field(view_order = 13, name = 'Linhas de Movimento de Caixa', condition = "caixa = '{id}'", model_name = 'linha_caixa.LinhaCaixa', list_edit_mode = 'inline', onlist = False)

    def get_terminal(self):
        return Terminal().get_options()

    def record_lines(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            try:
                from my_linha_caixa import LinhaCaixa
            except:
                from linha_caixa import LinhaCaixa
            record_lines = LinhaCaixa(where = "caixa = '{caixa}'".format(caixa = key)).get()
            return record_lines
        return erp_cache.get(key = self.__model_name__ + str(key), createfunc = get_results)

    def get_total(self, key):
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['entrada']) - to_decimal(line['saida'])
        return value

    def get_saldo(self, key):
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['entrada']) - to_decimal(line['saida'])
        return value

    def Imprimir(self, key, window_id):
        #Acção por defeito para imprimir o documento base
        #Deverá mudar o estado para impresso
        template = 'caixa'
        record = get_records_to_print(key = key, model = self)
        valor_documentos = to_decimal(0)
        documentos = {}
        metodos_pagamento = {}
        #print (record)
        #print ('im in imprimir')
        for line in record['linha_caixa']:
            valor_documentos = valor_documentos + to_decimal(line['entrada'])
            valor_documentos = valor_documentos - to_decimal(line['saida'])
            documento = line['documento'][0]
            metodo_pagamento = line['metodo']
            if documento in documentos:
                documentos[documento].append(str(line['num_doc']))
            else:
                documentos[documento] = [str(line['num_doc'])]
            if metodo_pagamento in metodos_pagamento:
                metodos_pagamento[metodo_pagamento] += to_decimal(line['entrada']) - to_decimal(line['saida'])
            else:
                metodos_pagamento[metodo_pagamento] = to_decimal(line['entrada']) - to_decimal(line['saida'])
        for metodo_pagamento in metodos_pagamento:
            metodos_pagamento[metodo_pagamento] = format_number(metodos_pagamento[metodo_pagamento])
        record['metodos_pagamento'] = metodos_pagamento
        diferenca = to_decimal(record['valor_final']) - to_decimal(record['valor_inicial']) - valor_documentos
        record['valor_inicial'] = format_number(record['valor_inicial'])
        record['valor_final'] = format_number(record['valor_final'])
        record['diferenca'] = format_number(diferenca)
        record['valor_facturado'] = format_number(valor_documentos)
        #print (documentos)
        for doc in documentos:
            quantidade_text = 'sum(linha_{table}.quantidade)'.format(table = doc)
            valor_text = 'sum(linha_{table}.valor_total)'.format(table = doc)
            sql = """SELECT produto.nome AS produto, {quantidade_text} AS quantidade, {valor_text} AS valor FROM linha_{table} JOIN {table} ON linha_{table}.{table} = {table}.id JOIN produto ON produto.id = linha_{table}.produto WHERE {table}.numero {num_doc} GROUP BY produto.nome""".format(table = doc, num_doc = to_tuple(documentos[doc]), quantidade_text = quantidade_text, valor_text = valor_text)
            #print ('o nosso sql e ', sql)
            produtos = get(sql)
        #print (produtos)
        record['produtos'] = produtos
        return Report(record = record, report_template = template).show()

    def Fechar(self, key, window_id):
        #Fecha a caixa
        if key != 'None':
            self.kargs = get_model_record(model = self, key = key)
            if not self.kargs['numero']:
                self.kargs['numero'] = base_models.Sequence().get_sequence('caixa')
            if not self.kargs['data_final']:
                self.kargs['data_final'] = datetime.date.today()
            if not self.kargs['hora_final']:
                self.kargs['hora_final'] = time.strftime('%H:%M')
            self.kargs['estado'] = 'Fechada'
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)
            return form_edit(window_id = window_id).show()

    def Cancelar(self, key, window_id):
        #Cancela a folha de caixa
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Cancelada'
        self.put()
        return form_edit(window_id = window_id).show()

    def Aberta(self, key, window_id):
        #Cancela a folha de caixa
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Aberta'
        self.put()
        return form_edit(window_id = window_id).show()
