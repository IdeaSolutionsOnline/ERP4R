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
__model_name__= 'sai_pesquisacont.SaiPesquisacont'
#import base_models#auth,
from orm import *
from form import *


class SaiPesquisacont (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_pesquisacont'
        self.__title__= 'Por Contribuinte'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__db_mode__ = 'None'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir','Exportar']}
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


        self.nu_nif = integer_field(view_order=1, name='NIF', size=80)
        self.cliente = boolean_field(view_order = 2, name = 'Cliente?', default = False)
        self.fornecedor = boolean_field(view_order = 3, name = 'Fornecedor?', default = True)
        self.estado = info_field(view_order=4, name ='Estado', default='Confirmado', hidden=True, nolabel=True,)



    def prepare_data(self):
        nu_nif = bottle.request.forms.get('nu_nif')

        descricao = 'Aletras e Infrações de um Contribuinte'
        cliente = bottle.request.forms.get('cliente')
        record = {}
        #print(nu_nif, cliente)
        if cliente == 'False' :
            sql="""select nu_nif, nm_contribuinte, dt_periodo, nu_nif_anexo, nm_contribuinte_anexo,nu_factura,dt_factura,vl_factura,vl_liquidado,validar_iva, nif_valido,declarado,info_valido from anexo_cli_out_13 where nu_nif=  '{nif}'  and validar_iva =1 or nu_nif='{nif}'  and nif_valido = false or nu_nif='{nif}' and declarado = false or nu_nif='{nif}' and info_valido = false ORDER BY dt_periodo DESC""".format(nif=nu_nif)
            data = run_sql(sql)
            for i in data:
                record['contribuinte']= i['nm_contribuinte']
                break
            record['sql2']=sql
            record['nu_nif'] =  nu_nif
            record['lines'] = data
            record['nome'] ='Cliente'
            record['descricao'] = descricao
            return record
        else:
            sql="""select nu_nif, nm_contribuinte, dt_periodo, nu_nif_anexo, nm_contribuinte_anexo,nu_factura,dt_factura,vl_factura,vl_dedutivel,validar_iva, nif_valido,declarado,info_valido from anexo_for_out_13 where nu_nif=  '{nif}'  and validar_iva =1 or nu_nif='{nif}'  and nif_valido = false or nu_nif='{nif}' and declarado = false or nu_nif='{nif}' and info_valido = false ORDER BY dt_periodo DESC""".format(nif=nu_nif)
            data = run_sql(sql)

            for i in data:
                record['contribuinte']= i['nm_contribuinte']
                break


            record['sql2']=sql
            record['nu_nif'] =  nu_nif
            record['lines'] = data
            record['nome'] ='Fornecedor'
            record['descricao'] = descricao
            return record







    def Imprimir(self, key, window_id):

        record = self.prepare_data()

        if record['nome'] == 'Fornecedor':
            template = 'sai_contribuintefor'
            return Report(record=record, report_template=template).show()
        else:
            template = 'sai_contribuintecli'
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


#253298121
