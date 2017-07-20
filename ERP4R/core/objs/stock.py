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
__model_name__ = 'stock.Stock'
import auth, base_models
from orm import *
from form import *
try:
    from my_periodo import Periodo
except:
    from periodo import Periodo
try:
    from my_tipo_documento import TipoDocumento
except:
    from tipo_documento import TipoDocumento

class Stock(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'stock'
        self.__title__ = 'Movimentos de Stock'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(stock.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir', 'Cancelar'], 'Impresso':['Imprimir', 'Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['All'],
            'Imprimir':['All'],
            'Cancelar':['Gestor'],
            'Rascunho':['Contabilista'],
            'full_access':['Gestor']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor de Stocks', 'Gestor'],
            'full_access':['Gestor de Stocks', 'Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name='Data', args='required ', default=datetime.date.today())
        self.numero = info_field(view_order=2, name='Número', args='readonly')
        self.descricao = string_field(view_order=3, name='Descrição', args='autocomplete="on"', size=60)
        self.documento = combo_field(view_order=4, name='Documento', size=40, onlist=False, column='nome', options="model.get_opts('TipoDocumento')")
        self.num_doc = integer_field(view_order=5, name='N.Documento')
        self.periodo = choice_field(view_order=6, name='Periodo', args='required', default='get_periodo()', model='periodo', column='nome', options="model.get_opts('Periodo')")
        self.funcionario = parent_field(view_order=7, name='Funcionario', size=40, default="session['user']", model_name='users.Users', onlist=False, column='nome')
        self.estado = info_field(view_order=8, name='Estado', default='Rascunho')
        self.linha_stock = list_field(view_order=9, name='Linhas de Movimento de Stock', condition="stock='{id}'", model_name='linha_stock.LinhaStock', list_edit_mode='inline', onlist = False)

    def get_opts(self, model):
        return eval(model + '().get_options()')

    def get_periodo(self):
        #print ('Im in get_periodo', Periodo().get_periodo(data = str(datetime.date.today())))
        return Periodo().get_periodo(data = str(datetime.date.today()))

    def Imprimir(self, key, window_id):
        template = 'stock'
        record = get_records_to_print(key=key, model=self)
        return Report(record=record, report_template=template).show()

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('stock')
#       periodo = self.kargs['periodo']
#       p = Periodo().get(key=periodo)[1][0]
#       lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
#       if str(format_date(record['data'])) not in lista_datas:
#           return error_message('O periodo escolhido não é válido! \n')
        self.put()
        ctx_dict = get_context(window_id)
        ctx_dict['main_key'] = self.kargs['id']
        set_context(window_id, ctx_dict)
        return form_edit(window_id = window_id).show()

    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()

