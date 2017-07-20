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
__model_name__ = 'movimento.Movimento'
import auth, base_models
from orm import *
from form import *
try:
    from my_diario import Diario
except:
    from diario import Diario
try:
    from my_periodo import Periodo
except:
    from periodo import Periodo
try:
    from my_tipo_documento import TipoDocumento
except:
    from tipo_documento import TipoDocumento



class Movimento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'movimento'
        self.__title__ = 'Movimentos Contabilisticos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'data'#'int8(movimento.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir', 'Cancelar'], 'Impresso':['Imprimir', 'Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['All'],
            'Imprimir':['All'],
            'Cancelar':['Gestor'],
            'Rascunho':['Contabilista'],
            'full_access':['Gestor'],
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso','Cancelado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.data = date_field(view_order=1, name ='Data', args='required ', default='datetime.date.today()')
        self.numero = info_field(view_order=2, name ='Número', args='readonly')
        self.descricao = string_field(view_order=3, name ='Descrição', args='autocomplete="on"', size=60)
        self.documento = combo_field(view_order=4, name ='Documento', size=80, onlist=False, args='required', model='tipo_documento', column='nome', options="model.get_opts('TipoDocumento')")
        self.diario = combo_field(view_order=5, name ='Diário', args='required', model='diario', column='nome', options="model.get_opts('Diario')")
        self.num_doc = integer_field(view_order=6, name ='Número Documento', size=30, args='required')
        self.periodo = choice_field(view_order=7, name ='Periodo', args='required', model='periodo', column='nome', options="model.get_opts('Periodo')")#default='self.get_periodo()'
        self.total_debito = function_field(view_order=9, name ='Total Débito', size=30, sum=True, search=False)
        self.total_credito = function_field(view_order=10, name ='Total Crédito', size=30, sum=True, search=False)
        self.estado = info_field(view_order=11, name ='Estado', default='Rascunho')
        self.linha_movimento = list_field(view_order=12, name ='Linhas de Movimento', condition="movimento='{id}'", model_name='linha_movimento.LinhaMovimento', list_edit_mode='inline', onlist = False)

    def get_opts(self, model):
        return eval(model + '().get_options()')

# ir buscar a periodo
#   def get_periodo(self):
#       periodos = Periodo().get()[1]
#       periodo = None
#       for p in periodos:
#           lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
#           if str(format_date(str(datetime.date.today()))) in lista_datas:
#               periodo = p['id']
#       return periodo

    def get_total_debito(self, key):
        from linha_movimento import LinhaMovimento
        value = to_decimal(0)
        record_lines = LinhaMovimento(where="movimento = '{movimento}'".format(movimento=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['debito'])
        return round(value,0)

    def get_total_credito(self, key):
        from linha_movimento import LinhaMovimento
        value = to_decimal(0)
        record_lines = LinhaMovimento(where="movimento = '{movimento}'".format(movimento=key)).get()
        if record_lines:
            for line in record_lines:
                value += to_decimal(line['credito'])
        return round(value,0)

    def print_doc(self, key, window_id):
        #Acção por defeito para imprimir o documento base
        #Deverá mudar o estado para impresso
        from linha_transferencia import LinhaTransferencia
        path = os.path.join("./objs", model.__name__, "movimento.html")
        tmpl_file = open(path, 'r', encoding='UTF8')
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
        record_lines = LinhaTransferencia(where="transferencia = '{transferencia}'".format(transferencia=record['id'])).get()
        final_record_lines = []
        for line in record_lines:
            final_line = {}
            for field in LinhaTransferencia().__fields__:
                final_line[field[0]] = get_field_value(line, field, LinhaTransferencia())['field_value']
        final_record['linhas'] = final_record_lines
        Transferencia(**record).put()
        return bottle.template(tmpl_string, final_record)

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model = self, key = key, force_db = self.__force_db__)
        #periodo = record['periodo']
        #p = Periodo().get(key=periodo)[0]
        #lista_datas = generate_dates(start_date=p['data_inicial'], end_date=p['data_final'])
        #if str(format_date(record['data'])) not in lista_datas:
        #    return error_message('O período escolhido não é válido! \n')
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('movimento')
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Cancelar(self, key, window_id):
        #faz sentido cancelar depois de ter gerado a entrega, se fizer terei que anular a entrega e eventualmente alguma factura e ate pagamento?
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()
