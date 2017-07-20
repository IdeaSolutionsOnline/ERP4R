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
__model_name__='rh_folha_salario.RHFolhaSalario'
import auth, base_models
from orm import *
from form import *

try:
    from my_rh_funcionario_subsidio import RHFuncionarioSubsidio
except:
    from rh_funcionario_subsidio import RHFuncionarioSubsidio

try:
    from my_rh_outros_rendimentos_funcionario import RHOutrosRendimentosFuncionario
except:
    from rh_outros_rendimentos_funcionario import RHOutrosRendimentosFuncionario
try:
    from my_rh_gasto_suportado import RHGastoSuportado
except:
    from rh_gasto_suportado import RHGastoSuportado

try:
    from my_rh_recibo_salario import RHReciboSalario
except:
    from rh_recibo_salario import RHReciboSalario
try:
    from my_rh_linha_recibo_salario import RHLinhaReciboSalario
except:
    from rh_linha_recibo_salario import RHLinhaReciboSalario

try:
    from my_rh_rendimento_funcionario import RHRendimentoFuncionario
except:
    from rh_rendimento_funcionario import RHRendimentoFuncionario
try:
    from my_rh_desconto_funcionario import RHDescontoFuncionario
except:
    from rh_desconto_funcionario import RHDescontoFuncionario

try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro
try:
    from my_rh_contrato_funcionario import RHContratoFuncionario
except:
    from rh_contrato_funcionario import RHContratoFuncionario
try:
    from my_rh_outros_descontos_funcionario import RHOutrosDescontosFuncionario
except:
    from rh_outros_descontos_funcionario import RHOutrosDescontosFuncionario
try:
    from my_rh_tipo_rendimento import RHTipoRendimento
except:
    from rh_tipo_rendimento import RHTipoRendimento
try:
    from my_rh_tipo_desconto import RHTipoDesconto
except:
    from rh_tipo_desconto import RHTipoDesconto

from rh_taxa_retencao import RHTaxaRetencao

