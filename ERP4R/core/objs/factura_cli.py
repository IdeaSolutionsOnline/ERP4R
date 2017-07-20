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
__model_name__='factura_cli.FacturaCliente'
import base_models#auth,
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class FacturaCliente(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'factura_cli'
        self.__title__= 'Facturas ao Cliente'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(factura_cli.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir Recibo', 'Imprimir', 'Cancelar', 'Pagar'], 'Pago':['Imprimir Recibo', 'Imprimir', 'Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Vendedor'],
            'Pagar':['Caixa'],
            'Rascunho':['Gestor'],
            'Imprimir':['Vendedor'],
            'Imprimir Recibo':['Caixa'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__workflow_context__ = {
            'Pagar':('residual', '>', 0),
            'Imprimir Recibo':('residual', '<', 'total'),
            }
        self.__tabs__ = [
            ('Faturação', ['data','numero','serie','cliente','notas','estado','residual','vendedor','retencao','taxa_retencao','linha_factura_cli','total','total_desconto', 'total_iva','valor_retido']),
            ('Movimentos', ['movs_contab']),
            ('Recebimentos',['pagamentos']),
            ]
        '''self.__no_edit__ = [
            ('estado', ['Confirmado','Pago','Cancelado'])
            ]'''
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor', 'Caixa'],
            'create':['Vendedor', 'Caixa'],
            'delete':['Vendedor'],
            'full_access':['Gestor']
            }

        self.__get_options__ = ['numero']        

        self.data = date_field(view_order = 1, name = 'Data', size=45,args = 'required', default = datetime.date.today())
        self.numero = info_field(view_order = 2, name = 'Número', size=30, args='readonly')
        self.serie = info_field(view_order = 3, name = 'Série', size=30, args='required', default="A")
        self.cliente = choice_field(view_order = 4, name = 'Cliente', size = 90, args = 'required', model = 'terceiro', column = 'nome', options = 'model.get_terceiros()')
        self.notas = string_field(view_order = 5, name = 'Notas', size = 110, args = 'autocomplete = "on"', onlist = False)
        self.estado = info_field(view_order = 6, name = 'Estado', default = 'Rascunho')
        self.residual = currency_field(view_order = 7, name = 'Valor Residual', sum = True, args = 'readonly')
        self.vendedor = parent_field(view_order = 8, name = 'Vendedor', size = 90, default = "session['user']", model_name = 'users.Users', onlist = False, column = 'nome')
        
        self.retencao = combo_field(view_order=9,name='Retenção?', default="NAO", options=[('NAO','NAO'),('SIM','SIM')], size=45)
        #self.retencao = boolean_field(view_order=9,name='Retenção?', default=False, size=45)
        self.taxa_retencao = percent_field(view_order=10, name ='Taxa Retenção', size=45, onlist=False)
        
        self.total = function_field(view_order = 12, name = 'Total', sum = True, size = 70, search = False)
        self.total_desconto = function_field(view_order = 13, name = 'Desconto', sum = True, size = 70, search = False)
        self.total_iva = function_field(view_order = 14, name = 'Total IVA', sum = True, size = 70, search = False)
        self.valor_retido=function_field(view_order=15, name='Total Retenção',size=70, onlist=False, args='readonly')
          
        self.movs_contab = list_field(view_order = 16, name = 'Movimentos Contab.', condition = "documento='factura_cli' and num_doc={numero}", model_name = 'movimento.Movimento', list_edit_mode = 'edit', onlist = False)
        self.pagamentos = list_field(view_order=17, name ='Pagamentos', condition="documento='factura_forn' and num_doc={numero}", model_name='linha_caixa.LinhaCaixa', list_edit_mode='edit', onlist = False)
        self.linha_factura_cli = list_field(view_order = 11, name = 'Linhas Facturas', model_name = 'linha_factura_cli.LinhaFacturaCliente', condition = "factura_cli='{id}'", list_edit_mode = 'inline', onlist = False)

    def get_terceiros(self):
        return Terceiro().get_clientes()


    def record_lines(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            try:
                from my_linha_factura_cli import LinhaFacturaCliente
            except:
                from linha_factura_cli import LinhaFacturaCliente
            record_lines = LinhaFacturaCliente(where="factura_cli = '{factura}'".format(factura=key)).get()
            return record_lines
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)


    def get_valor_retido(self, key):
        try:
            from my_rh_retencao import RHRetencao
        except:
            from rh_retencao import RHRetencao
        value = to_decimal(0)
        if self.kargs['retencao']=="SIM":
            taxa = self.kargs['taxa_retencao']
            if to_decimal(taxa) == to_decimal(0):
                ret = RHRetencao().get()
                if ret:
                    taxa = ret[0]['taxa_prestacao_servico']                    
            lines = self.record_lines(key=key)
            for line in lines:
                value += to_decimal(line['valor_total']*taxa/100)
            self.kargs['taxa_retencao']=taxa
            self.put()
        else:
            self.kargs['taxa_retencao']=to_decimal(0)
            self.put()
        return round(value,0)


    def get_total(self, key):
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        for line in record_lines:
            value += to_decimal(line['valor_total'])
        return round(value,0)

    def get_total_desconto(self, key):
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        for line in record_lines:
            value += to_decimal(line['valor_total']) * to_decimal(line['desconto']) / 100
        return round(value,0)

    def get_total_incidencia(self, key):
        value = to_decimal(0)
        if self.kargs['retencao']=="NAO":       
            record_lines = self.record_lines(key)
            if record_lines:
                for line in record_lines:                
                    if to_decimal(line['iva']) > to_decimal(0):
                        value += to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100))
        return round(value,0)

    def get_total_incidencia_por_taxa(self, record_lines):
        value = to_decimal(0)
        if record_lines:
            for line in record_lines:                
                if to_decimal(line['iva']) > to_decimal(0):
                    value += to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100))
        return round(value,0)

    def get_total_iva(self, key):
        value = to_decimal(0)
        if self.kargs['retencao']=="NAO":
            record_lines = self.record_lines(key)
            if record_lines:
                for line in record_lines:
                    value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100)))
        return round(value,0)

    def get_total_iva_por_taxa(self, record_lines):
        value = to_decimal(0)        
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100)))
        return round(value,0)

    def Imprimir(self, key, window_id):
        template = 'factura_cli'
        record = get_records_to_print(key=key, model=self)
        #print(record)
        cliente = Terceiro().get(key=record['cliente'][0])[0]
        try:
            from my_contacto import Contacto
        except:
            from contacto import Contacto
        moradas = Contacto(where="terceiro='{cliente}'".format(cliente=cliente['id'])).get()
        if len(moradas) != 0:
            moradas=moradas[0]
        else:
            moradas = {'morada':None}
        if moradas['morada']:
            record['morada'] = moradas['morada']
        else:
            record['morada'] = ''
        if cliente['nif']:
            record['cliente_nif'] = cliente['nif']
        else:
            record['cliente_nif'] = ''        
        if to_decimal(record['numero']) <10:
            record['numero']= str('00'+record['numero'])
        elif to_decimal(record['numero'])>9 & to_decimal(record['numero'])<100:
            record['numero']= str('0'+record['numero'])
        return Report(record=record, report_template=template).show()


    def Imprimir_Recibo(self, key, window_id):
        template = 'recibo'
        record = get_records_to_print(key=key, model=self)
        cliente = Terceiro().get(key=record['cliente'][0])[0]
        try:
            from my_contacto import Contacto
        except:
            from contacto import Contacto
        moradas = Contacto(where="terceiro='{cliente}'".format(cliente=cliente['id'])).get()
        if len(moradas) != 0:
            moradas=moradas[0]
        else:
            moradas = {'morada':None}
        if moradas['morada']:
            record['morada'] = moradas['morada']
        else:
            record['morada'] = ''
        if cliente['nif']:
            record['cliente_nif'] = cliente['nif']
        else:
            record['cliente_nif'] = ''
        caixas = []
        for pagamento in record['pagamentos']:
            caixas.append(pagamento['caixa'][0])
        sql = """
            SELECT id, data_inicial FROM caixa
            WHERE id {caixas}""".format(caixas = to_tuple(caixas))
        lista_datas_de_caixa = run_sql(sql)
        datas_de_caixa = {}
        for data in lista_datas_de_caixa:
            datas_de_caixa[str(data['id'])] = data['data_inicial']
        for pagamento in record['pagamentos']:
            pagamento['data'] = datas_de_caixa[pagamento['caixa'][0]]
        return Report(record=record, report_template=template).show()




    def efectuar_pagamento(self, key, window_id):
        """Esta acção efectua o pagamento"""
        record_id = key
        self.kargs = self.get(key=record_id)[0]
        self.kargs['user'] = bottle.request.session['user']
        self.kargs['id'] = key
        #Verifica se tem caixa aberta, se não tiver abre e deve atribuir um numero de caixa de imediato para que dessa forma possa constar no recibo!
        #Faz o pagamento em caixa
        try:
            from my_caixa import Caixa
        except:
            from caixa import Caixa
        try:
            from my_linha_caixa import LinhaCaixa
        except:
            from linha_caixa import LinhaCaixa
        caixa = Caixa(where="estado = 'Aberta' AND vendedor={user}".format(user=self.kargs['user'])).get()
        if not caixa:
            caixa = Caixa(data_inicial=datetime.date.today(), hora_inicial=time.strftime('%H:%M'), valor_inicial=0, valor_final=0 , estado='Aberta', terminal=get_terminal(bottle.request.session['terminal']), user=self.kargs['user'], vendedor=self.kargs['user'], numero=base_models.Sequence().get_sequence('caixa')).put()
        else:
            caixa = caixa[0]['id']
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
        for metodo in metodos_pagamento:
            if first == True:
                default_metodo = metodo
                first = False
            if bottle.request.forms.get(metodo[1]):
                method = to_decimal(str(bottle.request.forms.get(metodo[1])))
            else:
                method = to_decimal(0)
            if method > to_decimal(0):
                linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nossa Factura ao Cliente', documento='factura_cli', num_doc=self.kargs['numero'], valor_documento=to_decimal(bottle.request.forms.get('total_a_pagar')), terceiro=self.kargs['cliente'], metodo=metodo[0], entrada=bottle.request.forms.get(metodo[1]), saida=0, user=self.kargs['user']).put()
        troco = total_entregue - to_decimal(bottle.request.forms.get('total_a_pagar'))
        if troco > to_decimal(0):
            linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nossa Factura ao Cliente', documento='factura_cli', num_doc=self.kargs['numero'], valor_documento=to_decimal(bottle.request.forms.get('total_a_pagar')), terceiro=self.kargs['cliente'], metodo=default_metodo[0], entrada=0, saida=troco, user=self.kargs['user']).put()
        else:
            troco = to_decimal(0)
        self.kargs['residual'] = to_decimal(bottle.request.forms.get('total_a_pagar')) - total_entregue + troco
        #Faz o lançamento contabilistico
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
        periodos = Periodo().get()[1]
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(self.kargs['data'])) in lista_datas:
                periodo = p['id']
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        try:
            from my_linha_movimento import LinhaMovimento
        except:
            from linha_movimento import LinhaMovimento
        movimento = Movimento(data= datetime.date.today(), numero=base_models.Sequence().get_sequence('movimento'), num_doc=self.kargs['numero'], descricao='Pagamento de Factura', diario=diario, documento='factura_cli', periodo=periodo, estado='Rascunho', user=self.kargs['user']).put()
        if self.kargs['residual'] <= 0:
            self.kargs['estado'] = 'Pago'
        self.put()
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        conta_cliente = Terceiro().get(key=self.kargs['cliente'])[0]['a_receber']
        for metodo in metodos_pagamento:
            if bottle.request.forms.get(metodo[1]):
                method = to_decimal(bottle.request.forms.get(metodo[1]))
            else:
                method = to_decimal(0)
            if method > to_decimal(0):
                conta_pagamento = MetodoPagamento().get(key=metodo[0])[0]['conta']
                LinhaMovimento(movimento=movimento, descricao='Pagamento de Nota de Entrega', conta=conta_pagamento, quant_debito=to_decimal(0), debito=to_decimal(bottle.request.forms.get(metodo[1])), quant_credito=to_decimal(0), credito=to_decimal(0), user=self.kargs['user']).put()
                LinhaMovimento(movimento=movimento, descricao='Pagamento de Nota de Entrega', conta=conta_cliente, quant_debito=to_decimal(0), debito=to_decimal(0), quant_credito=to_decimal(0), credito=to_decimal(bottle.request.forms.get(metodo[1])), user=self.kargs['user']).put()
        return form_edit(window_id=window_id).show()



    def Confirmar(self, key, window_id, internal = False):
        """Gera movimento contabilistico (conta de receitas contra conta de terceiros)"""
        #print ('Inicio do confirmar factura_cli')
        self.kargs = get_model_record(model = self, key = key, force_db = self.__force_db__)

        if self.kargs['estado'] == 'Rascunho':            
            self.kargs['estado'] = 'Confirmado'
            self.kargs['residual'] = self.get_total(key = key)
            if not self.kargs['numero']:
                self.kargs['numero'] = base_models.Sequence().get_sequence('factura_cli')
            try:
                from my_diario import Diario
            except:
                from diario import Diario
            diario = Diario().get_diario(diario = 'vendas')
            try:
                from my_periodo import Periodo
            except:
                from periodo import Periodo
            periodo = Periodo().get_periodo(data = self.kargs['data'])
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
            movimento = Movimento(data = self.kargs['data'], numero = base_models.Sequence().get_sequence('movimento'), num_doc = self.kargs['numero'], descricao = 'Nossa Factura', diario = diario, documento = 'factura_cli', periodo = periodo, estado = 'Confirmado', user = self.kargs['user']).put()
            #self.kargs['movimento'] = movimento
            try:
                from my_linha_factura_cli import LinhaFacturaCliente
            except:
                from linha_factura_cli import LinhaFacturaCliente
            record_lines = LinhaFacturaCliente(where = "factura_cli = '{factura}'".format(factura = self.kargs['id'])).get()
            if record_lines:
                try:
                    from my_linha_movimento import LinhaMovimento
                except:
                    from linha_movimento import LinhaMovimento
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
                    quantidade = to_decimal(line['quantidade'])
                    product = Produto().get(key = line['produto'])[0]
                    contas = Produto().get_accounts(line['produto'])
                    #print (contas)
                    conta_receitas = contas['conta_receitas']
                    if sujeito_iva:
                        taxa_iva = product['iva']
                    else:
                        taxa_iva = to_decimal(0)
                    #familia = FamiliaProduto().get(key=product['familia'])[0]
                    descricao = product['nome']
                    total_sem_iva = line['valor_total']#/(1+taxa_iva)
                    #fazer o lancamento das receitas mas tambem do iva
                    LinhaMovimento(movimento = movimento, descricao = descricao, conta = conta_terceiro, quant_debito = quantidade, debito = total_sem_iva, quant_credito = to_decimal(0), credito = to_decimal(0), user = self.kargs['user']).put()
                    LinhaMovimento(movimento = movimento, descricao = descricao, conta = conta_receitas, quant_debito = to_decimal(0), debito = to_decimal(0), quant_credito = quantidade, credito = total_sem_iva, user = self.kargs['user']).put()
                self.put()
                ctx_dict = get_context(window_id)
                ctx_dict['main_key'] = self.kargs['id']
                set_context(window_id, ctx_dict)                
                result = form_edit(window_id = window_id).show()
            else:
                result = error_message('Não pode confirmar facturas sem linhas de factura! \n')
        if not internal:
            #não foi chamado pela side_bar e por isso deverá devolver o form, se vem do side_bar não tem necessidade            
            return result



    def Cancelar(self, key, window_id):
        """
        Estorna movimento contabilistico
        extorna caso confirmada ou simplesmente cancela se em rascunho
        """
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'        
        try:
            from my_diario import Diario
        except:
            from diario import Diario
        diario = Diario().get_diario(diario='vendas')
        try:
            from my_periodo import Periodo
        except:
            from periodo import Periodo
        periodo = Periodo().get_periodo(data=str(datetime.date.today()))
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        terceiro = Terceiro().get(key=self.kargs['cliente'])[0]
        sujeito_iva = terceiro['sujeito_iva']
        conta_terceiro = terceiro['a_receber']
        #Tanto no movimento como no stock eu poderei ter vários movimentos, por exemplo o movimento em si e a anulação, além disso teremos que ter reconciliação de movimentos.
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        movimento = Movimento(data=datetime.date.today(), numero=base_models.Sequence().get_sequence('movimento'), num_doc=self.kargs['numero'], descricao='Anulação de Nossa Factura', documento='factura_cli', diario=diario, periodo=periodo, estado='Confirmado', user=self.kargs['user']).put()
        #record['movimento'] = movimento
        try:
            from my_linha_factura_cli import LinhaFacturaCliente
        except:
            from linha_factura_cli import LinhaFacturaCliente
        record_lines = LinhaFacturaCliente(where="factura_cli = '{factura}'".format(factura=self.kargs['id'])).get()
        if record_lines:
            try:
                from my_linha_movimento import LinhaMovimento
            except:
                from linha_movimento import LinhaMovimento
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
                quantidade = to_decimal(line['quantidade'])
                product = Produto().get(key=line['produto'])[0]
                contas = Produto().get_accounts(line['produto'])
                conta_receitas = contas['conta_receitas']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = to_decimal(0)
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_receitas, quant_debito=quantidade, debito=total_sem_iva, quant_credito=to_decimal(0), credito=to_decimal(0), user=self.kargs['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_terceiro, quant_debito=to_decimal(0), debito=to_decimal(0), quant_credito=quantidade, credito=total_sem_iva, user=self.kargs['user']).put()
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
