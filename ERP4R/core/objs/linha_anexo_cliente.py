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
__model_name__ = 'linha_anexo_cliente.LinhaAnexoCliente'
import auth, base_models
from orm import *
from form import *

class LinhaAnexoCliente(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_anexo_cliente'
        self.__title__ = 'Linhas Anexo Cliente'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['numero_doc']


        self.factura_cliente = string_field(view_order = 1, args = 'required, readonly',name = 'Factura',onlist=False)
        
        self.designacao = string_field(view_order=2, name ='Nome', size=45, args = 'required, readonly', onlist=True)

        self.nif_cliente = string_field(view_order=3, name ='Nif', args = 'required, readonly', onlist=True)

        self.origem = string_field(view_order = 4, name = 'Origem',args = 'required, readonly', onlist=True)      
        
        self.serie = string_field(view_order=5, name ='Serie.', args = 'required, readonly',size=20, onlist=True)

        self.tipo_doc = string_field(view_order=6, name ='Tipo Doc', args = 'required, readonly')
       
        self.numero_doc = string_field(view_order=7, name ='Nº Doc.', onlist=True,args = 'required, readonly')

        self.data = string_field(view_order=8, name ='Data Doc.', size=30, onlist=True,args = 'required, readonly')

        self.valor_factura = string_field(view_order=9, name ='Total', args = 'required, readonly', sum=True)
        
        self.valor_base_incidencia = string_field(view_order=10, name ='Incidência', args = 'required, readonly', sum=True)
        
        self.taxa_iva = string_field(view_order=11, name ='Taxa IVA', args = 'required, readonly', size=20)        

        self.iva_liquidado = string_field(view_order=12, name ='IVA Liquidado', args = 'required, readonly', size=20, sum=True)

        self.nao_liq_imposto = string_field(view_order=13, name ='Não Liq.Imp',args = 'required, readonly')

        self.linha_mod106 = string_field(view_order=14, name ='Nº Linha MOD106', args = 'required, readonly', size=20)
    
        self.anexo_clientes = parent_field(view_order = 15, name = 'Anexo Cliente', hidden=True, model_name = 'anexo_clientes.AnexoClientes',nolabel=True, onlist = False, column = 'id')