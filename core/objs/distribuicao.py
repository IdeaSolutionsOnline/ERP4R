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
__model_name__= 'distribuicao.Distribuicao'
import auth, base_models
from orm import *
from form import *
try:
    from my_users import Users
except:
    from users import Users

class Distribuicao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'distribuicao'
        self.__title__= 'Guia de Distribuição'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__workflow__ = (
            'estado', {'Rascunho':['Gera Movimentos', 'Imprimir', 'Elimina Nao Usados', 'Confirmar'], 'Confirmado':['Imprime', 'Pagar', 'Cancelar'], 'Impresso':['Imprime', 'Pagar', 'Cancelar'], 'Pago':['Imprime', 'Cancelar'], 'Cancelado':[]})
        self.__workflow_auth__ = {
            'Gera Movimentos':['Vendedor','Caixa'],
            'Elimina Nao Usados':['Vendedor','Caixa'],
            'Confirmar':['Vendedor','Caixa'],
            'Imprimir':['All'],
            'Pagar':['Caixa'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__tabs__ = [
            ('Linhas de Guia de Distribuicao', ['linha_distribuicao']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ('Recebimentos',['pagamentos']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Pago','Impresso','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor','Caixa'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.data = date_field(view_order=1 , name='Data', args='required', default=datetime.date.today())
        self.numero = info_field(view_order=2 , name='Número', size=20)
        self.vendedor = choice_field(view_order=3 , name='Vendedor', args='required', default="session['user']", size=40, model='users', column='nome', options='model.get_users()')
        self.notas = string_field(view_order=4 , name='Notas', size=80, args='autocomplete="on"', onlist=False)
        self.estado = info_field(view_order=5 , name='Estado', default='Rascunho') #dynamic_atrs='estado_dyn_attrs'
        self.total = function_field(view_order=6 , name='Total', sum=True, search=False, size=20)
        self.residual = currency_field(view_order=7 , name='Valor Residual', sum=True, args='disabled', size=20)
        self.pagamentos = list_field(view_order=8 , name='Pagamentos', condition="documento='distribuicao' and num_doc='{numero}'", model_name='linha_caixa.LinhaCaixa', list_edit_mode='inline', onlist = False)
        self.movs_contab = list_field(view_order=9 , name='Movimentos Contab.', condition="documento='distribuicao' and num_doc={numero}", model_name='movimento.Movimento', list_edit_mode='inline', onlist = False)
        self.movs_stock = list_field(view_order=10 , name='Movimentos Stock', condition="documento='distribuicao' and num_doc={numero}", model_name='stock.Stock', list_edit_mode='inline', onlist = False)
        self.linha_distribuicao = list_field(view_order=11, name='Linhas de Distribuição', model_name='linha_distribuicao.LinhaDistribuicao', condition="distribuicao='{id}'", list_edit_mode='inline', onlist = False)

    def get_users(self):
        return Users().get_options()

    def get_options(self, cliente=None):
        options = []
        opts = self.get()
        for f in self.__fields__:
            if f[0] == 'cliente':
                field=f
        for option in opts:
            if cliente:
                if str(option['cliente']) == str(cliente):
                    nome_cliente = get_field_value(record=option, field=field, model=self)['field_value'][1]
                    options.append((str(option['id']), '{data} - {numero} - {cliente} - {total}'.format(data=str(option['data']), numero=str(option['numero']), cliente=nome_cliente,total=self.get_total(option['id']))))
            else:
                nome_cliente = get_field_value(record=option, field=field, model=self)['field_value']
                options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), cliente=nome_cliente,total=self.get_total(option['id']))))
        return options

    def get_total(self, key):
        from linha_distribuicao import LinhaDistribuicao
        value = to_decimal('0')
        record_lines = LinhaDistribuicao(where="distribuicao = '{distribuicao}'".format(distribuicao=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(str(line['valor_total']))
        return round(value,0)

    def print_doc(self, key, window_id):
        #Acção por defeito para imprimir o documento base
        #Deverá mudar o estado para impresso
        from linha_distribuicao import LinhaDistribuicao
        path = os.path.join("./objs", model.__name__, "distribuicao.html")
        tmpl_file = open(path, 'r')
        tmpl_string = tmpl_file.read()
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Impresso'
        final_record = {}
        for field in model.__fields__:
            field_value = utils.get_field_value(record, field, model)['field_value']
            #Os combo_field são tuples (id, valor)
            if isinstance(field_value, tuple):
                field_value = field_value[1]
            final_record[field[0]] = field_value
        record_lines = LinhaDistribuicao(where="distribuicao = '{distribuicao}'".format(distribuicao=record['id'])).get()
        final_record_lines = []
        for line in record_lines:
            final_line = {}
            for field in LinhaDistribuicao().__fields__:
                final_line[field[0]] = utils.get_field_value(line, field, LinhaDistribuicao())['field_value']
            final_line['valor_total_sem_iva'] = round(float(final_line['valor_total']) / (1 + float(final_line['iva'])/100),0)
            final_record_lines.append(final_line)
        final_record['linhas'] = final_record_lines
        Distribuicao(**record).put()
        return bottle.template(tmpl_string, final_record)

    def gera_movimentos(self, key, window_id):
        if key in ['None', None]:
            key = get_actions(action='save', key=None, model_name=model.__model_name__, internal=True)
        record_id = key
        from produto import Produto
        from linha_distribuicao import LinhaDistribuicao
        produtos = Produto(where = "para_distribuicao='True'").get()
        if len(produtos) > 0:
            for produto in produtos:
                valor_unitario = to_decimal(Produto().get_sale_price(produto=produto['id'], quantidade=to_decimal('1'), unidade=produto['unidade_medida_padrao'], terminal = get_terminal('Distribuicao')))
                LinhaDistribuicao(distribuicao=record_id, ean=produto['referencia'] , unidade=produto['unidade_medida_padrao'], valor_unitario=valor_unitario, iva=produto['iva'], valor_total=valor_unitario, quant_in=to_decimal('0'), quant_out=to_decimal('0'), user=session['user'], produto=produto['id']).put()
        return form_edit(key=key, window_id=window_id)

    def elimina_nao_usados(self, key, window_id):
        from linha_distribuicao import LinhaDistribuicao
        record_id = key
        record_lines = LinhaDistribuicao(where="""distribuicao='{record_id}'""".format(record_id=record_id)).get()
        if len(record_lines) > 0:
            records_to_delete = []
            for record_line in record_lines:
                if record_line['quant_out'] == to_decimal(0):
                    records_to_delete.append(record_line['id'])
            where = ''
            if len(records_to_delete) > 1:
                where += """id in {ids}""".format(ids=tuple(records_to_delete))
            else:
                where += """id = '{ids}'""".format(ids=records_to_delete[0])
            LinhaDistribuicao(where=where).delete()
        return form_edit(key=key, window_id=window_id)

    def Confirmar(self, key, window_id):#não tinha self nem key eu acrescentei mas não testei
        # Gera movimento contabilistico (conta de mercadorias contra conta de gastos)
        # Gera movimento de Stock (sai de armazem por contrapartida de cliente)
        #print ('Hello!!!')
        if key in ['None', None]:
            m_action = model_action(obj=self)
            m_action.save(key=None, internal=True)
        record_id = key
        #print ('model_get begin!')
        record = model.get(key=record_id)[0]
        #print (record)
        record['user'] = session['user']
        record['estado'] = 'Confirmado'
        record['numero'] = base_models.Sequence().get_sequence('distribuicao')
        from diario import Diario
        diario = Diario(where="tipo='stock'").get()[0]['id']
        periodo = None
        from periodo import Periodo
        periodos = Periodo().get()
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(record['data'])) in lista_datas:
                periodo = p['id']
        if not periodo:
            return error_message('não existe periodo definido para o data em questão! \n')
        from armazem import Armazem
        armazem_cliente = Armazem(where="tipo='cliente'").get()[0]['id']
        #Valida se o cliente é sujeito a iva
        from terceiro import Terceiro
        sujeito_iva = Terceiro(where="nome='Clientes Gerais'").get()[0]['sujeito_iva']
        from movimento import Movimento
        movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Nossa Guia de distribuição', diario=diario, documento='distribuicao', periodo=periodo, estado='Confirmado', user=session['user']).put()
        from stock import Stock
        stock = Stock(data=record['data'], numero=base_models.Sequence().get_sequence('stock'), num_doc=record['numero'], descricao='Nossa Guia de Distribuição', documento='distribuicao', periodo=periodo, estado='Confirmado', user=session['user']).put()
        Distribuicao(**record).put()
        from linha_distribuicao import LinhaDistribuicao
        record_lines = LinhaDistribuicao(where="distribuicao = '{distribuicao}'".format(distribuicao=record['id'])).get()
        if record_lines:
            from linha_movimento import LinhaMovimento
            from linha_stock import LinhaStock
            from produto import Produto
            from familia_produto import FamiliaProduto
            for line in record_lines:
                # aqui depois considerar a contabilização do desconto
                # tambem depois considerar a verificação se o total está bem calculado e logs se o preço unitário for modificado
                quantidade = to_decimal(line['quant_out']) - to_decimal(line['quant_in'])
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
            #print ('See You!!!')
            return form_edit(key=key, window_id=window_id)
        else:
            return error_message('Não pode confirmar guias de Distribuição sem linhas de Distribuição! \n')

    def efectuar_pagamento(self, key, window_id):
        """Esta acção efectua o pagamento"""
        active = False
        record_id=key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Pago'
        from terceiro import Terceiro
        terceiro = Terceiro(where="nome='Clientes Gerais'").get()[0]
        cliente = terceiro['id']
        conta_cliente = terceiro['a_receber']
        #Verifica se tem caixa aberta, se não tiver abre
        #Faz o pagamento em caixa
        from caixa import Caixa
        from linha_caixa import LinhaCaixa
        from terminal import Terminal
        terminal = Terminal(where = """name='Distribuicao'""").get()# substituir esta bosta para get_terminal
        if len(terminal) > 0:
            terminal=terminal[0]['id']
        caixa = Caixa(where="estado = 'Aberta' AND terminal='{terminal}' AND data_inicial <= '{today}'".format(terminal=terminal, today=record['data'])).get()
        if not caixa:
            caixa = Caixa(data_inicial=record['data'], hora_inicial=time.strftime('%H:%M:%S'), valor_inicial=0, valor_final=0 , estado='Aberta', user=session['user'], vendedor=session['user'], terminal=terminal).put()
        else:
            caixa = caixa[0]['id']
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
                    linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nossa Guia de Distribuição', documento='distribuicao', num_doc=record['numero'], valor_documento=to_decimal(str(bottle.request.forms.get('total_a_pagar'))), terceiro=cliente, metodo=metodo[0], entrada=bottle.request.forms.get(metodo[1]), saida=0, active=active, user=session['user']).put()
            troco = total_entregue - to_decimal(str(bottle.request.forms.get('total_a_pagar')))
            if troco > to_decimal('0'):
                linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nossa Guia de Distribuição', documento='distribuicao', num_doc=record['numero'], valor_documento=to_decimal(str(bottle.request.forms.get('total_a_pagar'))), terceiro=cliente, metodo=default_metodo[0], entrada=0, saida=troco, active=active, user=session['user']).put()
            else:
                troco = to_decimal('0')
            record['residual'] = to_decimal(str(bottle.request.forms.get('total_a_pagar'))) - total_entregue + troco
            #Faz o lançamento contabilistico se tiver factura como movimento activo, se não como movimento geral
            #Vê o metodo de pagamento e lança na conta adequada
            from diario import Diario
            diario = Diario(where="tipo='caixa'").get()[0]['id']
            periodo = None
            from periodo import Periodo
            periodos = Periodo().get()
            for p in periodos:
                lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
                if str(format_date(record['data'])) in lista_datas:
                    periodo = p['id']
            if not periodo:
                return error_message('não existe periodo definido para a data em questão! \n')
            from movimento import Movimento
            from linha_movimento import LinhaMovimento
            movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Pagamento de Guia de Distribuição', diario=diario, documento='distribuicao', periodo=periodo, estado='Rascunho', user=session['user'], active=active).put()
            #print (record)
            Distribuicao(**record).put()
            for metodo in metodos_pagamento:
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(str(bottle.request.forms.get(metodo[1])))
                else:
                    method = to_decimal('0')
                if method > to_decimal('0'):
                    conta_pagamento = MetodoPagamento().get(key=metodo[0])[0]['conta']
                    LinhaMovimento(movimento=movimento, descricao='Pagamento de Talão de Venda', conta=conta_pagamento, quant_debito=to_decimal('0'), debito=to_decimal(str(bottle.request.forms.get(metodo[1]))), quant_credito=to_decimal('0'), credito=to_decimal('0'), user=session['user']).put()
                    LinhaMovimento(movimento=movimento, descricao='Pagamento de Guia de Distribuição', conta=conta_cliente, quant_debito=to_decimal('0'), debito=to_decimal('0'), quant_credito=to_decimal('0'), credito=to_decimal(str(bottle.request.forms.get(metodo[1]))), user=session['user']).put()
            return form_edit(key='None', window_id=self.window_id)
        else:
            return error_message('Segundo as Regras da Empresa não é possivel receber valores inferiores ao valor a Pagar, Torne a efectuar o pagamento por Favor!')#depois ver a possibilidade de ficar no mesmo sitio

    def Cancelar(self, key, window_id):
        # Estorna movimento contabilistico
        # Estorna movimento de stock
        # verifica se existe factura gerada e se ouver verifica o estado e depois extorna caso confirmada ou simplesmente cancela se em rascunho
        # Estorna Pagamento
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Cancelado'
        from movimento import Movimento
        from linha_movimento import LinhaMovimento
        movimentos = Movimento(where="documento='distribuicao'and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
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
        from stock import Stock
        from linha_stock import LinhaStock
        stocks = Stock(where="documento='distribuicao'and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
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
        from linha_caixa import LinhaCaixa
        linhascaixa = LinhaCaixa(where="documento='distribuicao'and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
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
        Distribuicao(**record).put()
        return form_edit(key='None', window_id=window_id)
