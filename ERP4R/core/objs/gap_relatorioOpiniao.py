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
__model_name__ = 'gap_relatorioOpiniao.GAPRelatorioOpiniao'
import auth, base_models
from orm import *
from form import *
try:
    from my_terminal import Terminal
except:
    from terminal import Terminal
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPRelatorioOpiniao(Model, View):
    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_relatorioOpiniao'
        self.__title__ ='Relatório Opinião'
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
        self.loja = combo_field(view_order=1, name='Nome Loja', size=50, args='required', model='terminal', column='nome', options="model.get_opts('Terminal().get_options()')")
        self.servico = combo_field(view_order=2, name='Nome Serviço', size=50, model='gap_servico', column='nome', options="model.get_opts('GAPServico().get_options()')")
        self.data_inicial = date_field(view_order=3, args = 'required' , name='Data Inicial')
        self.data_final = date_field(view_order=4, args = 'required', name='Data Final', default=datetime.date.today())
        self.estado = info_field(view_order=5, name='Estado', hidden=True, default='Activo')

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
        lojaId = bottle.request.forms.get('loja')
        if not data_inicio or not data_fim:
            return 'sem_data'
        else:
            if not lojaId:
                return 'sem_loja'
            else:
                record = {}
                clientRating = None
                import erp_config as ec
                from gap_opiniao import GAPOpiniao
                from gap_servico import GAPServico
                lojainfo = Terminal().get_terminalInfo(terminalId=lojaId)
                lojainfo = str(lojainfo).split(";")
                terminalinfo = Terminal().get_terminalInfoByname(terminalname=ec.terminal_name)
                currentterminalinfo = Terminal().get_terminalInfoByname(terminalname=ec.terminal_name)
                if not servicoId:
                    servicos = GAPServico().get_servico_nome()
                    servicos = ''.join(servicos)
                    record['servicos'] = servicos
                    servicos= str(servicos).split(";")
                    for servico in servicos:
                        if clientRating == None:
                                clientRating=GAPOpiniao().getRating(servico=servico, loja=lojainfo[0], dataInicio=data_inicio, dataFim=data_fim)
                        else:
                            clientRating=str(clientRating)+";"+str(GAPOpiniao().getRating(servico=servico, loja=lojainfo[0], dataInicio=data_inicio, dataFim=data_fim))
                else:
                    servico = GAPServico().get_letra_servico(keyservico=servicoId)
                    record['servicos'] = servico
                    record['singleservice'] = 'True'
                    clientRating=GAPOpiniao().getRating(servico=servico, loja=lojainfo[0], dataInicio=data_inicio, dataFim=data_fim)
                record['title'] = 'Relatorio Classificação Opinião'
                record['enterprise'] = ec.enterprise
                record['targets'] = 'Opinião'
                record['targets_names'] = str(lojainfo[0])
                record['targets_contents'] = "Classificação"
                record['text_msg'] = "Classificação dos Clientes na Loja  "+lojainfo[0]+":"
                if (clientRating!=None):
                         record['targets_values'] = str(clientRating)
                record['data'] = str(data_inicio)+";"+str(data_fim)
                record['loja'] = currentterminalinfo
                return record

    def Imprimir(self, key, window_id):
        template = 'gap_relatorioGrafico'
        record = self.prepare_data()
        if record == 'sem_data':
            return error_message('Por favor introduza uma data de inicio e fim')
        elif record == 'sem_loja':
            return error_message('Por favor escolha o nome da Loja')
        else:
            return Report(record=record, report_template=template).show()