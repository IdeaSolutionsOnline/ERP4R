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
__model_name__ = 'gap_timeAtendimento.GAPTimeAtendimento'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPTimeAtendimento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_timeAtendimento'
        self.__title__ ='Gap Time Atendimento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_timeAtendimento.senha'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
        }
        self.nome_atendedor = string_field(view_order = 1, name = 'Nome Atendedor', args='readonly', size = 80)
        self.senha = string_field(view_order = 2, name = 'senha', args='readonly', size = 50)
        self.servico = string_field(view_order = 3, name = 'servico', args='readonly',size = 50)
        self.hora_entrada= time_field(view_order=4, name ='Hora Pedido', args='readonly', size=40, onlist=True)
        self.data = date_field(view_order = 5, name = 'Data', size=40, args='readonly')
        self.tempo_atendimento= time_field(view_order=6, name ='Tempo Atendimento', size=40, args='readonly', onlist=True)
        self.estado = combo_field(view_order = 7, name = 'Estado', size = 50, args='readonly', default = 'Espera', options = [('espera','Espera'), ('espera_atendedor','Espera Atendedor'), ('atendido','Atendido'), ('desistiu','Desistiu'), ('transferido','Transferido'), ('para_atendimento','Para Atendimento')])
        self.observacao = text_field(view_order=8, name='Observação', size=100, args="rows=30", onlist=False, search=False)
        self.loja = string_field(view_order = 9, name = 'Loja', size = 50, args='readonly')
        self.senha_id = string_field(view_order = 10, name = 'senha id', onlist=False, hidden=True, args='readonly', size = 50)

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)


    def getTimeAtendimento(self, senha=None,servico=None, loja=None):
        try:
            self.where = "nome_atendedor = '{name}' and  senha='{senha}' and servico='{servico}' and data='{data}' and loja='{loja}'".format(name=bottle.request.session['user_name'],senha=senha,servico=servico,data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return self.kargs['tempo_atendimento']
            return None
        except:
            return None

    def setTimeAtendimento(self,senha_id=None,tempo_atendimento=None, loja=None):
        try:
            self.where = "senha_id ='{senha_id}' and data='{data}' and loja='{loja}'".format(senha_id=senha_id,data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['tempo_atendimento'] = tempo_atendimento
                self.put()
            return True
        except:
            return False

    def setEstadoAtendimento(self,senha_id=None, estado=None, loja=None):
        try:
            self.where = "senha_id = '{senha_id}'  and data='{data}' and loja='{loja}'".format(senha_id=senha_id,data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = estado
                self.put()
            return True
        except:
            return False

    def setServicoAtendimento(self,senha_id=None, newservico=None, loja=None):
        try:
            self.where = "senha_id='{senha_id}' and data='{data}' and loja='{loja}'".format(senha_id=senha_id,data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['servico'] = newservico
                self.put()
            return True
        except:
            return False


    def setObservacao(self,senha_id=None,comentario=None, loja=None):
        try:
            self.where = "senha_id='{senha_id}' and data='{data}' and loja='{loja}'".format(senha_id=senha_id,data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['observacao'] = comentario
                self.put()
            return True
        except:
            return False


    #Faz o get das senhas em espera pelo atendedor xtpo na loja y (a filtragem e feita no proprio formulario devido a alguns factos...)
    def getClienteEspera(self, loja=None):
        options = []
        self.where = "nome_atendedor = '{name}' and estado='espera_atendedor' and loja='{loja}'".format(name=bottle.request.session['user_name'], loja=loja)
        opts = self.get()
        for option in opts:
                options.append(str(option['senha_id'])+";"+option['servico']+";"+str(option['senha'])+';'+str(option['observacao'])+';'+str(option['tempo_atendimento']))
        return options


    #Faz o get do servico actualmente em atendimento pelo atendedor
    def getServicoAtendimento(self, loja=None):
         try:
            self.where = "nome_atendedor = '{name}' and  estado='para_atendimento' and data='{data}' and loja='{loja}'".format(name=bottle.request.session['user_name'],data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return self.kargs['servico']
            return None
         except:
            return None

    #em caso de ter ocorrido algum erro e por algum engano o atendedor nao atender o cliente automaticamente e mudado para desistir
    def checkTimeAtendimento(self, loja=None):
         try:
            self.where = "nome_atendedor = '{name}' and  estado='para_atendimento' and data='{data}' and loja='{loja}'".format(name=bottle.request.session['user_name'],data=str(datetime.date.today()), loja=loja)
            args = self.get()
            for self.kargs in args:
                if (self.kargs['estado'] == 'para_atendimento'):
                        from gap_senha import GAPSenha
                        GAPSenha().Desistiu(id=self.kargs['senha_id'])
                        self.kargs['user'] = bottle.request.session['user']
                        self.kargs['estado'] = 'desistiu'
                        self.put()
            return True
         except:
            return False

    #em caso de ter ocorrido algum erro e por algum engano o atendedor nao atender o cliente em dia ou dias anteriores automaticamente e mudado para desistir
    def checkTimeAtendimentoLater(self, senha_id=None, loja=None):
         try:
            self.where = "senha_id = '{senha_id}' and loja='{loja}'".format(senha_id=senha_id, loja=loja)
            self.kargs = self.get()
            data_hoje = datetime.date.today()
            #para_atendimento ou espera atendedor de dias anteriores sao alterados para desistiriu
            if self.kargs:
                self.kargs = self.kargs[0]
                data_senha = str(self.kargs['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2])) < data_hoje):
                       if (self.kargs['estado'] == 'para_atendimento') or (self.kargs['estado'] == 'espera_atendedor'):
                                self.kargs['user'] = bottle.request.session['user']
                                self.kargs['estado'] = 'desistiu'
                                self.put()
            return True
         except:
            return False


    #aqui eu fasso o get do numero de pessoas que foram atendidas pelo atendedor xpto
    def get_clienteAtendido(self, nome=None, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            count = 0
            if servico == None:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}'".format(name=nome, loja=loja)
            else:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}' and servico='{servico}' ".format(name=nome, loja=loja, servico=servico)
            opts = self.get()
            for option in opts:
                data_senha = str(option['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        count+=1
            return count
         except:
            return 0

    #aqui eu fasso o get do numero de pessoas que desistiram pelo atendedor xpto
    def get_clienteDesistiram(self, nome=None, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            count = 0
            if servico == None:
                self.where = "nome_atendedor = '{name}' and  estado='desistiu' and  loja='{loja}'".format(name=nome, loja=loja)
            else:
                self.where = "nome_atendedor = '{name}' and  estado='desistiu' and  loja='{loja}' and servico='{servico}' ".format(name=nome, loja=loja, servico=servico)
            opts = self.get()
            for option in opts:
                data_senha = str(option['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        count+=1
            return count
         except:
            return 0


    #aqui eu fasso o get do numero de pessoas que foram atendidas na loja xpto
    def get_clienteAtendidoByLoja(self, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            count = 0
            if servico == None:
                self.where = "estado='atendido' and  loja='{loja}'".format(loja=loja)
            else:
                self.where = "estado='atendido' and  loja='{loja}' and servico='{servico}' ".format(loja=loja, servico=servico)
            opts = self.get()
            for option in opts:
                data_senha = str(option['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        count+=1
            return count
         except:
            return 0

    #aqui eu fasso o get do numero de pessoas que desistiram na loja xpto
    def get_clienteDesistiramByLoja(self, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            count = 0
            if servico == None:
                self.where = "estado='desistiu' and  loja='{loja}'".format(loja=loja)
            else:
                self.where = "estado='desistiu' and  loja='{loja}' and servico='{servico}' ".format(loja=loja, servico=servico)
            opts = self.get()
            for option in opts:
                data_senha = str(option['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        count+=1
            return count
         except:
            return 0

    #faz o get do tempo medio de atendimento
    def  get_mediaTempoAtendido(self, nome=None, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            hora = 0
            minuto = 0
            segundos = 0
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            count = 0
            if servico == None:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}'".format(name=nome, loja=loja)
            else:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}' and servico='{servico}' ".format(name=nome, loja=loja, servico=servico)
            opts = self.get()
            for option in opts:
                data_senha = str(option['data']).split("-")
                time = str(option['tempo_atendimento']).split(":")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                            hora+=int(time[0])
                            minuto+=int(time[1])
                            segundos+=int(time[2])
                            count+=1
            """
            if (segundos>60):
                  while(segundos>60):
                      minuto+=1
                      segundos-=60
            if(minuto>60):
                  while(minuto>60):
                      hora+=1
                      minuto-=60
            """
            hora = int(hora/count)
            minuto = int(minuto/count)
            segundos = int(segundos/count)
            if (hora< 10):
                  hora = '0'+str(hora)
            if(minuto < 10):
                  minuto = '0'+str(minuto)
            if(segundos < 10):
                  segundos = '0'+str(segundos)
            return str(hora)+":"+str(minuto)+":"+str(segundos)
         except:
            return "00:00:00"


    #faz o get do tempo maximo de atendimento
    def  get_tempoMaximoAtendido(self, nome=None, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            if servico == None:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}'".format(name=nome, loja=loja)
            else:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}' and servico='{servico}' ".format(name=nome, loja=loja, servico=servico)
            opts = self.get(order_by='tempo_atendimento DESC')
            for option in opts:
                data_senha = str(option['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        return str(option['tempo_atendimento'])
            return '00:00:00'
         except:
            return '00:00:00'


    #faz o get do tempo minimo de atendimento
    def  get_tempoMinimoAtendido(self, nome=None, dataInicio=None, dataFim=None, loja=None, servico=None):
         try:
            dataInicio = str(dataInicio).split("-")
            dataFim = str(dataFim).split("-")
            if servico == None:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}'".format(name=nome, loja=loja)
            else:
                self.where = "nome_atendedor = '{name}' and  estado='atendido' and  loja='{loja}' and servico='{servico}' ".format(name=nome, loja=loja, servico=servico)
            opts = self.get(order_by='tempo_atendimento ASC')
            for option in opts:
                data_senha = str(option['data']).split("-")
                if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))>=datetime.date(int(dataInicio[0]),int(dataInicio[1]), int(dataInicio[2]))) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))<=datetime.date(int(dataFim[0]),int(dataFim[1]), int(dataFim[2]))):
                        return str(option['tempo_atendimento'])
            return '00:00:00'
         except:
            return '00:00:00'


    #verifica se o atendedor tem algum cliente em atendimento actualmente
    def checkAtendedor(self, loja=None):
        try:
            self.where = "nome_atendedor = '{name}' and  estado='para_atendimento' and data='{data}' and loja='{loja}'".format(name=bottle.request.session['user_name'],data=str(datetime.date.today()), loja=loja)
            self.kargs = self.get()
            if self.kargs:
                return False
            return True
        except:
            return False


    #Faz o get do ultimo cliente atendido pelo atendedor xpto (essa funçao vai ser utilizada no adicionar opiniao partimos do principio que o cliente que vai dar a sua opiniao e o ultimo atendido pelo atendedor)
    def getLastClient(self, nome_atendedor=None, loja=None):
        self.where = "nome_atendedor='{nome_atendedor}' and data='{data}' and loja='{loja}' and estado='atendido' ".format(nome_atendedor=nome_atendedor,data=str(datetime.date.today()), loja=loja)
        self.kargs = self.get(order_by='hora_entrada DESC')
        if self.kargs:
            self.kargs = self.kargs[0]
            return self.kargs['senha']+";"+self.kargs['servico']
        return ";;"