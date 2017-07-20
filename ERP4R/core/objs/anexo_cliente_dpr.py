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
__model_name__ = 'anexo_cliente_dpr.AnexoClienteDPR'
import auth, base_models
from orm import *
from form import *
from linha_anexo_cliente_dpr import LinhaAnexoClienteDPR



class AnexoClienteDPR(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'anexo_cliente_dpr'
        self.__title__ = 'DPR - Anexo Cliente'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']

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


        self.nome = string_field(view_order = 1, name = 'Nome', size = 70,args = 'required, readonly')

        self.nif = string_field(view_order=2, name='Nif', size=50,args = 'required, readonly')

        self.ano = string_field(view_order = 3, size=40, name ='Ano',args = 'required, readonly')

        self.periodo = string_field(view_order = 4, name ='Periodo',size =40,args = 'required, readonly')

        self.cd_af = string_field(view_order = 5, name = 'Área Fiscal', size = 45,args = 'required, readonly')

        self.dec = string_field(view_order = 6, name = 'Tipo Declaração', size = 45,args = 'required, readonly')

        self.dt_emissao = string_field(view_order = 7, name = 'Data Emissão', size = 45,args = 'required, readonly')

        self.linha_anexo_cliente_dpr = list_field(view_order =8, name = 'Linhas de Anexo', condition = "anexo_cliente_dpr='{id}'", column='designacao', model_name = 'linha_anexo_cliente_dpr.LinhaAnexoClienteDPR', list_edit_mode = 'inline', onlist = False)

        self.vl_recibo = string_field(view_order = 9, name = 'Total Recibos', sum = True, size = 45,args = 'required, readonly')

        self.ir_teu = string_field(view_order = 10,name = 'Total Retenção', sum = True, size = 45,args = 'required, readonly')

        self.estado = info_field(view_order = 11, name ='Estado', hidden = True, default='Rascunho',args = 'required, readonly')

        self.modelo_dpr = parent_field(view_order = 12, name = 'Modelo DPR', hidden=True, model_name = 'modelo_dpr.ModeloDPR',nolabel=True, onlist = False, column = 'id')


    def Visualizar(self, key, window_id):
        template = 'previsualizar'
        record = get_model_record(model=self, key=key)
        return Report(record=record, report_template=template).show()