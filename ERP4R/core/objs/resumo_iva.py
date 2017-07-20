# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'resumo_iva.ResumoIva'
import auth, base_models
from orm import *
from form import *
'''
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas
'''
try:
    from my_factura_cli import FacturaCliente
except:
    from factura_cli import FacturaCliente

try:
    from my_factura_forn import FacturaFornecedor
except:
    from factura_forn import FacturaFornecedor

class ResumoIva(Model, View):
    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'resumo_iva'
        self.__title__ = 'Resumo do IVA'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__db_mode__ = 'None'
        self.__workflow__ = (
            'estado', {'Rascunho':['Gerar'],'Gerado':['Imprimir', 'Exportar']}
            )
        self.__workflow_auth__ = {
            'Gerar':['All'],
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

        self.data_inicial = date_field(view_order=1, name='Data Inicial', default=datetime.date(datetime.date.today().year,datetime.date.today().month,int(1)))
        self.data_final = date_field(view_order=2, name='Data Final', default=datetime.date.today())

        self.iva_pagar = string_field(view_order=3, name='IVA a Pagar')
        self.iva_receber = string_field(view_order=4, name='IVA a Receber')

        self.estado = info_field(view_order=5, name='Estado', hidden=True, default='Rascunho')


    def get_total_a_pagar(self, data_inicial, data_final):
        total_iva=0
        facturas = FacturaCliente(where="data>='{inicio}' AND data <='{fim}' AND estado ='Confirmado'".format(inicio=data_inicial,fim=data_final)).get()
        if len(facturas)!= 0:
            for line in facturas:
                total_iva+=int(line['total_iva'])
        return total_iva

    def get_total_a_receber(self, data_inicial, data_final):
        total_iva=0
        facturas = FacturaFornecedor(where="data>='{inicio}' AND data <='{fim}' AND estado ='Confirmado'".format(inicio=data_inicial,fim=data_final)).get()
        if len(facturas)!= 0:
            for line in facturas:
                total_iva += int(FacturaFornecedor().get_total_iva(key=line['id']))
        return total_iva

    def Gerar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['iva_pagar']=str(self.get_total_a_pagar(data_inicial=self.kargs['data_inicial'], data_final=self.kargs['data_final']))
        self.kargs['iva_receber']=str(self.get_total_a_receber(data_inicial=self.kargs['data_inicial'], data_final=self.kargs['data_final']))
        self.kargs['estado']='Gerado'
        self.put()
        return form_edit(window_id = window_id).show()

                                                                                                        
    def Imprimir(self, key, window_id):
        print('estou no imprimir do resumo iva')
        template = 'resumo_iva'
        #record = self.prepare_data()
        return Report(record=record, report_template=template).show()

    def Exportar(self, key, window_id):
        print('estou na função de Exportar no balancete')
        result = self.prepare_data()['lines']
        #print('result: ', result)
        return data_to_csv(data=result, model=self, text='Gravar', cols=['codigo', 'conta', 'debito', 'credito', 'saldo'])

    
