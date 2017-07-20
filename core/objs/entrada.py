# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
A Entrada regista entrada de materiais em armazem, é lançada pelo fiel de armazem ou pelo escritorário mas sempre confirmada pelo fiel de armazem, movimenta a conta de mercadorias contra a conta de compras. e movimenta de stock virtual para stock real no armazem em questão ou seja do fornecedor para o armazém escolhido
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'entrada.Entrada'
import auth, base_models
from orm import *
from form import *
try:
    from my_armazem import Armazem
except:
    from armazem import Armazem
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class Entrada(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'entrada'
        self.__title__ = 'Guias de Entrada'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(entrada.numero) DESC'

        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir', 'Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Vendedor'],
            'Imprimir':['All'],
            'Cancelar':['Gestor'],
            'Rascunho':['Gestor'],
            'full_access':['Gestor']
            }
        self.__tabs__ = [
            ('Linhas de Guia de Entrada', ['linha_entrada']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor','Caixa'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name ='Data', args='required ', default=datetime.date.today())
        self.numero = info_field(view_order=2, name ='Número', args='readonly')
        self.notas = string_field(view_order=3, name ='Notas', args='autocomplete="on"', size=80, onlist=False)
        self.armazem = combo_field(view_order=4, name ='Armazem', args='required', size=80, model='armazem', column='nome', options='model.get_armazens()')
        self.fornecedor = choice_field(view_order=5, name ='Fornecedor', size=80, model='terceiro', column='nome', options='model.get_fornecedores()')
        self.total_iva = function_field(view_order=6, name ='Total IVA', size=20, sum=True, search=False)
        self.total = function_field(view_order=7, name ='Total', size=20, sum=True, search=False)
        self.movs_contab = list_field(view_order=8, name ='Movimentos Contab.', condition="documento='entrada' and num_doc={numero}", model_name='movimento.Movimento', list_edit_mode='edit', onlist = False)
        self.movs_stock = list_field(view_order=9, name ='Movimentos Stock', condition="documento='entrada' and num_doc={numero}", model_name='stock.Stock', list_edit_mode='edit', onlist = False)
        self.estado = info_field(view_order=10, name ='Estado', default='Rascunho')
        self.linha_entrada = list_field(view_order=11, name ='Linhas de Entrada', condition="entrada='{id}'", model_name='linha_entrada.LinhaEntrada', list_edit_mode='inline', onlist = False)

    def get_armazens(self):
        return Armazem().get_options()

    def get_fornecedores(self):
        return Terceiro().get_fornecedores()

    def get_total(self, key):
        from linha_entrada import LinhaEntrada
        value = to_decimal(0)
        record_lines = LinhaEntrada(where="entrada = '{entrada}'".format(entrada=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total'])
        return value

    def get_total_iva(self, key):
        from linha_entrada import LinhaEntrada
        value = to_decimal(0)
        record_lines = LinhaEntrada(where="entrada = '{entrada}'".format(entrada=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  to_decimal(line['iva']) / 100))
        return round(value,0)

    def Imprimir(self, key, window_id):
        template = 'entrada'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()

    def Confirmar(self, key, window_id):
        # Gera movimento de Stock (entra no armazem por contrapartida de fornecedores)
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        self.kargs['numero'] = base_models.Sequence().get_sequence('entrada')
        periodo = None
        from periodo import Periodo
        periodos = Periodo().get()
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(self.kargs['data'])) in lista_datas:
                periodo = p['id']
        from armazem import Armazem
        armazem_fornecedor = Armazem(where="tipo='fornecedor'").get()[0]['id']
        from stock import Stock
        stock = Stock(data=self.kargs['data'], numero=base_models.Sequence().get_sequence('stock'), num_doc=self.kargs['numero'], descricao='Nossa Nota de Entrada', documento='entrada', periodo=periodo, estado='Confirmado', user=self.kargs['user']).put()
        from linha_entrada import LinhaEntrada
        record_lines = LinhaEntrada(where="entrada = '{entrada}'".format(entrada=self.kargs['id'])).get()
        if record_lines:
            from linha_stock import LinhaStock
            from produto import Produto
            for line in record_lines:
                quantidade = to_decimal(line['quantidade'])
                product = Produto().get(key=line['produto'])[0]
                descricao = product['nome']
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=self.kargs['armazem'], quant_saida=to_decimal(0), quant_entrada=quantidade, user=self.kargs['user']).put()
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_fornecedor, quant_saida=quantidade, quant_entrada=to_decimal(0), user=self.kargs['user']).put()
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)
            return form_edit(window_id=window_id).show()
        else:
            return error_message('Não pode confirmar entradas sem linhas de Entrada! \n')

    def Cancelar(self, key, window_id):
        # Estorna movimento contabilistico
        # Estorna movimento de stock
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        from movimento import Movimento
        from linha_movimento import LinhaMovimento
        movimentos = Movimento(where="documento='entrada'and num_doc={num_doc} ".format(num_doc=self.kargs['numero'])).get()
        if movimentos:
            for movimento in movimentos:
                new_movimento = {}
                new_movimento['user'] = self.kargs['user']
                for key in movimento.keys():
                    if key not in ['id', 'user_create', 'user_change', 'date_create', 'date_change','numero','descricao']:
                        new_movimento[key] = movimento[key]
                new_movimento['numero'] = base_models.Sequence().get_sequence('movimento')
                new_movimento['descricao'] = 'Anulação de ' + movimento['descricao']
                new_movimento_id = Movimento(**new_movimento).put()
                linhas_movimento = LinhaMovimento(where="movimento={movimento}".format(movimento=movimento['id'])).get()
                for linhamovimento in linhas_movimento:
                    new_linha_movimento = {}
                    new_quant_debito = to_decimal(0)
                    new_quant_credito = to_decimal(0)
                    new_debito = to_decimal(0)
                    new_credit = to_decimal(0)
                    for key in linhamovimento.keys():
                        if key not in ['id', 'user_create', 'user_change', 'date_create', 'date_change','movimento']:
                            if key == 'quant_debito':
                                new_quant_credito = linhamovimento[key]
                            elif key == 'quant_credito':
                                new_quant_debito = linhamovimento[key]
                            elif key == 'credito':
                                new_debito = linhamovimento[key]
                            elif key == 'debito':
                                new_credito = linhamovimento[key]
                            else:
                                new_linha_movimento[key] = linhamovimento[key]
                    new_linha_movimento['movimento'] = new_movimento_id
                    new_linha_movimento['quant_debito'] = new_quant_debito
                    new_linha_movimento['quant_credito'] = new_quant_credito
                    new_linha_movimento['debito'] = new_debito
                    new_linha_movimento['credito'] = new_credito
                    new_linha_movimento['user'] = self.kargs['user']
                    LinhaMovimento(**new_linha_movimento).put()
        from stock import Stock
        from linha_stock import LinhaStock
        stocks = Stock(where="documento='entrada' and num_doc={num_doc} ".format(num_doc=self.kargs['numero'])).get()
        if stocks:
            for stock in stocks:
                new_stock = {}
                new_stock['user'] = self.kargs['user']
                for key in stock.keys():
                    if key not in ['id', 'user_create', 'user_change', 'date_create', 'date_change','numero']:
                        new_stock[key] = stock[key]
                new_stock['numero'] = base_models.Sequence().get_sequence('stock')
                new_stock['descricao'] = 'Anulação de ' + stock['descricao']
                new_stock_id = Stock(**new_stock).put()
                linhas_stock = LinhaStock(where="stock='{stock}'".format(stock=stock['id'])).get()
                for linhastock in linhas_stock:
                    new_linha_stock = {}
                    new_quant_entrada = to_decimal(0)
                    new_quant_saida = to_decimal(0)
                    for key in linhastock.keys():
                        if key not in ['id', 'user_create', 'user_change', 'date_create', 'date_change','stock']:
                            if key == 'quant_entrada':
                                new_quant_saida = linhastock[key]
                            elif key == 'quant_saida':
                                new_quant_entrada = linhastock[key]
                            else:
                                new_linha_stock[key] = linhastock[key]
                    new_linha_stock['stock'] = new_stock_id
                    new_linha_stock['quant_entrada'] = new_quant_entrada
                    new_linha_stock['quant_saida'] = new_quant_saida
                    new_linha_stock['user'] = self.kargs['user']
                    LinhaStock(**new_linha_stock).put()
        self.put()
        ctx_dict = get_context(window_id)
        ctx_dict['main_key'] = self.kargs['id']
        set_context(window_id, ctx_dict)
        return form_edit(window_id=window_id).show()
