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
__model_name__ = 'xml_linha_anexo_reg_fornecedor_m106.LinhaAnexoRegFornecedor'
import auth, base_models
from orm import *
from form import *


class LinhaAnexoRegFornecedor(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'xml_linha_anexo_reg_fornecedor_m106'
        self.__title__ = 'Linha Anexo Reg. Fornecedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['numero_doc']
        


        self.tipo = string_field(view_order =0, nolabel = True, size=30, args='required, readonly')

        self.accao = string_field(view_order =1, name='Acção', size=30, args='required, readonly')

        self.factura = string_field(view_order = 2, name = 'Factura', size = 20 , args='required, readonly',onlist=False)
        
        self.origem = string_field(view_order = 3, name = 'Origem', size = 20, args='required, readonly')
        
        self.nif_fornecedor = string_field(view_order=4, name ='Nif', size=40, args='required, readonly')      

        self.tipo_doc = string_field(view_order=5, name ='Tipo Doc', size=20, args='required, readonly')
       
        self.numero_doc = string_field(view_order=6, name='Nº Doc', args='required, readonly=True')

        self.data = string_field(view_order=7, name ='Data Doc', args='required, readonly')

        self.valor_factura = string_field(view_order=8, name ='Val. Factura', args='required, readonly', size=40,sum=True)
        
        self.valor_base_incid = string_field(view_order=9, name ='Incidência', args='required, readonly', size=40,sum=True)

        self.taxa_iva = string_field(view_order=10, name ='IVA', args='required, readonly')

        self.iva_suportado = string_field(view_order=11, name ='IVA Sup', args='required, readonly', size=45,sum=True)

        self.direito_ded = string_field(view_order=12, name ='D. Dedução', args='required, readonly')

        self.iva_dedutivel = string_field(view_order=13, name ='IVA Ded', args='required, readonly', size=45,sum=True)

        self.tipologia = string_field(view_order=114, name ='Tipologia', args='required, readonly', size=20)

        self.linha_mod106 = string_field(view_order=15, name ='Linha M106', args='required, readonly', size=20)

        self.periodo_referencia = string_field(view_order=16, name ='P. Refer.', args='required, readonly')

        self.iniciativa = string_field(view_order=17, name ='Iniciativa', args='required, readonly', size=20)

        self.posicao = string_field(view_order=18, default='Posição', nolabel=True, hidden=True, args='required, readonly', onlist=False)
     
        self.xml_anexo_reg_fornecedor_m106 = parent_field(view_order = 19, name = 'Anexo Reg Fornecedor', hidden=True, model_name = 'xml_anexo_reg_fornecedor_m106.XMLAnexoRegFornecedorM106',nolabel=True, onlist = False)
    
        