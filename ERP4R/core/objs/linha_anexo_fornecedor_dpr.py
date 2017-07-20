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
__model_name__ = 'linha_anexo_fornecedor_dpr.LinhaAnexoFornecedorDPR'
import auth, base_models
from orm import *
from form import *

class LinhaAnexoFornecedorDPR(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_anexo_fornecedor_dpr'
        self.__title__ = 'Linhas Anexo Fornecedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['designacao']

        self.origem = string_field(view_order = 1, name = 'Origem',args = 'required, readonly', onlist=True)

        self.nif = string_field(view_order=2, name ='Nif Cliente', args = 'required, readonly', onlist=True)
        
        self.designacao = string_field(view_order=3, name ='Nome', size=45, args = 'required, readonly', onlist=True)        

        self.tp_doc = string_field(view_order = 4, name = 'Tipo Doc',args = 'required, readonly', onlist=True)      
        
        self.serie = string_field(view_order=5, name ='Serie.', args = 'required, readonly',size=20, onlist=True)        
       
        self.num_doc = string_field(view_order=6, name ='Nº Doc.', onlist=True,args = 'required, readonly')

        self.dt_recibo = string_field(view_order=7, name ='Data Doc.', size=30, onlist=True,args = 'required, readonly')

        self.vl_recibo = string_field(view_order=8, name ='Valor', args = 'required, readonly', sum=True)
        
        self.tipologia = string_field(view_order=9, name ='Tipologia', args = 'required, readonly')
        
        self.tx_ret = string_field(view_order=10, name ='Taxa Retenção', args = 'required, readonly', size=20)        

        self.ir_teu = string_field(view_order=11, name ='Valor Retido', args = 'required, readonly', size=20, sum=True)

        self.tp_oper = string_field(view_order=12, name ='Tipo Operação',args = 'required, readonly')

        self.anexo_fornecedor_dpr = parent_field(view_order = 13, name = 'Anexo Fornecedor DPR', hidden=True, model_name = 'anexo_fornecedor_dpr.AnexoFornecedorDPR',nolabel=True, onlist = False, column = 'id')

        