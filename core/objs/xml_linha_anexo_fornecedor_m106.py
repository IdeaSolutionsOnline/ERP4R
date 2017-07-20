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
__model_name__ = 'xml_linha_anexo_fornecedor_m106.XMLLinhaAnexoFornecedorM106'
import auth, base_models
from orm import *
from form import *


class XMLLinhaAnexoFornecedorM106(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'xml_linha_anexo_fornecedor_m106'
        self.__title__ = 'Linhas Anexo Fornecedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['numero_doc']


        self.numero_doc = string_field(view_order = 1, args='readonly, required', name = 'Nº Doc',size = 20)
        
        self.origem = string_field(view_order = 2, name = 'Origem', size = 20, args='readonly, required')
        
        self.nif_fornecedor = string_field(view_order=3, name ='Nif Fornecedor', args='readonly, required', size=40)

        self.designacao = string_field(view_order=4, name ='Designação Entidade', args='readonly, required', size=80)        

        self.tipo_doc = string_field(view_order=5, name ='Tipo Documento', size=45, args='readonly, required')
       
        self.data = string_field(view_order=6, name ='Data Doc.', args='readonly, required', size=40)

        self.valor_factura = string_field(view_order=7, name ='Val. Factura', args='readonly, required', size=40,sum=True)
        
        self.valor_base_incid = string_field(view_order=8, name ='Val.Base Incidência', args='readonly, required', size=40,sum=True)

        self.taxa_iva = string_field(view_order=9, name ='Taxa IVA', args='readonly, required')

        self.iva_suportado = string_field(view_order=10, name ='IVA Suportado', args='readonly, required', size=45,default='0',sum=True)

        self.direito_ded = string_field(view_order=11, name ='Dir. Dedução', args='readonly, required')

        self.iva_dedutivel = string_field(view_order=12, name ='IVA Dedutivel', args='readonly, required', size=45, default='0',sum=True)

        self.tipologia = string_field(view_order=13, name ='Tipologia', args='readonly, required', size=45)

        self.linha_mod106 = string_field(view_order=14, name ='Nº Linha MOD106', args='readonly, required', size=20)
     
        self.xml_anexo_fornecedor_m106 = parent_field(view_order = 15, name = 'Anexo Fornecedor', hidden=True, model_name = 'xml_anexo_fornecedor_m106.XMLAnexoFornecedorM106',nolabel=True, onlist = False)

        self.factura_fornecedor = parent_field(view_order = 16, name = 'Factura', hidden=True, model_name = 'factura_forn.FacturaFornecedor',nolabel=True, onlist = False)