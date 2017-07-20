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
__model_name__='factura_forn.FacturaFornecedor'
import auth, base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class FacturaFornecedor(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'factura_forn'
        self.__title__= 'Facturas de Fornecedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(factura_forn.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir', 'Pagar', 'Cancelar'], 'impresso':['Cancelar'], 'cancelado':[]}
            )
        self.__workflow_auth__ = {
            'Confirmar':['All'],
            'Imprimir':['All'],
            'Pagar':['Caixa'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
       
        self.__tabs__ = [
            ('Faturação', ['data','numero','serie','fornecedor','retencao','taxa_retencao','estado','residual','notas','vendedor','linha_factura_forn','total','total_desconto', 'total_iva','total_dedutivel','valor_retido']),
            ('Movimentos', ['movs_contab', 'movs_stock']),
            ('Pagamentos',['pagamentos']),
            ]
        self.__no_edit__ = [
            ('estado', ['Confirmado','Pago','Impresso','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name ='Data', args='required ', default=datetime.date.today())
        self.numero = info_field(view_order=2, name ='Número',size=30)
        self.serie = string_field(view_order=3, name='Serie', size=30, args='required')
        self.notas = string_field(view_order=4, name ='Notas', args='autocomplete="on"', size=200, onlist=False)
        self.fornecedor = choice_field(view_order=5, name ='Fornecedor', args='required', size=100, model='terceiro', column='nome', options='model.get_fornecedores()')
        self.residual = currency_field(view_order=6, name ='Valor Residual', args='readonly', size=45, sum=True)
        self.estado = info_field(view_order=7, name ='Estado', size=45, default='Rascunho', options=[('rascunho','Rascunho'), ('confirmado','Confirmado'), ('cancelado','Cancelado')])
        self.pagamentos = list_field(view_order=8, name ='Pagamentos', condition="documento='factura_forn' and num_doc={numero}", model_name='linha_caixa.LinhaCaixa', list_edit_mode='edit', onlist = False)
        self.movs_contab = list_field(view_order=9, name ='Movimentos Contab.', condition="documento='factura_forn' and num_doc={numero}", model_name='movimento.Movimento', list_edit_mode='edit', onlist = False)
        self.movs_stock = list_field(view_order=10, name ='Movimentos Stock', condition="documento='factura_forn' and num_doc={numero}", model_name='stock.Stock', list_edit_mode='edit', onlist = False)
        self.linha_factura_forn = list_field(view_order=11, name ='Linhas de Factura do Fornecedor', condition="factura_forn='{id}'", model_name='linha_factura_forn.LinhaFacturaFornecedor', list_edit_mode='inline', onlist= False, search= True)
        self.total = function_field(view_order=12, name ='Total', size=70, sum=True)
        self.total_iva = function_field(view_order=13, name ='Total IVA', size=70)
        self.total_dedutivel = function_field(view_order=14, name ='Total IVA Dedutivel', size=70)
        #self.retencao=boolean_field(view_order=15,name='Efectuar Retenção?', default=False,size=90)
        self.retencao = combo_field(view_order=15,name='Retenção?', default="NAO", options=[('NAO','NAO'),('SIM','SIM')], size=50)
        self.taxa_retencao = percent_field(view_order=16, name ='Taxa Retenção', size=45, onlist=False)
        self.valor_retido=function_field(view_order=17, name='Total Retenção', onlist=False, args='readonly',size=70)


    def get_fornecedores(self):
        #print('estou em get_fornecedores do factura fornecedor')
        return Terceiro().get_fornecedores()

    def record_lines(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            try:
                from my_linha_factura_forn import LinhaFacturaFornecedor
            except:
                from linha_factura_forn import LinhaFacturaFornecedor
            record_lines = LinhaFacturaFornecedor(where="factura_forn = '{factura}'".format(factura=key)).get()
            return record_lines
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)

    def getRecord(self, key):
        def get_record():
            record = FacturaFornecedor(where="id = '{id}'".format(id=key)).get()
            return record
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_record)


    def get_valor_retido(self, key):
        try:
            from my_rh_retencao import RHRetencao
        except:
            from rh_retencao import RHRetencao
        value = to_decimal(0)
        if self.kargs['retencao']:
            taxa = self.kargs['taxa_retencao']
            if to_decimal(taxa) == to_decimal(0):
                ret = RHRetencao().get()
                if ret:
                    taxa = ret[0]['taxa_prestacao_servico']                    
            total = self.get_total(key=key)    
            value = to_decimal(total*taxa/100)
            self.kargs['taxa_retencao']=taxa
            self.put()
        else:
            self.kargs['taxa_retencao']=to_decimal(0)
            self.put()
        return round(value,0)


    def get_total(self, key):
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total'])
        return round(value,0)


    def get_total_desconto(self, key):
        value = to_decimal(0)        
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += float(line['valor_total']) * float(line['desconto']) / 100
        return round(value,0)


    def get_total_iva(self, key):
        value = to_decimal(0)    
        if not self.kargs['retencao']: 
            record_lines = self.record_lines(key=key)
            if record_lines:
                for line in record_lines:                
                    value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100)))                
        return round(value,0)


    def get_total_incidencia(self, key):
        value = to_decimal(0)  
        if not self.kargs['retencao']:      
            record_lines = self.record_lines(key=key)
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

    def get_total_dedutivel(self, key):
        value = to_decimal(0)   
        if not self.kargs['retencao']:     
            record_lines = self.record_lines(key=key)
            if record_lines:
                for line in record_lines:                
                    if to_decimal(line['iva']) > to_decimal(0):
                        value += (to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100))))*(line['direito_deducao']/100)
        return round(value,0)

    def get_total_dedutivel_por_taxa(self, record_lines):
        value = to_decimal(0)        
        if record_lines:
            for line in record_lines:                
                if to_decimal(line['iva']) > to_decimal(0):
                    value += (to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  (to_decimal(line['iva']) / 100))))*(line['direito_deducao']/100)
        return round(value,0)

    def Imprimir(self, key, window_id):
        template = 'factura_forn'
        record = get_records_to_print(records=[self.kargs], model=self, child='linha_factura_forn')
        return Report(record=record, report_template=template).show()

