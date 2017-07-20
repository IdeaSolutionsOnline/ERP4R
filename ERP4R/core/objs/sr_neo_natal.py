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
__model_name__ = 'sr_neo_natal.SRNeoNatal'
import auth, base_models
from orm import *
from form import *
try:
    from my_sr_crianca import SRCrianca
except:
    from sr_crianca import SRCrianca

class SRNeoNatal(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sr_neo_natal'
        self.__title__ ='Periodo Neo-Natal'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['local_parto'] # define tambem o campo a ser mostrado  no m2m, independentemente da descricao no field do m2m
        self.__order_by__ = 'sr_neo_natal.local_parto'
       

        #choice field com a estrutura de saude
        self.local_parto = combo_field(view_order = 1, name = 'Local Parto', size = 40, default = '', options = [('institucional','Institucional'), ('domiciliar','Domiciliar'), ('outros','Outros')], onlist = True) 
        self.tipo_parto = combo_field(view_order = 2, name = 'Tipo Parto', size = 40, default = '', options = [('eutocico','Eutócico'), ('distocico','Distócico'), ('cesariana','Cesariana'), ('forceps','Fórceps'), ('ventosa','Ventosa'), ('outro','Outro')], onlist = True) 
        self.parto_multiplo = boolean_field(view_order = 3, name = 'Parto Múltiplo', default = False, size = 30)
        self.nados_vivos= integer_field(view_order = 4, name = 'Nados Vivos', size = 30)
        self.nados_mortos= integer_field(view_order = 5, name = 'Nados Mortos', size = 30)
        self.peso= integer_field(view_order = 6, name = 'Peso(g)', size = 30)
        self.comprimento= integer_field(view_order = 7, name = 'Compr.(cm)', size = 30)
        self.perimetro_cefalico= integer_field(view_order = 8, name = 'Perimetro Cefálico(cm)', size = 30)
        self.comprimento= integer_field(view_order = 9, name = 'Compr.(cm)', size = 30)
        self.reanimacao = boolean_field(view_order = 10, name = 'Reanimação?', default = False)
        self.profilaxia_ocular = boolean_field(view_order = 11, name = 'Profilaxia Ocular?', default = False)
        self.vitamina_k = boolean_field(view_order = 12, name = 'Vitamina K?', default = False)
        self.vitamina_a_mae = boolean_field(view_order = 13, name = 'Vitamina a Mãe?', default = False)
        self.data = date_field(view_order = 14, name = 'Data', size = 30)
        self.aleitamento_1hora = boolean_field(view_order = 15, name = 'Aleitamneto na Hora?', default = False)      
        self.observacoes = text_field(view_order=16, name='Observações', size=50, onlist=True) 
        self.sr_crianca = combo_field(view_order = 17, name  = 'Criança', size = 50, args = 'required', model = 'sr_criança', search = False, column = 'nome', options = "model.get_opts('SRCrianca().get_options()')", onlist=False)

    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

       

