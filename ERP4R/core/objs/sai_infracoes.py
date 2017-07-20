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
__model_name__= 'sai_infracoes.Sai_Infracoes'
#import base_models#auth,
from orm import *
from form import *


class Sai_Infracoes(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_infracoes'
        self.__title__= 'Infrações'
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
        #     ('estado', ['Confirmado','Impresso','Cancelado'])

        self.__auth__ = {
            'read':['All'],
            'write':['Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }

        self.nome = string_field(view_order=1, name='Nome', size=100)
        self.descricao = text_field(view_order=4, name='Descrição', size=250)
        self.data_inicial = date_field(view_order=2, name ='Data Inicial', onlist=False)
        self.data_final = date_field(view_order=3, name ='Data Final', default=datetime.date.today(), onlist=False)
        self.sql = text_field(view_order=5, name ='SQL', onlist=False, size=170)
        self.valor = integer_field(view_order=6, name ='A partir do valor de:', onlist=False, size=100 )
        self.estado = info_field(view_order=9, name ='Estado', default='Rascunho', onlist=True, hidden=True,  dynamic_atrs = 'estado_dynamic_atrs',nolabel=True,)
        self.cliente = boolean_field(view_order = 8, name = 'Cliente?', default = False, onlist=False)
        self.fornecedor = boolean_field(view_order = 7, name = 'Fornecedor?', default = True, onlist=False)
        #self.reparticaoFinanca = combo_field(view_order=5, name ='Repartições das Finanças', options=[('praia','Praia'), ('mindelo','Mindelo'), ('santaMaria','Santa Maria')], onlist=False, default='Praia')

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

        sql2 = eval(bottle.request.forms.get('sql'))
        x=sql2.split("//")
        #print(x)
        where=x[0]
        condicao=x[1]
        nome= bottle.request.forms.get('nome')
        valor= bottle.request.forms.get('valor')
        descricao= bottle.request.forms.get('descricao')
        data_final = bottle.request.forms.get('data_final')
        #print(data_final)
        data_inicial = bottle.request.forms.get('data_inicial')

        cliente = bottle.request.forms.get('cliente')
        record = {}
        #print(nu_nif, cliente)

        if nome == 'InformaÃ§Ã£o InvÃ¡lida':
            if cliente == 'False' :
            # print(data_inicial)
            #data_where = """and dt_factura <= '{data_final}'""".format(data_final=data_final)
            #print(data_where)
            #if data_inicial:
            #data_where += """and dt_factura >= '{data_inicial}'""".format(data_inicial=data_inicial)
            #print(data_where)
            # sql2 = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo, nu_factura, nm_contribuinte_anexo,dt_factura,vl_factura from anexo_cli_out_13 where nif_valido =  '{nif_valido}' and vl_factura >= '{valor}' """.format(nif_valido=False,valor=5200000)
            # sql = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo, nu_factura, nm_contribuinte_anexo,dt_factura,vl_factura from  {table} where {where} = '{condicao}' and vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor,table='anexo_cli_out_13')
                sql = """select cli.nu_nif, cli.nm_contribuinte, cli.dt_periodo,cli.nu_nif_anexo, cli.nm_contribuinte_anexo,cli.nu_factura,cli.dt_factura, cli.vl_factura as cli_vl_factura, f.vl_factura as f_vl_factura from anexo_cli_out_13 AS cli INNER JOIN anexo_for_out_13 AS f ON f.nu_factura=cli.nu_factura  and f.dt_factura= cli.dt_factura WHERE cli.{where} ='{condicao}' and cli.vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor)
                #print(sql)
                data = run_sql(sql)
                #print(data[0])
                record['sql2']=sql
                record['lines'] = data
                record['nome'] = nome
                record['table'] ='Cliente'
                record['descricao'] = descricao
                record['data_inicial'] = data_inicial
                record['data_final'] = data_final
                return record

            else:
            # print(data_inicial)
            #data_where = """and dt_factura <= '{data_final}'""".format(data_final=data_final)
            #print(data_where)
            #if data_inicial:
            #data_where += """and dt_factura >= '{data_inicial}'""".format(data_inicial=data_inicial)
            #print(data_where)
            # sql2 = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo,  nm_contribuinte_anexo,nu_factura,dt_factura,vl_factura from anexo_cli_out_13 where info_valido =  '{info_valido}' and vl_factura >= '{valor}' """.format(info_valido=False,valor=5200000)
                sql = """select cli.nu_nif, cli.nm_contribuinte, cli.dt_periodo,cli.nu_nif_anexo, cli.nm_contribuinte_anexo,cli.nu_factura,cli.dt_factura, cli.vl_factura as cli_vl_factura, f.vl_factura as f_vl_factura from anexo_for_out_13 AS cli INNER JOIN anexo_cli_out_13 AS f ON f.nu_factura=cli.nu_factura  and f.dt_factura= cli.dt_factura WHERE cli.{where} ='{condicao}' and cli.vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor)
                data = run_sql(sql)
                #print(data)
                record['sql2']=sql
                record['lines'] = data
                record['nome'] = nome
                record['table'] ='Fornecedor'
                record['descricao'] = descricao
                record['data_inicial'] = data_inicial
                record['data_final'] = data_final
                return record
        else:
            if cliente == 'False' :
            # print(data_inicial)
            #data_where = """and dt_factura <= '{data_final}'""".format(data_final=data_final)
            #print(data_where)
            #if data_inicial:
            #data_where += """and dt_factura >= '{data_inicial}'""".format(data_inicial=data_inicial)
            #print(data_where)
            # sql2 = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo, nu_factura, nm_contribuinte_anexo,dt_factura,vl_factura from anexo_cli_out_13 where nif_valido =  '{nif_valido}' and vl_factura >= '{valor}' """.format(nif_valido=False,valor=5200000)
            # sql = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo, nu_factura, nm_contribuinte_anexo,dt_factura,vl_factura from  {table} where {where} = '{condicao}' and vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor,table='anexo_cli_out_13')
                sql =  """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo, nu_factura, nm_contribuinte_anexo,dt_factura,vl_factura from {table} where {where} = '{condicao}' and vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor,table='anexo_for_out_13')
                #print(sql)
                data = run_sql(sql)
                #print(data[0])
                record['sql2']=sql
                record['lines'] = data
                record['nome'] = nome
                record['table'] ='Cliente'
                record['descricao'] = descricao
                record['data_inicial'] = data_inicial
                record['data_final'] = data_final
                return record

            else:
            # print(data_inicial)
            #data_where = """and dt_factura <= '{data_final}'""".format(data_final=data_final)
            #print(data_where)
            #if data_inicial:
            #data_where += """and dt_factura >= '{data_inicial}'""".format(data_inicial=data_inicial)
            #print(data_where)
            # sql2 = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo,  nm_contribuinte_anexo,nu_factura,dt_factura,vl_factura from anexo_cli_out_13 where info_valido =  '{info_valido}' and vl_factura >= '{valor}' """.format(info_valido=False,valor=5200000)
                sql = """select  nu_nif,  nm_contribuinte, dt_periodo, nu_nif_anexo, nu_factura, nm_contribuinte_anexo,dt_factura,vl_factura from {table} where {where} = '{condicao}' and vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor,table='anexo_for_out_13')
                data = run_sql(sql)
                #print(data)
                record['sql2']=sql
                record['lines'] = data
                record['nome'] = nome
                record['table'] ='Fornecedor'
                record['descricao'] = descricao
                record['data_inicial'] = data_inicial
                record['data_final'] = data_final
                return record
























    def Imprimir(self, key, window_id):

        #template =  nomeInfra(nome)

        record =self.prepare_data()
        #get_records_to_print(key=key, model=self)
        print(record['nome'],'record')
        print('1')
        template = self.nomeInfra(record['nome'])

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

        #5200000


    def nomeInfra(self,nome):
        print('entrou')
        x=nome
        print(nome,'nomeee')
        if  x == 'InformaÃ§Ã£o InvÃ¡lida':
            tamplate='infracao_invalida'
            return tamplate
        else:
            tamplate='infracao'
            return tamplate

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
