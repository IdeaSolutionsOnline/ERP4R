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
__model_name__ = 'leitura.Leitura'
import auth, base_models
from orm import *
from form import *
try:
    from my_contrato import Contrato
except:
    from contrato import Contrato
try:
    from my_contador_contrato import ContadorContrato
except:
    from contador_contrato import ContadorContrato
try:
    from my_linha_leitura import LinhaLeitura
except:
    from linha_leitura import LinhaLeitura
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro
try:
    from my_zona import Zona
except:
    from zona import Zona

class Leitura(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'leitura'
        self.__title__= 'Folhas de Leitura'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(leitura.numero) DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Imprimir', 'Confirmar','Gera Leituras', 'Gera Estimativas'], 'Confirmado':['Imprimir','Gera Facturas','Cancelar'], 'Facturado':[], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Vendedor'],
            'Facturar':['Vendedor'],
            'Gera Leituras':['Vendedor'],
            'Gera Estimativas':['Vendedor'],
            'Gera Facturas':['Vendedor'],
            'Rascunho':['Gestor'],
            'Imprimir':['All'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado','Cancelado','Facturado'])
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Vendedor'],
            'create':['Vendedor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']

        self.numero = info_field(view_order=1, name ='Número')
        self.zona = choice_field(view_order=2, name ='Zona de Distribuição', args='required', size=50, model='zona', column='nome', options='model.get_zonas()')
        self.leitor = combo_field(view_order=3, name ='Leitor', args='required', size=50, column='nome', options='model.get_terceiros()')
        self.data = date_field(view_order=4, name ='Data', default=datetime.date.today())
        self.tipo = combo_field(view_order=5, name ='Tipo', args='required', size=50, options=[('estimativa','Estimativa'), ('presencial','Presencial'), ('declarativa','Declarativa')])
        self.estado = info_field(view_order=6, name ='Estado', default='Rascunho')
        self.linha_leitura = list_field(view_order=7, name ='Linhas de Leitura', condition="leitura='{id}'", model_name='linha_leitura.LinhaLeitura', list_edit_mode='inline', onlist = False)

    def get_terceiros(self):
        return Terceiro().get_funcionarios()

    def get_zonas(self):
        return Zona().get_options()

    def Imprimir(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        template = 'leitura'
        record = get_records_to_print(key=key, model=self)
        #print (record)
        return Report(record=record, report_template=template).show()

    def Gera_Leituras(self, key, window_id):
        """
        Vai buscar todos os contratos da zona escolhida e cria uma linha de leitura por cada contrato com a leitura anterior correcta
        """
        self.kargs = get_model_record(model=self, key=key)
        zona = self.kargs['zona']
        #transformar isto num select
        contadores = ContadorContrato(where="estado='activo'").get()
        contratos = Contrato(where="zona={zona}".format(zona=zona)).get()
        if len(contratos) == 0:
            contratos = []
        for contract in contratos:
            for c in contadores:
                if c['contrato'] == contract['id']:
                    contador = c['contador']
            LinhaLeitura(contador=contador, leitura=self.kargs['id'], user=self.kargs['user']).put()
        return form_edit(window_id=window_id).show()

    def Gera_Estimativas(self, key, window_id):
        """
        Vai buscar todos os contratos da zona escolhida e cria uma linha de leitura por cada contrato que não tenha leituras nos 20 dias anteriores a data selecionada é obrigatório as folhas de leitura estarem confirmadas ou facturadas mas nunca em rascunho
        mesmo que o tipo não esteja como estimativa vai ficar!
        """
        self.kargs = get_model_record(model=self, key=key)
        zona = self.kargs['zona']
        #vai buscar as folhas de leitura do mesmo periodo (20 dias antes) nos estados confirmado ou facturado
        end_date = datetime.datetime.strptime(self.kargs['data'], '%Y-%m-%d')
        start_date = end_date - datetime.timedelta(days=20)#depois pensar numa melhor alternativa
        start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        datas = generate_dates(start_date, self.kargs['data'])
        sql = """
        SELECT * FROM leitura WHERE id!='{key}'' AND zona='{zona}'' AND estado in ('Confirmado', 'Facturado')AND data {datas}
        """.format(datas=to_tuple(datas), zona=zona, key=key)
        leituras = run_sql(sql)
        lista_leituras = []
        if leituras:
            for leitura in leituras:
                lista_leituras.append(leitura['id'])
            sql = """
            SELECT * FROM linha_leitura WHERE leitura {leituras}
            """.format(leituras=to_tuple(lista_leituras))
            linhas_leitura = run_sql(sql)
            #aqui tenho as linhas de leitura que ja foram cofirmadas ou facturadas e por isso não podem constar da estimativa vou agora buscar os contratos activos (o contador tambem tem que estar activo pois pode ter varios contadores mas so um deve estar activo) desta zona ter em conta que mesmo os suspensos deverão ser facturados só nas taxas mas todos os outros não. aqui termos depois de ter em conta as datas do contrato e de activacao do contador.
            contadores_com_leitura = []
            for linha in linhas_leitura:
                contadores_com_leitura.append(linha['contador'])
            sql = """
            SELECT * FROM contrato AS c
JOIN contador_contrato AS cc
ON c.id = cc.contrato
WHERE c.estado IN ('Activo','Suspenso') AND cc.estado = 'activo'
AND zona = '{zona}'
            """.format(zona=zona)
            contratos = run_sql(sql)
            contadores_para_estimativa = []
            for contrato in contratos:
                if contrato['contador'] not in contadores_com_leitura:
                    contadores_para_estimativa.append(contrato['contador'])
            #já tenho a listagem dos contadores em situação de estimativa falta agora calcular a médias das ultimas 5 leituras, se não tiver vai a zero mesmo para poder cobrar pelo menos as taxas. este select só devolve os contadores que já tiverem alguma leitura por isso os que não estiverem cá serão facturados a zero
            start_date = end_date - datetime.timedelta(days=150)
            start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
            datas = generate_dates(start_date, self.kargs['data'])
            sql = """
            SELECT contador, avg(leitura_actual) as leitura_actual FROM linha_leitura as ll
JOIN leitura as l
ON l.id = ll.leitura
WHERE 
estado in ('Confirmado','Facturado')
AND data {datas}
AND contador {contadores}
GROUP BY contador
            """.format(contadores=to_tuple(contadores_para_estimativa), datas=to_tuple(datas))
            estimativas = run_sql(sql)
            #aqui depois testar melhor neste momento dá lista vaziz o que é suposto por isso não vou testar com 100% de certeza
            estimativas_final = {}
            for estimativa in estimativas:
                estimativas_final[estimativa['contador']] = estimativa['leitura_actual']
            for contador in contadores_para_estimativa:
                if contador not in estimativas_final:
                    estimativas_final[contador] = 0
            for contador in estimativas_final:
                leitura_actual = estimativas_final[contador]
                LinhaLeitura(contador=contador, leitura_actual=leitura_actual, leitura=self.kargs['id'], user=self.kargs['user']).put()
        else:
            return error_message('Ainda não tem nenhuma folha de leitura confirmada ou facturada neste periodo!!!')
        return form_edit(window_id = window_id).show()

    def Gera_Facturas(self, key, window_id):
        """
        Gera uma factura por cada linha de leitura
        """
        try:
            from my_factura_cli import FacturaCliente
        except:
            from factura_cli import FacturaCliente
        try:
            from my_linha_factura_cli import LinhaFacturaCliente
        except:
            from linha_factura_cli import LinhaFacturaCliente
        try:
            from my_produto import Produto
        except:
            from produto import Produto
        self.kargs = get_model_record(model=self, key=key)
        sql = """
            SELECT terceiro.id AS cliente, contador_contrato.contador AS contador, contrato.tipo 
            AS tipo_contrato FROM terceiro 
            JOIN contrato
            ON contrato.cliente = terceiro.id
            JOIN contador_contrato
            ON contador_contrato.contrato = contrato.id
            WHERE contador_contrato.estado = 'activo'
            """
        lista_clientes = run_sql(sql)
        clientes = {}
        tipos_contrato = {}
        for c in lista_clientes:
            clientes[c['contador']] = c['cliente']
            tipos_contrato[c['contador']] = c['tipo_contrato']
        sql = """
        SELECT * from produto where nome in ('Impresso', 'Taxa de Manutenção', 'Água Canalizada')
        """
        lista_produtos = run_sql(sql)
        produtos = {}
        for p in lista_produtos:
            produtos[p['nome']] = {'id':p['id'], 'unidade':p['unidade_medida_venda'], 'iva':p['iva'], 'preco_venda':p['preco_venda']}
        linhas_leitura = LinhaLeitura(where="""leitura={leitura}""".format(leitura=key)).get()[1]
        for linha in linhas_leitura:
            sql = """
                SELECT max(linha_leitura.leitura_actual) as leitura_actual FROM linha_leitura 
                JOIN leitura
                ON leitura.id = linha_leitura.leitura
                WHERE leitura.data < (SELECT data FROM leitura WHERE id = '{leitura}') 
                AND leitura.zona = (SELECT zona FROM leitura WHERE id = '{leitura}')
                AND linha_leitura.contador = {contador}""".format(leitura = linha['leitura'], contador = linha['contador'])
            leitura_anterior = run_sql(sql)
            if leitura_anterior and leitura_anterior[0]['leitura_actual'] != None:
                leitura_anterior = leitura_anterior[0]['leitura_actual']
            else:
                leitura_anterior = 0
            prod1 = produtos['Impresso']
            prod2 = produtos['Taxa de Manutenção']
            #aqui nos termos da politica de escalões devo cobrar o correspondente a cada escalao
            #ou seja:
            #4 M3 a 220, 4 a 250 3 o resto a 350
            prod3 = produtos['Água Canalizada']
            tipo = tipos_contrato[linha['contador']]
            quantidade = linha['leitura_actual'] - leitura_anterior
            precos = Produto().get_sale_prices_escaloes(produto = prod3['id'], quantidade = quantidade, unidade = prod3['unidade'], categoria = tipo, terminal = get_terminal(bottle.request.session['terminal']))
            #print (precos)
            residual = to_decimal(prod1['preco_venda']) + to_decimal(prod2['preco_venda'])
            for preco in precos:
                residual += to_decimal(precos[preco][0]) * to_decimal(precos[preco][1])
            numero_factura = base_models.Sequence().get_sequence('factura_cli')
            factura = FacturaCliente(estado='Rascunho', residual=residual, user=self.kargs['user'], data=self.kargs['data'], numero=numero_factura, cliente=clientes[linha['contador']], zona=self.kargs['zona'], leitura=self.kargs['id'], vendedor=self.kargs['user'], contador=linha['contador'], leitura_actual=linha['leitura_actual'], leitura_anterior=leitura_anterior).put()
            # aqui depois modificar o produto para que eu diga que produtos facturar, por enquanto fica hardcoded
            LinhaFacturaCliente(factura_cli=factura, produto=prod1['id'], descricao='', quantidade=1, unidade=prod1['unidade'], valor_unitario=prod1['preco_venda'], desconto=0, iva=prod1['iva'], valor_total=prod1['preco_venda'], user=self.kargs['user']).put()
            LinhaFacturaCliente(factura_cli=factura, produto=prod2['id'], descricao='', quantidade=1, unidade=prod2['unidade'], valor_unitario=prod2['preco_venda'], desconto=0, iva=prod2['iva'], valor_total=prod2['preco_venda'], user=self.kargs['user']).put()
            for preco in precos:
                total = to_decimal(precos[preco][0]) * to_decimal(precos[preco][1])
                LinhaFacturaCliente(factura_cli=factura, produto=prod3['id'], descricao=preco, quantidade=to_decimal(precos[preco][0]), unidade=prod3['unidade'], valor_unitario=to_decimal(precos[preco][1]), desconto=0, iva=prod3['iva'], valor_total=total, user=self.kargs['user']).put()
            LinhaLeitura(factura=factura, user=self.kargs['user'], id=linha['id']).put()
        self.kargs['estado'] = 'Facturado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Confirmar(self, key, window_id):
        """
        Alem de mudar de estado também ilimina todos os registos de linha de leitura sem leitura_actual
        se for estimativa pode emitir facturas sem consumo só com as taxas
        """
        self.kargs = get_model_record(model=self, key=key)
        #estimativas podem ser a zero
        if self.kargs['tipo'] != 'estimativa':
            LinhaLeitura(where="""leitura={leitura} AND (leitura_actual = 0.0 OR leitura_actual IS NULL)""".format(leitura=key)).delete()
        if not self.kargs['numero']:
            self.kargs['numero'] = base_models.Sequence().get_sequence('leitura')
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id = window_id).show()
