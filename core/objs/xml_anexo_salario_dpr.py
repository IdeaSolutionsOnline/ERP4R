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
__model_name__ = 'xml_anexo_salario_dpr.XMLAnexoSalarioDPR'
import auth, base_models
from orm import *
from form import *
import erp_config


class XMLAnexoSalarioDPR(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'xml_anexo_salario_dpr'
        self.__title__ = 'DPR - Anexo Salário'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['periodo']

        self.__workflow_auth__ = {                      
            'Rascunho':['All'],            
            'full_access':['All']
            }        

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }

            
        self.nome = string_field(view_order = 1, name = 'Nome', size = 70,args = 'required')

        self.nif = string_field(view_order=2, name='Nif', size=50,args = 'required')

        self.ano = string_field(view_order = 3, size=40, name ='Ano',args = 'required')

        self.periodo = string_field(view_order = 4, name ='Periodo',size =40,args = 'required')

        self.cd_af = string_field(view_order = 5, name = 'Área Fiscal', size = 50, args = 'required', onlist = False)

        self.dec = string_field(view_order = 6, name = 'Tipo Declaração', size = 45,args = 'required')
        
        self.dt_emissao = string_field(view_order = 7, name = 'Data Emissão', size = 45,args = 'required')
        ########
        self.xml_linha_anexo_salario_dpr = list_field(view_order =8, name = 'Linhas de Anexo', condition = "xml_anexo_salario_dpr='{id}'", column='designacao', model_name = 'xml_linha_anexo_salario_dpr.XMLLinhaAnexoSalarioDPR', list_edit_mode = 'inline', onlist = False)
        ########
        self.base = function_field(view_order = 9, name = 'Tot. Base Declarado', size = 45,args = 'required, readonly')

        self.aces = function_field(view_order = 10, name = 'Tot. Rend. Acessórios', sum = True, size = 45,args = 'required, readonly')

        self.isento = function_field(view_order = 11, name = 'Tot. Rend. Isentos', sum = True, size = 45,args = 'required, readonly')

        self.trib = function_field(view_order = 12, name = 'Tot. Rend. Tributaveis', sum = True, size = 45,args = 'required, readonly')        
        
        self.ir_teu = function_field(view_order = 13,name = 'Tot. Retenções', sum = True, size = 45,args = 'required, readonly')    

        self.inps = function_field(view_order = 14,name = 'Tot. INPS', sum = True, size = 45,args = 'required, readonly') 

        self.outros = function_field(view_order = 15,name = 'Tot. Outros Rend.', sum = True, size = 45,args = 'required, readonly')     

        self.estado = info_field(view_order = 16, name ='Estado', hidden = True, default='Rascunho',args = 'required, readonly')

        self.xml_modelo_dpr = parent_field(view_order = 17, name = 'Modelo DPR', hidden=True, model_name = 'xml_modelo_dpr.XMLModeloDPR',nolabel=True, onlist = False, column = 'id')
    

    def get_opts(self, get_str):     
        return eval(get_str)
        

    def record_lines(self, key):
        def get_results():
            try:
                from my_linha_anexo_salario_dpr import XMLLinhaAnexoSalarioDPR
            except:
                from xml_linha_anexo_salario_dpr import XMLLinhaAnexoSalarioDPR
            record_lines = XMLLinhaAnexoSalarioDPR(where="xml_anexo_salario_dpr = '{id}'".format(id=key)).get()
            return record_lines
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)


    def get_base(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['base'])
        return int(to_decimal(soma))


    def get_aces(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['aces'])
        return int(to_decimal(soma))


    def get_isento(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['isento'])
        return int(to_decimal(soma))


    def get_trib(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['trib'])
        return int(to_decimal(soma))


    def get_ir_teu(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['ir_teu'])
        return int(to_decimal(soma))


    def get_inps(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['inps'])
        return int(to_decimal(soma))


    def get_outros(self, key):
        soma = to_decimal(0)
        record_lines= self.record_lines(key=key)                   
        for line in record_lines:
            soma+=to_decimal(line['outros'])
        return int(to_decimal(soma))  


    def Visualizar(self, key, window_id):
        template = 'previsualizar'
        record = get_model_record(model=self, key=key)
        return Report(record=record, report_template=template).show()