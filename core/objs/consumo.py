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
__model_name__ = 'consumo.Consumo'
import base_models#auth,
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class Consumo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'consumo'
        self.__title__ = 'Talão de Consumo Interno'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'consumo.data'#posso ordenar por qualquer coluna de qualquer tabela que se relacione com esta
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'],'Confirmado':['Imprime', 'Cancelar'], 'Impresso':['Imprime', 'Cancelar'], 'Cancelado':[]}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Vendedor'],
            'Imprime':['All'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__tabs__ = [
            ('Linhas de Talão de Consumo', ['linha_consumo']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor','Caixa'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1 , name='Data', default=datetime.date.today(), args='required')
        self.numero = info_field(view_order=2 , name='Número', size=20)
        self.funcionario = choice_field(view_order=3 , name='Funcionario', size=40, args='required', model='terceiro', column='nome', options='model.get_terceiro()')
        self.motivo = string_field(view_order=4 , name='Motivo', size=80, args='autocomplete="on"')
        self.notas = string_field(view_order=5 , name='Notas', size=80, args='autocomplete="on"')
        self.estado = info_field(view_order=6 , name='Estado', default='Rascunho') #dynamic_atrs='estado_dyn_attrs'
        self.vendedor = parent_field(view_order=7 , name='Vendedor', onlist=False, default="session['user']", model_name='users.Users', size=40, column='nome')
        self.total_iva = function_field(view_order=8 , name='Total IVA', sum=True, size=20)
        self.total = function_field(view_order=9 , name='Total', sum=True, size=20)
        self.movs_contab = list_field(view_order=10 , name='Movimentos Contab.', condition="documento='consumo' and num_doc={numero}", model_name='movimento.Movimento', list_edit_mode='edit')
        self.movs_stock = list_field(view_order=11 , name='Movimentos Stock', condition="documento='consumo' and num_doc={numero}", model_name='stock.Stock', list_edit_mode='edit')
        self.linha_consumo = list_field(view_order=12 , name='Linhas de Talão de Consumo', model_name='linha_consumo.LinhaConsumo', condition="consumo='{id}'", list_edit_mode='inline')

    def get_terceiro(self):
        return Terceiro().get_funcionarios()

    def get_options(self, funcionario=None):
        #a ideia aqui é poder ver os consumos apenas de um funcionario
        options = []
        opts = self.get()
        for f in self.__fields__:
            if f[0] == 'funcionario':
                field=f
        for option in opts:
            if funcionario:
                if str(option['funcionario']) == str(funcionario):
                    nome_funcionario = get_field_value(record=option, field=field, model=self)['field_value'][1]
                    options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), funcionario=nome_funcionario,total=self.get_total(option['id']))))
            else:
                nome_funcionario = get_field_value(record=option, field=field, model=self)['field_value']
                options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), funcionario=nome_funcionario,total=self.get_total(option['id']))))
        return options

    def get_total(self, key):
        from linha_consumo import LinhaConsumo
        value = to_decimal(0)
        record_lines = LinhaConsumo(where="consumo = '{consumo}'".format(consumo=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total'])
        return round(value,0)

    def get_total_iva(self, key):
        from linha_consumo import LinhaConsumo
        value = to_decimal(0)
        #print (value)
        record_lines = LinhaConsumo(where="consumo = '{consumo}'".format(consumo=key)).get()
        if record_lines:
            for line in record_lines:
                #print (to_decimal(line['valor_total']))
                #print (to_decimal(line['iva']))
                #print ((to_decimal(line['valor_total']) / (1 +  to_decimal(line['iva'])/100)))
                value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  to_decimal(line['iva'])/100))
        return round(value,0)

    def Imprime(self, key, window_id):
        #Acção por defeito para imprimir o documento base
        #Deverá mudar o estado para impresso
        from linha_consumo import LinhaConsumo
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Impresso'
        record_lines = run_sql("SELECT linha_consumo.*, produto.nome as nome_produto FROM linha_consumo JOIN produto on produto.id = linha_consumo.produto WHERE consumo = '{consumo}'".format(consumo=record['id']))
        from subprocess import Popen,PIPE
        lpr = Popen(["/usr/bin/lpr", "-P", "bar"], stdin=PIPE, shell=False, stdout=PIPE, stderr=PIPE)
        printDoc = ''
        OpenDraw=chr(27) + chr(112) + chr(0) + chr(32) + chr(32)
        Now = time.strftime("%X")
        Today = datetime.date.today()
        Line = '----------------------------------------' + '\n'
        LineAdvance=chr(27) + chr(100) + chr(5)
        StartPrinter=chr(27)+ chr(61) + chr(1) + chr(27) + chr(64) + chr(27) + "" + chr(0) + chr(27)+ chr(73) + chr(0)
        CutPaper=chr(27) + chr(86) + chr(0)
        printDoc += '{today:20} Consumo n.:{number:>8}\n'.format(today=str(Today), number=str(record['numero']))
        printDoc += Now + '\n'
        printDoc += 'Funcionario: {funcionario}\n'.format(funcionario=record['funcionario'])
        printDoc += 'Motivo: {motivo}\n'.format(motivo=record['motivo'])
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
        printDoc += Line + LineAdvance + LineAdvance + CutPaper
        lpr.communicate(printDoc.encode("utf-8"))
        Consumo(**record).put()
        return form_edit(key=key, window_id=window_id)

    def Confirmar(self, key, window_id):
        # Gera movimento contabilistico (conta de mercadorias contra conta de gastos)
        # Gera movimento de Stock (sai de armazem por contrapartida de cliente)
        if key in ['None', None]:
            key = get_actions(action='save', key=None, model_name=model.__model_name__, internal=True)
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Confirmado'
        record['numero'] = base_models.Sequence().get_sequence('consumo')
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
            return error_message('não existe periodo definido para a data em questão! \n')
        from armazem import Armazem
        armazem_cliente = Armazem(where="tipo='cliente'").get()[0]['id']
        from movimento import Movimento
        movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Nosso Talão de Consumo', diario=diario, documento='consumo', periodo=periodo, estado='Confirmado', user=session['user'], active=False).put()
        from stock import Stock
        stock = Stock(data=record['data'], numero=base_models.Sequence().get_sequence('stock'), num_doc=record['numero'], descricao='Nosso Talão de Consumo', documento='consumo', periodo=periodo, estado='Confirmado', user=session['user']).put()
        Consumo(**record).put()
        from linha_consumo import LinhaConsumo
        record_lines = LinhaConsumo(where="consumo = '{consumo}'".format(consumo=record['id'])).get()
        if record_lines:
            from linha_movimento import LinhaMovimento
            from linha_stock import LinhaStock
            from produto import Produto
            from familia_produto import FamiliaProduto
            for line in record_lines:
                # tambem depois considerar a verificação se o total está bem calculado e logs se o preço unitário for modificado
                quantidade = to_decimal(line['quantidade'])
                product = Produto().get(key=line['produto'])[0]
                contas = Produto().get_accounts(line['produto'])
                conta_mercadorias = contas['conta_mercadorias']
                conta_gastos = contas['conta_gastos']
                taxa_iva = product['iva']
                armazem_vendas = None
                familia = FamiliaProduto().get(key=product['familia'])
                if familia:
                    familia = familia[0]
                    if familia['armazem_vendas']:
                        armazem_vendas = familia['armazem_vendas']
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_gastos, quant_debito=quantidade, debito=line['valor_total'], quant_credito=0.0, credito=0.0, user=session['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_mercadorias, quant_debito=0.0, debito=0.0, quant_credito=quantidade, credito=line['valor_total'], user=session['user']).put()
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_vendas, quant_saida=quantidade, quant_entrada=0.0, user=session['user']).put()
                LinhaStock(stock=stock, descricao=descricao, produto=line['produto'], armazem=armazem_cliente, quant_saida=0.0, quant_entrada=quantidade, user=session['user']).put()
            return form_edit(key=key, window_id=window_id)
        else:
            return error_message('Não pode confirmar talões sem linhas de Talão! \n')

    def Cancelar(self, key, window_id):
        # Estorna movimento contabilistico
        # Estorna movimento de stock
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Cancelado'
        from movimento import Movimento
        from linha_movimento import LinhaMovimento
        movimentos = Movimento(where="documento='consumo'and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
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
                    new_linha_movimento['user'] = session['user']
                    LinhaMovimento(**new_linha_movimento).put()
        from stock import Stock
        from linha_stock import LinhaStock
        stocks = Stock(where="documento='consumo'and num_doc={num_doc} ".format(num_doc=record['numero'])).get()
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
                    new_linha_stock['user'] = session['user']
                    LinhaStock(**new_linha_stock).put()
        Consumo(**record).put()
        return form_edit(key='None', window_id=window_id)
