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
__model_name__ = 'gap_sequencia.GAPSequencia'
import auth, base_models
from orm import *
from form import *
try:
    from my_terminal  import Terminal
except:
    from terminal  import Terminal
try:
    from my_gap_senha import GAPSenha
except:
    from gap_senha import GAPSenha

class GAPSequencia(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_sequencia'
        self.__title__ ='Sequência de Senha' #Gestão de sequencia de senha
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'int8(gap_sequencia.num_senha)'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.num_senha = integer_field(view_order = 1, name = 'Número', args = 'required', size = 20)
        self.data = date_field(view_order = 2, name = 'Data', size=50, args = 'required', default = datetime.date.today())
        self.loja = info_field(view_order=3 , name='Loja', size=40)


    def get_sequence(self, loja=None, user=None):
        #Apanha o numero de senha incrimentando +1 do valor da senha anterior
        self.where = "loja = '{loja}' and active=True".format(loja=loja)
        self.kargs = self.get(order_by='int8(gap_sequencia.num_senha)')
        if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['num_senha'] = self.kargs['num_senha'] + 1
                self.kargs['user'] = user
                self.put()
                return self.kargs['num_senha']
        else:
            #try a few more times,this it's a temporary turn around for the problem
            for z in range(10):
                self.kargs = self.get()
                if self.kargs:
                    self.kargs = self.kargs[0]
                    self.kargs['num_senha'] = self.kargs['num_senha'] + 1
                    self.kargs['user'] = user
                    self.put()
                    return self.kargs['num_senha']
            data_hoje = datetime.date.today()
            self.kargs = {'loja':loja, 'num_senha':1, 'data':data_hoje,'user':user}
            self.put()
            return self.kargs['num_senha']


    #Faz o reset dos numeros das senhas para uma loja xpto
    def reset_numero(self,loja=None):
        try:
            data_hoje = datetime.date.today()
            #Faz o reset do numero das senhas para uma loja xpto cujo a data em que foi retirada seja < que a data de hoje
            self.where = "loja = '{loja}' and active=True".format(loja=loja)
            args = self.get(order_by='int8(gap_sequencia.num_senha)')
            for self.kargs in args:
                    data_fim = str(self.kargs['data']).split("-")
                    if (datetime.date(int(data_fim[0]),int(data_fim[1]), int(data_fim[2])) < data_hoje) and (self.kargs['active'] == True):
                            self.kargs['user'] = bottle.request.session['user']
                            self.kargs['where'] = "id='{id}'".format(id=self.kargs['id'])
                            self.delete()
            return True
        except:
            return False



    #Chamar Senha
    def chamar_senha(self,user_estado=None, loja=None):
        from my_terminal import Terminal
        #Para sabermos o ID da loja onde nos encontramos
        lojaID = Terminal().get_lojaID(loja=loja)
        #Apanha a proxima senha em espera na loja xpto
        senha = GAPSenha().get_proximo(loja=lojaID)
        if senha != None:
            from my_users import Users
            #Se o estado estiver em intervalo ou terminado e alterado e mudado para em serviço
            if (user_estado=='intervalo') or (user_estado=='terminado'):
                 Users().EmServico()

            #questoes de alteraçoes para dados estatisticos
            from gap_timeAtendimento import  GAPTimeAtendimento

            senha_id = self.get_id_senha(senha=senha)

            #Muda o estado da senha para_atendimento
            GAPSenha().Para_Atendimento(id=senha_id)

            if (self.get_estado_senha(senha=senha) == 'transferido'):
                  GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id,estado="para_atendimento", loja=loja)
            else:
                #addTimeAtendimento necessario para ajudar na gestao das estatisticas e relatorios
                self.addTimeAtendimento(senha=GAPSenha().get_senhaInfo(id=senha_id), tempo_atendimento='00:00:00', servico=self.get_servico_senha(senha=senha), loja=loja, senha_id=senha_id)

            #retorna a respectiva senha
            return senha
        else:
            return None


    #Chamar Senha especifica
    def chamar_por_senha(self, senha=None,user_estado=None, loja=None):
        from my_terminal import Terminal
        #Para sabermos o ID da loja onde nos encontramos
        lojaID = Terminal().get_lojaID(loja=loja)
        senha = GAPSenha().get_senha(senha=senha, loja=lojaID)
        if senha != None:
            from my_users import Users
            #Se o estado estiver em intervalo ou terminado e alterado e mudado para em serviço
            if (user_estado=='intervalo') or (user_estado=='terminado'):
                    Users().EmServico()

            #questoes de alteraçoes para dados estatisticos
            from gap_timeAtendimento import  GAPTimeAtendimento

            senha_id = self.get_id_senha(senha=senha)

            #Muda o estado da senha para_atendimento
            GAPSenha().Para_Atendimento(id=senha_id)

            if (self.get_estado_senha(senha=senha) == 'transferido'):
                  GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id,estado="para_atendimento", loja=loja)
            else:
                #addTimeAtendimento necessario para ajudar na gestao das estatisticas e relatorios
                self.addTimeAtendimento(senha=GAPSenha().get_senhaInfo(id=senha_id), tempo_atendimento='00:00:00', servico=self.get_servico_senha(senha=senha), loja=loja, senha_id=senha_id)

            #retorna a respectiva senha
            return senha
        else:
            return None


    #coloca a senha em espera pelo atendedor xpto
    def espera_atendedor(self,senha=None,tempo_atendimento=None,comentario=None, loja=None):
        try:
            senha_id = self.get_id_senha(senha=senha)
            #change senha estado para espera pelo atendedor
            GAPSenha().Espera_Atendedor(id=senha_id)
            #questoes de alteraçoes para dados estatisticos
            from gap_timeAtendimento import  GAPTimeAtendimento
            GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id, estado="espera_atendedor", loja=loja)
            GAPTimeAtendimento().setTimeAtendimento(senha_id=senha_id, tempo_atendimento=tempo_atendimento, loja=loja)
            GAPTimeAtendimento().setObservacao(senha_id=senha_id, comentario=comentario, loja=loja)
            return True
        except:
            return False

    #chamar pela senha em espera do atendedor xpto
    def chamar_senhaEspera(self,senha_id=None,user_estado=None, loja=None):
            from my_terminal import Terminal
            from gap_timeAtendimento import GAPTimeAtendimento
            #Verificamos se o atendedor encontra-se disponivel no momento
            atendedorDisponivel = GAPTimeAtendimento().checkAtendedor(loja=loja)
            if (atendedorDisponivel):
                #Para sabermos o ID da loja onde nos encontramos
                lojaID = Terminal().get_lojaID(loja=loja)
                senha = GAPSenha().get_senhaExtraInfo(id=senha_id)
                if senha != None:
                    from my_users import Users
                    #Se o estado estiver em intervalo ou terminado e alterado e mudado para em serviço
                    if (user_estado=='intervalo') or (user_estado=='terminado'):
                         Users().EmServico()

                    #Muda o seu estado para_atendimento
                    GAPSenha().Para_Atendimento(id=senha_id)
                    #mudar o estado da senha em espera pelo atendedor presenta na lista de estatistica
                    GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id,estado="para_atendimento", loja=loja)
                    #retorna a respectiva senha
                    return senha
                else:
                    return None
            else:
                return 'atendedor_ocupado'


    #Transferir Senha
    def transferir_senha(self, senha=None, keyservico=None, newservico=None, loja=None):
        senha_id = self.get_id_senha(senha=senha)
        GAPSenha().Transferido(id=senha_id,keyservico=keyservico)
        from gap_timeAtendimento import GAPTimeAtendimento
        GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id, estado="transferido", loja=loja)
        GAPTimeAtendimento().setServicoAtendimento(senha_id=senha_id, newservico=newservico, loja=loja)
        return senha


    #Terminar Senha
    def terminar_senha(self, senha=None,tempo_atendimento=None, loja=None):
        senha_id = self.get_id_senha(senha=senha)
        #Muda o estado para atendido
        GAPSenha().Atendido(id=senha_id)
        from gap_timeAtendimento import GAPTimeAtendimento
        #Altera o estado do individuo para atendido na lista necessario para estatistica
        GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id, estado="atendido", loja=loja)
        #Altera o seu tempo de atendimento
        GAPTimeAtendimento().setTimeAtendimento(senha_id=senha_id,tempo_atendimento=tempo_atendimento, loja=loja)
        return senha

    #Desistir Senha
    def desistir_senha(self, senha=None,tempo_atendimento=None, loja=None):
        senha_id = self.get_id_senha(senha=senha)
        #Muda o estado para desistiu
        GAPSenha().Desistiu(id=senha_id)
        from gap_timeAtendimento import GAPTimeAtendimento
        #Altera o estado do individuo para desistiu na lista necessario para estatistica
        GAPTimeAtendimento().setEstadoAtendimento(senha_id=senha_id,estado="desistiu", loja=loja)
        #Altera o seu tempo de atendimento
        GAPTimeAtendimento().setTimeAtendimento(senha_id=senha_id, tempo_atendimento=tempo_atendimento, loja=loja)
        return senha


    #get id Senha clean retirando a letra e o numero do respectivo serviço associado
    def get_id_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[0]

   #get letra+numero da senha clean
    def get_letra_numero(self, senha=None):
        senha= senha.split(";")
        return  senha[1]

    #get a letra da senha clean
    def get_letra_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[1][:1]

    #get o servico da senha clean
    def get_servico_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[2]

    #get o estado da senha clean
    def get_estado_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[3]

    #get a numero da senha clean
    def get_numero_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[1][1:]

    #guarda o tempo de atendimento
    def saveTime(self,senha_id=None, tempo_atendimento=None, loja=None):
        try:
            from gap_timeAtendimento import GAPTimeAtendimento
            GAPTimeAtendimento().setTimeAtendimento(senha_id=senha_id,tempo_atendimento=tempo_atendimento, loja=loja)
            return True
        except:
            return False


    #adiciona dados na tabela timeAtendimento para ajudar na qestao dos relatorios :)
    def addTimeAtendimento(self,senha=None,tempo_atendimento=None,comentario=None,servico=None, loja=None, senha_id=None):
        try:
            senha = senha.split(';')
            from gap_timeAtendimento import GAPTimeAtendimento
            content = {
            'user': '{user}'.format(user=bottle.request.session['user']),
            'nome_atendedor': '{name}'.format(name=bottle.request.session['user_name']),
            'senha':senha[1],
            'servico':servico,
            'hora_entrada':senha[2],
            'data':senha[3],
            'tempo_atendimento':tempo_atendimento,
            'estado':senha[4],
            'observacao':comentario,
            'loja':loja,
            'senha_id':senha_id,
            }
            GAPTimeAtendimento(**content).put()
            return True
        except:
            return False