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
__model_name__ = 'balancete.Balancete'
import auth, base_models
from orm import *
from form import *
try:
    from my_ano_fiscal import AnoFiscal
except:
    from ano_fiscal import AnoFiscal
try:
    from my_periodo import Periodo
except:
    from periodo import Periodo

class Balancete(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'balancete'
        self.__title__ = 'Balancete'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__db_mode__ = 'None'# se o db_mode for none abre directo no edit em vez da lista
        self.__workflow__ = (
            'estado', {'Rascunho':['Imprimir', 'Exportar']}
            )
        self.__workflow_auth__ = {
            'Imprimir':['Contabilista'],
            'Exportar':['Contabilista'],
            'full_access':['Gestor']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Contabilista'],
            'full_access':['Gestor']
            }

        self.data_inicial = date_field(view_order=1, name ='Data Inicial')
        self.data_final = date_field(view_order=2, name ='Data Final', default=datetime.date.today())
        self.nivel = combo_field(view_order=5, name ='Nivel', options=[('lancamento','Lançamento'), ('razao','Razão'), ('agrupadoras','Agrupadoras')])
        # ano fiscal e periodos deverá ser lista idealmente seria um multiselect
        #self.ano_fiscal = choice_field(view_order=3, name ='Ano Fiscal', model='ano_fiscal', column='nome', options='model.get_ano_fiscal()')
        #self.periodo = choice_field(view_order=4, name ='Periodo', model='periodo', column='nome', options='model.get_periodo()')
        #self.saldos_do_periodo = boolean_field(view_order=6, name ='Saldos do Periodo?')
        #self.Inclui_passado = boolean_field(view_order=6, name ='Inclui Saldos Anteriores?')
        self.estado = info_field(view_order=7, name ='Estado', hidden=True, nolabel=True, default='Rascunho')

    def get_ano_fiscal(self):
        return AnoFiscal().get_options()

    def get_periodo(self):
        return Periodo().get_options()

    def prepare_data(self):
        #print('prepare data do balancete')
        nivel = bottle.request.forms.get('nivel')
        #print(nivel)
        #depois implementar os restantes filtros
        #ano_fiscal =
        #periodo =
        #saldos_do_periodo = 
        data_final = bottle.request.forms.get('data_final')
        #print(data_final)
        data_inicial = bottle.request.forms.get('data_inicial')
        #print(data_inicial)
        data_where = """and m.data <= '{data_final}'""".format(data_final=data_final)
        #print(data_where)
        if data_inicial:
            data_where += """and m.data >= '{data_inicial}'""".format(data_inicial=data_inicial)
        #print(data_where)
        sql = """
select 
    pc.id,
    pc.codigo,
    pc.nome as conta,
    pc.ascendente,
    coalesce(sum(lm.debito),0.00) as debito,
    coalesce(sum(lm.credito),0.00) as credito,
    coalesce(sum(lm.debito),0.00) - coalesce(sum(lm.credito),0.00) as saldo
from plano_contas pc 
join linha_movimento lm
on lm.conta = pc.id
join movimento m
on lm.movimento = m.id
where (pc.active = True or pc.active is null)
and (m.active = True or m.active is null)
and (lm.active = True or lm.active is null)
{data_where}
group by pc.id, pc.codigo, pc.nome, pc.ascendente
order by pc.codigo
""".format(data_where=data_where)
        #print(sql)
        db_lines = run_sql(sql)
        #print(db_lines)
        try:
            from my_plano_contas import PlanoContas
        except:
            from plano_contas import PlanoContas
        all_contas = PlanoContas().get(order_by='codigo')
        contas = {}
        for conta in all_contas:
            contas[conta['id']] = conta
        #descendentes = {}
        #for conta in all_contas:
         #   if conta['ascendente'] in descendentes:
          #      descendentes[conta['ascendente']].append(conta['id'])
           # else:
           #     descendentes[conta['ascendente']] = [conta['id']]
        #print(contas)
        movimentos = {}
        for line in db_lines:
            #print(line)
            movimentos[line['id']] = {'codigo':line['codigo'], 'conta':line['conta'], 'ascendente':line['ascendente'], 'debito':line['debito'], 'credito':line['credito'], 'saldo':line['saldo'], 'somado':False}
        #print(movimentos)
        for x in range(30):#abordagem feia e deselegante
            linhas = movimentos.copy()
            for m in linhas:
                movimento = linhas[m]
                if not movimento['somado']:
                    movimento['somado'] = True
                    if movimento['ascendente']:
                        if movimento['ascendente'] in movimentos:
                            movimentos[movimento['ascendente']]['debito'] += movimento['debito']
                            movimentos[movimento['ascendente']]['credito'] += movimento['credito']
                            movimentos[movimento['ascendente']]['saldo'] += movimento['saldo']
                        else:
                            movimentos[movimento['ascendente']] = {'codigo': contas[movimento['ascendente']]['codigo'], 'conta': contas[movimento['ascendente']]['nome'], 'ascendente': contas[movimento['ascendente']]['ascendente'], 'debito': movimento['debito'], 'credito': movimento['credito'], 'saldo': movimento['saldo'], 'somado':False}
        #print(movimentos)
        lines = []
        for line in all_contas:
            #print(line['id'])
            #print(movimentos[line['id']])
            if line['id'] in movimentos:
                #print('im in movimentos')
                rec_line = {}
                rec_line['codigo'] = movimentos[line['id']]['codigo']
                rec_line['conta'] = movimentos[line['id']]['conta'].replace(';', ',')
                rec_line['debito'] = format_number(movimentos[line['id']]['debito'])
                rec_line['credito'] = format_number(movimentos[line['id']]['credito'])
                rec_line['saldo'] = format_number(movimentos[line['id']]['saldo'])
                lines.append(rec_line)
            #else:
                #print('im not in movimentos')
                #rec_line = {}
                #rec_line['codigo'] = line['codigo']
                #rec_line['conta'] = line['nome'].replace(';', ',')
                #rec_line['debito'] = format_number(0)
                #rec_line['credito'] = format_number(0)
                #rec_line['saldo'] = format_number(0)
                #lines.append(rec_line)
        #print(lines)
        record = {}
        record['lines'] = lines
        record['data_inicial'] = data_inicial
        record['data_final'] = data_final
        record['periodos'] = ''#periodos
        record['anos_fiscais'] = ''#anos_fiscais
        record['nivel'] = ''#nivel
        return record
                                                                                                        
    def Imprimir(self, key, window_id):
        #print('estou no imprimir do balancete')
        template = 'balancete'
        record = self.prepare_data()
        return Report(record=record, report_template=template).show()

    def Exportar(self, key, window_id):
        #print('estou na função de Exportar no balancete')
        result = self.prepare_data()['lines']
        #print('result: ', result)
        return data_to_csv(data=result, model=self, text='Gravar', cols=['codigo', 'conta', 'debito', 'credito', 'saldo'])
