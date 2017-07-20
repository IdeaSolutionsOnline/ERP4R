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
__model_name__ = 'gap_checklist.GAPChecklist'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPChecklist(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_checklist'
        self.__title__= 'Checklist'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'gap_checklist.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order = 1, name = 'Nome', args = 'required', size = 50)
        self.servico = combo_field(view_order = 2, name  = 'Serviço', size = 50, args = 'required', model = 'gap_servico', search = False, column = 'nome', options = "model.get_opts('GAPServico().get_options()')")

    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

    #Apanha OS checklist por nome
    def get_checklist_nome(self, nome=None):
        #Essa funçao apanha checklist por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                    if option['nome'] == nome:
                        options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_checklist_nome', createfunc=get_results)

    #Apanha OS checklist
    def get_checklist(self):
        #Essa funçao apanha checklist associado ao respectivo serviço em atendimento
        options = []
        opts = self.get()
        for f in get_model_fields(self):
            if f[0] == 'servico':
                field=f
        for option in opts:
                letraservico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                options.append(option['nome']+"-"+letraservico)
        return options