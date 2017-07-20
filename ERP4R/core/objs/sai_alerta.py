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
__model_name__= 'sai_alerta.Sai_Alerta'
#import base_models#auth,
from orm import *
from form import *


class Sai_Alerta (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_alerta'
        self.__title__= 'Alerta'
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
        self.descricao = text_field(view_order=4, name='Descrição', size=250)
        self.data_inicial = date_field(view_order=2, name ='Data Inicial', onlist=False)
        self.data_final = date_field(view_order=3, name ='Data Final', default=datetime.date.today(), onlist=False)
        self.sql = text_field(view_order=5, name ='SQL', onlist=False, size=170 )
        self.valor = integer_field(view_order=6, name ='A partir do valor de:', onlist=False, size=100 )
        self.cliente = boolean_field(view_order = 7, name = 'Cliente?', default = False, onlist=False)
        self.fornecedor = boolean_field(view_order = 8, name = 'Fornecedor?', default = True, onlist=False)
        self.estado = info_field(view_order=9, name ='Estado', default='Rascunho', onlist=True, hidden=True, dynamic_atrs = 'estado_dynamic_atrs',nolabel=True,)
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
        sql = eval(bottle.request.forms.get('sql'))
        x=sql.split("//")
        #print(x)
        where=x[0]
        condicao=x[1]
        #print(where, condicao)
        nome= bottle.request.forms.get('nome')
        descricao= bottle.request.forms.get('descricao')
        data_final = bottle.request.forms.get('data_final')
        data_inicial = bottle.request.forms.get('data_inicial')
        valor= bottle.request.forms.get('valor')
        #data_where = """and dt_factura <= '{data_final}'""".format(data_final=data_final)
        #print(data_where)
        #if data_inicial:
            #data_where += """and dt_factura >= '{data_inicial}'""".format(data_inicial=data_inicial)
        #print(data_where)



        cliente = bottle.request.forms.get('cliente')
        record = {}

        if cliente == 'False' :
            sql = """select cli.nu_nif, cli.nm_contribuinte, cli.dt_periodo,cli.nu_nif_anexo, cli.nm_contribuinte_anexo,cli.nu_factura,cli.dt_factura,cli.vl_factura,f.vl_dedutivel,cli.vl_liquidado from anexo_cli_out_13 AS cli INNER JOIN anexo_for_out_13 AS f ON f.nu_factura=cli.nu_factura  and f.vl_factura = cli.vl_factura and f.dt_factura= cli.dt_factura WHERE cli.{where} ='{condicao}' and cli.vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor)

            data = run_sql(sql)
            #print(data)
            record['sql2']=sql
            record['lines'] = data
            record['nome'] = nome
            record['table'] ='Cliente'
            record['descricao'] = descricao
            record['data_inicial'] = data_inicial
            record['data_final'] = data_final
            return record

        else:

            sql = """select f.nu_nif, f.nm_contribuinte, f.dt_periodo, f.nu_nif_anexo,  f.nm_contribuinte_anexo,f.nu_factura, f.dt_factura,f.vl_factura,f.vl_dedutivel,cli.vl_liquidado from anexo_for_out_13 AS f INNER JOIN anexo_cli_out_13 AS cli ON cli.nu_factura=f.nu_factura  and f.vl_factura = cli.vl_factura and f.dt_factura= cli.dt_factura WHERE f.{where}='{condicao}' and f.vl_factura >= '{valor}'  ORDER BY dt_periodo DESC """.format(where=where,condicao=condicao,valor=valor)

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
        #print('4')
        template = 'alerta_for'
        #print('3')
        record =self.prepare_data()#get_records_to_print(key=key, model=self)
        #print('1')
        #print (template)
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




#         $sql = "SELECT tipo FROM atrativos AS a JOIN lista_atrativos AS l  ON a.cod_atrativo = l.cod_atrativo WHERE
# l. cod_hotel='$cod_hotel'";



# def prepare_data(self):
#         sql = eval(bottle.request.forms.get('sql'))
#         print(sql)
#         #depois implementar os restantes filtros
#         #ano_fiscal =
#         #periodo =
#         #saldos_do_periodo =
#         nome= bottle.request.forms.get('nome')
#         descricao= bottle.request.forms.get('descricao')
#         data_final = bottle.request.forms.get('data_final')
#         #print(data_final)
#         data_inicial = bottle.request.forms.get('data_inicial')
#        # print(data_inicial)
#         #data_where = """and dt_factura <= '{data_final}'""".format(data_final=data_final)
#         #print(data_where)
#         #if data_inicial:
#             #data_where += """and dt_factura >= '{data_inicial}'""".format(data_inicial=data_inicial)
#         #print(data_where)

#         # sql2 = """select f.nu_nif, f.nm_contribuinte, f.dt_periodo, f.nu_nif_anexo,  f.nm_contribuinte_anexo,f.nu_factura,f.dt_factura,f.vl_factura,f.vl_dedutivel,cli.vl_liquidado from anexo_for_out_13 AS f INNER JOIN anexo_cli_out_13 AS cli ON cli.nu_factura=f.nu_factura  and f.vl_factura = cli.vl_factura and f.related= cli.id WHERE f.validar_iva='{iva}' and f.vl_factura >= '{valor}' """.format(iva=1,valor=200000)





#         #print('2')
#         data = run_sql(sql)
#         #print(data)

#         record = {}
#         record['lines'] = data
#         record['nome'] = nome
#         record['descricao'] = descricao
#         record['data_inicial'] = data_inicial
#         record['data_final'] = data_final
#         return record




# """select f.nu_nif, f.nm_contribuinte, f.dt_periodo, f.nu_nif_anexo,  f.nm_contribuinte_anexo,f.nu_factura, f.dt_factura,f.vl_factura,f.vl_dedutivel,cli.vl_liquidado from anexo_for_out_13 AS f INNER JOIN anexo_cli_out_13 AS cli
# ON cli.nu_factura=f.nu_factura  and f.vl_factura = cli.vl_factura and f.dt_factura= cli.dt_factura WHERE f.declarado='{declarado}' and f.vl_factura >= '{valor}' """.format(declarado=True,valor=200000)


# """select f.nu_nif, f.nm_contribuinte, f.dt_periodo, f.nu_nif_anexo,  f.nm_contribuinte_anexo,f.nu_factura,
# f.dt_factura,f.vl_factura,f.vl_dedutivel,cli.vl_liquidado from anexo_for_out_13 AS f INNER JOIN anexo_cli_out_13 AS cli
# ON cli.nu_factura=f.nu_factura  and f.vl_factura = cli.vl_factura and f.related= cli.id WHERE f.validar_iva='{iva}' and f.vl_factura >= '{valor}' """.format(iva=1,valor=200000)
