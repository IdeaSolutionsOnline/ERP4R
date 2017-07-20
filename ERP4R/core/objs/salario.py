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
__model_name__='salario.Salario'
import auth, base_models
from orm import *
from form import *

from linha_recibo_salario import LinhaReciboSalario
from rendimento_funcionario import RendimentoFuncionario
from desconto_funcionario import DescontoFuncionario
from recibo_salario import ReciboSalario
from terceiro import Terceiro
from contrato_funcionario import ContratoFuncionario
from outros_descontos_funcionario import OutrosDescontosFuncionario
from tipo_rendimento import TipoRendimento
from tipo_desconto import TipoDesconto

class Salario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'salario'
        self.__title__= 'Salários'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'salario.periodo'
        self.__workflow__ = (
            'estado', {'Rascunho':['Activar'], 'Activo':['Gerar Recibos', 'Cancelar'], 'Gerado':['Cancelar Recibos','Cancelar','Confirmar Recibos'],'Recibos Cancelado':['Gerar Recibos'],'Recibos Confirmado':['Efectuar Pagamento']}
            )
        self.__workflow_auth__ = {
            'Gerar Recibos':['Contabilista'],
            'Cancelar Recibos':['Contabilista'],
            'Confirmar Recibos':['Contabilista'],
            'Efectuar Pagamento':['Contabilista'],
            'Activar':['Contabilista'],
            'Encerrar':['Contabilista'],
            'Rascunho':['Gestor'],
            'Cancelar':['Gestor'],
            'full_access':['Gestor']
            }

        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Contabilista'],
            'full_access':['Gestor']
            }

        self.__no_edit__ = [('estado', ['Pago'])]

        self.__get_options__ = ['periodo']

        self.__tabs__ = [('Salários',['ano','periodo','mes','para_todos','estado','funcionario_subsidio']),('Outros Descontos',['outros_descontos_funcionario','desconto_funcionario']),('Recibos',['recibo_salario','recibo_subsidio'])]



        self.ano = combo_field(view_order = 1, size=45, name ='Ano', args = 'required', default = datetime.date.today().year, options='model.getAno()')
        
        self.periodo = combo_field(view_order = 2, size=70, name ='Periodo', args = 'required', default = datetime.date.today().strftime("%m"), options='model.getPeriodo()')
        
        #self.mes = combo_field(view_order = 3, size=70, name ='Mês de Referência(em caso de subsidios)', args = 'required', default = datetime.date.today().strftime("%m"), options='model.getMes()')
        
        self.para_todos = boolean_field(view_order = 4, size=50, name = 'Subsídiar Todos Funcionários', default = False)
        
        self.estado = info_field(view_order=5, name='Estado', size=45, default='Rascunho', args='readonly')
        
        self.funcionario_subsidio = list_field(view_order=6, name='Funcionários á Subsidiar',condition="salario='{id}'", model_name='funcionario_subsidio.FuncionarioSubsidio', list_edit_mode='popup', onlist=False)

        self.outros_descontos_funcionario = list_field(view_order=7, condition="salario='{id}'", model_name='outros_descontos_funcionario.OutrosDescontosFuncionario', list_edit_mode='inline', onlist=False, name='Outros Descontos (*Permite adicionar descontos ao processo de salário apenas no periodo. Ex. faltas)')

        self.recibo_salario = list_field(view_order=8, name='Recibos Salários', condition="salario='{id}' AND estado!='Cancelado'", model_name='recibo_salario.ReciboSalario', list_edit_mode='popup', onlist=False)
        
        #self.recibo_subsidio = list_field(view_order=9, name='Recibos de Subsídios', condition="salario='{id}' AND estado!='Cancelado'", model_name='recibo_subsidio.ReciboSubsidio', list_edit_mode='popup', onlist=False)



    def getAno(self):
        options = []
        for ano in range(2015,datetime.date.today().year+2):
            options.append((str(ano), str(ano)))
        return options

    def getPeriodo(self):
        return [('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Nuvembro'),('12','Dezembro'),('13','Subsídio Natal'),('14','Prémio Produtividade'),('15','Subsídio Féria')]

    def getMes(self):
        return [('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Nuvembro'),('12','Dezembro')]


    def Gerar_Recibos(self, key, window_id):
        """Gera os recibos de salário e de subsídio em um periodo"""        
        self.kargs = get_model_record(model=self, key=key,force_db=True)

        este_periodo = "{ano}-{mes}".format(ano=self.kargs['ano'], mes=self.kargs['periodo'])

        if self.kargs['periodo'] in ('13','14','15'):
            self.gerarRecibosSubsidios(key=key)

        else:
            #gera recibos de salario
            funcionarios = Terceiro(where="funcionario=True").get(order_by='nome')                
            for func in funcionarios:
                contrato = ContratoFuncionario(where="terceiro='{id}'".format(id=func['id'])).get()             
                if contrato:
                    contrato=contrato[0]
                    content = {
                        'estado':'Rascunho',
                        'user':self.kargs['user'],
                        'salario':self.kargs['id'],
                        'terceiro':func['id'],                        
                        'periodo':self.kargs['periodo'],
                        'ano':self.kargs['ano']
                    }
                    idRecibo = ReciboSalario(**content).put()                    
                    
                    linhas = []
                    #adicionar o salario                   
                    linhas.append({'nome':'Salário', 'valor':contrato['salario_base'],'tipo_rendimento':None,'tipo_desconto':None})                   
                    #adicionar o IUR
                    iur = to_decimal(0)
                    if contrato['tipo'] in ('Permanente','Temporario'):
                        #calcular a nova base tributavel (salario e rendiemento tributaveis)
                        salario_bruto_iur = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_tributaveis(idFuncionario=func['id']))
                        iur = self.calcularIURfuncionario(salario=salario_bruto_iur)                        
                    elif contrato['tipo'] == 'Pensionista':
                        iur = self.calcularRetencaoPensionista(salario=contrato['salario_base'])
                    else:
                        iur = self.calcularIURprestadorServico(salario=contrato['salario_base'])                    
                    linhas.append({'nome':'IUR', 'valor':-iur, 'tipo_rendimento':None, 'tipo_desconto':None})                    
                    #adicionar o desconto inps
                    if contrato['tipo'] in ('Permanente','Temporario'):
                        salario_bruto_inps = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_Inps(idFuncionario=func['id']))
                        inps = self.calcularInpsFuncionario(salario=salario_bruto_inps)
                        linhas.append({'nome':'Segurança Social', 'valor':-inps,'tipo_rendimento':None,'tipo_desconto':None})
                    #adicionar os rendimentos
                    rendimentos = RendimentoFuncionario(where="terceiro='{id}'".format(id=func['id'])).get()
                    for line in rendimentos:
                        tipo = TipoRendimento(where="id='{tr}'".format(tr=line['tipo_rendimento'])).get()                        
                        if tipo:
                            linhas.append({'nome':tipo[0]['nome'], 'valor':line['valor'], 'tipo_rendimento':tipo[0]['id'], 'tipo_desconto':None})
                    #adicionar os descontos
                    print('\n\n\n\n##################1###################\n\n\n')
                    descontos = DescontoFuncionario(where="terceiro='{idTer}'".format(idTer=func['id'])).get()
                    for line in descontos:
                        tipo = TipoDesconto(where="id='{tr}'".format(tr=line['tipo_desconto'])).get()
                        if tipo:
                            tipo = tipo[0]
                            if tipo['taxa']:
                                if tipo['base']=='salario base':
                                    valor = contrato['salario_base']*line['valor']/100
                                    linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                                else:
                                    valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis(idFuncionario=func['id']))*line['valor']/100
                                    linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                            else:
                                linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                    #adicionar a outros descontos funcionario
                    outrosDescontos = OutrosDescontosFuncionario(where="terceiro='{idTer}' AND salario='{idSal}'".format(idTer=func['id'], idSal=key)).get()
                    for line in outrosDescontos:
                        tipo = TipoDesconto(where="id='{tr}'".format(tr=line['tipo_desconto'])).get()
                        if tipo:
                            tipo = tipo[0]
                            if tipo['taxa']:
                                if tipo['base']=='salario base':
                                    valor = contrato['salario_base']*line['valor']/100
                                    linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                                else:
                                    valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis(idFuncionario=func['id']))*line['valor']/100
                                    linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                            else:
                                linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                    for line in linhas:
                        content = {
                        'user':self.kargs['user'],
                        'recibo_salario':idRecibo,
                        'nome':line['nome'],
                        'valor':line['valor'],
                        'tipo_rendimento':line['tipo_rendimento'],
                        'tipo_desconto':line['tipo_desconto']                   
                        }
                        LinhaReciboSalario(**content).put()
                    
            self.kargs['estado']='Gerado'
            self.put()

        return form_edit(window_id=window_id).show()



    def gerarRecibosSubsidios(self, key, funcionarios):
        self.kargs = get_model_record(model=self, key=key,force_db=True)

        este_periodo = "{ano}-{mes}".format(ano=self.kargs['ano'], mes=self.kargs['periodo'])

        funcionarios=[]
        if (self.kargs['para_todos']==True & (self.kargs['periodo'] in ('13','14','15'))):                
            funcionarios = Terceiro(where="funcionario=True").get(order_by='nome')

        elif self.kargs['periodo'] in ('13','14','15'):

            sql = """SELECT t.* FROM terceiro t                
            WHERE (t.active = True OR t.active IS NULL)                
            AND t.id IN (
                SELECT fs.terceiro FROM funcionario_subsidio fs 
                WHERE (fs.active = True OR fs.active IS NULL)
                AND fs.salario = '{idSal}'
                )""".format(idSal=key)
            funcionarios = run_sql(sql)        

        for func in funcionarios:
            contrato = ContratoFuncionario(where="terceiro='{id}'".format(id=func['id'])).get()             
            if contrato:
                contrato=contrato[0]
                content = {
                    'estado':'Rascunho',
                    'user':self.kargs['user'],
                    'salario':self.kargs['id'],
                    'terceiro':func['id'],                        
                    'periodo':self.kargs['periodo'],
                    'ano':self.kargs['ano']
                }
                idRecibo = ReciboSalario(**content).put()                    
                
                linhas = []
                #adicionar o salario                   
                linhas.append({'nome':'Salário', 'valor':contrato['salario_base'],'tipo_rendimento':None,'tipo_desconto':None})                   
                #adicionar o IUR
                iur = to_decimal(0)
                if contrato['tipo'] in ('Permanente','Temporario'):
                    #calcular a nova base tributavel (salario e rendiemento tributaveis)
                    salario_bruto_iur = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_tributaveis(idFuncionario=func['id']))
                    iur = self.calcularIURfuncionario(salario=salario_bruto_iur)                        
                elif contrato['tipo'] == 'Pensionista':
                    iur = self.calcularRetencaoPensionista(salario=contrato['salario_base'])
                else:
                    iur = self.calcularIURprestadorServico(salario=contrato['salario_base'])                    
                linhas.append({'nome':'IUR', 'valor':-iur, 'tipo_rendimento':None, 'tipo_desconto':None})                    
                #adicionar o desconto inps
                if contrato['tipo'] in ('Permanente','Temporario'):
                    salario_bruto_inps = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_Inps(idFuncionario=func['id']))
                    inps = self.calcularInpsFuncionario(salario=salario_bruto_inps)
                    linhas.append({'nome':'Segurança Social', 'valor':-inps,'tipo_rendimento':None,'tipo_desconto':None})
                #adicionar os rendimentos
                rendimentos = RendimentoFuncionario(where="terceiro='{id}'".format(id=func['id'])).get()
                for line in rendimentos:
                    tipo = TipoRendimento(where="id='{tr}'".format(tr=line['tipo_rendimento'])).get()                        
                    if tipo:
                        linhas.append({'nome':tipo[0]['nome'], 'valor':line['valor'], 'tipo_rendimento':tipo[0]['id'], 'tipo_desconto':None})
                #adicionar os descontos
                print('\n\n\n\n##################1###################\n\n\n')
                descontos = DescontoFuncionario(where="terceiro='{idTer}'".format(idTer=func['id'])).get()
                for line in descontos:
                    tipo = TipoDesconto(where="id='{tr}'".format(tr=line['tipo_desconto'])).get()
                    if tipo:
                        tipo = tipo[0]
                        if tipo['taxa']:
                            if tipo['base']=='salario base':
                                valor = contrato['salario_base']*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                            else:
                                valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis(idFuncionario=func['id']))*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                        else:
                            linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                #adicionar a outros descontos funcionario
                outrosDescontos = OutrosDescontosFuncionario(where="terceiro='{idTer}' AND salario='{idSal}'".format(idTer=func['id'], idSal=key)).get()
                for line in outrosDescontos:
                    tipo = TipoDesconto(where="id='{tr}'".format(tr=line['tipo_desconto'])).get()
                    if tipo:
                        tipo = tipo[0]
                        if tipo['taxa']:
                            if tipo['base']=='salario base':
                                valor = contrato['salario_base']*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                            else:
                                valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis(idFuncionario=func['id']))*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                        else:
                            linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'tipo_rendimento':None, 'tipo_desconto':tipo['id']})
                for line in linhas:
                    content = {
                    'user':self.kargs['user'],
                    'recibo_salario':idRecibo,
                    'nome':line['nome'],
                    'valor':line['valor'],
                    'tipo_rendimento':line['tipo_rendimento'],
                    'tipo_desconto':line['tipo_desconto']                   
                    }
                    LinhaReciboSalario(**content).put()
                
        self.kargs['estado']='Gerado'
        self.put()



    def get_total_rendimento_tributaveis(self, idFuncionario):
        """
            retorna o total tributavel dos rendimentos (excepto salario) de um funcionario
        """        
        total = to_decimal(0)
        sql = """SELECT rf.valor, tr.* 
                FROM rendimento_funcionario rf, tipo_rendimento tr                
                WHERE (rf.active = True OR rf.active IS NULL)
                AND (tr.active = True OR tr.active IS NULL)
                AND rf.tipo_rendimento = tr.id
                AND rf.terceiro = '{id}'""".format(id=idFuncionario)
        rendimentos = run_sql(sql)
        for line in rendimentos:
            #verificar se o valor é maior que o limite de isencao
            if to_decimal(line['valor']) > to_decimal(line['limite_isento']):
                a_tributar = to_decimal(line['valor']) - to_decimal(line['limite_isento'])
                total+=a_tributar*to_decimal(line['percent_tribuavel'])/100
        return total

    def get_total_rendimento_Inps(self, idFuncionario):
        """
            retorna o total de rendimentos de um funcionario que contribui para a seguranca social
        """        
        total = to_decimal(0)
        sql = """SELECT rf.valor, tr.* 
                FROM rendimento_funcionario rf, tipo_rendimento tr 
                where rf.tipo_rendimento = tr.id
                and rf.terceiro = '{id}'""".format(id=idFuncionario)
        rendimentos = run_sql(sql)
        for line in rendimentos:           
            if line['desconto_inps']:                
                total+=to_decimal(line['valor'])
        return total
            


    def Activar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Activo'
        self.put()
        return form_edit(window_id=window_id).show()

    def Cancelar_Recibos(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_recibo_salario import ReciboSalario
        except:
            from recibo_salario import ReciboSalario      
        recibos = ReciboSalario(where="salario='{id}'".format(id=self.kargs['id'])).get()                
        for recibo in recibos:
            recibo['estado']='Cancelado'
            recibo['user']=self.kargs['user']            
            ReciboSalario(**recibo).put()
        self.kargs['estado']='Recibos Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Confirmar_Recibos(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_recibo_salario import ReciboSalario
        except:
            from recibo_salario import ReciboSalario      
        recibos = ReciboSalario(where="salario='{id}' AND estado='Rascunho'".format(id=self.kargs['id'])).get()                
        for recibo in recibos:
            recibo['estado']='Confirmado'
            recibo['user']=self.kargs['user']            
            ReciboSalario(**recibo).put()
        self.kargs['estado']='Recibos Confirmado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Efectuar_Pagamento(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_recibo_salario import ReciboSalario
        except:
            from recibo_salario import ReciboSalario      
        recibos = ReciboSalario(where="salario='{id}' AND estado='Confirmado'".format(id=self.kargs['id'])).get()                
        for recibo in recibos:
            recibo['estado']='Pago'
            recibo['user']=self.kargs['user']            
            ReciboSalario(**recibo).put()
        self.kargs['estado']='Pago'
        self.put()
        return form_edit(window_id=window_id).show()


    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_recibo_salario import ReciboSalario
        except:
            from recibo_salario import ReciboSalario      
        recibos = ReciboSalario(where="salario='{id}'".format(id=key)).get()                
        for recibo in recibos:
            recibo['estado']='Cancelado'
            recibo['user']=self.kargs['user']            
            ReciboSalario(**recibo).put()
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()

    
    def taxas_retencao(self):        
        def get_results():
            try:
                from my_retencao import Retencao
            except:
                from retencao import Retencao
            taxa = Retencao().get()
            if taxa:
                return taxa[0]
        return erp_cache.get(key=self.__model_name__ + 'retencoes', createfunc=get_results)
    

    def calcularIURfuncionario(self, salario):
        if salario not in (0,None,'0','None',''):
            salario=to_decimal(salario)
            if salario < to_decimal(0):
                return to_decimal(0)
            if (salario > to_decimal(0)) & (salario <= to_decimal(80000)):
                retencao = to_decimal(salario) * to_decimal(15)/100 - to_decimal(5500)
                return retencao
            elif (salario > to_decimal(80000)) & (salario <= to_decimal(150000)):                
                retencao = to_decimal(salario) * to_decimal(21) /100 - to_decimal(10300)
                return retencao
            elif salario > to_decimal(150000):
                retencao = to_decimal(salario) * to_decimal(25) / 100 - to_decimal(16300)
                return retencao
        else:
            return to_decimal(0)


    def calcularRetencaoPensionista(self, salario):
        if salario not in (0,None,'0','None',''):
            salario=to_decimal(salario)            
            retencao = salario - to_decimal(960000)/12
            return retencao            
        else:
            return to_decimal(0)


    def calcularIURnaoResidente(self, salario):
        if salario not in (0,None,'0','None',''):
            salario=to_decimal(salario)            
            taxa = self.taxas_retencao()
            if taxa:
                retencao = salario * to_decimal(taxa['taxa_nao_residente'])/100
                return retencao
            else:
                return to_decimal(0)         
        else:
            return to_decimal(0)

    def calcularIURprestadorServico(self, salario):
        if salario not in (0,None,'0','None',''):
            salario=to_decimal(salario)            
            taxa = self.taxas_retencao()
            if taxa:
                retencao = salario * to_decimal(taxa['taxa_prestacao_servico'])/100
                return retencao
            else:
                return to_decimal(0)         
        else:
            return to_decimal(0)


    def calcularInpsFuncionario(self, salario):
        if salario not in (0,None,'0','None',''):            
            salario=to_decimal(salario)
            taxa = self.taxas_retencao()
            if taxa:
                retencao = salario * to_decimal(taxa['taxa_inps_func'])/100
                return retencao
            else:
                return to_decimal(0)            
        else:
            return to_decimal(0)


    def calcularDescontoInpsEntidade(self, salario):
        if salario not in (0,None,'0','None',''):            
            salario=to_decimal(salario)
            taxa = self.taxas_retencao()
            if taxa:
                retencao = salario * to_decimal(taxa['taxa_inps_entidade'])/100
                return retencao
            else:
                return to_decimal(0)            
        else:
            return to_decimal(0)