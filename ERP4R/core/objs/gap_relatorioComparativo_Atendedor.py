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
__model_name__ = 'gap_relatorioComparativo_Atendedor.GAPRelatorioComparativoAtendedor'
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

class GAPRelatorioComparativoAtendedor(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_relatorioComparativo_Atendedor'
        self.__title__ ='Relatorio Comparativo Atendedor'
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
        self.nome_primeiroAtendedor = combo_field(view_order=1, name='Nome Atendedor 1', size=50, args='required', model='users', column='nome', options="model.get_opts('Users().get_atendedor()')")
        self.nome_segundoAtendedor = combo_field(view_order=2, name='Nome Atendedor 2', size=50, args='required', model='users', column='nome', options="model.get_opts('Users().get_atendedor()')")
        self.servico = combo_field(view_order=3, name='Nome Serviço', size=50, model='gap_servico', column='nome', options="model.get_opts('GAPServico().get_options()')")
        self.loja = combo_field(view_order=4, name='Nome Loja', size=50, args='required', model='terminal', column='nome', options="model.get_opts('Terminal().get_options()')")
        self.data_inicial = date_field(view_order=5, args = 'required' , name='Data Inicial')
        self.data_final = date_field(view_order=6, args = 'required', name='Data Final', default=datetime.date.today())
        self.estado = info_field(view_order=7, name='Estado', hidden=True, default='Activo')

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)


    def prepare_data(self):
        primeiroAtendedorId = bottle.request.forms.get('nome_primeiroAtendedor')
        segundoAtendedorId = bottle.request.forms.get('nome_segundoAtendedor')
        servicoId = bottle.request.forms.get('servico')
        data_inicio = bottle.request.forms.get('data_inicial')
        data_fim = bottle.request.forms.get('data_final')
        lojaId = bottle.request.forms.get('loja')
        if not data_inicio or not data_fim:
            return 'sem_data'
        else:
            if not primeiroAtendedorId or not segundoAtendedorId:
                return 'sem_nome'
            elif not lojaId:
                return 'sem_loja'
            else:
                record = {}
                import erp_config as ec
                from gap_timeAtendimento import GAPTimeAtendimento
                clientesAtendidos1 = None
                clientesAtendidos2 = None
                primeiroAtendedorinfo = Users().get_userProfile(userId=primeiroAtendedorId)
                segundoAtendedorinfo = Users().get_userProfile(userId=segundoAtendedorId)
                terminalinfo = Terminal().get_terminalInfo(terminalId=lojaId)
                currentterminalinfo = Terminal().get_terminalInfoByname(terminalname=ec.terminal_name)
                terminalname = str(terminalinfo).split(";")
                primeiroAtendedorinfo = str(primeiroAtendedorinfo).split(";")
                segundoAtendedorinfo = str(segundoAtendedorinfo).split(";")
                if not servicoId:
                    servicos = GAPServico().get_servico_nome()
                    servicos = ''.join(servicos)
                    record['servicos'] = servicos
                    servicos= str(servicos).split(";")
                    for servico in servicos:
                        if clientesAtendidos1 == None:
                                clientesAtendidos1 = GAPTimeAtendimento().get_clienteAtendido(nome=primeiroAtendedorinfo[0], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                                clientesAtendidos2 = GAPTimeAtendimento().get_clienteAtendido(nome=segundoAtendedorinfo[0], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                        else:
                                clientesAtendidos1=str(clientesAtendidos1)+";"+str(GAPTimeAtendimento().get_clienteAtendido(nome=primeiroAtendedorinfo[0], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                                clientesAtendidos2=str(clientesAtendidos2)+";"+str(GAPTimeAtendimento().get_clienteAtendido(nome=segundoAtendedorinfo[0], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico))
                else:
                    servico = GAPServico().get_letra_servico(keyservico=servicoId)
                    record['servicos'] = servico
                    record['singleservice'] = 'True'
                    clientesAtendidos1 = GAPTimeAtendimento().get_clienteAtendido(nome=primeiroAtendedorinfo[0], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                    clientesAtendidos2 = GAPTimeAtendimento().get_clienteAtendido(nome=segundoAtendedorinfo[0], dataInicio=data_inicio, dataFim=data_fim, loja=terminalname[0], servico=servico)
                record['title'] = 'Relatorio Comparativo Atendedor'
                record['enterprise'] = ec.enterprise
                record['targets'] = 'Atendedores'
                record['compare_targets'] = 'True'
                record['targets_names'] = str(primeiroAtendedorinfo[0])+";"+str(segundoAtendedorinfo[0])
                record['targets_contents'] = "Atendidos por "+primeiroAtendedorinfo[0]+";"+"Atendidos por "+segundoAtendedorinfo[0]
                record['text_msg'] = "Gráfico comparativo do numero de clientes Atendidos por "+primeiroAtendedorinfo[0]+"  -  "+segundoAtendedorinfo[0]+":"
                if (clientesAtendidos1!=None):
                      record['targets_values'] = str(clientesAtendidos1)+"-"+str(clientesAtendidos2)
                record['data'] = str(data_inicio)+";"+str(data_fim)
                record['loja'] = currentterminalinfo
                return record

    def Imprimir(self, key, window_id):
        template = 'gap_relatorioGrafico'
        record = self.prepare_data()
        if record == 'sem_data':
            return error_message('Por favor introduza uma data de inicio e fim')
        elif record == 'sem_nome':
            return error_message('Por favor escolha um nome de Atendedor')
        elif record == 'sem_loja':
            return error_message('Por favor escolha o nome da Loja')
        else:
            return Report(record=record, report_template=template).show()