class RHFolhaSalario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'rh_folha_salario'
        self.__title__= 'Folhas de Salários'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'rh_folha_salario.periodo'
        self.__workflow__ = (
            'estado', {'Rascunho':['Activar', 'Cancelar'], 'Activo':['Gerar Recibos', 'Cancelar'], 'Gerado':['Cancelar Recibos','Cancelar','Confirmar Recibos'],'Recibos Cancelado':['Gerar Recibos'],'Recibos Confirmado':['Efectuar Pagamento']}
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

        self.__no_edit__ = [('estado', ['Pago', 'Cancelado'])]

        self.__get_options__ = ['periodo']

        self.__tabs__ = [
            ('Salários',['ano','periodo','mes','para_todos','estado','rh_funcionario_subsidio']),
            ('Outros Rendimentos e Descontos',['rh_outros_rendimentos_funcionario','rh_outros_descontos_funcionario']),
            ('Recibos',['rh_recibo_salario'])
        ]


        self.ano = combo_field(view_order = 1, size=45, name ='Ano', args = 'required', default = datetime.date.today().year, options='model.getAno()')
        
        self.periodo = combo_field(view_order = 2, size=70, name ='Periodo', args = 'required', default = datetime.date.today().strftime("%m"), options='model.getPeriodo()')
                
        self.para_todos = boolean_field(view_order = 4, size=50, name = 'Todos Funcionários', default = True)
        
        self.estado = info_field(view_order=5, name='Estado', size=45, default='Rascunho', args='readonly')
        
        self.rh_funcionario_subsidio = list_field(view_order=6, name='Funcionários á Processar',condition="rh_folha_salario='{id}'", model_name='rh_funcionario_subsidio.RHFuncionarioSubsidio', list_edit_mode='popup', onlist=False)

        self.rh_outros_rendimentos_funcionario = list_field(view_order=7, condition="rh_folha_salario='{id}'", model_name='rh_outros_rendimentos_funcionario.RHOutrosRendimentosFuncionario', list_edit_mode='inline', onlist=False, name='Outros Rendimentos (Apenas Neste Periodo)')

        self.rh_outros_descontos_funcionario = list_field(view_order=8, condition="rh_folha_salario='{id}'", model_name='rh_outros_descontos_funcionario.RHOutrosDescontosFuncionario', list_edit_mode='inline', onlist=False, name='Outros Descontos (Apenas Neste Periodo)')

        self.rh_recibo_salario = list_field(view_order=9, name='Recibos Salários', condition="rh_folha_salario='{id}' AND estado!='Cancelado'", model_name='rh_recibo_salario.RHReciboSalario', list_edit_mode='popup', onlist=False)

        


    def getAno(self):
        options = []
        for ano in range(datetime.date.today().year-2,datetime.date.today().year+2):
            options.append((str(ano), str(ano)))
        return options

    def getPeriodo(self):
        return [('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Nuvembro'),('12','Dezembro'),('13','Subsídio Natal'),('14','Prémio Produtividade'),('15','Subsídio Féria')]


    def Gerar_Recibos(self, key, window_id):
        """Gera os recibos de salário e de subsídio em um periodo"""      
        self.kargs = get_model_record(model=self, key=key,force_db=True)
            
        #funcionarios=[]
        if self.kargs['para_todos']:                
            funcionarios = Terceiro(where="funcionario=True").get(order_by='nome')
        else:
            sql = """SELECT t.* FROM terceiro t                
                WHERE (t.active = True OR t.active IS NULL)  AND t.id IN (
                    SELECT fs.terceiro FROM rh_funcionario_subsidio fs 
                    WHERE (fs.active = True OR fs.active IS NULL)
                    AND fs.rh_folha_salario = '{idSal}')""".format(idSal=key)
            funcionarios = run_sql(sql)

        if len(funcionarios)!=0:
            if self.kargs['periodo'] in ('13','14','15'):
                self.gerarRecibosSubsidios(key=key)
            else:
                for func in funcionarios:
                    contrato = RHContratoFuncionario(where="terceiro='{id}' AND activo=True".format(id=func['id'])).get()             
                    if contrato:
                        contrato=contrato[0]
                        content = {
                            'estado':'Rascunho',
                            'user':self.kargs['user'],
                            'rh_folha_salario':self.kargs['id'],
                            'terceiro':func['id'],                        
                            'periodo':self.kargs['periodo'],
                            'ano':self.kargs['ano'],
                            'tipo_funcionario':contrato['tipo']
                        }
                        idRecibo = RHReciboSalario(**content).put()                    
                        
                        linhas = []
                        #SALARIO                   
                        linhas.append({'nome':'Salário', 'valor':contrato['salario_base'],'rh_tipo_rendimento':None,'rh_tipo_desconto':None, 'origem':'salario','parte_trib':to_decimal(0)})                   
                        #IUR
                        if (contrato['tipo'] == 'dependente') & (contrato['vinculo'] in ('efectivo','a_termo')):
                            #calcular a nova base tributavel (salario e rendiementos tributaveis)
                            salario_bruto_iur = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_tributaveis(idFuncionario=func['id']))
                            iur = self.calcularIURfuncionario(salario=salario_bruto_iur)
                            print('\n\n\n\n\nAAAAAAAAAAAAAAAAAAA\n\n',iur,'\n\nAAAAAAAAAAAAAAAAAAAAAAAAa\n\n')
                            linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})
                        elif (contrato['tipo'] == 'dependente') & (contrato['vinculo'] =='prestacao_servico'):
                            #calcular a nova base tributavel (salario e rendiementos tributaveis)
                            salario_bruto_iur = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_tributaveis(idFuncionario=func['id']))
                            iur = self.calcularIURprestadorServico(salario=salario_bruto_iur)
                            linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})                        
                        elif contrato['tipo'] == 'pensionista':
                            iur = self.calcularRetencaoPensionista(salario=contrato['salario_base'])
                            linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})
                        elif contrato['tipo'] == 'nao_residente':
                            iur = self.calcularIURnaoResidente(salario=contrato['salario_base'])                    
                            linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})                   
                        #SEGURANCA SOCIAL
                        if (contrato['tipo'] == 'dependente') & (contrato['vinculo'] in ('efectivo','a_termo')):
                            salario_bruto_inps = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_Inps(idFuncionario=func['id']))
                            inps = self.calcularDescontoInpsFuncionario(salario=salario_bruto_inps)
                            linhas.append({'nome':'Segurança Social', 'valor':-inps,'rh_tipo_rendimento':None,'rh_tipo_desconto':None, 'origem':'inps','parte_trib':to_decimal(0)})
                            ####
                            RHGastoSuportado(rh_recibo_salario=idRecibo, nome="INPS", valor=self.calcularDescontoInpsEntidade(salario=salario_bruto_inps), user=self.kargs['user']).put()
                        #RENDIMENTOS
                        rendimentos = RHRendimentoFuncionario(where="terceiro='{id}'".format(id=func['id'])).get()
                        for line in rendimentos:
                            tipo = RHTipoRendimento(where="id='{tr}'".format(tr=line['rh_tipo_rendimento'])).get()                       
                            if tipo:
                                linhas.append({'nome':tipo[0]['nome'], 'valor':line['valor'], 'rh_tipo_rendimento':tipo[0]['id'], 'rh_tipo_desconto':None, 'origem':'rendimento','parte_trib':self.get_parteTributavel(tipo_rend=tipo[0]['id'], valor=line['valor'])})
                        #OUTROS RENDIMENTOS
                        outrosRendimentos = RHOutrosRendimentosFuncionario(where="terceiro='{id}' AND rh_folha_salario = '{folha}'".format(id=func['id'], folha=key)).get()
                        for line in outrosRendimentos:
                            tipo = RHTipoRendimento(where="id='{tr}'".format(tr=line['rh_tipo_rendimento'])).get()                        
                            if tipo:
                                linhas.append({'nome':tipo[0]['nome'], 'valor':line['valor'], 'rh_tipo_rendimento':tipo[0]['id'], 'rh_tipo_desconto':None, 'origem':'rendimento','parte_trib':self.get_parteTributavel(tipo_rend=tipo[0]['id'], valor=line['valor'])})
                        #DESCONTOS
                        descontos = RHDescontoFuncionario(where="terceiro='{idTer}'".format(idTer=func['id'])).get()
                        for line in descontos:
                            tipo = RHTipoDesconto(where="id='{tr}'".format(tr=line['rh_tipo_desconto'])).get()
                            if tipo:
                                tipo = tipo[0]
                                if tipo['taxa']:
                                    if tipo['base']=='salario base':
                                        valor = contrato['salario_base']*line['valor']/100
                                        linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'desconto','parte_trib':to_decimal(0)})
                                    else:
                                        valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis(idFuncionario=func['id']))*line['valor']/100
                                        linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'desconto','parte_trib':to_decimal(0)})
                                else:
                                    linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'desconto','parte_trib':to_decimal(0)})
                        #OUTROS DESCONTOS
                        outrosDescontos = RHOutrosDescontosFuncionario(where="terceiro='{idTer}' AND rh_folha_salario='{idSal}'".format(idTer=func['id'], idSal=key)).get()
                        for line in outrosDescontos:
                            tipo = RHTipoDesconto(where="id='{tr}'".format(tr=line['rh_tipo_desconto'])).get()
                            if tipo:
                                tipo = tipo[0]
                                if tipo['taxa']:
                                    if tipo['base']=='salario base':
                                        valor = contrato['salario_base']*line['valor']/100
                                        linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'outros_descontos','parte_trib':to_decimal(0)})
                                    else:
                                        valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis(idFuncionario=func['id']))*line['valor']/100
                                        linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'outros_descontos','parte_trib':to_decimal(0)})
                                else:
                                    linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'outros_descontos','parte_trib':to_decimal(0)})
                        for line in linhas:
                            content = {
                            'user':self.kargs['user'],
                            'rh_recibo_salario':idRecibo,
                            'nome':line['nome'],
                            'valor':line['valor'],
                            'rh_tipo_rendimento':line['rh_tipo_rendimento'],
                            'rh_tipo_desconto':line['rh_tipo_desconto'],
                            'origem':line['origem'],
                            'parte_trib':line['parte_trib']                 
                            }
                            RHLinhaReciboSalario(**content).put()
            #alterar estado
            self.kargs['estado']='Gerado'
            self.put()
        else:
            return error_message('Não pode gerar recibos sem indicar os funcionarios!\n')   

        return form_edit(window_id=window_id).show()



    def gerarRecibosSubsidios(self, key):
        self.kargs = get_model_record(model=self, key=key,force_db=True)
        funcionarios=[]
        if self.kargs['para_todos']:                
            funcionarios = Terceiro(where="funcionario=True").get(order_by='nome')
        else:
            sql = """SELECT t.* FROM terceiro t                
            WHERE (t.active = True OR t.active IS NULL)                
            AND t.id IN (
                SELECT fs.terceiro FROM rh_funcionario_subsidio fs 
                WHERE (fs.active = True OR fs.active IS NULL)
                AND fs.rh_folha_salario = '{idSal}'
                )""".format(idSal=key)
            funcionarios = run_sql(sql)        

        for func in funcionarios:
            contrato = RHContratoFuncionario(where="terceiro='{id}'".format(id=func['id'])).get()             
            if contrato:
                contrato=contrato[0]
                content = {
                    'estado':'Rascunho',
                    'user':self.kargs['user'],
                    'rh_folha_salario':self.kargs['id'],
                    'terceiro':func['id'],                        
                    'periodo':self.kargs['periodo'],
                    'ano':self.kargs['ano']
                }
                idRecibo = RHReciboSalario(**content).put()                   
                
                linhas = []
                #SALARIO                   
                linhas.append({'nome':'Salário', 'valor':contrato['salario_base'],'rh_tipo_rendimento':None,'rh_tipo_desconto':None, 'origem':'salario','parte_trib':to_decimal(0)})                   
                #IUR
                if (contrato['tipo'] == 'dependente') & (contrato['vinculo'] in ('efectivo','a_termo')):
                    #calcular a nova base tributavel (salario e rendiementos tributaveis)
                    salario_bruto_iur = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_tributaveis(idFuncionario=func['id']))
                    iur = self.calcularIURfuncionario(salario=salario_bruto_iur)
                    linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})
                elif (contrato['tipo'] == 'dependente') & (contrato['vinculo'] =='prestacao_servico'):
                    #calcular a nova base tributavel (salario e rendiementos tributaveis)
                    salario_bruto_iur = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_tributaveis(idFuncionario=func['id']))
                    iur = self.calcularIURprestadorServico(salario=salario_bruto_iur)
                    linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})                        
                elif contrato['tipo'] == 'pensionista':
                    iur = self.calcularRetencaoPensionista(salario=contrato['salario_base'])
                    linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})
                elif contrato['tipo'] == 'nao_residente':
                    iur = self.calcularIURnaoResidente(salario=contrato['salario_base'])                    
                    linhas.append({'nome':'IUR', 'valor':-iur, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':None, 'origem':'iur','parte_trib':to_decimal(0)})                     
                #SEGURANCA SOCIAL
                if (contrato['tipo'] == 'dependente') & (contrato['vinculo'] in ('efectivo','a_termo')):
                    salario_bruto_inps = to_decimal(contrato['salario_base'])+to_decimal(self.get_total_rendimento_Inps_subsidio(idFuncionario=func['id']))
                    inps = self.calcularDescontoInpsFuncionario(salario=salario_bruto_inps)
                    linhas.append({'nome':'Segurança Social', 'valor':-inps,'rh_tipo_rendimento':None,'rh_tipo_desconto':None, 'origem':'inps','parte_trib':to_decimal(0)})
                    ####
                    RHGastoSuportado(rh_recibo_salario=idRecibo, nome="INPS", valor=self.calcularDescontoInpsEntidade(salario=salario_bruto_inps), user=self.kargs['user']).put()
                #RENDIMENTOS
                rendimentos = RHRendimentoFuncionario(where="terceiro='{id}' AND em_subsidio = True".format(id=func['id'])).get()
                for line in rendimentos:
                    tipo = RHTipoRendimento(where="id='{tr}'".format(tr=line['rh_tipo_rendimento'])).get()                        
                    if tipo:
                        linhas.append({'nome':tipo[0]['nome'], 'valor':line['valor'], 'rh_tipo_rendimento':tipo[0]['id'], 'rh_tipo_desconto':None, 'origem':'rendimento','parte_trib':self.get_parteTributavel(tipo_rend=tipo[0]['id'], valor=line['valor'])})
                #OUTROS RENDIMENTOS
                outrosRendimentos = RHOutrosRendimentosFuncionario(where="terceiro='{id}' AND rh_folha_salario = '{folha}'".format(id=func['id'], folha=key)).get()
                for line in outrosRendimentos:
                    tipo = RHTipoRendimento(where="id='{tr}'".format(tr=line['rh_tipo_rendimento'])).get()                        
                    if tipo:
                        linhas.append({'nome':tipo[0]['nome'], 'valor':line['valor'], 'rh_tipo_rendimento':tipo[0]['id'], 'rh_tipo_desconto':None, 'origem':'rendimento','parte_trib':self.get_parteTributavel(tipo_rend=tipo[0]['id'], valor=line['valor'])})
                #DESCONTOS
                descontos = RHDescontoFuncionario(where="terceiro='{idTer}' AND em_subsidio=True".format(idTer=func['id'])).get()
                for line in descontos:
                    tipo = RHTipoDesconto(where="id='{tr}'".format(tr=line['rh_tipo_desconto'])).get()
                    if tipo:
                        tipo = tipo[0]
                        if tipo['taxa']:
                            if tipo['base']=='salario base':
                                valor = contrato['salario_base']*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'desconto','parte_trib':to_decimal(0)})
                            else:
                                valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis_subsidio(idFuncionario=func['id']))*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'desconto','parte_trib':to_decimal(0)})
                        else:
                            linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'desconto','parte_trib':to_decimal(0)})
                #OUTROS DESCONTOS
                outrosDescontos = RHOutrosDescontosFuncionario(where="terceiro='{idTer}' AND rh_folha_salario='{idSal}'".format(idTer=func['id'], idSal=key)).get()
                for line in outrosDescontos:
                    tipo = RHTipoDesconto(where="id='{tr}'".format(tr=line['rh_tipo_desconto'])).get()
                    if tipo:
                        tipo = tipo[0]
                        if tipo['taxa']:
                            if tipo['base']=='salario base':
                                valor = contrato['salario_base']*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'outros_descontos', 'parte_trib':to_decimal(0)})
                            else:
                                valor = (contrato['salario_base']+self.get_total_rendimento_tributaveis_subsidio(idFuncionario=func['id']))*line['valor']/100
                                linhas.append({'nome':tipo['nome'], 'valor':-valor, 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'outros_descontos', 'parte_trib':to_decimal(0)})
                        else:
                            linhas.append({'nome':tipo['nome'], 'valor':-line['valor'], 'rh_tipo_rendimento':None, 'rh_tipo_desconto':tipo['id'], 'origem':'outros_descontos', 'parte_trib':to_decimal(0)})
                for line in linhas:
                    content = {
                    'user':self.kargs['user'],
                    'rh_recibo_salario':idRecibo,
                    'nome':line['nome'],
                    'valor':line['valor'],
                    'rh_tipo_rendimento':line['rh_tipo_rendimento'],
                    'rh_tipo_desconto':line['rh_tipo_desconto'],
                    'origem':line['origem'],
                    'parte_trib':line['parte_trib']                  
                    }
                    RHLinhaReciboSalario(**content).put()



    def get_total_rendimento_tributaveis(self, idFuncionario):
        """
            retorna o total tributavel dos rendimentos (excepto salario) de um funcionario
        """        
        total = to_decimal(0)
        sql = """SELECT rf.valor, tr.* 
                FROM rh_rendimento_funcionario rf, rh_tipo_rendimento tr                
                WHERE (rf.active = True OR rf.active IS NULL)
                AND (tr.active = True OR tr.active IS NULL)
                AND rf.rh_tipo_rendimento = tr.id
                AND rf.terceiro = '{id}'""".format(id=idFuncionario)
        rendimentos = run_sql(sql)
        for line in rendimentos:
            #verificar se o valor é maior que o limite de isencao
            if to_decimal(line['valor']) > to_decimal(line['limite_isento']):
                a_tributar = to_decimal(line['valor']) - to_decimal(line['limite_isento'])
                total+=a_tributar*to_decimal(line['percent_tribuavel'])/100
        return total

    def get_parteTributavel(self,tipo_rend, valor):
        '''
            retorna a parte tributavel do valor de um rendimento
        '''
        total=to_decimal(0)
        tipo = RHTipoRendimento(where="id='{id}'".format(id=tipo_rend)).get()
        if tipo:
            tipo=tipo[0]
            if to_decimal(valor) > to_decimal(tipo['limite_isento']):
                a_tributar = to_decimal(valor) - to_decimal(tipo['limite_isento'])
                total+=a_tributar*to_decimal(tipo['percent_tribuavel'])/100
        return total


    def get_total_rendimento_tributaveis_subsidio(self, idFuncionario):
        """
            retorna o total tributavel dos rendimentos (excepto salario) de um funcionario
        """        
        total = to_decimal(0)
        sql = """SELECT rf.valor, tr.* 
                FROM rh_rendimento_funcionario rf, rh_tipo_rendimento tr                
                WHERE (rf.active = True OR rf.active IS NULL)
                AND (tr.active = True OR tr.active IS NULL)
                AND rf.rh_tipo_rendimento = tr.id
                AND rf.em_subsidio=True
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
                FROM rh_rendimento_funcionario rf, rh_tipo_rendimento tr 
                WHERE rf.rh_tipo_rendimento = tr.id
                AND tr.desconto_inps = True
                AND rf.terceiro = '{id}'""".format(id=idFuncionario)
        rendimentos = run_sql(sql)
        for line in rendimentos:           
            if line['desconto_inps']:                
                total+=to_decimal(line['valor'])
        return total

    def get_total_rendimento_Inps_subsidio(self, idFuncionario):
        """
            retorna o total de rendimentos de um funcionario que conta em subsidios e que contribui para a seguranca social
        """        
        total = to_decimal(0)
        sql = """SELECT rf.valor, tr.* 
                FROM rh_rendimento_funcionario rf, rh_tipo_rendimento tr 
                WHERE rf.rh_tipo_rendimento = tr.id
                AND rf.em_subsidio=True
                AND tr.desconto_inps = True
                AND rf.terceiro = '{id}'""".format(id=idFuncionario)
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
        """
            cancela os recobos gerados a partir desta folha de salario
        """
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_rh_recibo_salario import RHReciboSalario
        except:
            from rh_recibo_salario import RHReciboSalario      
        recibos = RHReciboSalario(where="rh_folha_salario='{id}'".format(id=self.kargs['id'])).get()                
        for recibo in recibos:
            recibo['estado']='Cancelado'
            recibo['user']=self.kargs['user']            
            RHReciboSalario(**recibo).put()
        self.kargs['estado']='Recibos Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Confirmar_Recibos(self, key, window_id):
        """
            confirma os recobos gerados a partir desta folha de salario
        """
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_rh_recibo_salario import RHReciboSalario
        except:
            from rh_recibo_salario import RHReciboSalario      
        recibos = RHReciboSalario(where="rh_folha_salario='{id}' AND estado='Rascunho'".format(id=self.kargs['id'])).get()                
        for recibo in recibos:
            recibo['estado']='Confirmado'
            recibo['user']=self.kargs['user']            
            RHReciboSalario(**recibo).put()
        self.kargs['estado']='Recibos Confirmado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Efectuar_Pagamento(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_rh_recibo_salario import RHReciboSalario
        except:
            from rh_recibo_salario import RHReciboSalario      
        recibos = RHReciboSalario(where="rh_folha_salario='{id}' AND estado='Confirmado'".format(id=self.kargs['id'])).get()                
        for recibo in recibos:
            recibo['estado']='Pago'
            recibo['user']=self.kargs['user']            
            RHReciboSalario(**recibo).put()
        self.kargs['estado']='Pago'
        self.put()
        return form_edit(window_id=window_id).show()


    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_rh_recibo_salario import RHReciboSalario
        except:
            from rh_recibo_salario import RHReciboSalario      
        recibos = RHReciboSalario(where="rh_folha_salario='{id}'".format(id=key)).get()                
        for recibo in recibos:
            recibo['estado']='Cancelado'
            recibo['user']=self.kargs['user']            
            RHReciboSalario(**recibo).put()
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
                from my_rh_retencao import RHRetencao
            except:
                from rh_retencao import RHRetencao
            taxa = RHRetencao().get()
            if taxa:
                return taxa[0]
        return erp_cache.get(key=self.__model_name__ + 'retencoes', createfunc=get_results)
    

    def calcularIURfuncionario(self, salario):
        """
            calcura o IUR do funcionario dado o valor do salario tributavel
        """
        iur = to_decimal(0)
        taxa = RHTaxaRetencao(where="minimo<='{sal}' AND maximo >='{sal}'".format(sal=salario)).get()
        print("\n\n\nDDDDDDDDDDDDDDDDDDDDDDD\n\ntaxa:",taxa,"\n\n\n")
        if taxa:
            iur = to_decimal(salario)*to_decimal(taxa[0]['taxa'])/100
        return iur


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


    def calcularDescontoInpsFuncionario(self, salario):
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