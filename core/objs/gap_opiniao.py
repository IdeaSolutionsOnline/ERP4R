# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVTek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_opiniao.GAPOpiniao'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_senha import GAPSenha
except:
    from gap_senha import GAPSenha

class GAPOpiniao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_opiniao'
        self.__title__ = 'Opinião'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'gap_opiniao.nome'
        self.__workflow__ = (
            'estado', {'Confirmado':[]}
            )
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado'])
            ]
        self.nome = string_field(view_order = 1, name = 'Nome', args='readonly', size = 80, search=False, onlist=False)
        self.contacto = string_field(view_order = 2, args='readonly', name = 'Contacto', onlist=False, size = 40)
        self.data = date_field(view_order=3, name ='Data', args='readonly', default=datetime.date.today())
        self.hora = time_field(view_order=4, name ='Hora', args='readonly', default=time.strftime('%H:%M:%S'))
        self.observacao = text_field(view_order=5, name='Observação', size=100, args="rows=30", onlist=False, search=False)
        self.classificacao = string_field(view_order = 6, args='readonly', name = 'Classificação', size = 40)
        self.senha = string_field(view_order = 7, args='readonly', name = 'Senha', size = 50)
        self.servico = string_field(view_order = 8, name = 'Serviço', args='readonly',size = 50)
        self.loja = string_field(view_order = 9, name = 'Loja', size = 50, args='readonly')
        self.estado = info_field(view_order = 10, name='Estado', default='Confirmado', args='readonly', hidden=True, nolabel=True, onlist=False)


    #Apanha todas as opinioes disponiveis
    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

    #Apanha todas as opinioes por data
    def get_opiniao_data(self, data=None):
        #Essa funçao apanha opiniao por data
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                    if option['data'] == data:
                        options.append((str(option['id']), option['nome'] + ' - ' + option['observacao']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_opiniao_data', createfunc=get_results)


   #Apanha todas as opinioes por nome
    def get_opiniao_nome(self, nome=None):
        #Essa funçao apanha opiniao por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['nome'] == nome:
                    options.append((str(option['id']), option['nome'] + ' - ' + option['observacao']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_opiniao_nome', createfunc=get_results)


    #adiciona dados na tabela gap_opiniao
    def addOpiniao(self,user=None,nome=None,contacto=None,comentario=None,classificacao=None, loja=None, nome_atendedor=None):
        try:
            from gap_timeAtendimento import GAPTimeAtendimento
            #Apanho o ultimo cliente atendido por esse atendedor que teoricamente foi aquele que fez a avaliaçao
            result = GAPTimeAtendimento().getLastClient(nome_atendedor=nome_atendedor, loja=loja)
            result = str(result).split(";")
            senha = result[0]
            servico = result[1]
            data = datetime.date.today()
            hora = datetime.datetime.now().time().strftime('%H:%M:%S')
            content = {
            'user': user,
            'nome': nome,
            'contacto':contacto,
            'data':data,
            'hora':hora,
            'observacao':comentario,
            'classificacao':classificacao,
            'senha':senha,
            'servico':servico,
            'loja':loja,
            'estado':'Confirmado',
            }
            GAPOpiniao(**content).put()
            return True
        except:
            return False


    #get avaliaçao do serviço
    def getRating(self, servico=None, loja=None, dataInicio=None, dataFim=None):
        try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            if servico == None:
                self.where = "loja='{loja}'".format(loja=loja)
            else:
                self.where = "servico='{servico}' and loja='{loja}'".format(servico=servico, loja=loja)
            opts = self.get()
            for option in opts:
                data_opiniao = str(option['data']).split("-")
                if (datetime.date(int(data_opiniao[0]),int(data_opiniao[1]), int(data_opiniao[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_opiniao[0]),int(data_opiniao[1]), int(data_opiniao[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        return str(option['classificacao'])
            return "0.0"
        except:
            return "0.0"