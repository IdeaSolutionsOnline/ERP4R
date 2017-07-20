# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVtek dev"
__status__ = "Development"
__model_name__ = 'gap_relatorioIndividual.GAPRelatorioIndividual'
import auth, base_models
from orm import *
from form import *
try:
    from my_users import Users
except:
    from users import Users
try:
    from my_terminal import Terminal
except:
    from terminal import Terminal
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPRelatorioIndividual(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_relatorioIndividual'
        self.__title__ ='Relatorio Atendedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__db_mode__ = 'None'
        self.__workflow__ = (
            'estado', {'Activo':['Imprimir']}
            )
        self.__workflow_auth__ = {
            'Imprimir':['All'],
            'Exportar':['All'],
            'full_access':['Gestor de Atendimento']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = combo_field(view_order=1, name='Nome Atendedor', size=50, model='users', column='nome', options="model.get_opts('Users().get_atendedor()')")
        self.servico = combo_field(view_order=2, name='Nome Serviço', size=50, model='gap_servico', column='nome', options="model.get_opts('GAPServico().get_options()')")
        self.loja = combo_field(view_order=3, name='Nome Loja', size=50, args='required', model='terminal', column='nome', options="model.get_opts('Terminal().get_options()')")
        self.data_inicial = date_field(view_order=4, args = 'required' , name='Data Inicial')
        self.data_final = date_field(view_order=5, args = 'required', name='Data Final', default=datetime.date.today())
        self.estado = info_field(view_order=6, name='Estado', hidden=True, default='Activo')

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)


    def prepare_data(self):
        data_inicio = bottle.request.forms.get('data_inicial')
        data_fim = bottle.request.forms.get('data_final')
        servicoId = bottle.request.forms.get('servico')
        userId = bottle.request.forms.get('nome')
        lojaId = bottle.request.forms.get('loja')
        if not data_inicio or not data_fim:
            return 'sem_data'
        elif not lojaId:
            return 'sem_loja'
        else:
            record = {}
            import erp_config as ec
            from gap_timeAtendimento import GAPTimeAtendimento
            terminalinfo = Terminal().get_terminalInfo(terminalId=lojaId)
            terminalname = str(terminalinfo).split(";")
            nomeAtendedor = None
            clientesAtendidos = None
            tempo_medio = None
            tempo_maximo = None
            tempo_minimo = None
            if  userId:
                userinfo = Users().get_userProfile(userId=userId)
                record['singleatendedor'] = 'True'
                if userinfo != None:
                    record['atendedor'] = userinfo
                    userinfo = str(userinfo).split(";")
                    nomeAtendedor = userinfo[0]
                if not servicoId:
                    servicos = GAPServico().get_servico_nome()
                    servicos = ''.join(servicos)
                    record['servicos'] = servicos
                    servicos= str(servicos).split(";")
                    for servico in servicos:
                        if clientesAtendidos == None:
                                clientesAtendidos=GAPTimeAtendimento().get_clienteAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_medio=GAPTimeAtendimento().get_mediaTempoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_maximo=GAPTimeAtendimento().get_tempoMaximoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_minimo=GAPTimeAtendimento().get_tempoMinimoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                        else:
                                clientesAtendidos=str(clientesAtendidos)+";"+str(GAPTimeAtendimento().get_clienteAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_medio=str(tempo_medio)+";"+str(GAPTimeAtendimento().get_mediaTempoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_maximo=str(tempo_maximo)+";"+str(GAPTimeAtendimento().get_tempoMaximoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_minimo=str(tempo_minimo)+";"+str(GAPTimeAtendimento().get_tempoMinimoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                else:
                    servico = GAPServico().get_letra_servico(keyservico=servicoId)
                    record['servicos'] = servico
                    record['singleservice'] = 'True'
                    clientesAtendidos=GAPTimeAtendimento().get_clienteAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                    tempo_medio=GAPTimeAtendimento().get_mediaTempoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                    tempo_maximo=GAPTimeAtendimento().get_tempoMaximoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                    tempo_minimo=GAPTimeAtendimento().get_tempoMinimoAtendido(nome=nomeAtendedor, dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                record['clientes_atendidos'] = clientesAtendidos
                record['text_msg'] = "Numero de clientes Atendidos por "+nomeAtendedor+":"
                record['tempo_medio_atendimento'] = tempo_medio
                record['tempo_maximo_atendimento'] = tempo_maximo
                record['tempo_minimo_atendimento'] = tempo_minimo
                record['enterprise'] = ec.enterprise
                record['data'] = str(data_inicio)+";"+str(data_fim)
                record['loja'] = terminalinfo
            else:
                users = Users().get_atendedoresLoja(lojaid=lojaId)
                user_content = ''.join(users)
                record['atendedor'] = user_content
                user_content = str(user_content).split(";")
                if not servicoId:
                    servicos = GAPServico().get_servico_nome()
                    servicos = ''.join(servicos)
                    record['servicos'] = servicos
                    servicos= str(servicos).split(";")
                    for servico in servicos:
                        count = 0
                        for i in range(0,len(user_content)):
                            if clientesAtendidos == None:
                                clientesAtendidos=GAPTimeAtendimento().get_clienteAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_medio=GAPTimeAtendimento().get_mediaTempoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_maximo=GAPTimeAtendimento().get_tempoMaximoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_minimo=GAPTimeAtendimento().get_tempoMinimoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                            else:
                                clientesAtendidos=str(clientesAtendidos)+";"+str(GAPTimeAtendimento().get_clienteAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_medio=str(tempo_medio)+";"+str(GAPTimeAtendimento().get_mediaTempoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_maximo=str(tempo_maximo)+";"+str(GAPTimeAtendimento().get_tempoMaximoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_minimo=str(tempo_minimo)+";"+str(GAPTimeAtendimento().get_tempoMinimoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                            count+=1
                else:
                    servico = GAPServico().get_letra_servico(keyservico=servicoId)
                    record['servicos'] = servico
                    record['singleservice'] = 'True'
                    count = 0
                    for i in range(0,len(user_content)):
                        if clientesAtendidos == None:
                                clientesAtendidos=GAPTimeAtendimento().get_clienteAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_medio=GAPTimeAtendimento().get_mediaTempoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_maximo=GAPTimeAtendimento().get_tempoMaximoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                tempo_minimo=GAPTimeAtendimento().get_tempoMinimoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                        else:
                                clientesAtendidos=str(clientesAtendidos)+";"+str(GAPTimeAtendimento().get_clienteAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_medio=str(tempo_medio)+";"+str(GAPTimeAtendimento().get_mediaTempoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_maximo=str(tempo_maximo)+";"+str(GAPTimeAtendimento().get_tempoMaximoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                tempo_minimo=str(tempo_minimo)+";"+str(GAPTimeAtendimento().get_tempoMinimoAtendido(nome=user_content[count], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                        count+=1
                record['clientes_atendidos'] = clientesAtendidos
                record['tempo_medio_atendimento'] = tempo_medio
                record['tempo_maximo_atendimento'] = tempo_maximo
                record['tempo_minimo_atendimento'] = tempo_minimo
                record['enterprise'] = ec.enterprise
                record['data'] = str(data_inicio)+";"+str(data_fim)
                record['loja'] = terminalinfo
        return record

    def Imprimir(self, key, window_id):
        template = 'gap_relatorioAtendedor'
        record = self.prepare_data()
        if record == 'sem_data':
            return error_message('Por favor introduza uma data de inicio e fim')
        elif record == 'sem_loja':
            return error_message('Por favor escolha o nome da Loja')
        else:
            return Report(record=record, report_template=template).show()