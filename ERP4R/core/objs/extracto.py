# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'extracto.Extracto'
import auth, base_models
from orm import *
from form import *
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

class Extracto(Model, View):
    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'extracto'
        self.__title__ = 'Extracto de Conta'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__db_mode__ = 'None'
        self.__workflow__ = (
            'estado', {'Rascunho':['Imprimir', 'Exportar']}
            )
        self.__workflow_auth__ = {
            'Imprimir':['All'],
            'Exportar':['All'],
            'full_access':['Gestor']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.conta = choice_field(view_order=1, name='Conta', size=100, args='required', model='plano_contas', column='codigo nome', options='model.get_contas()')
        self.data_inicial = date_field(view_order=2, name='Data Inicial')
        self.data_final = date_field(view_order=3, name='Data Final', default=datetime.date.today())
        self.estado = info_field(view_order=4, name='Estado', hidden=True, default='Rascunho')

    def get_contas(self):
        return PlanoContas().get_lancamento()

    def prepare_data(self):
        #print('estou no prepare data')
        conta = bottle.request.forms.get('conta')
        conta_show = bottle.request.forms.get('conta_show')
        if not conta:
            return 'sem_conta'
        #print(conta)
        data_final = bottle.request.forms.get('data_final')
        #print(data_final)
        data_inicial = bottle.request.forms.get('data_inicial')
        #print(data_inicial)
        data_where = """and data <= '{data_final}'""".format(data_final=data_final)
        #print(data_where)
        if data_inicial:
            data_where += """and data >= '{data_inicial}'""".format(data_inicial=data_inicial)
            #print(data_where)

        #depois acrescentar mais filtros como seja ano_fiscal, periodo, diario
            sql = """
select
sum(lm.debito) - sum(lm.credito) as saldo
from linha_movimento lm
join movimento m
on lm.movimento = m.id
where lm.conta = '{conta}'
and data < '{data_inicial}'
and (m.active = True or m.active is null)
and (lm.active = True or lm.active is null)
""".format(conta=conta, data_inicial=data_inicial)
            #print(sql)
            saldo_inicial = run_sql(sql)[0]['saldo']
        else:
            saldo_inicial = 0
        #print(saldo_inicial)
        sql = """
select
m.data as data, m.numero as movimento, m.documento, m.num_doc, lm.descricao, lm.debito, lm.credito
from linha_movimento lm
join movimento m
on lm.movimento = m.id
where lm.conta = '{conta}'
{data_where}
and (m.active = True or m.active is null)
and (lm.active = True or lm.active is null)
order by m.data""".format(conta=conta, data_where=data_where)
        #print(sql)
        db_lines = run_sql(sql)
        lines = []
        #print(lines)
        saldo = saldo_inicial
        #print('antes de lines')
        for line in db_lines:
            #print('in db_lines', line)
            debito = line['debito'] or 0
            credito = line['credito'] or 0
            #print(saldo, debito, credito)
            saldo += debito - credito
            line['debito'] = format_number(debito)
            line['credito'] = format_number(credito)
            line['saldo'] = format_number(saldo)
            lines.append(line)
        record = {}
        record['lines'] = lines
        record['saldo_inicial'] = format_number(saldo_inicial)
        record['conta'] = conta_show
        record['data_inicial'] = data_inicial
        record['data_final'] = data_final
        return record

    def Imprimir(self, key, window_id):
        #print('estou na função de Imprimir no extrato')
        template = 'extracto'
        record = self.prepare_data()
        if record == 'sem_conta':
            return error_message('Tem que escolher uma conta contabilística!')
        else:
            return Report(record=record, report_template=template).show()

    def Exportar(self, key, window_id):
        #print('estou na função de Exportar no extrato')
        result = self.prepare_data()['lines']
        if result == 'sem_conta':
            return error_message('Tem que escolher uma conta contabilística!')
        else:
            return data_to_csv(data=result, model=self, text='Gravar', cols=['data', 'movimento', 'descricao', 'debito', 'credito', 'saldo'])

    