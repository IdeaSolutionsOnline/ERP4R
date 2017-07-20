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
__model_name__ = 'modelo_1b.Modelo_1B'

import auth, base_models
from orm import *
from form import *
from area_fiscal import AreaFiscal
import erp_config
from anexo_clientes import AnexoClientes
from linha_anexo_cliente import LinhaAnexoCliente
from anexo_fornecedor import AnexoFornecedor
from linha_anexo_fornecedor import LinhaAnexoFornecedor
from factura_cli import FacturaCliente
from factura_forn import FacturaFornecedor
from terceiro import Terceiro
from codigo_pais import CodigoPais
from linha_factura_cli import LinhaFacturaCliente
from linha_factura_forn import LinhaFacturaFornecedor
from anexo_reg_fornecedor import AnexoRegFornecedor
from linha_anexo_reg_fornecedor import LinhaAnexoRegFornecedor

from anexo_reg_cliente import AnexoRegCliente
from linha_anexo_reg_cliente import LinhaAnexoRegCliente

class Modelo_1B(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'modelo_1b'
        self.__title__ = 'Modelo 1B'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        #self.__get_options__ = ['nome']

               

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }


        self.ano = combo_field(view_order = 1, name ='Ano', args = 'required', default = datetime.date.today().year, options='model.getAno()')

        self.tipo_declaracao = combo_field(view_order = 2, name = 'Tipo Declaração', size = 65, default = 'primeira', options = [('primeira','Primeira'), ('alteracoes','Alterações'),('outra', 'Outra')], onlist = False)

        self.data_entrega = date_field(view_order=3, size=40, name ='Data de Entrega', args='required ', default=datetime.date.today())

        self.reparticao_fin = combo_field(view_order = 4, name = 'Repartição Finanças', size = 70, model = 'area_fiscal', args = 'required', onlist = False, search = False, column = 'local', options = "model.get_opts('AreaFiscal().get_options_local()')")

        self.nome = string_field(view_order = 5, name = 'Nome', size = 120, default=erp_config.enterprise)

        self.nif = string_field(view_order = 6, name = 'Nif', size = 45, default=erp_config.nif)

        self.outras_info = string_field(view_order = 7, name = 'Rua/Avenida/Lugar/etc.', size = 120, default=erp_config.street)

        self.numero = string_field(view_order = 8, name = 'Nº', size = 45)

        self.andar = string_field(view_order = 9, name = 'Andar', size = 45)

        self.cp = string_field(view_order = 10, name = 'CP', size = 45)

        self.localidade = string_field(view_order = 11, name = 'Localidade', size = 45)

        self.activid_principal = string_field(view_order = 12, name = 'Actividade Principal', size = 120)

        self.outras_activid = string_field(view_order = 13, name = 'Outras Actividades', size = 120)

        self.importador = combo_field(view_order = 14, name = 'É importador', size = 45, default = '0', options = [('1','Sim'), ('0','Não')], onlist = False)

        self.estab_outra_af = combo_field(view_order = 15, name = 'Estab. em Outra Area Fiscal', size = 45, default = '0', options = [('1','Sim'), ('0','Não')], onlist = False)

        self.num_area_fiscal = combo_field(view_order = 16, name = 'Nº Area Fiscal', size = 70, model = 'area_fiscal', args = 'required', onlist = False, search = False, column = 'local', options = "model.get_opts('AreaFiscal().get_options_buyable()')")

        self.resultado_exerc = string_field(view_order = 17, name = '1- Resultado do exercvício (linha 34 do Quadro 5)', size = 120)

        self.resultado_exerc = string_field(view_order = 19, name = '2.1.- Utilizações e provisões para impostos s/ lucros exertcício anterior', size = 150)

        







    def get_opts(self, get_str):       
        return eval(get_str)


    def getAno(self):
        options = []
        opts = range(2000,2051)
        for option in opts:
            options.append((str(option), str(option)))
        return options