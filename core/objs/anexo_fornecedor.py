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
__model_name__ = 'anexo_fornecedor.AnexoFornecedor'
import auth, base_models
from orm import *
from form import *


class AnexoFornecedor(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'anexo_fornecedor'
        self.__title__ = 'MOD 106 - Anexos Fornecedores'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']

        self.__workflow_auth__ = {            
            'Rascunho':['All'],
            'Visualizar':['All'],
            'full_access':['All']
            }        

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }
            
        self.__workflow__ = ('estado', {'Gerado':['Visualizar']})
        

        self.nome = string_field(view_order = 1, name = 'Nome do documento', size=70, args = 'required, readonly')

        self.nif_entidade = string_field(view_order=2, name='Nif', size=45, args = 'required, readonly')

        self.ano = string_field(view_order = 3, size=40, name ='Ano', args = 'required, readonly')

        self.mes = string_field(view_order = 4, name ='Mês',size =40, args = 'required, readonly')

        self.area_fiscal = string_field(view_order = 5, name = 'Área Fiscal', args = 'required, readonly')

        ### linhas do anexo de forn aqui
        self.linha_anexo_fornecedor = list_field(view_order = 6, name = 'Linhas de Anexo Fornecedor', condition = "anexo_fornecedor='{id}'", model_name = 'linha_anexo_fornecedor.LinhaAnexoFornecedor', list_edit_mode = 'inline', onlist = False)

        self.data_entrega = string_field(view_order=7, size=60, name ='Data Entrega', args = 'required, readonly')
        
        self.total_factura = string_field(view_order = 8, name = 'Total Facturas', size = 45, args = 'required, readonly')
        
        self.total_base_incidencia = string_field(view_order = 9, name = 'Total Incidência', size = 45, args = 'required, readonly')

        self.total_suportado = string_field(view_order = 10, name = 'Total Suportado', size = 45, args = 'required, readonly')

        self.total_dedutivel = string_field(view_order = 11, name = 'Total Dedutivel', size = 45, args = 'required, readonly')

        self.estado = info_field(view_order = 12, name ='Estado', default='Rascunho', args = 'required, readonly')

        self.xml_gerado = text_field(view_order=13,name='Conteudo XML Gerado', size=100, args = 'required, readonly',onlist=False)

        self.modelo106 = string_field(view_order = 14, name = 'Modelo106', hidden=True, model_name = 'modelo106.Modelo106',nolabel=True, onlist = False)

   

    


    

