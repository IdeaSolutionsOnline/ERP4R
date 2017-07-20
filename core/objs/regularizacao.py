# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
A Regularizacao regista regularizacaos de materiais em armazem, é lançada pelo fiel de armazem ou pelo escriturário mas sempre confirmada pelo fiel de armazem
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'regularizacao.Regularizacao'
import auth, base_models
from orm import *
from form import *
try:
    from my_armazem import Armazem
except:
    from armazem import Armazem

class Regularizacao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'regularizacao'
        self.__title__ = 'Guias de Regularizacao'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(regularizacao.numero) DESC'
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
            ('Linhas de Guia de Regularizacao', ['linha_regularizacao']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name ='Data', args='required ', default=datetime.date.today())
        self.numero = info_field(view_order=2, name ='Número', args='readonly')
        self.notas = string_field(view_order=3, name ='Notas', args='autocomplete="on"', size=60, onlist=False)
        self.estado = info_field(view_order=4, name ='Estado', default='Rascunho')
        self.armazem = combo_field(view_order=5, name ='Armazem', args='required', size=40, model='armazem', column='nome', options='model.get_armazens()')
        self.movs_contab = list_field(view_order=6, name ='Movimentos Contab.', condition="documento='regularizacao' and num_doc={numero}", model_name='movimento.Movimento', list_edit_mode='edit', onlist = False)
        self.movs_stock = list_field(view_order=7, name ='Movimentos Stock', condition="documento='regularizacao' and num_doc={numero}", model_name='stock.Stock', list_edit_mode='edit', onlist = False)
        self.linha_regularizacao = list_field(view_order=8, name ='Linhas de Regularizacao', condition="regularizacao='{id}'", model_name='linha_regularizacao.LinhaRegularizacao', list_edit_mode='inline', onlist = False)

    def get_armazens(self):
        return Armazem().get_options()

    def Imprimir(self, key, window_id):
        template = 'regularizacao'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()

    def Confirmar(self, key, window_id):
        # Gera movimento de Stock (movimenta o armazem escolhido por contrapartida de regularizacoes)
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('regularizacao')
        periodo = None
        try:
            from my_periodo import Periodo
        except:
            from periodo import Periodo
        periodo = Periodo().get_periodo(data=self.kargs['data'])
        try:
            from my_stock import Stock
        except:
            from stock import Stock
        stock = Stock(data=self.kargs['data'], numero=base_models.Sequence().get_sequence('stock'), num_doc=self.kargs['numero'], descricao='Nossa Nota de Regularização', documento='regularizacao', periodo=periodo, estado='Confirmado', user=self.kargs['user']).put()
        try:
            from my_linha_regularizacao import LinhaRegularizacao
        except:
            from linha_regularizacao import LinhaRegularizacao
        record_lines = LinhaRegularizacao(where="regularizacao = '{regularizacao}'".format(regularizacao=self.kargs['id'])).get()
        if record_lines:
            try:
                from my_armazem import Armazem
            except:
                from armazem import Armazem
            armazem_regularizacao = Armazem(where="tipo='regularizacoes'").get()[0]['id']
            try:
                from my_linha_stock import LinhaStock
            except:
                from linha_stock import LinhaStock
            try:
                from my_produto import Produto
            except:
                from produto import Produto
            for line in record_lines:
                product = Produto().get(key=line['produto'])[0]
                descricao = product['nome']
                quantidade = to_decimal(line['diferenca'])
                if quantidade < 0:
                    armazem_in = armazem_regularizacao
                    armazem_out = self.kargs['armazem']
                    quantidade = - quantidade
                else:
                    armazem_in = self.kargs['armazem']
                    armazem_out = armazem_regularizacao
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_in, quant_saida=0.0, quant_entrada=quantidade, user=self.kargs['user']).put()
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_out, quant_saida=quantidade, quant_entrada=0.0, user=self.kargs['user']).put()
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)
            return form_edit(window_id = window_id).show()
        else:
            return error_message('Não pode confirmar Regularizações sem linhas de Regularização! \n')

    def Cancelar(self, key, window_id):
        # Estorna movimento contabilistico
        # Estorna movimento de stock
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        try:
            from my_linha_movimento import LinhaMovimento
        except:
            from linha_movimento import LinhaMovimento
        movimentos = Movimento(where="documento='regularizacao' and num_doc={num_doc} ".format(num_doc=self.kargs['numero'])).get()
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
                linhas_movimento = LinhaMovimento(where="movimento='{movimento}'".format(movimento=movimento['id'])).get()
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
        try:
            from my_stock import Stock
        except:
            from stock import Stock
        try:
            from my_linha_stock import LinhaStock
        except:
            from linha_stock import LinhaStock
        stocks = Stock(where="documento='regularizacao' and num_doc={num_doc} ".format(num_doc=self.kargs['numero'])).get()
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
                linhas_stock = LinhaStock(where="stock={stock}".format(stock=stock['id'])).get()
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
        return form_edit(window_id = window_id).show()
