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
__model_name__ = 'anexo.Anexo'
#import base_models
from orm import *
from form import *


class Anexo(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'anexo'
        self.__title__ = 'Anexos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'inline'
        self.__get_options__ = ['descricao']

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['All']
            }

        self.tarefa = parent_field(view_order=1, name ='Inscrição', args='style:visibility="hidden"', model_name='inscricao.Inscricao', nolabel=True, onlist=False, column='numero')#ao ligar a tarefa estou automaticamente a ligar a todos os objectos que estão ligados a tarefas, a unica questão é se eu quiser ligar a uma actividade por exemplo sem ligar a nenhuma tarefa
        self.nome = string_field(view_order = 2, name = 'Nome', size = 80)
        self.upload = upload_field(view_order = 3, name = 'Documento', size = 100)
        #self.tipo =
        #self.editores =
        #self.leitores =
        #self.projectos =
        #self.processos =

