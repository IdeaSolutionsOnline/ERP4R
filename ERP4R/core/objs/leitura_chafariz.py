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
__model_name__='leitura_chafariz.LeituraChafariz'
import auth, base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro

class LeituraChafariz(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'leitura_chafariz'
        self.__title__= 'Folhas de Leitura de Chafariz'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(leitura_chafariz.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar','Gera Leituras'], 'Confirmado':['Imprimir', 'Cancelar'], 'Impresso':['Cancelar'], 'Cancelado':[]}
            )
        self.__workflow_auth__ = {
            'Confirmar':['All'],
            'Gera Leituras':['Vendedor'],
            'Imprimir':['Vendedor'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.numero = info_field(view_order=1, name ='Número')
        self.leitor = combo_field(view_order=2, name ='Leitor', args='required', size=50, column='nome', options='model.get_terceiros()')
        self.data = date_field(view_order=3, name ='Data', default=datetime.date.today())
        self.notas = string_field(view_order=4, name ='Notas', args='autocomplete="on"', size=60, onlist=False)
        self.estado = info_field(view_order=5, name ='Estado', default='Rascunho')
        self.linha_leitura_chafariz = list_field(view_order=6, name ='Linhas de Leitura de Chafariz', condition="leitura_chafariz='{id}'", model_name='linha_leitura_chafariz.LinhaLeituraChafariz', list_edit_mode='inline', onlist = False)

    def get_terceiros(self):
        return Terceiro().get_funcionarios()

    def get_total(self, key):
        from linha_leitura_chafariz import LinhaLeituraChafariz
        value = to_decimal(0)
        record_lines = LinhaLeituraChafariz(where="leitura_chafariz = '{factura}'".format(factura=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total'])
        return value

    def get_total_desconto(self, key):
        from linha_leitura_chafariz import LinhaLeituraChafariz
        value = to_decimal(0)
        record_lines = LinhaLeituraChafariz(where="leitura_chafariz = '{factura}'".format(factura=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total']) * to_decimal(line['desconto']) / 100
        return round(value,0)

    def get_total_iva(self, key):
        from linha_leitura_chafariz import LinhaLeituraChafariz
        value = to_decimal(0)
        record_lines = LinhaLeituraChafariz(where="leitura_chafariz = '{factura}'".format(factura=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['valor_total']) - (to_decimal(line['valor_total']) / (1 +  to_decimal(line['iva']) / 100))
        return round(value,0)

    def print_doc(self, key, window_id):
        #Acção por defeito para imprimir o documento base
        #Deverá mudar o estado para impresso
        from linha_leitura_chafariz import LinhaLeituraChafariz
        path = os.path.join("./objs", model.__name__, "document.html")
        tmpl_file = open(path, 'r')
        tmpl_string = tmpl_file.read()
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Impresso'
        final_record = {}
        for field in model.__fields__:
            field_value = get_field_value(record, field, model)['field_value']
            #Os combo_field são tuples (id, valor)
            if isinstance(field_value, tuple):
                field_value = field_value[1]
            final_record[field[0]] = field_value
        record_lines = LinhaLeituraChafariz(where="leitura_chafariz = '{factura}'".format(factura=record['id'])).get()
        final_record_lines = []
        for line in record_lines:
            final_line = {}
            for field in LinhaLeituraChafariz().__fields__:
                final_line[field[0]] = get_field_value(line, field, LinhaLeituraChafariz())['field_value']
            final_line['valor_total_sem_iva'] = round(float(final_line['valor_total']) / (1 + float(final_line['iva'])/100),0)
            final_record_lines.append(final_line)
        final_record['linhas'] = final_record_lines
        LeituraChafariz(**record).put()
        return bottle.template(tmpl_string, final_record)

    def Gera_Leituras(self, key, window_id):
        return error_message('ainda não esta implementado')

    def Confirmar(self, key, window_id):
        # Gera movimento contabilistico (conta de receitas contra conta de terceiros)
        if key == 'None':
            #Grava o registo se ainda não estiver guardado
            key = get_actions(request=bottle.request, action='save', key=None, model_name=model.__model_name__, title=model.__title__, name=model.__name__, internal=True)
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Confirmado'
        record['numero'] = base_models.Sequence().get_sequence('leitura_chafariz')
        from diario import Diario
        diario = Diario(where="tipo='vendas'").get()[0]['id']
        periodo = None
        from periodo import Periodo
        periodos = Periodo().get()
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(record['data'])) in lista_datas:
                periodo = p['id']
        if not periodo:
            return error_message('não existe periodo definido para a data em questão! \n')
        #Valida se o cliente é sujeito a iva
        from terceiro import Terceiro
        terceiro = Terceiro(where="id='{cliente}'".format(cliente=record['cliente'])).get()[0]
        sujeito_iva = terceiro['sujeito_iva']
        conta_terceiro = terceiro['a_receber']
        from movimento import Movimento
        movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Nossa Factura', diario=diario, documento='leitura_chafariz', periodo=periodo, estado='Confirmado', user=session['user']).put()
        record['movimento'] = movimento
        LeituraChafariz(**record).put()
        from linha_leitura_chafariz import LinhaLeituraChafariz
        record_lines = LinhaLeituraChafariz(where="leitura_chafariz = '{factura}'".format(factura=record['id'])).get()
        if record_lines:
            from linha_movimento import LinhaMovimento
            from produto import Produto
            from familia_produto import FamiliaProduto
            for line in record_lines:
                # aqui depois considerar a contabilização do desconto
                quantidade = float(line['quantidade'])
                product = Produto().get(key=line['produto'])[0]
                conta_mercadorias = product['conta_receitas']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = 0.0
                #familia = FamiliaProduto().get(key=product['familia'])[1][0]
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_terceiro, quant_debito=quantidade, debito=total_sem_iva, quant_credito=0.0, credito=0.0, user=session['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_receitas, quant_debito=0.0, debito=0.0, quant_credito=quantidade, credito=total_sem_iva, user=session['user']).put()
            return form_edit(key=key, window_id = window_id)
        else:
            return error_message('Não pode confirmar facturas sem linhas de factura! \n')

    def Cancelar(self, key, window_id):
        #Estorna movimento contabilistico
        #extorna caso confirmada ou simplesmente cancela se em rascunho
        record_id = key
        record = model.get(key=record_id)[0]
        record['user'] = session['user']
        record['estado'] = 'Cancelado'
        from diario import Diario
        diario = Diario(where="tipo='vendas'").get()[0]['id']
        periodo = None
        from periodo import Periodo
        periodos = Periodo().get()
        for p in periodos:
            lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
            if str(format_date(str(datetime.date.today()))) in lista_datas:
                periodo = p['id']
        if not periodo:
            return error_message('não existe periodo definido para o data em questão! \n')
        #Valida se o cliente é sujeito a iva
        from terceiro import Terceiro
        terceiro = Terceiro(where="id='{cliente}'".format(cliente=record['cliente'])).get()[0]
        sujeito_iva = terceiro['sujeito_iva']
        conta_terceiro = terceiro['a_receber']
        #Tanto no movimento como no stock eu poderei ter vários movimentos, por exemplo o movimento em si e a anulação, além disso teremos que ter reconciliação de movimentos.
        from movimento import Movimento
        movimento = Movimento(data=datetime.date.today(), numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Anulação de Nossa Factura', documento='leitura_chafariz', diario=diario, periodo=periodo, estado='Confirmado', user=session['user']).put()
        record['movimento'] = movimento
        LeituraChafariz(**record).put()
        from linha_leitura_chafariz import LinhaLeituraChafariz
        record_lines = LinhaLeituraChafariz(where="leitura_chafariz = '{factura}'".format(factura=record['id'])).get()
        if record_lines:
            from linha_movimento import LinhaMovimento
            from produto import Produto
            from familia_produto import FamiliaProduto
            for line in record_lines:
                # aqui depois considerar a contabilização do desconto
                quantidade = float(line['quantidade'])
                product = Produto().get(key=line['produto'])[0]
                conta_receitas = product['conta_receitas']
                if sujeito_iva:
                    taxa_iva = product['iva']
                else:
                    taxa_iva = 0.0
                descricao = product['nome']
                total_sem_iva = line['valor_total']/(1+taxa_iva)
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_receitas, quant_debito=quantidade, debito=total_sem_iva, quant_credito=0.0, credito=0.0, user=session['user']).put()
                LinhaMovimento(movimento=movimento, descricao=descricao, conta=conta_terceiro, quant_debito=0.0, debito=0.0, quant_credito=quantidade, credito=total_sem_iva, user=session['user']).put()
            return form_edit(key=key, window_id = window_id)
