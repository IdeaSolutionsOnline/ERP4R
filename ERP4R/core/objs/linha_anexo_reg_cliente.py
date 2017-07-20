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
__model_name__ = 'linha_anexo_reg_cliente.LinhaAnexoRegCliente'
import auth, base_models
from orm import *
from form import *


class LinhaAnexoRegCliente(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'linha_anexo_reg_cliente'
        self.__title__ = 'Linha Anexo Reg. Cliente'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ ='posicao'
        


        self.tipo = string_field(view_order =1, nolabel = True, size=30, args='required, readonly')

        self.accao = string_field(view_order =2, name='Acção', size=30, args='required, readonly')

        self.posicao = string_field(view_order=3, default='Posição', nolabel=True, hidden=True, args='required, readonly', onlist=False)

        self.anexo_reg_cliente = parent_field(view_order = 4, name = 'Anexo Reg Cliente', hidden=True, model_name = 'anexo_reg_cliente.AnexoRegCliente',nolabel=True, onlist = False)

        self.factura = string_field(view_order = 5, name = 'Factura', size = 20 , args='required, readonly',onlist=False)
        
        self.origem = string_field(view_order = 6, name = 'Origem', size = 20, args='required, readonly')
        
        self.nif_cliente = string_field(view_order=7, name ='Nif', size=40, args='required, readonly')      

        self.tipo_doc = string_field(view_order=8, name ='Tipo Doc', size=20, args='required, readonly')
       
        self.numero_doc = string_field(view_order=9, name='Nº Doc', args='required, readonly=True')

        self.data = string_field(view_order=10, name ='Data Doc', args='required, readonly')

        self.valor_factura = string_field(view_order=11, name ='Val. Factura', args='required, readonly', size=40,sum=True)
        
        self.valor_base_incid = string_field(view_order=12, name ='Incidência', args='required, readonly', size=40,sum=True)

        self.taxa_iva = string_field(view_order=13, name ='IVA', args='required, readonly')

        self.iva_liquidado = string_field(view_order=14, name ='IVA Liq.', args='required, readonly', size=45,sum=True)

        self.linha_mod106 = string_field(view_order=15, name ='Linha M106', args='required, readonly', size=20)

        self.periodo_referencia = string_field(view_order=16, name ='P. Refer.', args='required, readonly')

        self.iniciativa = string_field(view_order=17, name ='Iniciativa', args='required, readonly', size=20)