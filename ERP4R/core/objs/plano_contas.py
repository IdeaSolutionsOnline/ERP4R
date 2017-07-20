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
__model_name__ = 'plano_contas.PlanoContas'
#import auth, base_models
from orm import *
from form import *

class PlanoContas(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'plano_contas'
        self.__title__ = 'Plano de Contas'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['codigo','nome']
        self.__list_edit_mode__ = 'inline'
        self.__order_by__ = 'plano_contas.codigo'
        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.codigo = string_field(view_order=1 , name='Código')
        self.nome = string_field(view_order=2 , name='Nome', size=80)
        self.ascendente = choice_field(view_order=3 , name='Ascendente', size=80, model=self.__name__, column='nome', options='model.get_self()')
        self.tipo = combo_field(view_order=4 , name='Tipo', size=60, options=[('acumuladora','Acumuladora'),('dinheiro','Dinheiro'), ('credora','Credora'), ('devedora','Devedora'), ('receitas','Receitas'), ('gastos','Gastos'), ('resultados','Resultados'), ('compras','Compras'),('inventario','Inventário'), ('activos','Activos'), ('impostos','Impostos')])

    def get_self(self):
        return self.get_options()

    # def record_lines(self, key):
    #     #usar esta funcao para que sempre que aceda a este objecto ele decida se vale a pena recarregar ou nao e devolver os resultados filtrados consoante as necessidades, eventualmente por no get de uma vez, heheheh
    #     #dentro desse principio o get é sempre global e eu devo arranjar python ways de order, where, etc.
    #     def get_results():
    #         try:
    #             from my_linha_entrega import LinhaEntrega
    #         except:
    #             from linha_entrega import LinhaEntrega
    #         record_lines = LinhaEntrega(where="entrega = '{entrega}'".format(entrega=key)).get()
    #         return record_lines
    #     return short_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)

    def get_inventario(self):
        def get_results():
            #print ('get_inventario')
            options = []
            #print(1, self)
            opts = self.get(order_by='codigo')
            #print(2)
            for option in opts:
                if option['tipo'] == 'inventario':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            #print(options)
            return options
        return erp_cache.get(key=self.__model_name__ + '_inventario', createfunc=get_results)

    def get_gastos(self):
        def get_results():
            #print ('get_gastos')
            options = []
            opts = self.get(order_by='codigo')
            for option in opts:
                if option['tipo'] == 'gastos':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_gastos', createfunc=get_results)

    def get_receitas(self):
        def get_results():
            #print ('get_receitas')
            options = []
            opts = self.get(order_by='codigo')
            for option in opts:
                if option['tipo'] == 'receitas':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_receitas', createfunc=get_results)

    def get_dinheiro(self):
        def get_results():
            #print ('get_dinheiro')
            options = []
            opts = self.get(order_by='codigo')
            for option in opts:
                if option['tipo'] == 'dinheiro':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_dinheiro', createfunc=get_results)

    def get_devedora(self):
        def get_results():
            #print ('get_devedora')
            options = []
            opts = self.get(order_by='codigo')
            for option in opts:
                if option['tipo'] == 'devedora':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_devedora', createfunc=get_results)

    def get_credora(self):
        def get_results():
            #print ('get_credora')
            options = []
            opts = self.get(order_by='codigo')
            for option in opts:
                if option['tipo'] == 'credora':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_credora', createfunc=get_results)

    def get_compras(self):
        def get_results():
            #print ('get_compras')
            options = []
            opts = self.get(order_by='codigo')
            for option in opts:
                if option['tipo'] == 'compras':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_compras', createfunc=get_results)

    def get_lancamento(self):
        def get_results():
            #print('get_lancamento')
            options = []
            opts = self.get(order_by='codigo')
            #print(opts)
            for option in opts:
                if option['tipo'] != 'acumuladora':
                    options.append((str(option['id']), option['codigo'] + ' - ' + option['nome']))
            #print(options)
            return options
        return erp_cache.get(key=self.__model_name__ + '_lancamento', createfunc=get_results)