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
__model_name__ = 'talao_bar.TalaoBar'
import base_models #auth,
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class TalaoBar(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'talao_bar'
        self.__title__ = 'Talão de Venda de Bar'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'talao_bar.data'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprime', 'Pagar', 'Facturar', 'Cancelar'], 'Impresso':['Imprime', 'Pagar', 'Facturar', 'Cancelar'], 'Facturado':['Imprime', 'Pagar', 'Cancelar'], 'Pago':['Imprime', 'Facturar', 'Cancelar'], 'Cancelado':[]}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Vendedor'],
            'Imprime':['All'],
            'Pagar':['Caixa'],
            'Facturar':['Caixa'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__workflow_context__ = {
            'Pagar':('residual', '>', 0),
            'Facturar':('factura', '==', None),
            }
        self.__records_view__ = [
            ('active', 'True', ['Gestor']),
            ]
        self.__tabs__ = [
            ('Linhas de Venda de Bar', ['linha_talao_bar']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ('Recebimentos',['pagamentos']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Pago','Impresso','Facturado','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor','Caixa'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name ='Data', args='required', default=datetime.date.today())
        self.numero = info_field(view_order=2, name ='Número', args='readonly')
        self.cliente = choice_field(view_order=3, name ='Cliente', args='required', size=40, model='terceiro', column='nome', options='model.get_terceiros()') # default='get_default_cliente()',
        self.notas = string_field(view_order=4, name ='Notas', args='autocomplete="on"', size=80, onlist=False, search=False)
        self.factura = parent_field(view_order=5, name ='Factura', model_name='factura_cli.FacturaCliente', search=False, column='numero')
        self.estado = info_field(view_order=6, name ='Estado', default='Rascunho')# dynamic_atrs='estado_dyn_attrs',
        self.vendedor = parent_field(view_order=7, name ='Vendedor', size=40, default="session['user']", model_name='users.Users', onlist=False, column='nome')
        self.total_desconto = function_field(view_order=8, name ='Desconto', size=20, sum=True, search=False)
        self.total_iva = function_field(view_order=9, name ='Total IVA', size=20, sum=True, search=False)
        self.total = function_field(view_order=10, name ='Total', size=20, sum=True, search=False)
        self.residual = currency_field(view_order=11, name ='Valor Residual', args='readonly', size=15, sum=True)
        self.pagamentos = list_field(view_order=13, name ='Pagamentos', condition="documento='talao_bar' and num_doc='{numero}'", model_name='linha_caixa.LinhaCaixa', list_edit_mode='edit', onlist = False)
        self.movs_contab = list_field(view_order=14, name ='Movimentos Contab.', condition="documento='talao_bar' and num_doc='{numero}'", model_name='movimento.Movimento', list_edit_mode='edit', onlist = False)
        self.movs_stock = list_field(view_order=15, name ='Movimentos Stock', condition="documento='talao_bar' and num_doc='{numero}'", model_name='stock.Stock', list_edit_mode='edit', onlist = False)
        self.linha_talao_bar = list_field(view_order=16, name ='Linhas de Talão', condition="talao_bar='{id}'", model_name='linha_talao_bar.LinhaTalaoBar', list_edit_mode='inline', onlist = False)

    def get_terceiros(self):
        return Terceiro().get_clientes()

    def get_default_client(self):
        default_cliente = 0
        for cliente in Terceiro().get_clientes():
            if cliente[1] == 'Clientes Gerais':
                return cliente[0]

#   def get_options(self, cliente=None):
#       options = []
#       opts = self.get()[1]
#       for f in get_model_fields(self):
#           if f[0] == 'cliente':
#               field=f
#       for option in opts:
#           if cliente:
#               if str(option['cliente']) == str(cliente):
#                   nome_cliente = get_field_value(record=option, field=field, model=self)['field_value'][1]
#                   options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), cliente=nome_cliente,total=self.get_total(option['id']))))
#           else:
#               nome_cliente = get_field_value(record=option, field=field, model=self)['field_value']
#               options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), cliente=nome_cliente,total=self.get_total(option['id']))))
#       return options


    def record_lines(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        #print('im in record_lines')
        def get_results():
            try:
                from my_linha_talao_bar import LinhaTalaoBar
            except:
                from linha_talao_bar import LinhaTalaoBar
            record_lines = LinhaTalaoBar(where="talao_bar = '{id}'".format(id=key)).get()
            return record_lines
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)

    def get_total(self, key):
        #print('im in get_total')
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total'])
        return value

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
        return value

    def get_total_iva(self, key):
        value = to_decimal('0')
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(str(line['valor_total'])) - (to_decimal(str(line['valor_total'])) / (1 + to_decimal(str(line['iva']))/100))
        return value

    def Imprime(self, key, window_id):
        #Acção por defeito para imprimir o documento base
        #Deverá mudar o estado para impresso
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Impresso'
        record_lines = run_sql("SELECT linha_talao_bar.*, produto.nome as nome_produto FROM linha_talao_bar JOIN produto on produto.id = linha_talao_bar.produto WHERE talao_bar = '{talao_bar}'".format(talao_bar=record['id']))
        from subprocess import Popen,PIPE
        lpr = Popen(["/usr/bin/lpr", "-P", "bar"], stdin=PIPE, shell=False, stdout=PIPE, stderr=PIPE)
        printDoc = ''
        OpenDraw=chr(27) + chr(112) + chr(0) + chr(32) + chr(32)
        Now = time.strftime("%X")
        Today = datetime.date.today()
        Line = '----------------------------------------' + '\n'
        VatLine = 'Iva Incluido a Taxa de 15.5%' + '\n'
        TanksLine = 'Obrigado pela sua visita' + '\n'
        LineAdvance=chr(27) + chr(100) + chr(5)
        StartPrinter=chr(27)+ chr(61) + chr(1) + chr(27) + chr(64) + chr(27) + "" + chr(0) + chr(27)+ chr(73) + chr(0)
        CutPaper=chr(27) + chr(86) + chr(0)
        Entreprise = 'Romarigo Vinhos Cabo Verde\n'
        street = 'Av.Porto da Praia '
        street2 = 'Lem Ferreira\n'
        Phone = '+238 263 50 00'
        NIF = '200 125 435'
        Country = 'Cabo Verde'
        City = 'Praia '
        Capital = '5.000.000$00'
        header = Entreprise + street + street2 + '\nTel: ' + Phone + '\n' + City + Country + '\nNIF:' + NIF + '\nC.Social:' + Capital + '\n'
        printDoc += OpenDraw
        printDoc += header
        printDoc += '{today:21} VD bar n.:{number:>8}\n'.format(today=str(Today), number=str(record['numero']))
        printDoc += Now + '\n'
        printDoc += Line
        total = to_decimal('0')
        for item in record_lines:
            description=item['nome_produto']
            quantity=str(int(item['quantidade']))
            value=str(item['valor_total'])
            total += to_decimal(value)
            printDoc += '{description:<25} {quantity:>5} {value:>8}\n'.format(description=description, quantity=quantity, value=value)
        printDoc += Line
        printDoc += 'Total: {total:>33}\n'.format(total=str(total))
        printDoc += Line + VatLine + TanksLine  + LineAdvance + LineAdvance + CutPaper
        lpr.communicate(printDoc.encode("utf-8"))
        TalaoBar(**record).put()
        return form_edit(key = key, window_id = window_id)

    def Confirmar(self, key, window_id):
        # Gera movimento contabilistico (conta de mercadorias contra conta de gastos)
        # Gera movimento de Stock (sai de armazem por contrapartida de cliente)
        if key in ['None', None]:
            key = get_actions(action='save', key=None, model_name=model.__model_name__, internal=True)
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Confirmado'
        record['numero'] = base_models.Sequence().get_sequence('talao_bar')
        record['residual'] = model.get_total(key=record_id)
        try:
            from my_diario import Diario
        except:
            from diario import Diario
        diario = Diario(where="tipo='stock'").get()[0]['id']
        periodo = None
        try:
            from my_periodo import Periodo
        except:
            from periodo import Periodo
        periodos = Periodo().get()[1]
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(record['data'])) in lista_datas:
                periodo = p['id']
        if not periodo:
            return error_message('não existe periodo definido para a data em questão! \n')
        try:
            from my_armazem import Armazem
        except:
            from armazem import Armazem
        armazem_cliente = Armazem(where="tipo='cliente'").get()[0]['id']
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        sujeito_iva = Terceiro(where="id='{cliente}'".format(cliente=str(record['cliente']))).get()[0]['sujeito_iva']
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Nosso Talão de Venda', diario=diario, documento='talao_bar', periodo=periodo, estado='Confirmado', user=session['user'], active=False).put()
        try:
            from my_stock import Stock
        except:
            from stock import Stock
        stock = Stock(data=record['data'], numero=base_models.Sequence().get_sequence('stock'), num_doc=record['numero'], descricao='Nosso Talão de Venda', documento='talao_bar', periodo=periodo, estado='Confirmado', user=session['user']).put()
        TalaoBar(**record).put()
        try:
            from my_linha_talao_bar import LinhaTalaoBar
        except:
            from linha_talao_bar import LinhaTalaoBar
        record_lines = LinhaTalaoBar(where="talao_bar = '{talao_bar}'".format(talao_bar=record['id'])).get()
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
                # aqui depois considerar a contabilização do desconto
                # tambem depois considerar a verificação se o total está bem calculado e logs se o preço unitário for modificado
                quantidade = to_decimal(str(line['quantidade']))
                product = Produto().get(key=line['produto'])[0]
                contas = Produto().get_accounts(line['produto'])
                conta_mercadorias = contas['conta_mercadorias']
                conta_gastos = contas['conta_gastos']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = to_decimal('0')
                armazem_vendas = None
                familia = FamiliaProduto().get(key=product['familia'])
                if familia:
                    familia = familia[0]
                    if familia['armazem_vendas']:
                        armazem_vendas = familia['armazem_vendas']
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_gastos, quant_debito=quantidade, debito=line['valor_total'], quant_credito=to_decimal('0'), credito=to_decimal('0'), user=session['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_mercadorias, quant_debito=to_decimal('0'), debito=to_decimal('0'), quant_credito=quantidade, credito=line['valor_total'], user=session['user']).put()
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_vendas, quant_saida=quantidade, quant_entrada=to_decimal('0'), user=session['user']).put()
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_cliente, quant_saida=to_decimal('0'), quant_entrada=quantidade, user=session['user']).put()
            return form_edit(key = key, window_id = window_id)
        else:
            return error_message('Não pode confirmar talões sem linhas de Talão! \n')

    def Facturar(self, key, window_id):
        #Gera Factura em rascunho!!!
        #Altera o movimento contabilistico para active!!!
        record_id=key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Facturado'
        try:
            from my_factura_cli import FacturaCliente
        except:
            from factura_cli import FacturaCliente
        factura = FacturaCliente(data=record['data'], notas=record['notas'], talao_bar=record['id'], cliente=record['cliente'], residual=str(to_decimal('0')), estado='rascunho', user=session['user']).put()
        record['factura'] = factura
        TalaoBar(**record).put()
        #Muda o movimento de não active para active
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        movimentos = Movimento(where="documento='talao_bar'and num_doc={num_doc} ".format(num_doc=record['id'])).get()
        if movimentos:
            for movimento in movimentos:
                movimento['active'] = 'True'
                movimento['user'] = session['user']
                Movimento(**movimento).put()
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        sujeito_iva = Terceiro(where="id='{cliente}'".format(cliente=str(record['cliente']))).get()[1][0]['sujeito_iva']
        try:
            from my_linha_talao_bar import LinhaTalaoBar
        except:
            from linha_talao_bar import LinhaTalaoBar
        record_lines = LinhaTalaoBar(where="talao_bar = '{talao_bar}'".format(talao_bar=record['id'])).get()
        if record_lines:
            try:
                from my_linha_factura_cli import LinhaFacturaCliente
            except:
                from linha_factura_cli import LinhaFacturaCliente
            for line in record_lines:
                quantidade = to_decimal(str(line['quantidade']))
                LinhaFacturaCliente(factura_cli=factura, produto=line['produto'], quantidade=quantidade, valor_total=line['valor_total'], desconto=line['desconto'], iva=line['iva'], valor_unitario=line['valor_unitario'], ean=line['ean'], user=session['user']).put()
        return form_edit(key = key, window_id = window_id)

    def efectuar_pagamento(self, key, window_id):
        """Esta acção efectua o pagamento"""
        active = False
        record_id=key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Pago'
        #Verifica se tem caixa aberta, se não tiver abre
        #Faz o pagamento em caixa
        try:
            from my_caixa import Caixa
        except:
            from caixa import Caixa
        try:
            from my_linha_caixa import LinhaCaixa
        except:
            from linha_caixa import LinhaCaixa
        try:
            from my_terminal import Terminal
        except:
            from terminal import Terminal
        terminal = Terminal(where = """name='Esplanada'""").get()
        if terminal[0] > 0:
            terminal=terminal[1][0]['id']
        caixa = Caixa(where="estado = 'Aberta' AND terminal='{terminal}' AND data_inicial <= '{today}'".format(terminal=terminal, today=record['data'])).get()
        if not caixa:
            caixa = Caixa(data_inicial=record['data'], hora_inicial=time.strftime('%H:%M:%S'), valor_inicial=0, valor_final=0 , estado='Aberta', user=session['user'], vendedor=session['user'], terminal=terminal).put()
        else:
            caixa = caixa[0]['id']
        if record['factura']:
            active = True
        record['estado'] = 'Pago'
        try:
            from my_metodo_pagamento import MetodoPagamento
        except:
            from metodo_pagamento import MetodoPagamento
        metodos_pagamento = MetodoPagamento().get_options()
        first = True
        total_entregue = to_decimal('0')
        for metodo in metodos_pagamento:
            if bottle.request.forms.get(metodo[1]):
                method = to_decimal(str(bottle.request.forms.get(metodo[1])))
            else:
                method = to_decimal('0')
            if method > to_decimal('0'):
                total_entregue += to_decimal(str(bottle.request.forms.get(metodo[1])))
        if total_entregue >= to_decimal(str(bottle.request.forms.get('total_a_pagar'))):
            for metodo in metodos_pagamento:
                if first == True:
                    default_metodo = metodo
                    first = False
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(str(bottle.request.forms.get(metodo[1])))
                else:
                    method = to_decimal('0')
                if method > to_decimal('0'):
                    linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nosso Talão de Bar', documento='talao_bar', num_doc=record['numero'], valor_documento=to_decimal(str(bottle.request.forms.get('total_a_pagar'))), terceiro=record['cliente'], metodo=metodo[0], entrada=bottle.request.forms.get(metodo[1]), saida=0, active=active, user=session['user']).put()
            troco = total_entregue - to_decimal(str(bottle.request.forms.get('total_a_pagar')))
            if troco > to_decimal('0'):
                linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nosso Talão de Bar', documento='talao_bar', num_doc=record['numero'], valor_documento=to_decimal(str(bottle.request.forms.get('total_a_pagar'))), terceiro=record['cliente'], metodo=default_metodo[0], entrada=0, saida=troco, active=active, user=session['user']).put()
            else:
                troco = to_decimal('0')
            record['residual'] = to_decimal(str(bottle.request.forms.get('total_a_pagar'))) - total_entregue + troco
            #Faz o lançamento contabilistico se tiver factura como movimento activo, se não como movimento geral
            #Vê o metodo de pagamento e lança na conta adequada
            try:
                from my_diario import Diario
            except:
                from diario import Diario
            diario = Diario(where="tipo='caixa'").get()[0]['id']
            periodo = None
            try:
                from my_periodo import Periodo
            except:
                from periodo import Periodo
            periodos = Periodo().get()
            for p in periodos:
                lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
                if str(format_date(record['data'])) in lista_datas:
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
            movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Pagamento de Talão de Bar', diario=diario, documento='talao_bar', periodo=periodo, estado='Rascunho', user=session['user'], active=active).put()
            TalaoBar(**record).put()
            try:
                from my_terceiro import Terceiro
            except:
                from terceiro import Terceiro
            conta_cliente = Terceiro().get(key=record['cliente'])[0]['a_receber']
            for metodo in metodos_pagamento:
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(str(bottle.request.forms.get(metodo[1])))
                else:
                    method = to_decimal('0')
                if method > to_decimal('0'):
                    conta_pagamento = MetodoPagamento().get(key=metodo[0])[0]['conta']
                    LinhaMovimento(movimento=movimento, descricao='Pagamento de Talão de Bar', conta=conta_pagamento, quant_debito=to_decimal('0'), debito=to_decimal(str(bottle.request.forms.get(metodo[1]))), quant_credito=to_decimal('0'), credito=to_decimal('0'), user=session['user']).put()
                    LinhaMovimento(movimento=movimento, descricao='Pagamento de Talão de Bar', conta=conta_cliente, quant_debito=to_decimal('0'), debito=to_decimal('0'), quant_credito=to_decimal('0'), credito=to_decimal(str(bottle.request.forms.get(metodo[1]))), user=session['user']).put()
            return form_edit(key = 'None', window_id = window_id)
        else:
            return 'Segundo as Regras da Empresa não é possivel receber valores inferiores ao valor a Pagar, Torne a efectuar o pagamento por Favor!'#depois ver a possibilidade de ficar no mesmo sitio

    def Cancelar(self, key, window_id):
        # Estorna movimento contabilistico
        # Estorna movimento de stock
        # verifica se existe factura gerada e se ouver verifica o estado e depois extorna caso confirmada ou simplesmente cancela se em rascunho
        # Estorna Pagamento
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Cancelado'
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        try:
            from my_linha_movimento import LinhaMovimento
        except:
            from linha_movimento import LinhaMovimento
        movimentos = Movimento(where="documento='talao_bar' and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
        if movimentos:
            for movimento in movimentos:
                new_movimento = {}
                new_movimento['user'] = session['user']
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
                    new_linha_movimento['user'] = session['user']
                    LinhaMovimento(**new_linha_movimento).put()
        try:
            from my_stock import Stock
        except:
            from stock import Stock
        try:
            from my_linha_stock import LinhaStock
        except:
            from linha_stock import LinhaStock
        stocks = Stock(where="documento='talao_bar' and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
        if stocks:
            for stock in stocks:
                new_stock = {}
                new_stock['user'] = session['user']
                for key in stock.keys():
                    if key not in ['id', 'user_create', 'user_change', 'date_create', 'date_change','numero']:
                        new_stock[key] = stock[key]
                new_stock['numero'] = base_models.Sequence().get_sequence('stock')
                new_stock['descricao'] = 'Anulação de ' + stock['descricao']
                new_stock_id = Stock(**new_stock).put()
                linhas_stock = LinhaStock(where="stock={stock}".format(stock=stock['id'])).get()
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
                    new_linha_stock['user'] = session['user']
                    LinhaStock(**new_linha_stock).put()
        try:
            from my_linha_caixa import LinhaCaixa
        except:
            from linha_caixa import LinhaCaixa
        linhascaixa = LinhaCaixa(where="documento='talao_bar' and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
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
                new_linha_caixa['user'] = session['user']
                LinhaCaixa(**new_linha_caixa).put()
        try:
            from my_factura_cli import FacturaCliente
        except:
            from factura_cli import FacturaCliente
        #aqui depois validar se está confirmada e se estiver estornar o movimento contabilistico
        facturas_cli = FacturaCliente(where="id='{factura}'".format(factura=record['factura'])).get()
        if facturas_cli:
            for factura_cli in facturas_cli:
                factura_cli['estado'] = 'Cancelado'
                factura_cli['user'] = session['user']
                FacturaCliente(**factura_cli).put()
        TalaoBar(**record).put()
        return form_edit(key = 'None', window_id = window_id)
