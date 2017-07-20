# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""ERP+"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'entrega.Entrega'
import base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro


class Entrega(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'entrega'
        self.__title__ = 'Guias de Entrega'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(entrega.numero) DESC'
        self.__workflow__ = (
            'estado', {
                'Rascunho': ['Confirmar'],
                'Confirmado': ['Imprimir', 'Pagar', 'Facturar', 'Cancelar'],
                'Facturado': ['Imprimir', 'Cancelar'],
                'Pago': ['Imprimir', 'Facturar', 'Cancelar'],
                'Cancelado': ['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar': ['Vendedor'],
            'Imprimir': ['All'],
            'Pagar': ['Caixa'],
            'Facturar': ['Caixa'],
            'Cancelar': ['Gestor'],
            'Rascunho': ['Gestor'],
            'full_access': ['Gestor']
            }
        self.__workflow_context__ = {
            'Pagar': ('residual', '>', 0),
            'Facturar': ('factura', '==', None),
            }
        self.__records_view__ = [
            ]
        self.__tabs__ = [
            ('Linhas de Talão de Entrega', ['linha_entrega']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ('Recebimentos', ['pagamentos']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado', 'Pago', 'Impresso', 'Facturado', 'Cancelado'])
            ]
        self.__auth__ = {
            'read': ['All'],
            'write': ['Vendedor', 'Caixa'],
            'create': ['Vendedor'],
            'delete': ['Vendedor'],
            'full_access': ['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name='Data', args='required', default=datetime.date.today(), size=40)
        self.numero = info_field(view_order=2, name='Número', args='readonly', size=30)
        self.cliente = choice_field(view_order=3, name='Cliente', args='required', size=80, default='get_default_cliente()', model = 'terceiro', column='nome', options='model.get_clientes()')
        self.notas = string_field(view_order=4, name='Notas', args='autocomplete="on"', size=80, onlist=False, search=False)
        self.factura = parent_field(view_order=5, name='Factura', model_name='factura_cli.FacturaCliente', search=False, column='numero')
        self.estado = info_field(view_order=6, name='Estado', default='Rascunho')# dynamic_atrs='estado_dyn_attrs',
        self.vendedor = parent_field(view_order=7, name='Vendedor', size=40, default="session['user']", model_name='users.Users', onlist=False, column='nome')
        self.total_desconto = function_field(view_order=8, name='Desconto', size=20, sum=True, search=False)
        self.total_iva = function_field(view_order=9, name='Total IVA', size=20, sum=True, search=False)
        self.total = function_field(view_order=10, name='Total', size=20, sum=True, search=False)
        self.residual = currency_field(view_order=11, name='Valor Residual', args='readonly', sum=True)
        self.pagamentos = list_field(view_order=13, name='Pagamentos', condition="documento = 'entrega' and num_doc = '{numero}'", model_name='linha_caixa.LinhaCaixa', list_edit_mode='edit', onlist=False)
        self.movs_contab = list_field(view_order=14, name='Movimentos Contab.', condition="documento='entrega' and num_doc = '{numero}'", model_name='movimento.Movimento', list_edit_mode='edit', onlist=False)
        self.movs_stock = list_field(view_order=15, name='Movimentos Stock', condition="documento='entrega' and num_doc = '{numero}'", model_name='stock.Stock', list_edit_mode='edit', onlist=False)
        self.linha_entrega = list_field(view_order=16, name='Linhas de Entrega', condition="entrega='{id}'", model_name='linha_entrega.LinhaEntrega', list_edit_mode='inline', onlist=False)

    def get_clientes(self):
        return Terceiro().get_clientes()

    def get_default_cliente(self):
        default_cliente = 0
        for cliente in Terceiro().get_clientes():
            if cliente[1] == 'Clientes Gerais':
                return cliente[0]

    def record_lines(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            try:
                from my_linha_entrega import LinhaEntrega
            except:
                from linha_entrega import LinhaEntrega
            record_lines = LinhaEntrega(where = "entrega = '{entrega}'".format(entrega = key)).get()
            return record_lines
        return short_cache.get(key = self.__model_name__ + str(key), createfunc = get_results)

    def get_total(self, key):
        value = to_decimal('0')
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(str(line['valor_total']))
        return round(value, 0)

    def get_total_desconto(self, key):
        value = to_decimal('0')
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                if line['desconto']:
                    desconto = to_decimal(line['desconto'])
                else:
                    desconto = to_decimal('0')
                value += to_decimal(str(line['valor_total'])) * desconto / 100
        return round(value, 0)

    def get_total_iva(self, key):
        value = to_decimal('0')
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(str(line['valor_total'])) - (to_decimal(str(line['valor_total'])) / (1 + to_decimal(str(line['iva']))/100))
        return round(value, 0)

    def Imprimir(self, key, window_id):
        template = 'entrega'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()

    def Confirmar(self, key, window_id):
        # Gera movimento contabilistico (conta de mercadorias contra conta de gastos)
        # Gera movimento de Stock (sai de armazem por contrapartida de cliente)
        #       if key in ['None', None]:
        #           m_action = model_action(obj=self)
        #           key = m_action.save(key=None, internal=True)
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        self.kargs['residual'] = self.get_total(key=key)
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('entrega')
        try:
            from my_diario import Diario
        except:
            from diario import Diario
        diario = Diario().get_diario(diario = 'stock')
        try:
            from my_periodo import Periodo
        except:
            from periodo import Periodo
        periodo = Periodo().get_periodo(data = self.kargs['data'])
        try:
            from my_armazem import Armazem
        except:
            from armazem import Armazem
        armazem_cliente = Armazem(where = "tipo = 'cliente'").get()[0]['id']
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        terceiro = Terceiro().get(key = self.kargs['cliente'])[0]
        sujeito_iva = terceiro['sujeito_iva']
        conta_terceiro = terceiro['a_receber']
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        movimento = Movimento(data = self.kargs['data'], numero = base_models.Sequence().get_sequence('movimento'), num_doc = self.kargs['numero'], descricao = 'Nossa Nota de Entrega', diario = diario, documento = 'entrega', periodo = periodo, estado = 'Rascunho', user = self.kargs['user'], active = False).put()
        try:
            from my_stock import Stock
        except:
            from stock import Stock
        stock = Stock(data = self.kargs['data'], numero = base_models.Sequence().get_sequence('stock'), num_doc = self.kargs['numero'], descricao = 'Nossa Nota de Entrega', documento = 'entrega', periodo = periodo, estado = 'Confirmado', user = self.kargs['user']).put()
        try:
            from my_linha_entrega import LinhaEntrega
        except:
            from linha_entrega import LinhaEntrega
        record_lines = LinhaEntrega(where = "entrega = '{entrega}'".format(entrega = self.kargs['id'])).get()
        if record_lines:
            try:
                from my_linha_movimento import LinhaMovimento
            except:
                from linha_movimento import LinhaMovimento
            try:
                from my_linha_stock import LinhaStock
            except:
                from linha_stock import LinhaStock
            try:
                from my_produto import Produto
            except:
                from produto import Produto
            try:
                from my_familia_produto import FamiliaProduto
            except:
                from familia_produto import FamiliaProduto
            for line in record_lines:
                # aqui depois considerar a contabilização do desconto e do iva
                quantidade = line['quantidade']
                product = Produto().get(key = line['produto'])[0]
                contas = Produto().get_accounts(line['produto'])
                conta_mercadorias = contas['conta_mercadorias']
                conta_gastos = contas['conta_gastos']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = to_decimal('0')
                armazem_vendas = None
                familia = FamiliaProduto().get(key = product['familia'])
                if familia:
                    familia = familia[0]
                    if familia['armazem_vendas']:
                        armazem_vendas = familia['armazem_vendas']
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento = movimento, descricao = descricao, conta = conta_gastos, quant_debito = quantidade, debito = line['valor_total'], quant_credito = to_decimal('0'), credito = to_decimal('0'), user = self.kargs['user']).put()
                LinhaMovimento(movimento = movimento, descricao = descricao, conta = conta_mercadorias, quant_debito = to_decimal('0'), debito = to_decimal('0'), quant_credito = quantidade, credito = line['valor_total'], user = self.kargs['user']).put()
                LinhaStock(stock = stock, descricao = descricao, produto = line['produto'], armazem = armazem_vendas, quant_saida = quantidade, quant_entrada = to_decimal('0'), user = self.kargs['user']).put()
                LinhaStock(stock = stock, descricao = descricao, produto = line['produto'], armazem = armazem_cliente, quant_saida = to_decimal('0'), quant_entrada = quantidade, user = self.kargs['user']).put()
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)
            return form_edit(window_id = window_id).show()
        else:
            return error_message('Não pode confirmar entregas sem linhas de Entrega! \n')

    def Facturar(self, key, window_id):
        #Gera Factura em rascunho!!!
        #Aqui se o a entrega estiver paga a factura deve de alguma forma reflectir isso ou seja deve estar logo como paga
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Facturado'
        try:
            from my_factura_cli import FacturaCliente
        except:
            from factura_cli import FacturaCliente
        factura = FacturaCliente(data = self.kargs['data'], notas = self.kargs['notas'], entrega = self.kargs['id'], cliente = self.kargs['cliente'], residual = str(to_decimal('0')), estado = 'Rascunho', vendedor = self.kargs['user'], user = self.kargs['user']).put()
        self.kargs['factura'] = factura
        #Muda o movimento de não active para active
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        movimentos = Movimento(where = "documento = 'entrega' and num_doc = {num_doc} ".format(num_doc = self.kargs['id'])).get()
        if movimentos:
            for movimento in movimentos:
                movimento['active'] = 'True'
                movimento['user'] = self.kargs['user']
                Movimento(**movimento).put()
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        sujeito_iva = Terceiro(where="id=" + str(self.kargs['cliente'])).get()[0]['sujeito_iva']
        try:
            from my_linha_entrega import LinhaEntrega
        except:
            from linha_entrega import LinhaEntrega
        record_lines = LinhaEntrega(where = "entrega = '{entrega}'".format(entrega = self.kargs['id'])).get()
        if record_lines:
            try:
                from my_produto import Produto
            except:
                from produto import Produto
            try:
                from my_linha_factura_cli import LinhaFacturaCliente
            except:
                from linha_factura_cli import LinhaFacturaCliente
            for line in record_lines:
                quantidade = to_decimal(line['quantidade'])
                product = Produto().get(key = line['produto'])[0]
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = to_decimal(0)
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                iva = taxa_iva
                LinhaFacturaCliente(factura_cli = factura, unidade = line['unidade'], valor_unitario = line['valor_unitario'], produto = line['produto'], quantidade = quantidade, valor_total = line['valor_total'], desconto = line['desconto'], iva = iva, user = self.kargs['user']).put()
        self.put()
        ctx_dict = get_context(window_id)
        ctx_dict['main_key'] = self.kargs['id']
        set_context(window_id, ctx_dict)
        return form_edit(window_id = window_id).show()

    def efectuar_pagamento(self, key, window_id):
        """Esta acção efectua o pagamento"""
        self.kargs = get_model_record(model = self, key = key, force_db = True)
        self.kargs['estado'] = 'Pago'
        #print (self.kargs, self)
        #Verifica se tem caixa aberta, se não tiver abre
        #Faz o pagamento em caixa
        #print ('inicio do efectuar pagamento')
        try:
            from my_caixa import Caixa
        except:
            from caixa import Caixa
        try:
            from my_linha_caixa import LinhaCaixa
        except:
            from linha_caixa import LinhaCaixa
        #print ('1')
        try:
            from my_metodo_pagamento import MetodoPagamento
        except:
            from metodo_pagamento import MetodoPagamento
        metodos_pagamento = MetodoPagamento().get_options()
        first = True
        total_entregue = to_decimal('0')
        #print ('1.1')
        for metodo in metodos_pagamento:
            if bottle.request.forms.get(metodo[1]):
                method = to_decimal(str(bottle.request.forms.get(metodo[1])))
            else:
                method = to_decimal('0')
            if method > to_decimal('0'):
                total_entregue += to_decimal(str(bottle.request.forms.get(metodo[1])))
        #print ('1.2')
        if total_entregue >= to_decimal(str(bottle.request.forms.get('total_a_pagar'))):
            caixa = Caixa(where = "estado = 'Aberta' AND vendedor = '{user}'".format(user = self.kargs['user'])).get()
            if not caixa:
                caixa = Caixa(data_inicial = datetime.date.today(), hora_inicial = time.strftime('%H:%M'), valor_inicial = 0, valor_final = 0 , estado = 'Aberta', terminal = get_terminal(bottle.request.session['terminal']), user = self.kargs['user'], vendedor = self.kargs['user'], numero = base_models.Sequence().get_sequence('caixa')).put()
            else:
                caixa = caixa[0]['id']
            for metodo in metodos_pagamento:
                if first == True:
                    default_metodo = metodo
                    first = False
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(str(bottle.request.forms.get(metodo[1])))
                else:
                    method = to_decimal(0)
                if method > to_decimal(0):
                    linha_caixa = LinhaCaixa(caixa = caixa, descricao = 'Nossa Nota de Entrega', documento = 'entrega', num_doc = self.kargs['numero'], valor_documento = to_decimal(bottle.request.forms.get('total_a_pagar')), terceiro = self.kargs['cliente'], metodo = metodo[0], entrada = bottle.request.forms.get(metodo[1]), saida = 0, user = self.kargs['user']).put()
            #print ('1.3')
            troco = total_entregue - to_decimal(bottle.request.forms.get('total_a_pagar'))
            if troco > to_decimal(0):
                linha_caixa = LinhaCaixa(caixa = caixa, descricao = 'Nossa nota de Entrega', documento = 'entrega', num_doc = self.kargs['numero'], valor_documento = to_decimal(bottle.request.forms.get('total_a_pagar')), terceiro = self.kargs['cliente'], metodo = default_metodo[0], entrada = 0, saida = troco, user = self.kargs['user']).put()
            else:
                troco = to_decimal(0)
            #print ('2')
            self.kargs['residual'] = to_decimal(bottle.request.forms.get('total_a_pagar')) - total_entregue + troco
            #Faz o lançamento contabilistico se tiver factura como movimento activo, se não como movimento geral
            #Vê o metodo de pagamento e lança na conta adequada
            try:
                from my_diario import Diario
            except:
                from diario import Diario
            diario = Diario(where = "tipo='caixa'").get()[0]['id']
            periodo = None
            try:
                from my_periodo import Periodo
            except:
                from periodo import Periodo
            periodos = Periodo().get()
            for p in periodos:
                lista_datas = generate_dates(start_date = p['data_inicial'], end_date = p['data_final'])
                if str(format_date(self.kargs['data'])) in lista_datas:
                    periodo = p['id']
            if not periodo:
                return error_message('não existe periodo definido para a data em questão! \n')
            try:
                from my_movimento import Movimento
            except:
                from movimento import Movimento
            try:
                from my_linha_movimento import LinhaMovimento
            except:
                from linha_movimento import LinhaMovimento
            movimento = Movimento(data = datetime.date.today(), numero = base_models.Sequence().get_sequence('movimento'), num_doc = self.kargs['numero'], descricao = 'Pagamento de Nota de Entrega', diario = diario, documento = 'entrega', periodo = periodo, estado = 'Rascunho', user = self.kargs['user']).put()
            try:
                from my_terceiro import Terceiro
            except:
                from terceiro import Terceiro
            conta_cliente = Terceiro().get(key = self.kargs['cliente'])[0]['a_receber']
            for metodo in metodos_pagamento:
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(bottle.request.forms.get(metodo[1]))
                else:
                    method = to_decimal(0)
                if method > to_decimal(0):
                    conta_pagamento = MetodoPagamento().get(key = metodo[0])[0]['conta']
                    LinhaMovimento(movimento = movimento, descricao = 'Pagamento de Nota de Entrega', conta = conta_pagamento, quant_debito = to_decimal(0), debito = to_decimal(bottle.request.forms.get(metodo[1])), quant_credito = to_decimal(0), credito = to_decimal(0), user = self.kargs['user']).put()
                    LinhaMovimento(movimento = movimento, descricao = 'Pagamento de Nota de Entrega', conta = conta_cliente, quant_debito = to_decimal(0), debito = to_decimal(0), quant_credito = to_decimal(0), credito = to_decimal(bottle.request.forms.get(metodo[1])), user = self.kargs['user']).put()
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            ctx_dict['model_name'] = self.__model_name__
            set_context(window_id, ctx_dict)
            #print ('fim do efectuar pagamento')
            return form_edit(window_id = window_id).show()
        else:
            return 'Segundo as Regras da Empresa não é possivel receber valores inferiores ao valor a Pagar, Torne a efectuar o pagamento por Favor!'

    def Cancelar(self, key, window_id):
        """ Estorna movimento contabilistico
        Estorna movimento de stock
        verifica se existe factura gerada e se ouver verifica o estado e depois extorna caso confirmada ou simplesmente cancela se em rascunho
        Estorna Pagamento"""
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
        movimentos = Movimento(where="documento='entrega' and num_doc={num_doc}".format(num_doc=self.kargs['numero'])).get()
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
                    new_quant_debito = to_decimal('0')
                    new_quant_credito = to_decimal('0')
                    new_debito = to_decimal('0')
                    new_credit = to_decimal('0')
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
        stocks = Stock(where="documento='entrega' and num_doc={num_doc} ".format(num_doc=self.kargs['numero'])).get()
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
                    new_quant_entrada = to_decimal('0')
                    new_quant_saida = to_decimal('0')
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
        try:
            from my_linha_caixa import LinhaCaixa
        except:
            from linha_caixa import LinhaCaixa
        linhascaixa = LinhaCaixa(where="documento='entrega' and num_doc={num_doc} ".format(num_doc=self.kargs['numero'])).get()
        if linhascaixa:
            for linhacaixa in linhascaixa:
                new_linha_caixa = {}
                new_entrada = to_decimal('0')
                new_saida = to_decimal('0')
                for key in linhacaixa.keys():
                    if key not in ['id', 'user_create', 'user_change', 'date_create', 'date_change', 'descricao']:
                        if key == 'entrada':
                            new_saida = linhacaixa[key]
                        elif key == 'saida':
                            new_entrada = linhacaixa[key]
                        else:
                            new_linha_caixa[key] = linhacaixa[key]
                new_linha_caixa['descricao'] = 'Anulação de ' + linhacaixa['descricao']
                new_linha_caixa['entrada'] = new_entrada
                new_linha_caixa['saida'] = new_saida
                new_linha_caixa['user'] = self.kargs['user']
                LinhaCaixa(**new_linha_caixa).put()
        if self.kargs['factura']:
            try:
                from my_factura_cli import FacturaCliente
            except:
                from factura_cli import FacturaCliente
            #aqui depois validar se está confirmada e se estiver estornar o movimento contabilistico
            facturas_cli = FacturaCliente(where="id='{factura}' ".format(factura=self.kargs['factura'])).get()
            if facturas_cli:
                for factura_cli in facturas_cli:
                    factura_cli['estado'] = 'Cancelado'
                    factura_cli['user'] = self.kargs['user']
                    FacturaCliente(**factura_cli).put()
        self.put()
        ctx_dict = get_context(window_id)
        ctx_dict['main_key'] = self.kargs['id']
        set_context(window_id, ctx_dict)
        return form_edit(window_id=window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()
