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
__model_name__ = 'gap_faq.GAPFaq'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPFaq(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_faq'
        self.__title__ ='FAQ´S'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'gap_faq.pergunta'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.pergunta = text_field(view_order=1, name='Pergunta', size=80, args="rows=20", onlist=True, search=False)
        self.resposta = text_field(view_order=2, name='Resposta', size=80, args="rows=20", onlist=True, search=False)
        self.servico = combo_field(view_order = 3, name  = 'Serviço', size = 50, args = 'required', model = 'gap_servico', search = False, column = 'nome', options = "model.get_opts('GAPServico().get_options()')")

    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

    #Apanha Faqs por pergunta
    def get_faqs_pergunta(self, pergunta=None):
        #Essa funçao apanha faqs por pergunta
        def get_results():
            options = []
            opts = self.get()
            for option in opts:
                if option['pergunta'] == pergunta:
                     options.append((str(option['id']), option['pergunta']+'-'+option['resposta']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_faqs_pergunta', createfunc=get_results)


    #Apanha todos os Faqs
    def get_faqs(self):
        #Essa funçao apanha todas as faqs
        options = []
        opts = self.get()
        for f in get_model_fields(self):
            if f[0] == 'servico':
                field=f
        for option in opts:
                 letraservico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                 options.append(option['pergunta']+'-'+option['resposta']+'-'+letraservico)
        return options