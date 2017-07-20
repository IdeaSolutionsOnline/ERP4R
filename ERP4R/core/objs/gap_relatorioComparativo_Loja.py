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
__model_name__ = 'gap_relatorioComparativo_Loja.GAPRelatorioComparativoLoja'
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

class GAPRelatorioComparativoLoja(Model, View):
    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_relatorioComparativo_Loja'
        self.__title__ ='Relatorio Comparativo Loja'
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
        self.nome_primeiraLoja = combo_field(view_order=1, name='Nome Loja 1', size=50, args='required', model='terminal', column='nome', options="model.get_opts('Terminal().get_options()')")
        self.nome_segundaLoja = combo_field(view_order=2, name='Nome Loja 2', size=50, args='required', model='terminal', column='nome', options="model.get_opts('Terminal().get_options()')")
        self.servico = combo_field(view_order=3, name='Nome Serviço', size=50, model='gap_servico', column='nome', options="model.get_opts('GAPServico().get_options()')")
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
        primeiraLojaId = bottle.request.forms.get('nome_primeiraLoja')
        segundaLojaId = bottle.request.forms.get('nome_segundaLoja')
        data_inicio = bottle.request.forms.get('data_inicial')
        data_fim = bottle.request.forms.get('data_final')
        servicoId = bottle.request.forms.get('servico')
        if not data_inicio or not data_fim:
            return 'sem_data'
        else:
            if not primeiraLojaId or not segundaLojaId:
                return 'sem_nome'
            else:
                record = {}
                import erp_config as ec
                from gap_timeAtendimento import GAPTimeAtendimento
                primeiraLojainfo = Terminal().get_terminalInfo(terminalId=primeiraLojaId)
                segundaLojainfo = Terminal().get_terminalInfo(terminalId=segundaLojaId)
                currentterminalinfo = Terminal().get_terminalInfoByname(terminalname=ec.terminal_name)
                terminalname = str(currentterminalinfo).split(";")
                primeiraLojainfo = str(primeiraLojainfo).split(";")
                segundaLojainfo = str(segundaLojainfo).split(";")
                clientesAtendidos1 = None
                clientesAtendidos2 = None
                clientesDesistiram1 = None
                clientesDesistiram2 = None
                if not servicoId:
                    servicos = GAPServico().get_servico_nome()
                    servicos = ''.join(servicos)
                    record['servicos'] = servicos
                    servicos= str(servicos).split(";")
                    for servico in servicos:
                        if clientesAtendidos1 == None:
                                clientesAtendidos1 = GAPTimeAtendimento().get_clienteAtendidoByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=primeiraLojainfo[0], servico=servico)
                                clientesAtendidos2 = GAPTimeAtendimento().get_clienteAtendidoByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=segundaLojainfo[0], servico=servico)
                                clientesDesistiram1=GAPTimeAtendimento().get_clienteDesistiramByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=primeiraLojainfo[0], servico=servico)
                                clientesDesistiram2=GAPTimeAtendimento().get_clienteDesistiramByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=segundaLojainfo[0], servico=servico)
                        else:
                                clientesAtendidos1=str(clientesAtendidos1)+";"+str(GAPTimeAtendimento().get_clienteAtendidoByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=primeiraLojainfo[0], servico=servico))
                                clientesAtendidos2=str(clientesAtendidos2)+";"+str(GAPTimeAtendimento().get_clienteAtendidoByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=segundaLojainfo[0], servico=servico))
                                clientesDesistiram1=str(clientesDesistiram1)+";"+str(GAPTimeAtendimento().get_clienteDesistiramByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=primeiraLojainfo[0], servico=servico))
                                clientesDesistiram2=str(clientesDesistiram2)+";"+str(GAPTimeAtendimento().get_clienteDesistiramByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=segundaLojainfo[0], servico=servico))
                else:
                    servico = GAPServico().get_letra_servico(keyservico=servicoId)
                    record['servicos'] = servico
                    record['singleservice'] = 'True'
                    clientesAtendidos1 = GAPTimeAtendimento().get_clienteAtendidoByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=primeiraLojainfo[0], servico=servico)
                    clientesAtendidos2 = GAPTimeAtendimento().get_clienteAtendidoByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=segundaLojainfo[0], servico=servico)
                    clientesDesistiram1=GAPTimeAtendimento().get_clienteDesistiramByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=primeiraLojainfo[0], servico=servico)
                    clientesDesistiram2=GAPTimeAtendimento().get_clienteDesistiramByLoja(dataInicio=data_inicio, dataFim=data_fim, loja=segundaLojainfo[0], servico=servico)
                record['title'] = 'Relatorio Comparativo Loja'
                record['enterprise'] = ec.enterprise
                record['targets'] = 'Lojas'
                record['targets_names'] = str(primeiraLojainfo[0])+";"+str(segundaLojainfo[0])
                record['targets_contents'] = "Atendidos por  "+primeiraLojainfo[0]+";Desistiram por  "+primeiraLojainfo[0]+";"+"Atendidos por  "+segundaLojainfo[0]+";Desistiram por "+segundaLojainfo[0]
                record['compare_targets'] = 'True'
                record['text_msg'] = "Gráfico comparativo do numero de clientes Atendidos e Desistentes nas Lojas "+primeiraLojainfo[0]+"  -  "+segundaLojainfo[0]
                if (clientesAtendidos1!=None):
                      record['targets_values'] = str(clientesAtendidos1)+"-"+str(clientesDesistiram1)+"-"+str(clientesAtendidos2)+"-"+str(clientesDesistiram2)
                record['data'] = str(data_inicio)+";"+str(data_fim)
                record['loja'] = currentterminalinfo
                return record

    def Imprimir(self, key, window_id):
        template = 'gap_relatorioGrafico'
        record = self.prepare_data()
        if record == 'sem_data':
            return error_message('Por favor introduza uma data de inicio e fim')
        elif record == 'sem_nome':
            return error_message('Por favor escolha as duas lojas a se comparar')
        else:
            return Report(record=record, report_template=template).show()