# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__= 'familia_produto.FamiliaProduto'
import auth, base_models
from orm import *
from form import *
try:
    from my_armazem import Armazem
except:
    from armazem import Armazem
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas

class FamiliaProduto(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'familia_produto'
        self.__title__= 'Familias de Produtos'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['nome']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'familia_produto.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.nome = string_field(view_order=1, name ='Nome', size=60)
        self.ascendente = combo_field(view_order=2, name ='Ascendente', size=65, model='familia_produto', column='nome', options="model.get_opts('self.get_options()')")
        self.armazem_compras = combo_field(view_order=3, name ='Armazem Compras', args='required', size=65, model='armazem', column='nome', options="model.get_opts('Armazem().get_options()')")
        self.armazem_vendas = combo_field(view_order=4, name ='Armazem Vendas', args='required', size=65, model='armazem', column='nome', options="model.get_opts('Armazem().get_options()')")
        self.conta_compras = choice_field(view_order=5, name ='Conta Compras', size=80, onlist=False, search=False, model='plano_contas', column='codigo nome', options="model.get_opts('PlanoContas().get_inventario()')")
        self.conta_mercadorias = choice_field(view_order=6, name ='Conta Mercadorias', size=80, onlist=False, search=False, model='plano_contas', column='codigo nome', options="model.get_opts('PlanoContas().get_inventario()')")
        self.conta_gastos = choice_field(view_order=7, name ='Conta Gastos', size=80, onlist=False, search=False, model='plano_contas', column='codigo nome', options="model.get_opts('PlanoContas().get_gastos()')")
        self.conta_receitas = choice_field(view_order=8, name ='Conta Receitas', size=80, onlist=False, search=False, model='plano_contas', column='cofigo nome', options="model.get_opts('PlanoContas().get_receitas()')")
        self.desconto_maximo = percent_field(view_order=9, name ='Desconto Máximo')
        self.estado = combo_field(view_order=10, name ='Estado', args='required', size=40, options=[('activo','Activo'), ('cancelado','Cancelado'), ('acumulador','Acumulador')], default='activo')

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções 
        get_options deste modelo quando chamadas a partir de um outro! 
        """
        return eval(get_str)


    def get_options_activo(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['estado'] == 'activo':
                    options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_activo', createfunc=get_results)