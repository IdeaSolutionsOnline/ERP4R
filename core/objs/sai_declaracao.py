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
__model_name__= 'sai_declaracao.Sai_declaracao'
#import base_models#auth,
from orm import *
from form import *


class Sai_declaracao (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_declaracao'
        self.__title__= 'Periodos declarados'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__db_mode__ = 'None'
        self.__workflow__ = (
            'estado', {'Confirmado':['Imprimir','Exportar']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Rascunho':['Gestor'],
            'Exportar':['All'],
            'Imprimir':['All'],
           }

        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso'])
            ]

        self.__auth__ = {
            'read':['All'],
            'write':['Técnico DNRE','Gestor DNRE' ],
            'create':['Administrador'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }



        self.ano = string_field(view_order=1, name='Ano', size=50)
        self.estado = info_field(view_order=2, name ='Estado', default='Confirmado', hidden=True, nolabel=True,onlist=False)

    def prepare_data(self):
        ano = bottle.request.forms.get('ano')

        descricao = 'Declações  feitas por periodo dos contribuintes'
        #cliente = bottle.request.forms.get('cliente')
        record = {}
        #print(nu_nif, cliente)
        #if cliente == 'False' :
        sql ="""select cli.nu_nif, cli.nm_contribuinte, cli.jan ,cli.fev, cli.mar, cli.abr, cli.mai, cli.jun, cli.jul, cli.ago, cli.setb, cli.otu, cli.nov, cli.dez, f.ds_area_fiscal from contribuinte_decalaracao_periodo AS cli INNER JOIN gre_v_cadastro_3 AS f ON f.nm_contribuinte=cli.nm_contribuinte and ano='{ano}' """.format(ano=ano)
        data = run_sql(sql)

            #record['nu_nif'] =  nu_nif
        record['sql2']=sql
        record['lines'] = data
        record['ano'] = ano
        record['descricao'] = descricao
        return record





    def Imprimir(self, key, window_id):

        record = self.prepare_data()
        template='contribuinte_periodo'
        return Report(record=record, report_template=template).show()

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
