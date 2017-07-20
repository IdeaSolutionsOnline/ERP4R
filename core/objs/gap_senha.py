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
__model_name__ = 'gap_senha.GAPSenha'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPSenha(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_senha'
        self.__title__ ='Senha' #Gestão de atendimento Presencial senha
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nr_senha']
        self.__order_by__ = 'int8(gap_senha.nr_senha)'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.servico = combo_field(view_order = 1, name  = 'Serviço', size = 50, args = 'required', model = 'gap_servico', search = False, column = 'nome', options = "model.get_opts('GAPServico().get_options()')")
        self.letra = string_field(view_order=2, name='Letra', size=15, args='readonly',onlist = False)
        self.nr_senha = string_field(view_order=3 , name='Nº Senha', args='readonly',size=30, onlist = True)
        self.data = date_field(view_order = 4, name = 'Data Inicial', args='readonly',size=40, default = datetime.date.today())
        self.hora_ped = time_field(view_order=5, name ='Hora Pedido', args='readonly',size=40, onlist=False, default=time.strftime('%H:%M:%S'))
        self.est_atend = string_field(view_order=6 , name='Estimativa Atendimento', args='readonly', size=40, onlist = False)
        self.pess_fila = string_field(view_order=7, name='Nº Pessoas na Fila', args='readonly',size=40, default = 0, onlist = False)
        self.estado = combo_field(view_order = 8, name = 'Estado', args = 'required', size = 50, default = 'Espera', options = [('espera','Espera'), ('espera_atendedor','Espera Atendedor'), ('atendido','Atendido'), ('desistiu','Desistiu'), ('transferido','Transferido'), ('para_atendimento','Para Atendimento')], onlist = True)
        self.terminal = many2many(view_order = 9, name = 'Loja', size = 50, fields=['name'], model_name = 'terminal.Terminal', condition = "gap_senha='{id}'", hidden=True, onlist=False)


    #Apanha Senha Geral :)
    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)


    #Apanha Senhas Atendidas
    def get_atendido(self):
        #Essa funçao apanha todas as senhas atendidas
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            for option in opts:
                if option['estado'] == 'atendido':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_atendido', createfunc=get_results)

    #Apanha Senhas em Espera
    def get_espera(self):
        #Essa funçao apanha todas as senhas em espera
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            for option in opts:
                if option['estado'] == 'espera':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_espera', createfunc=get_results)

    #Apanha Senhas que desistiram
    def get_desistiu(self):
        #Essa funçao apanha todas as senhas que desistiram
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            for option in opts:
                if option['estado'] == 'desistiu':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_desistiu', createfunc=get_results)

    #Apanha Senhas Transferidas
    def get_transferidas(self):
        #Essa funçao apanha todas as senhas transferidas
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            for option in opts:
                if option['estado'] == 'transferido':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_transferido', createfunc=get_results)

    #Apanha Senhas para atendimento
    def get_para_atendimento(self):
        #Essa funçao apanha todas as senhas para atendimento
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            for option in opts:
                if option['estado'] == 'para_atendimento':
                     options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_para_atendimento', createfunc=get_results)


    #Apanha Senha por Data
    def get_senha_data(self, data=None):
        #Essa funçao apanha todas as senhas em uma determinada data
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            for option in opts:
                if option['data'] == data:
                        options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_senha_data', createfunc=get_results)


    #Mudar Estado Senha para Espera
    def  Espera(self, id=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'espera'
                self.put()
            return True
         except:
            return False

     #Mudar Estado Senha para Atendido
    def  Atendido(self, id=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'atendido'
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para Desistido
    def  Desistiu(self, id=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'desistiu'
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para Transferido
    def  Transferido(self, id=None,keyservico=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'transferido'
                self.kargs['servico'] = keyservico
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para atendimento
    def  Para_Atendimento(self, id=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'para_atendimento'
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para espera por atendedor
    def  Espera_Atendedor(self, id=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'espera_atendedor'
                self.put()
            return True
         except:
            return False


    #set numero de pessoas em fila
    def  Pessoas_Fila(self, id=None,user=None, pess_fila=None):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = user
                self.kargs['pess_fila'] = pess_fila
                self.put()
            return True
         except:
            return False

    #get Numero de senha
    def get_numero_senha(self, loja=None, user=None):
        #apanha o numero de senha
        from gap_sequencia import GAPSequencia
        numero = GAPSequencia().get_sequence(loja=loja, user=user)
        return  numero


    #get Numero de pessoas na fila numa loja xpto
    def get_pessoas_fila(self, loja=None):
        #Essa funçao retorna o numero de pessoas em fila na loja xpto
        self.kargs['join'] = ",gap_senha_terminal"
        self.where ="gap_senha_terminal.terminal = '{id}' and gap_senha_terminal.gap_senha= gap_senha.id".format(id=str(loja))
        options = []
        opts = self.get(order_by='int8(gap_senha.nr_senha)')
        count = -1
        data_hoje = datetime.date.today()
        for option in opts:
                data_senha = str(option['data']).split("-")
                if (option['estado'] == 'espera') and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))==data_hoje):
                        count += 1
        return count


    #get Estimativa atendimento
    def get_estimativa(self, loja=None):
        #apanha a estimativa de atendimento para uma determinada senha numa loja
        #Essa funçao faz uma prespectiva que cada senha em espera vai ter pelomenos 5 minutos a serem atendidos
        self.kargs['join'] = ",gap_senha_terminal"
        self.where ="gap_senha_terminal.terminal = '{id}' and gap_senha_terminal.gap_senha= gap_senha.id".format(id=str(loja))
        options = []
        opts = self.get(order_by='int8(gap_senha.nr_senha)')
        hora = 0
        minuto = 0
        count = -1
        data_hoje = datetime.date.today()
        for option in opts:
                data_senha = str(option['data']).split("-")
                if (option['estado'] == 'espera') and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))==data_hoje):
                        count+=1
                        if(count>0):
                            if (minuto < 59):
                                   minuto = minuto+5
                            elif (minuto >= 59):
                                     minuto = 0
                                     hora=hora+1
        if (hora == 0) and (minuto == 0):
              return '00:00:00'
        else:
            if (hora < 10):
                   hora = '0'+str(hora)
            if (minuto < 10):
                   minuto = '0'+str(minuto)

            return str(hora)+":"+str(minuto)+":00"


    #Apanhar a proxima senha em espera ou transferido ordenando pela ordem na loja xpto (recebendo o id da respectiva loja :)
    def get_proximo(self, loja=None):
        try:
            self.kargs['join'] = ",gap_senha_terminal"
            self.where ="gap_senha_terminal.terminal = '{id}' and gap_senha_terminal.gap_senha= gap_senha.id".format(id=str(loja))
            options = []
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            data_hoje = datetime.date.today()
            for f in get_model_fields(self):
                if f[0] == 'servico':
                    field=f
            for option in opts:
                    data_senha = str(option['data']).split("-")
                    if (option['estado'] == 'espera') or (option['estado'] == 'transferido'):
                            if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))==data_hoje):
                                    servico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                                    res = str(option['gap_senha'])+";"+str(option['letra'])+str(option['nr_senha'])+";"+str(servico)+";"+str(option['estado'])
                                    return  res
            return None
        except:
            return None



    #Atraves de uma letra e um numero de senha retorna a respectivo senha com o ID
    def get_senha(self,senha=None, loja=None):
        try:
            self.kargs['join'] = ",gap_senha_terminal"
            self.where ="gap_senha_terminal.terminal = '{id}' and gap_senha_terminal.gap_senha= gap_senha.id".format(id=str(loja))
            opts = self.get(order_by='int8(gap_senha.nr_senha)')
            letrasenha = senha[:1]
            numerosenha = senha[1:]
            data_hoje = datetime.date.today()
            for f in get_model_fields(self):
                if f[0] == 'servico':
                    field=f
            for option in opts:
                    data_senha = str(option['data']).split("-")
                    if(int(option['nr_senha'])==int(numerosenha)) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2])) == data_hoje):
                                if (option['estado'] == 'espera') or (option['estado'] == 'transferido'):
                                        servico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                                        if(letrasenha==str(option['letra'])):
                                                return str(option['gap_senha'])+";"+str(option['letra'])+str(option['nr_senha'])+";"+str(servico)+";"+str(option['estado'])
            return None
        except:
            #Em caso o inviduo insirir uma senha a brincar logo invalida :)
            return None


    #get senha com mais informaçoes
    def get_senhaInfo(self,id=None):
        try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            if self.kargs:
                self.kargs = self.kargs[0]
                return str(self.kargs['id'])+";"+str(self.kargs['letra'])+str(self.kargs['nr_senha'])+";"+str(self.kargs['hora_ped'])+";"+str(self.kargs['data'])+";"+str(self.kargs['estado'])
            return None
        except:
            return None

    #get senha com mais informaçoes plus extras :D
    def get_senhaExtraInfo(self,id=None):
        try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
            for f in get_model_fields(self):
                if f[0] == 'servico':
                    field=f
            if self.kargs:
                self.kargs = self.kargs[0]
                servico = get_field_value(record=self.kargs, field=field, model=self)['field_value'][1]
                return str(self.kargs['id'])+";"+str(self.kargs['letra'])+str(self.kargs['nr_senha'])+";"+str(servico)+";"+str(self.kargs['hora_ped'])+";"+str(self.kargs['data'])+";"+str(self.kargs['estado'])
            return None
        except:
            return None

    #Retornar ecran de atendimento
    def get_ecran_atendimento(self, window_id):
        return form_gap_atendedor(window_id=window_id).show()


    #Descartar senhas com data limite expirada para uma loja especifica
    def descartar_senha(self,loja=None):
        try:
            from my_terminal import Terminal
            from gap_timeAtendimento import GAPTimeAtendimento
            #Para sabermos o ID da loja onde nos encontramos
            lojaID = Terminal().get_lojaID(loja=loja)
            self.kargs['join'] = ",gap_senha_terminal"
            self.where ="gap_senha_terminal.terminal = '{id}' and gap_senha_terminal.gap_senha=gap_senha.id".format(id=str(lojaID))
            args = self.get(order_by='int8(gap_senha.nr_senha)')
            data_hoje = datetime.date.today()
            for self.kargs in args:
                data_fim = str(self.kargs['data']).split("-")
                if (datetime.date(int(data_fim[0]),int(data_fim[1]), int(data_fim[2])) < data_hoje) and (self.kargs['active'] == True):
                        if(self.kargs['estado'] == 'para_atendimento') or (self.kargs['estado'] == 'espera_atendedor') or (self.kargs['estado'] == 'espera'):
                               senha_id = self.kargs['gap_senha']
                               self.Desistiu(id=senha_id)
                               GAPTimeAtendimento().checkTimeAtendimentoLater(senha_id=senha_id, loja=loja)
            return True
        except:
            return False


    #essa funçao e chamada quando o cliente retira uma senha
    def get_SenhaCliente(self, user=None, servico=None, letra=None, loja=None):
        try:
            #Aviso para que o imprimir senha funcione como deve ser e necessario instalar um plugin no browser mozila AttendPrint  ou soluçoes do genero para o google chrome aplicando-se comandos como o --kioske print
            from my_terminal import Terminal
            from gap_servico import   GAPServico
            lojaId = Terminal().get_lojaID(loja=loja)
            servico_id = GAPServico().get_servico_id(nome=servico)
            output = None
            if(lojaId==0):
                return None
            else:
                if(GAPServico().check_turnoServico(servico_id=servico_id) == True):
                    print("dentro do if ca podi :( ")
                    data = datetime.date.today()
                    hora = datetime.datetime.now().time().strftime('%H:%M:%S')
                    nr_senha = self.get_numero_senha(loja=loja,user=user)
                    content = {
                    'user': '{user}'.format(user=user),
                    'servico': servico_id,
                    'letra':letra,
                    'nr_senha': nr_senha,
                    'data':data,
                    'hora_ped':hora,
                    'pess_fila': 0,
                    'est_atend': 0,
                    'estado':'espera',
                    }
                    GAPSenha(**content).put()
                    #agora buscamos pelo id da senha que acabamos de insirir
                    self.where = "servico = '{servico}' and nr_senha= '{nr_senha}' and hora_ped= '{hora_ped}' and data= '{data}'".format(servico=str(servico_id),nr_senha=str(nr_senha),hora_ped=str(hora),data=str(data))
                    self.kargs = self.get(order_by='int8(gap_senha.nr_senha)')
                    if self.kargs:
                        self.kargs = self.kargs[0]
                        kargs = {}
                        kargs['terminal'] = lojaId
                        kargs['parent_name'] = 'terminal'
                        kargs['gap_senha'] = self.kargs['id']
                        kargs['user'] = user
                        #adicionamos na relaçao m2m
                        GAPSenha(**kargs).put_m2m()
                        #actualizamos a senha com os valores das pessoas em fila , estimativa de atendimento nessa loja
                        pess_fila = self.get_pessoas_fila(loja=lojaId)
                        est_atend = self.get_estimativa(loja=lojaId)
                        updatedcontent = {
                            'id':'{id}'.format(id=self.kargs['id']),
                            'user': '{user}'.format(user=user),
                            'pess_fila': pess_fila,
                            'est_atend': est_atend,
                        }
                        GAPSenha(**updatedcontent).put()
                        #Enfim finalmente vamos imprimir a nossa senha :)
                        from gap_senha_config import  GAPSenhaConfig
                        senhaConfigServico = GAPSenhaConfig().get_config_servico(servico=servico_id)
                        senhaConfigLoja =  GAPSenhaConfig().get_config_loja(loja=lojaId)
                        senhaConfigLoja = str(senhaConfigLoja).split(";")
                        senhaConfigServico = str(senhaConfigServico).split(";")
                        #Estou a utilizar esse metodo por causa de alguns problemas com o reports nesse caso especifico....alterar depois
                        output = """
                            <!DOCTYPE html>
                                <html>
                                    <head>
                                        <title>Senha</title>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <link rel="stylesheet" href="/static/css/foundation.css" />
                                        <link rel="stylesheet" href="/static/css/gap.css" />
                                    </head>
                                    <body>
                                            <h6 id="TextoSenha"> <img src="/static/logos/logo_minfin.png"/></h6>
                                            <h6 id="TextoSenhaCR">{message_cabesalho_loja}</h6>
                                            <h6 id="TextoSenhaCR">{message_cabesalho_servico}</h6>
                                            <h6 id="TextoSenha">Data: {data}</h6>
                                            <h6 id="TextoSenha">Hora de Entrada: {hora_ped}</h6>
                                            <h1 id="TextoSenhaSenha"><b>{servico} {nr_senha}</b></h1>
                                            <h6 id="TextoSenha">Pessoas na Fila: {pess_fila}</h6>
                                            <h6 id="TextoSenha">Tempo estimado: {est_atend}</h6>
                                            <h6 id="TextoSenha">{message_rodape_servico}</h6>
                                            <h6 id="TextoSenha">{message_rodape_loja}</h6>
                        """.format(message_cabesalho_loja=senhaConfigLoja[0], message_cabesalho_servico=senhaConfigServico[0],data=data, hora_ped=hora, servico=letra, nr_senha=nr_senha,pess_fila=pess_fila, est_atend=est_atend, message_rodape_servico=senhaConfigServico[1], message_rodape_loja=senhaConfigLoja[1])
                        output+="""
                                        <script src="/static/js/modernizr.js"></script>
                                        <script src="/static/js/jquery.min.js"></script>
                                        <script>
                                                  window.print();
                                                  window.close();
                                        </script>
                                    </body>
                                </html>
                                """
            print("retornando output ------------------------------------  ")
            return str(output)
        except BaseException as e:
            return None