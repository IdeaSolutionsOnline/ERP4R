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
__model_name__ = 'gap_turno.GAPTurno'
import auth, base_models
from orm import *
from form import *

class GAPTurno(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_turno'
        self.__title__ ='Turno' #Gestão de atendimento Presencial turno
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_turno.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__get_options__ = ['nome']
        self.nome = string_field(view_order = 1, name = 'Nome', size = 40)
        self.hora_inicio = time_field(view_order=2, name ='Hora Inicio',size=40, args='required', default=time.strftime('%H:%M:%S'), onlist=False)
        self.hora_fim = time_field(view_order=3, name ='Hora Fim',size=40, args='required', default=time.strftime('%H:%M:%S'), onlist=False)
        self.gap_servico = many2many(view_order=4, name='Serviço', fields=['nome'], size=50, model_name='gap_servico.GAPServico', condition="gap_turno='{id}'", onlist=False)
        self.gap_balcao = many2many(view_order=5, name='Balcão', fields=['nome'], size=50, model_name='gap_balcao.GAPBalcao', condition="gap_turno='{id}'", onlist=False)
        self.users = many2many(view_order=6 , name='Utilizadores', condition="gap_turno='{id}'", size=50, model_name='users.Users', fields = ['nome'], onlist = False)
        #self.estado = info_field(view_order = 6, name = 'Estado', default = 'Aberta')
        #self.numero = info_field(view_order = 7, name = 'Número')


    #Apanha todos os turnos
    def get_self(self):
        return self.get_options()

    #get turno xpto dentro do horario actual do sistema retornando o seu id
    def get_turno(self):
        opts = self.get()
        hora_actual = datetime.datetime.now()
        for option in opts:
                hora_inicio = str(option['hora_inicio']).split(":")
                hora_fim = str(option['hora_fim']).split(":")
                hora_inicio = hora_actual.replace(hour=int(hora_inicio[0]), minute=int(hora_inicio[1]), second=int(hora_inicio[2]), microsecond=0)
                hora_fim = hora_actual.replace(hour=int(hora_fim[0]), minute=int(hora_fim[1]), second=int(hora_fim[2]), microsecond=0)
                if  (hora_actual >= hora_inicio) and (hora_actual<= hora_fim):
                              return str(option['id'])
        return '0'

    #Check Turno
    def check_turno(self, turno_id):
        self.where = "id = '{id}'".format(id=turno_id)
        self.kargs = self.get()
        hora_actual = datetime.datetime.now()
        if self.kargs:
            self.kargs = self.kargs[0]
            hora_inicio = str(self.kargs['hora_inicio']).split(":")
            hora_fim = str(self.kargs['hora_fim']).split(":")
            hora_inicio = hora_actual.replace(hour=int(hora_inicio[0]), minute=int(hora_inicio[1]), second=int(hora_inicio[2]), microsecond=0)
            hora_fim = hora_actual.replace(hour=int(hora_fim[0]), minute=int(hora_fim[1]), second=int(hora_fim[2]), microsecond=0)
            if  (hora_actual >= hora_inicio) and (hora_actual<= hora_fim):
                              return True
        return False