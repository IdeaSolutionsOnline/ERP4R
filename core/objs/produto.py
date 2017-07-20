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
__model_name__= 'produto.Produto'
import auth, base_models
from orm import *
from form import *
try:
    from my_familia_produto import FamiliaProduto
except:
    from familia_produto import FamiliaProduto
try:
    from my_plano_contas import PlanoContas
except:
    from plano_contas import PlanoContas
try:
    from my_unidade import Unidade
except:
    from unidade import Unidade

class Produto(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'produto'
        self.__title__= 'Produtos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'produto.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor de Stocks']
            }
        self.__get_options__ = ['nome']

        self.__tabs__ = [('Identificação',['referencia', 'nome', 'pode_vender', 'pode_comprar', 'stock', 'estado', 'preco_custo', 'preco_compra', 'preco_venda', 'iva', 'nao_liq_imposto', 'deducao', 'desconto_maximo', 'unidade_medida_padrao', 'unidade_medida_compra', 'unidade_medida_venda', 'familia', 'tipo']),
        ('Contabilidade',['conta_compras', 'conta_mercadorias', 'conta_gastos', 'conta_receitas'])]

        self.referencia = string_field(view_order = 1, name = 'Referencia', size = 50)
        self.nome = string_field(view_order = 2, name = 'Nome', args = 'required', size = 90)
        self.pode_vender = boolean_field(view_order = 3, name = 'Pode Vender', onlist = False, search = False, size = 40)
        self.pode_comprar = boolean_field(view_order = 4, name = 'Pode Comprar', onlist = False, search = False, size = 40)
        self.stock = function_field(view_order = 5, name = 'Stock', size = 20, sum = True, search = False)
        self.estado = combo_field(view_order = 6, name = 'Estado', default = 'activo', options = [('activo','Activo'), ('cancelado','Cancelado')], size = 50)
        self.preco_custo = currency_field(view_order = 7, name = 'Preço de Custo', onlist = False, args = 'required', search = False, size = 50)
        self.preco_compra = currency_field(view_order = 8, name = 'Preço de Compra', onlist = False, args = 'required', search = False, size = 50)
        self.preco_venda = currency_field(view_order = 9, name = 'P.Venda Padrão', args = 'required', search = False, size = 50)
        self.iva = percent_field(view_order = 10, name = 'Iva', default = to_decimal(15), onlist = False, args = 'required', search = False, size = 50)
        self.nao_liq_imposto = combo_field(view_order = 11, name = 'Motivo Não Liquidação IVA', options = [('A','Bens Lista Anexa'), ('B','Exportação ou operações semilares'), ('C','Outras Insenções')], size = 50)
        self.deducao = combo_field(view_order=12, name='Dedução IVA', args='required', default='0', options=[('0','0%'),('50','50%'),('100','100%')])
        self.desconto_maximo = percent_field(view_order = 13, name ='Desconto Máximo', size = 50)
        self.unidade_medida_padrao = combo_field(view_order = 14, name = 'Uni.Med.Padrão', size = 50, model = 'unidade', args = 'required', onlist = False, search = False, column = 'nome', options = "model.get_opts('Unidade().get_options()')")
        self.unidade_medida_compra = combo_field(view_order = 15, name = 'Uni.Med.Compra', size = 50, model = 'unidade', args = 'required', onlist = False, search = False, column = 'nome', options = "model.get_opts('Unidade().get_options()')")
        self.unidade_medida_venda = combo_field(view_order = 16, name  = 'Uni.Med.Venda', size = 50, args = 'required', model = 'unidade', search = False, column = 'nome', options = "model.get_opts('Unidade().get_options()')")
        self.familia = combo_field(view_order = 17, name = 'Familia', size = 80, model = 'familia_produto', args = 'required', onlist = False, column = 'nome', options = "model.get_opts('FamiliaProduto().get_options_activo()')")
        self.tipo = combo_field(view_order = 18, name = 'Tipo', size = 50, onlist = False, args = 'required', search = False, options = [('armazenavel','Armazenavel'), ('consumivel','Consumivel'), ('servico','Serviço'),('produzido','Produzido'),('imobilizado','Imobilizado')])
        self.conta_compras = choice_field(view_order = 19, name = 'Conta Compras', size = 80, model = 'plano_contas', onlist = False, search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_inventario()')")
        self.conta_mercadorias = choice_field(view_order = 20, name = 'Conta Mercadorias', size = 80, model = 'plano_contas', onlist = False, search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_inventario()')")
        self.conta_gastos = choice_field(view_order = 21, name = 'Conta Gastos', size = 80, model = 'plano_contas', onlist = False, search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_gastos()')")
        self.conta_receitas = choice_field(view_order = 22, name = 'Conta Receitas', size = 80, model = 'plano_contas', onlist = False, search = False, column = 'nome', options = "model.get_opts('PlanoContas().get_receitas()')")


    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

#   Esta função prevê mostrar o stock actual
#   def get_options_sellable(self):
#       def get_results():
#           sql = """
#               SELECT p.id, p.nome, p.preco_venda,sum(ls.quant_entrada) as quant_entrada, sum(quant_saida) as quant_saida
#               FROM produto AS p
#               LEFT JOIN linha_stock AS ls
#               ON ls.produto = p.id
#               LEFT JOIN armazem AS a
#               On a.id = ls.armazem AND a.tipo not in ('Fornecedor','Cliente')
#               WHERE p.pode_vender = True AND p.estado = 'activo'
#               GROUP BY p.id, p.nome
#               ORDER BY p.nome
#           """
#           opts = run_sql(sql)
#           #print (opts)
#           options = []
#           for option in opts:
#               entrada = to_decimal(0)
#               saida = to_decimal(0)
#               if option['quant_entrada']:
#                   entrada = option['quant_entrada']
#               if option['quant_saida']:
#                   saida = option['quant_saida']
#               value = entrada - saida
#               options.append((str(option['id']), '{nome}'.format(nome=option['nome'])))
#               #, str(value), str(option['preco_venda']){0:<55s},{1:>8s},{2:^12s}
#           return options
#       return erp_cache.get(key=self.__model_name__ + '_sellable', createfunc=get_results)

    def get_options_sellable(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['pode_vender'] and option['estado'] == 'activo':
                    options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_sellable', createfunc=get_results)

    def get_options_buyable(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['pode_comprar'] and option['estado'] == 'activo':
                    options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_buyable', createfunc=get_results)

    def get_options_produced(self):
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['tipo'] == 'produzido' and option['estado'] == 'activo':
                    options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_produced', createfunc=get_results)

    def get_accounts(self, produto):
        from familia_produto import FamiliaProduto
        produto_obj = self.get(key=produto)[0]
        conta_compras = produto_obj['conta_compras']
        conta_mercadorias = produto_obj['conta_mercadorias']
        conta_gastos = produto_obj['conta_gastos']
        conta_receitas = produto_obj['conta_receitas']
        familia = FamiliaProduto().get(key=produto_obj['familia'])[0]
        if not conta_compras:
            conta_compras = familia['conta_compras']
        if not conta_mercadorias:
            conta_mercadorias = familia['conta_mercadorias']
        if not conta_gastos:
            conta_gastos = familia['conta_gastos']
        if not conta_receitas:
            conta_receitas = familia['conta_receitas']
        accounts = {'conta_compras':conta_compras, 'conta_mercadorias':conta_mercadorias, 'conta_gastos':conta_gastos, 'conta_receitas':conta_receitas}
        #print ('oi estou em get_accounts ', accounts)
        return accounts

    def get_sale_price(self, produto, terminal, quantidade, unidade, categoria=None):
        #print ('----------------------------- im on get_sale_price')
        #Esta é a unica forma correcta de conseguir o preço para o produto em questão
        #Vai ás listas de preços e verifica se existe preço para as variaveis, e existindo devolve-o
        #Caso contrario cria uma nova entrada na lista de preços para estas variaveis
        #Vai ver se é a unidade padrão, se não for ver a conversão a aplicar e gera a entrada na lista de preços
        from lista_precos import ListaPrecos
        from linha_lista_precos import LinhaListaPrecos
        from unidade import Unidade
        from linha_unidade import LinhaUnidade
        quantidade = to_decimal(quantidade)
        #print ('terminal', terminal)
        lista_precos = ListaPrecos(where="""terminal = '{terminal}' AND estado = 'Confirmado'""".format(terminal=terminal)).get()
        if len(lista_precos) == 0:
            lista_precos = ListaPrecos(nome='A Rever', terminal=terminal, data_inicial=datetime.date.today(), estado='Confirmado',user=bottle.request.session['user']).put()
        else:
            lista_precos = lista_precos[0]['id']
        categoria_str = ''
        if categoria:
            categoria_str = """ AND categoria = '{categoria}'""".format(categoria=categoria)
        linha_lista_precos = LinhaListaPrecos(where="""lista_precos = '{lista_precos}' AND produto='{produto}' AND unidade='{unidade}' {categoria}""".format(lista_precos=lista_precos, produto=produto, unidade=unidade, quantidade=quantidade, categoria=categoria_str)).get()
        sale_price = 0
        if len(linha_lista_precos) == 0:
            produto_obj = Produto().get(key=produto)[0]
            preco = produto_obj['preco_venda']
            unidade_padrao = produto_obj['unidade_medida_padrao']
            if unidade != unidade_padrao:
                formula = LinhaUnidade(where="""unidade='{unidade}' AND para_unidade='{para_unidade}'""".format(unidade=unidade,para_unidade=unidade_padrao)).get()
                if len(formula) != 0:
                    formula = formula[0]['formula']
                    preco = eval(str(preco) + formula)
            linha_lista_precos = LinhaListaPrecos(lista_precos=lista_precos, produto=produto, unidade=unidade, quant_min=0, quant_max=0, preco=preco, categoria = categoria, user=bottle.request.session['user']).put()
            sale_price = preco
        else:
            for linha in linha_lista_precos:
                if linha['quant_max'] == to_decimal(0):
                    linha['quant_max'] = quantidade
                if linha['quant_min'] < quantidade and linha['quant_max'] >= quantidade:
                    sale_price = linha['preco']
        #print ('sale_price', sale_price)
        return sale_price

    def get_cost_value(self, produto):
        #Por enquanto sempre consideramos o calculo do custo médio dado que é o mais aceite a nivel mundial
        #outros são facilmente parameterizados fazendo novas funções
        cost_value = to_decimal(0)
        return cost_value

    def get_stock(self, key):
        # aqui o stock deve calcular todos os produtos e depois enviar um dicionario com todos os produtos de uma vez
        #print('estou em get_stock')
        from linha_stock import LinhaStock
        entradas = to_decimal(0)
        saidas = to_decimal(0)
        record_lines = LinhaStock(where="produto = '{produto}'".format(produto=key)).get()
        #print('record_lines', record_lines)
        from armazem import Armazem
        armazens = Armazem(where="tipo in ('fisico')").get()
        #print('armazens', armazens)
        ids_armazem = []
        for armazem in armazens:
            ids_armazem.append(armazem['id'])
        #print('ids_armazem', ids_armazem)
        if record_lines:
            for line in record_lines:
                if line['armazem'] in ids_armazem:
                    #se for de armazem cliente ou fornecedor não conta aqui
                    entradas += to_decimal(line['quant_entrada'])
                    saidas += to_decimal(line['quant_saida'])
        value = entradas - saidas
        return round(value,0)
