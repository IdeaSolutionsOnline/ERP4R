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
__model_name__='proforma.Proforma'
import auth, base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class Proforma(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'proforma'
        self.__title__= 'Facturas Proforma'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(proforma.numero) DESC'

        self.__workflow__ = (
            'estado', {'Rascunho':['Gerar Factura', 'Imprimir'], 'Com Factura':['Imprimir', 'Cancelar'], 'Cancelada':['Rascunho']}
            )

        self.__workflow_auth__ = {
            'Gerar Factura':['Vendedor'],
            'Imprimir':['All'],
            'Cancelar':['Gestor'],
            'Rascunho':['Gestor'],
            'full_access':['Gestor']
            }

        self.__no_edit__ = [
            ('estado', ['Com Factura','Cancelada'])
            ]

        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order = 1, name = 'Data', default = datetime.date.today())
        self.numero = info_field(view_order = 2, name = 'Número', args='readonly')
        self.cliente = choice_field(view_order = 3, name = 'Cliente', args = 'required', size = 80, model = 'terceiro', column = 'nome', options = 'model.get_terceiros()')
        self.notas = string_field(view_order = 4, name = 'Notas', args = 'autocomplete="on"', size = 100, onlist = False)
        self.total_desconto = function_field(view_order = 5, name = 'Desconto', size = 20, sum = True, search = False)
        self.factura = parent_field(view_order = 6, name = 'Factura', model_name = 'factura_cli.FacturaCliente', column = 'numero')
        self.total_iva = function_field(view_order = 7, name = 'Total IVA', size = 20, sum = True, search = False)
        self.total = function_field(view_order = 8, name = 'Total', size = 20, sum = True, search = False)
        self.estado = info_field(view_order = 9, name = 'Estado', default = 'Rascunho')
        self.linha_proforma = list_field(view_order = 10, name = 'Linhas de Factura Proforma', condition = "proforma='{id}'", model_name = 'linha_proforma.LinhaProforma', list_edit_mode = 'inline', onlist = False)

    def get_terceiros(self):
        return Terceiro().get_clientes()


    def record_lines(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            try:
                from my_linha_proforma import LinhaProforma
            except:
                from linha_proforma import LinhaProforma
            record_lines = LinhaProforma(where = "proforma = '{proforma}'".format(proforma = key)).get()
            return record_lines
        return erp_cache.get(key = self.__model_name__ + str(key), createfunc = get_results)


    def get_total(self, key):
        #print('Im in get_total em proforma')
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total'])
        #print('fim do get_total em proforma')
        return value

    def get_total_desconto(self, key):
        #print('Im in get_total_desconto em proforma')
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total']) * to_decimal(line['desconto']) / 100
        #print('fim do get_total_desconto em proforma')
        return round(value,0)

    def get_total_iva(self, key):
        #print('Im in get_total_iva em proforma')
        value = to_decimal(0)
        record_lines = self.record_lines(key)
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  to_decimal(line['iva']) / 100))
        #print('fim do get_total_iva em proforma')
        return round(value,0)

    def Imprimir(self, key, window_id):
        template = 'proforma'
        record = get_records_to_print(key = key, model = self)
        cliente = Terceiro().get(key = record['cliente'][0])[0]
        try:
            from my_contacto import Contacto
        except:
            from contacto import Contacto
        moradas = Contacto(where = "terceiro = '{cliente}'".format(cliente = cliente['id'])).get()
        if len(moradas) != 0:
            moradas = moradas[0]
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
        return Report(record = record, report_template = template).show()


    def Gerar_Factura(self, key, window_id):
        #Gera Factura em rascunho!!!
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Com Factura'
        try:
            from my_factura_cli import FacturaCliente
        except:
            from factura_cli import FacturaCliente
        factura = FacturaCliente(data = self.kargs['data'], notas = self.kargs['notas'], entrega = self.kargs['id'], cliente = self.kargs['cliente'], residual = str(to_decimal('0')), estado = 'Rascunho', user = self.kargs['user']).put()
        self.kargs['factura'] = factura
        #Valida se o cliente é sujeito a iva
        try:
            from my_terceiro import Terceiro
        except:
            from terceiro import Terceiro
        sujeito_iva = Terceiro(where = "id='{cliente}'".format(cliente=str(self.kargs['cliente']))).get()[0]['sujeito_iva']
        try:
            from my_linha_proforma import LinhaProforma
        except:
            from linha_proforma import LinhaProforma
        record_lines = LinhaProforma(where = "proforma = '{proforma}'".format(proforma = self.kargs['id'])).get()
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

    def Cancelar(self, key, window_id):
        #faz sentido cancelar depois de ter gerado a entrega, se fizer terei que anular a entrega e eventualmente alguma factura e ate pagamento?
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Cancelada'
        self.put()
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()

