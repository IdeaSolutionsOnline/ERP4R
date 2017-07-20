# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina']
__credits__ = []
__version__ = "1.0"
__maintainer__ =  ['António Anacleto', 'Jair Medina']
__status__ = "Development"
__model_name__= 'sai_modelo.Sai_Modelo'
#import base_models#auth,
from orm import *
from form import *


class Sai_Modelo (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_modelo'
        self.__title__= 'Modelo106 cruzamentos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir','Rascunho','Exportar']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Rascunho':['Gestor'],
            'Exportar':['All'],
            'Imprimir':['All'],
           }

        # self.__no_edit__ = [
        #     ('estado', ['Confirmado','Impresso'])
        #     ]
        self.__auth__ = {
            'read':['All'],
            'write':['Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }


        self.nome = string_field(view_order=1, name='Nome', size=100)
        self.descricao = text_field(view_order=3, name='Descrição', size=250)
        self.ano= string_field(view_order=2, name='Período', size=20, onlist=False)
        self.sql = text_field(view_order=4, name ='SQL', onlist=False, size=170 )
        self.estado = info_field(view_order=5, name ='Estado', default='Rascunho', onlist=True, dynamic_atrs = 'estado_dynamic_atrs',hidden=True, nolabel=True,)


        #AS cli INNER JOIN gre_v_modelo_106_3 AS f ON f.nu_factura=cli.nu_factura  and f.vl_factura = cli.vl_factura and f.dt_factura= cli.dt_factura
    def estado_dynamic_atrs(self, record, internal=False):
        #se inernal for igual a True é porque foi chamada internamente pelo forms
        #print('estou no estado_dynamic_atrs', record)
        result = {}
        from ujson import dumps
        if internal == False:
            bottle.response.content_type = 'application/json'
        #print(1)
        estado = record['estado']
        #print(estado)
        if estado == 'Confirmado':
            result = {'sql':{'nolabel':True, 'atrs':'style="visibility:hidden"'}}
        #print(result)
        return dumps(result)
    def prepare_data(self):

        sql = eval(bottle.request.forms.get('sql'))
        #print(sql)
        x=sql.split("//")
        #print(x)
        campo1=x[0]
        print(  campo1,'1')
        campo2=x[1]
        print(  campo2,'2')
        where=x[2]
        condicao=x[3]
        print(where, condicao)
        nome= bottle.request.forms.get('nome')
        descricao= bottle.request.forms.get('descricao')
        ano= bottle.request.forms.get('ano')
        record = {}
        print(nome,'nome')
        if nome=='Campo 01+04+05 = soma Valor de factura  (anexo de Clientes)' :

            sql = """select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,c.dt_periodo,sum(f.campo_01+f.campo_04+f.campo_05) as campo1, c.soma_vl_fc_cli as campo2  from cruz_modelo106 as c  JOIN gre_v_modelo_106_3 AS f  on f.nu_nif=c.nu_nif and f.dt_periodo=c.dt_periodo  and  c1_4_5_soma_fat_cli='{condicao}' and  c.dt_periodo='{ano}'  group by   c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,c.dt_periodo,c.soma_vl_fc_cli """.format(condicao=condicao,ano=ano)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['descricao'] = descricao
            record['ano'] = ano
            return record

        elif  nome =='(Campo 16/0.15) =  soma Valor de factura (anexo fornecedores)':

            sql = """select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,sum(f.campo_16/0.15) as campo1 ,sum(cl.vl_factura) as campo2,f.dt_periodo from cruz_modelo106 as c INNER JOIN gre_v_modelo_106_3 AS f  on c.nu_duc=f.nu_duc and c16_15port_soma_fat_for ='{condicao}' and  c.dt_periodo='{ano}' INNER JOIN gre_v_anxfor_2013 AS cl  on cl.nu_nif=c.nu_nif where cl.dt_periodo=f.dt_periodo group by  f.dt_periodo, c.nu_nif,c.nm_contribuinte,c.nu_duc,f.campo_06,f.campo_07,f.campo_08,f.campo_09,f.campo_10,f.campo_11,f.campo_12,f.campo_13,f.campo_14,f.campo_15,f.campo_16,f.campo_17,f.campo_18,f.campo_19,f.campo_20, f.campo_21,f.campo_22,f.campo_23,f.campo_24,f.campo_25,f.ds_area_fiscal""".format(condicao=condicao,ano=ano)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['descricao'] = descricao
            record['ano'] = ano
            return record

        elif nome == 'Campo 19 = Campo 25 (periodo anterior)':
            #print(nome, 'aquiiiiiiiiii')

            sql="""select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,f.campo_19 as campo1 ,cl.campo_25 as campo2,f.dt_periodo from cruz_modelo106 as c INNER JOIN gre_v_modelo_106_3 AS f  on c.nu_duc=f.nu_duc and c19_igual25ant = '{condicao}' and  c.dt_periodo='{ano}'   INNER JOIN gre_v_modelo_106_3 AS cl  on c.nu_nif=cl.nu_nif where c.periodo_ant=cl.dt_periodo """.format(condicao=condicao,ano=ano)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['descricao'] = descricao
            record['ano'] = ano
            return record
        elif nome == 'Campo 26 diferente Campo 19 (periodo posterior)':
            #print(nome, 'aquiiiiiiiiii')

            sql="""select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,f.campo_26 as campo1 ,cl.campo_19 as campo2,f.dt_periodo from cruz_modelo106 as c INNER JOIN gre_v_modelo_106_3 AS f  on c.nu_duc=f.nu_duc and c26_dif_19dep = '{condicao}' and  c.dt_periodo='{ano}'  INNER JOIN gre_v_modelo_106_3 AS cl  on c.nu_nif=cl.nu_nif where c.periodo_dep=cl.dt_periodo  """.format(condicao=condicao,ano=ano)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['descricao'] = descricao
            record['ano'] = ano
            return record
        elif nome == 'soma Campo 15 (Jan a Dez) igual Q5_V19 (Mod 1B)':
            #print(nome, 'aquiiiiiiiiii')

            sql="""select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,sum(f.campo_15) as campo1 ,cl.q5_v19 as campo2,f.dt_ano from cruz_modelo106 as c INNER JOIN gre_v_modelo_106_3 AS f  on c.nu_duc=f.nu_duc and c.ano=f.dt_ano and c15_igual_q5_v19 = '{condicao}'  and c.ano='{ano}'   INNER JOIN gre_v_n_mod_1b_3 AS cl  on c.nu_nif=cl.nu_nif where cast (c.ano as int)=cl.ano_economico group by cl.q5_v19,c.nu_nif,f.dt_ano,c.nm_contribuinte,f.ds_area_fiscal  """.format(condicao=condicao,ano=ano)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['descricao'] = descricao
            record['ano'] = ano
            return record

        else:

            sql = """ select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,{campo1},{campo2},f.dt_periodo from cruz_modelo106 as c INNER JOIN gre_v_modelO_106_3 AS f  on c.nu_duc=f.nu_duc WHERE {where} ='{condicao}'  and  c.dt_periodo='{ano}'  group by f.dt_periodo, c.nu_nif,c.nm_contribuinte,c.nu_duc,f.campo_01,f.campo_02,f.campo_03,f.campo_04,f.campo_05,f.campo_06,f.campo_07,f.campo_08,f.campo_09,f.campo_10,f.campo_11,f.campo_12,f.campo_13,f.campo_14,f.campo_15,f.campo_16,f.campo_17,f.campo_18,f.campo_19,f.campo_20, f.campo_21,f.campo_22,f.campo_23,f.campo_24,f.campo_25,f.ds_area_fiscal """.format(where=where,condicao=condicao,ano=ano,campo1=campo1,campo2=campo2)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['descricao'] = descricao
            record['ano'] = ano
            return record



#

#select c.nu_nif,c.nm_contribuinte,f.ds_area_fiscal,c.nu_duc,sum(f.campo_15) as campo1 ,cl.q5_v19 as campo2,f.dt_periodo from cruz_modelo106 as c INNER JOIN gre_v_modelo_106_3 AS f  on c.nu_duc=f.nu_duc and c.ano=f.dt_ano and c15_igual_q5_v19 = True   INNER JOIN gre_v_n_mod_1b_3 AS cl  on c.nu_nif=cl.nu_nif where cast (c.ano as int)=cl.ano_economico group by cl.q5_v19,c.nu_nif,c.nm_contribuinte,f.dt_periodo,f.ds_area_fiscal,c.nu_duc  order by nu_nif asc








    def Imprimir(self, key, window_id):
        print('4')
        record =self.prepare_data()

        if record['nome']== 'soma Campo 15 (Jan a Dez) igual Q5_V19 (Mod 1B)':
            template = 'modelo106_1b'
            #print('3')

            #print('1')
            print (template)
            return Report(record=record, report_template=template).show()
        else:
            template = 'modelo106'
        #print('3')

        #print('1')
            print (template)
            return Report(record=record, report_template=template).show()




    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id = window_id).show()


    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()


    def Exportar(self, key, window_id):
        x=self.prepare_data()
        #record = get_records_to_print(key=key, model=self)
        #print (record, key)
        sql = x['sql2'] #record['sql']
        print(sql, 'noooooooooo Exportar')
        # variaveis = record['linha_sql_report']
        # if variaveis:
        #     variaveis_dict = {}
        #     for variavel in variaveis:
        #         variaveis_dict[variavel['variavel']] = variavel['valor']
        #     sql = sql.format(**variaveis_dict)
        result = run_sql(sql)
        return data_to_csv(result, self, 'Gravar')