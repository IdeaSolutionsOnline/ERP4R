# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+ Policia Nacional de Cabo Verde

Gestão de Pbjectos, Bens e Valores, que por algum motivo estão relacionadas com ocorrencias, seja por apreenção, furto ou desapareceimento

"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'objecto.Objecto'
import auth, base_models
from orm import *
from form import *
from terceiro import Terceiro

class Objecto(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'objecto'
        self.__title__ = 'Gestão de Objectos, Bens e Valores'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'objecto.n_serie'
        self.__workflow__ = (
            'estado', {'Rascunho':['Apreender'], 'Apreendida':['Devolver']}
            )#imprimir, gerar queixa, gerar denuncia, imprimir queixa, etc...
            # desaparecido, roubado, etc.
        self.__workflow_auth__ = {
            'Apreender':['Agente'],
            'Devolver':['Agente'],
            'full_access':['Comandante']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Agente'],
            'create':['Agente'],
            'delete':['Chefe'],
            'full_access':['Comandante']
            }
        self.__get_options__ = ['n_serie']

        self.ocorrencia = parent_field(view_order=1, name ='Ocorrencia', args='style:visibility="hidden"', model_name='ocorrencia.Ocorrencia', nolabel=True, onlist=False, column='numero')
        self.tipo = combo_field(view_order=2, name ='Tipo', size=40, onchange='tipo_onchange', options=[('arma','Arma'), ('veiculo','Veiculo'), ('barco_navio','Barco ou Navio'), ('droga','Droga'), ('bebidas','Bebidas'), ('cigarros','Cigarros'), ('dinheiro','Dinheiro'), ('joias','Joias'), ('electronica','Electrónica'), ('vestuario','Vestuário'), ('outros', 'Outros')])
        self.subtipo = combo_field(view_order=3, name ='Sub-Tipo', size=40, model='tipo', options="model.get_subtipo()")
        self.fabricante = string_field(view_order=4, name ='Fabricante', size=50)
        self.origem = string_field(view_order=5, name ='Origem', size=50)
        self.n_serie = string_field(view_order=6, name ='N.Série', size=50)
        self.licenca = string_field(view_order=7, name ='Licença', size=50)
        self.terceiro = choice_field(view_order=8, name ='Proprietario', size=80, model='terceiro', column='nome', options="model.get_terceiros()")
        self.estado = info_field(view_order=9, name='Estado', size=60, default='Rascunho')
        self.localizacao = string_field(view_order=10, name ='Localização', size=50, options=[('esquadra','Esquadra'), ('desconhecida','Desconhecida'), ('proprietario','Proprietário')])
        self.descricao = text_field(view_order=11, name ='Descrição', size=100, colspan=3)

    def get_terceiros(self):
        return Terceiro().get_options()

    def get_subtipo(self):
        request_items = request_items_to_dict()
        #print (request_items)
        if 'tipo' in request_items:
            tipo = request_items['tipo']
        else:
            tipo = 'nao_tem'
        if tipo == 'arma':
            opcoes = [('pedra','Pedra'), ('branca','Branca'), ('fogo_artezanal','Fogo Artezanato (Boca Bedjo)'), ('fogo','Fogo'), ('esplosivo','Esplosivo'), ('outra', 'Outra')]
        elif tipo == 'electronica':
            opcoes = [('telemovel','Telemóvel'), ('tablet','Tablet'), ('relogio','Relógio'), ('portatil','Portátil'), ('computador','Computador'), ('tv','TV'), ('dvd','DVD'), ('maquina_fotografica','Máquina Fotográfica'), ('music_player','Music Player'), ('outro','Outro')]
        else:
            opcoes = []
        return opcoes

    def tipo_onchange(self, record):
        result = record.copy()
        result['subtipo'] = None
        return result

    def Apreender(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Apreendida'
        self.put()
        return form_edit(window_id = window_id).show()

    def Devolver(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Devolvida'
        self.put()
        return form_edit(window_id = window_id).show()
