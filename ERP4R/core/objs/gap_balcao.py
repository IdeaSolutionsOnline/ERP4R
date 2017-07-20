# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVtek dev"
__status__ = "Development"
__model_name__ = 'gap_balcao.GAPBalcao'
import auth, base_models
from orm import *
from form import *

class GAPBalcao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_balcao'
        self.__title__ ='Balcão' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'int8(gap_balcao.numero)'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.numero = integer_field(view_order=1 , name='Número', size=30)
        self.nome = string_field(view_order=2 , name='Nome', size=50)
        self.terminal = many2many(view_order=3 , name='Loja', size = 50, fields=['name'], model_name = 'terminal.Terminal', condition = "gap_balcao='{id}'", onlist=False)
        self.gap_turno = many2many(view_order=4, name='Horario', size=50 , fields=['nome'], model_name='gap_turno.GAPTurno', condition = "gap_balcao='{id}'", onlist=False)
        self.users = many2many(view_order = 5, name = 'Atendedor', size = 50, fields=['nome'], model_name = 'users.Users', condition = "gap_balcao='{id}'", onlist=False)


    #Apanha todos os balcoes
    def get_self(self):
        return self.get_options()


    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

    #Apanha balcoes por nome
    def get_balcao_nome(self, nome=None):
        #Essa funçao apanha balcao por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                    if option['nome'] == nome:
                        options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_balcao_nome', createfunc=get_results)


    #Apanha o numero do balcao do utilizador actualmente logado no sistema
    def get_balcao(self,loja=None):
        from my_terminal import Terminal
        from my_users import Users
        lojaID = Terminal().get_lojaID(loja=loja)
        turnoID = Users().get_turnoUser()
        self.kargs['join'] = ",gap_balcao_terminal, gap_balcao_gap_turno, gap_balcao_users"
        self.where ="gap_balcao_terminal.terminal = '{lojaid}' and gap_balcao_terminal.gap_balcao= gap_balcao.id  and gap_balcao_gap_turno.gap_balcao=gap_balcao.id and gap_balcao_gap_turno.gap_turno='{turnoid}' and gap_balcao_users.users ='{userid}' and  gap_balcao_users.gap_balcao= gap_balcao.id".format(lojaid=lojaID,userid=bottle.request.session['user'],turnoid=turnoID)
        self.kargs = self.get()
        if self.kargs:
            self.kargs = self.kargs[0]
            return str(self.kargs['numero'])
        return '0'