# falta converter de cliente para fornecedor

    def Confirmar(self, key, window_id):
        """Gera movimento contabilistico (conta de receitas contra conta de terceiros)"""
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('factura_forn')
        try:
            from my_diario import Diario
        except:
            from diario import Diario
        diario = Diario().get_diario(diario='compras')
        try:
            from my_periodo import Periodo
        except:
            from periodo import Periodo
        periodo = Periodo().get_periodo(data=self.kargs['data'])
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        terceiro = Terceiro().get(key=self.kargs['fornecedor'])[0]
        sujeito_iva = terceiro['sujeito_iva']
        conta_terceiro = terceiro['a_receber']
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento

        movimento = Movimento(data=self.kargs['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=self.kargs['numero'], descricao='Vossa Factura', diario=diario, documento='factura_forn', periodo=periodo, estado='Confirmado', user=self.kargs['user']).put()
        #self.kargs['movimento'] = movimento
        try:
            from my_linha_factura_forn import LinhaFacturaFornecedor
        except:
            from linha_factura_forn import LinhaFacturaFornecedor
        record_lines = LinhaFacturaFornecedor(where="factura_forn = '{factura}'".format(factura=self.kargs['id'])).get()
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
                quantidade = float(line['quantidade'])
                product = Produto().get(key=line['produto'])[0]
                contas = Produto().get_accounts(line['produto'])
                #print (contas)
                conta_gastos = contas['conta_gastos']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = to_decimal(0)
                descricao = product['nome']                
                total_sem_iva = line['valor_total']/(1+taxa_iva)                
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_terceiro, quant_debito=quantidade, debito=total_sem_iva, quant_credito=to_decimal(0), credito=to_decimal(0), user=self.kargs['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_gastos, quant_debito=to_decimal(0), debito=to_decimal(0), quant_credito=quantidade, credito=total_sem_iva, user=self.kargs['user']).put()
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)
            return form_edit(window_id = window_id).show()
        else:
            return error_message('Não pode confirmar facturas sem linhas de factura! \n')

    def Cancelar(self, key, window_id):
        """
        Estorna movimento contabilistico
        extorna caso confirmada ou simplesmente cancela se em rascunho
        """
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        #print (self.kargs)
        try:
            from my_diario import Diario
        except:
            from diario import Diario
        diario = Diario().get_diario(diario='compras')
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
        terceiro = Terceiro().get(key=self.kargs['fornecedor'])[0]
        sujeito_iva = terceiro['sujeito_iva']
        conta_terceiro = terceiro['a_receber']
        #Tanto no movimento como no stock eu poderei ter vários movimentos, por exemplo o movimento em si e a anulação, além disso teremos que ter reconciliação de movimentos.
        try:
            from my_movimento import Movimento
        except:
            from movimento import Movimento
        movimento = Movimento(data=datetime.date.today(), numero=base_models.Sequence().get_sequence('movimento'), num_doc=self.kargs['numero'], descricao='Anulação de Vossa Factura', documento='factura_forn', diario=diario, periodo=periodo, estado='Confirmado', user=self.kargs['user']).put()
        #record['movimento'] = movimento
        try:
            from my_linha_factura_forn import LinhaFacturaFornecedor
        except:
            from linha_factura_forn import LinhaFacturaFornecedor
        record_lines = LinhaFacturaFornecedor(where="factura_forn = '{factura}'".format(factura=self.kargs['id'])).get()
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
                conta_gastos = contas['conta_gastos']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = to_decimal(0)
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_gastos, quant_debito=quantidade, debito=total_sem_iva, quant_credito=to_decimal(0), credito=to_decimal(0), user=self.kargs['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_terceiro, quant_debito=to_decimal(0), debito=to_decimal(0), quant_credito=quantidade, credito=total_sem_iva, user=self.kargs['user']).put()
        self.put()
        ctx_dict = get_context(window_id)
        ctx_dict['main_key'] = self.kargs['id']
        set_context(window_id, ctx_dict)
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()
