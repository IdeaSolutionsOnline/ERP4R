# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'modelo_dpr.ModeloDPR'

import auth, base_models
from orm import *
from form import *

from area_fiscal import AreaFiscal
import erp_config
from anexo_cliente_dpr import AnexoClienteDPR
from linha_anexo_cliente_dpr import LinhaAnexoClienteDPR
from anexo_fornecedor_dpr import AnexoFornecedorDPR
from linha_anexo_fornecedor_dpr import LinhaAnexoFornecedorDPR
from anexo_salario_dpr import AnexoSalarioDPR
from linha_anexo_salario_dpr import LinhaAnexoSalarioDPR
from salario import Salario
from recibo_salario import ReciboSalario

class ModeloDPR(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'modelo_dpr'
        self.__title__ = 'Modelo DPR'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
                      

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.__workflow__ = (
            'estado', {'Rascunho':['Verificar'],'Verificado':['Cancelar', 'Confirmar'], 'Confirmado':['GerarXML DPR'],'Cancelado':['Rascunho']}
            )

        self.__workflow_auth__ = {
            'GerarXML DPR':['All'],
            'Confirmar':['All'],
            'Cancelar':['All'],
            'Verificar':['All'],
            'Rascunho':['All'],
            'full_access':['Gestor']
            }

        self.__tabs__ = [('XML DPR',['xml_dpr']),
                        ('XML Cliente',['xml_cliente']),
                        ('XML Fornecedor',['xml_fornecedor']),
                        ('XML Salário',['xml_salario']),]

        self.dec = combo_field(view_order = 1, name = 'Tipo Declaração', size = 70, default = '1', options = [('1','No Prazo'), ('2','Fora de Prazo'),('4', 'Substituição')], onlist = False)

        self.tipo_operacao = combo_field(view_order = 2, name='Tipo Operação',size=70, default='N', options=[('N','Normal'),('O','Omissão'),('C','Correção Fav. Contribuinte'),('E','Correção Fav. Estado'),('A','Anulado')])

        self.cli = combo_field(view_order = 3, name = 'Anexos Cliente', size=50,args='required',default='1',options=[('0','-NÃO-'),('1','-SIM-')])

        self.forn = combo_field(view_order = 4, name = 'Anexos Fornecedor', size=45,args='required',default='1',options=[('0','-NÃO-'),('1','-SIM-')])

        self.sal = combo_field(view_order = 5, name = 'Anexo Salario',size=45,args='required',default='1',options=[('0','-NÃO-'),('1','-SIM-')])

        self.ano = combo_field(view_order = 6, name ='Ano', args = 'required', size=70, default = datetime.date.today().year, options='model.getAno()')
        
        self.periodo = combo_field(view_order = 7, size=70, name ='Periodo', args = 'required', default = datetime.date.today().strftime("%m"), options='model.getPeriodo()')

        self.cd_af = combo_field(view_order = 8, name = 'Repartição Finanças', size = 70, model = 'area_fiscal', args = 'required', onlist = False, search = False, column = 'local', options = "model.get_opts('AreaFiscal().get_options_buyable()')")
        
        self.nif = string_field(view_order = 9, name = 'Nif', size = 70, default=erp_config.nif, onlist=False)

        self.nome = string_field(view_order = 10, name = 'Nome', size = 230, default=erp_config.enterprise, onlist=False)

        self.dt_emissao = date_field(view_order = 11, size=70, name ='Data de Emissão', args='required ', default=datetime.date.today())

        self.g1 = currency_field(view_order = 12, name ='G1 Retenções da Categoria A', args='required',size=90,onlist=False)
        self.g2 = currency_field(view_order = 13, name ='G2 Retenções da Categoria B', args='required',size=90,onlist=False)
        self.g3 = currency_field(view_order = 14, name ='G3 Retenções da Categoria C', args='required',size=90,onlist=False)
        self.g4 = currency_field(view_order = 15, name ='G4 Retenções da Categoria D', args='required',size=90,onlist=False)
        self.g5 = currency_field(view_order = 16, name ='G5 Retenções da Categoria D(PC)', args='required',size=90,onlist=False)
        self.g6 = currency_field(view_order = 17, name ='G6 Retenções da Categoria E', args='required',size=90,onlist=False)
        self.g7 = currency_field(view_order = 18, name ='G7 Retenções TEU', args='required',size=90,onlist=False)

        self.tp = function_field(view_order = 19, name='Total a Pagar', args='required',size=90,default=0)
        self.obs = text_field(view_order = 20, name='Observações', size = 90, onlist=False)
        
        self.xml_cliente = text_field(view_order = 21, nolabel=True, name='', size = 310, onlist=False, args='rows=12')
        self.xml_fornecedor = text_field(view_order = 22, nolabel=True, name='', size = 310, onlist=False, args='rows=12')
        self.xml_salario = text_field(view_order = 23, nolabel=True, name='', size = 310, onlist=False, args='rows=12')
        self.xml_dpr = text_field(view_order = 24, nolabel=True, name='', size = 310, onlist=False, args='rows=12')
        self.estado = info_field(view_order = 25, name ='Estado', hidden = True, default='Rascunho')



    def get_opts(self, get_str):       
        return eval(get_str)


    def getAno(self):
        options = []
        for ano in range(2014,datetime.date.today().year+2):
            options.append((str(ano), str(ano)))
        return options

    def getPeriodo(self):
        return [('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Nuvembro'),('12','Dezembro')]


    def get_tp(self, key):
        soma = to_decimal(0)              
        modelo = self.get(key=key)[0]       
        for campo in ('g1','g2','g3','g4','g5','g6','g7'): 
            try:               
                if modelo[campo] not in('',0,None):
                    soma+=to_decimal(modelo[campo])
            except:
                pass          
        return int(soma)

    
    def GerarXML_DPR(self, key, window_id, internal = False):
        """ 
        Metodo para a confirmacao do modelo
        """
        self.kargs = get_model_record(model = self, key = key)
        if self.kargs['estado'] == 'Confirmado':
            xml = self.gerar_xml_modelo_dpr(key=key)
            self.kargs['xml_dpr'] = xml
            self.kargs['estado']='Gerado'
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result


    def Verificar(self, key, window_id, internal = False):
        """ 
        Metodo que faz a verificao e geração dos anexos do modelo 106
        """
        self.kargs = get_model_record(model = self, key = key)
        if self.kargs['estado'] == 'Rascunho':            
            #mostrar os anexos desse periodo
            if self.kargs['cli']=='1':
                xml_cli = self.gerar_xml_cliente_dpr(key=key)
                self.kargs['xml_cliente']=xml_cli
                
            if self.kargs['forn']=='1':
                xml_forn = self.gerar_xml_fornecedor_dpr(key=key)                
                self.kargs['xml_fornecedor']=xml_forn                

            if self.kargs['sal']=='1':
                self.getInfoRecibosSalario(key=key)
                xml_sal = self.gerar_xml_salario_dpr(key=key)              
                self.kargs['xml_salario']=xml_sal
                
            self.kargs['estado'] = 'Verificado'
            self.put()

            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result

    
    def Confirmar(self, key, window_id, internal = False):
        """ 
        Metodo para a confirmacao do modelo
        """
        self.kargs = get_model_record(model = self, key = key)
        if self.kargs['estado'] == 'Verificado':            
            self.kargs['estado'] = 'Confirmado'
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result


    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()


    def Cancelar(self, key, window_id, internal = False):
        self.kargs = get_model_record(model=self, key=key)
        if self.kargs['estado'] in ('Verificado','Gerado'):            
            for campo in ('g1','g2','g3','g4','g5','g6','g7'):
                try:                               
                    self.kargs[campo]=to_decimal(0)
                except:
                    pass
            self.kargs['estado']='Cancelado'
            self.kargs['xml_cliente'] = ' '
            self.kargs['xml_fornecedor']=' '
            self.kargs['xml_salario']=' '
            self.kargs['xml_dpr']=' '
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result        

    def Gerar_XML_DPR(self, key, window_id, internal = False):
        self.kargs = get_model_record(model=self, key=key)
        if self.kargs['estado'] == 'Confirmado':           

            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result


    def gerar_xml_modelo_dpr(self, key):    
        conteudoFinalXml=' '
        modelo = get_model_record(model=self, key=key)            
        if modelo:                   
            #CRIACAO DO MODELO XML        
            import xml.dom.minidom
            doc = xml.dom.minidom.Document()
            # Cria os elementos
            tag_dpr_mod = doc.createElement('dpr_mod')
            tag_header = doc.createElement('header')
            tag_g1 = doc.createElement('g1')
            tag_g2 = doc.createElement('g2')
            tag_g3 = doc.createElement('g3')
            tag_g4 = doc.createElement('g4')
            tag_g5 = doc.createElement('g5')
            tag_g6 = doc.createElement('g6')
            tag_g7 = doc.createElement('g7')
            tag_tp = doc.createElement('tp')
            tag_obs = doc.createElement('obs')
            tag_dt_emissao = doc.createElement('dt_emissao')
            ##atributos de header
            tag_header.setAttribute('dec', str(modelo['dec']))
            tag_header.setAttribute('sal', str(modelo['sal']))
            tag_header.setAttribute('cli', str(modelo['cli']))
            tag_header.setAttribute('for', str(modelo['forn']))
            tag_header.setAttribute('ano', str(modelo['ano']))
            tag_header.setAttribute('periodo', str(modelo['periodo']))
            tag_header.setAttribute('cd_af', str(modelo['cd_af']))
            tag_header.setAttribute('nif', str(modelo['nif']))
            tag_header.setAttribute('nome', str(modelo['nome']))                
            ##colocar os valores do campos
            tag_g1.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g1'])))))
            tag_g2.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g2'])))))
            tag_g3.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g3'])))))
            tag_g4.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g4'])))))
            tag_g5.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g5'])))))
            tag_g6.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g6'])))))
            tag_g7.appendChild(doc.createTextNode(str(int(to_decimal(modelo['g7'])))))
            tag_tp.appendChild(doc.createTextNode(str(self.get_tp(key=key))))
            tag_obs.appendChild(doc.createTextNode(str(modelo['obs'])))         
            tag_dt_emissao.appendChild(doc.createTextNode(str(modelo['dt_emissao'])))
            # Cria a estrutura
            doc.appendChild(tag_dpr_mod)
            tag_dpr_mod.appendChild(tag_header)
            tag_dpr_mod.appendChild(tag_g1)
            tag_dpr_mod.appendChild(tag_g2) 
            tag_dpr_mod.appendChild(tag_g3) 
            tag_dpr_mod.appendChild(tag_g4) 
            tag_dpr_mod.appendChild(tag_g5) 
            tag_dpr_mod.appendChild(tag_g6) 
            tag_dpr_mod.appendChild(tag_g7) 
            tag_dpr_mod.appendChild(tag_tp) 
            tag_dpr_mod.appendChild(tag_obs) 
            tag_dpr_mod.appendChild(tag_dt_emissao)                           
            #GERANDO O XML
            conteudoXmlCriado= doc.toprettyxml()        
            #colocar o encoding
            conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>')           
        return conteudoFinalXml


    def gerar_xml_cliente_dpr(self, key):    
        conteudoFinalXml=' '
        anexoCliDPR = AnexoClienteDPR(where="modelo_dpr='{id}'".format(id=key)).get()        
        if anexoCliDPR:
            anexoClienteDPR = anexoCliDPR[0]
            linhaAnexoCliDPR = LinhaAnexoClienteDPR(where="anexo_cliente_dpr='{id}'".format(id=anexoClienteDPR['id'])).get()            
            if len(linhaAnexoCliDPR)>0:                
                #CRIACAO DO MODELO XML        
                import xml.dom.minidom
                doc = xml.dom.minidom.Document()
                # Cria os elementos
                tag_dpr_cli = doc.createElement('dpr_cli')
                tag_header = doc.createElement('header')
                tag_linhas = doc.createElement('linhas')
                tag_totais = doc.createElement('totais')
                ##header
                tag_header.setAttribute('ano', str(anexoClienteDPR['ano']))
                tag_header.setAttribute('periodo', str(anexoClienteDPR['periodo']))
                tag_header.setAttribute('cd_af', str(anexoClienteDPR['cd_af']))
                tag_header.setAttribute('nif', str(anexoClienteDPR['nif']))
                tag_header.setAttribute('nome', str(anexoClienteDPR['nome']))
                tag_header.setAttribute('dt_emissao', str(anexoClienteDPR['dt_emissao']))
                tag_header.setAttribute('dec', str(anexoClienteDPR['dec']))                
                ##totais
                tag_totais.setAttribute('vl_recibo', str(anexoClienteDPR['vl_recibo']))
                tag_totais.setAttribute('ir_teu', str(anexoClienteDPR['ir_teu'])) 

                # Cria a estrutura
                doc.appendChild(tag_dpr_cli)
                tag_dpr_cli.appendChild(tag_header)
                tag_dpr_cli.appendChild(tag_linhas)                
                tag_dpr_cli.appendChild(tag_totais)                    
                
                for line in linhaAnexoCliDPR:                    
                    #criar a tag linha
                    tag_linha = doc.createElement('linha')
                    #colocar os valor da linnha
                    tag_linha.setAttribute('designacao',str(line['designacao']))
                    tag_linha.setAttribute('nif',str(line['nif']))
                    tag_linha.setAttribute('origem',str(line['origem']))
                    tag_linha.setAttribute('serie',str(line['serie']))
                    tag_linha.setAttribute('tp_doc',str(line['tp_doc']))
                    tag_linha.setAttribute('num_doc',str(line['num_doc']))                    
                    tag_linha.setAttribute('dt_recibo',str(line['dt_recibo']))                    
                    tag_linha.setAttribute('vl_recibo',str(line['vl_recibo']))                    
                    tag_linha.setAttribute('tipologia',str(line['tipologia']))
                    tag_linha.setAttribute('tx_ret',str(line['tx_ret']))
                    tag_linha.setAttribute('ir_teu',str(line['ir_teu']))
                    tag_linha.setAttribute('tp_oper',str(line['tp_oper']))
                    #adicionar a tag linha na tag linhas
                    tag_linhas.appendChild(tag_linha)               
                #GERANDO O XML
                conteudoXmlCriado= doc.toprettyxml()        
                #colocar o encoding
                conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>')           
        return conteudoFinalXml


    def gerar_xml_fornecedor_dpr(self, key):    
        conteudoFinalXml=' '
        anexoFornDPR = AnexoFornecedorDPR(where="modelo_dpr='{id}'".format(id=key)).get()        
        if anexoFornDPR:              
            anexoFornecedorDPR = anexoFornDPR[0]
            linhaAnexoFornDPR = LinhaAnexoFornecedorDPR(where="anexo_fornecedor_dpr='{id}'".format(id=anexoFornecedorDPR['id'])).get()            
            if len(linhaAnexoFornDPR)>0:               
                #CRIACAO DO MODELO XML        
                import xml.dom.minidom
                doc = xml.dom.minidom.Document()
                # Cria os elementos
                tag_dpr_for = doc.createElement('dpr_for')
                tag_header = doc.createElement('header')
                tag_linhas = doc.createElement('linhas')
                tag_totais = doc.createElement('totais')
                ##header
                tag_header.setAttribute('ano', str(anexoFornecedorDPR['ano']))
                tag_header.setAttribute('periodo', str(anexoFornecedorDPR['periodo']))
                tag_header.setAttribute('cd_af', str(anexoFornecedorDPR['cd_af']))
                tag_header.setAttribute('nif', str(anexoFornecedorDPR['nif']))
                tag_header.setAttribute('nome', str(anexoFornecedorDPR['nome']))
                tag_header.setAttribute('dt_emissao', str(anexoFornecedorDPR['dt_emissao']))
                tag_header.setAttribute('dec', str(anexoFornecedorDPR['dec']))                
                ##totais
                tag_totais.setAttribute('vl_recibo', str(anexoFornecedorDPR['vl_recibo']))
                tag_totais.setAttribute('ir_teu', str(anexoFornecedorDPR['ir_teu'])) 

                # Cria a estrutura
                doc.appendChild(tag_dpr_for)
                tag_dpr_for.appendChild(tag_header)
                tag_dpr_for.appendChild(tag_linhas)                
                tag_dpr_for.appendChild(tag_totais)                    
                
                for line in linhaAnexoFornDPR:                    
                    #criar a tag linha
                    tag_linha = doc.createElement('linha')
                    #colocar os valor da linnha
                    tag_linha.setAttribute('designacao',str(line['designacao']))
                    tag_linha.setAttribute('nif',str(line['nif']))
                    tag_linha.setAttribute('origem',str(line['origem']))
                    tag_linha.setAttribute('serie',str(line['serie']))
                    tag_linha.setAttribute('tp_doc',str(line['tp_doc']))
                    tag_linha.setAttribute('num_doc',str(line['num_doc']))                    
                    tag_linha.setAttribute('dt_recibo',str(line['dt_recibo']))                    
                    tag_linha.setAttribute('vl_recibo',str(line['vl_recibo']))                    
                    tag_linha.setAttribute('tipologia',str(line['tipologia']))
                    tag_linha.setAttribute('tx_ret',str(line['tx_ret']))
                    tag_linha.setAttribute('ir_teu',str(line['ir_teu']))
                    tag_linha.setAttribute('tp_oper',str(line['tp_oper']))
                    #adicionar a tag linha na tag linhas
                    tag_linhas.appendChild(tag_linha)               
                #GERANDO O XML
                conteudoXmlCriado= doc.toprettyxml()        
                #colocar o encoding
                conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>')           
        return conteudoFinalXml





    def gerar_xml_salario_dpr(self, key):
        conteudoFinalXml=' '
        anexoSalDPR = AnexoSalarioDPR(where="modelo_dpr='{id}'".format(id=key)).get()           
        if anexoSalDPR:                          
            anexoSalarioDPR = anexoSalDPR[0]
            linhaAnexoSalDPR = LinhaAnexoSalarioDPR(where="anexo_salario_dpr='{id}'".format(id=anexoSalarioDPR['id'])).get()            
            if len(linhaAnexoSalDPR)>0:                                          
                ##CRIACAO DO MODELO XML        
                import xml.dom.minidom
                doc = xml.dom.minidom.Document()
                ##Cria os elementos
                tag_dpr_sal = doc.createElement('dpr_sal')
                tag_header = doc.createElement('header')
                tag_linhas = doc.createElement('linhas')
                tag_totais = doc.createElement('totais')
                ##header
                tag_header.setAttribute('ano', str(anexoSalarioDPR['ano']))
                tag_header.setAttribute('periodo', str(anexoSalarioDPR['periodo']))
                tag_header.setAttribute('cd_af', str(anexoSalarioDPR['cd_af']))
                tag_header.setAttribute('nif', str(anexoSalarioDPR['nif']))
                tag_header.setAttribute('nome', str(anexoSalarioDPR['nome']))
                tag_header.setAttribute('dt_emissao', str(anexoSalarioDPR['dt_emissao']))
                tag_header.setAttribute('dec', str(anexoSalarioDPR['dec']))                
                ##totais
                tag_totais.setAttribute('base', str(int(to_decimal(anexoSalarioDPR['base']))))
                tag_totais.setAttribute('aces', str(int(to_decimal(anexoSalarioDPR['aces']))))
                tag_totais.setAttribute('isento', str(int(to_decimal(anexoSalarioDPR['isento']))))
                tag_totais.setAttribute('trib', str(int(to_decimal(anexoSalarioDPR['trib']))))
                tag_totais.setAttribute('ir_teu', str(int(to_decimal(anexoSalarioDPR['ir_teu']))))
                tag_totais.setAttribute('inps', str(int(to_decimal(anexoSalarioDPR['inps']))))
                tag_totais.setAttribute('outros', str(int(to_decimal(anexoSalarioDPR['outros']))))
                ##Cria a estrutura
                doc.appendChild(tag_dpr_sal)
                tag_dpr_sal.appendChild(tag_header)
                tag_dpr_sal.appendChild(tag_linhas)                
                tag_dpr_sal.appendChild(tag_totais)            
                
                for line in linhaAnexoSalDPR:                    
                    #criar a tag linha
                    tag_linha = doc.createElement('linha')
                    #colocar os valor da linnha
                    tag_linha.setAttribute('designacao',str(line['designacao']))
                    tag_linha.setAttribute('nif',str(line['nif']))
                    tag_linha.setAttribute('periodo',str(line['periodo']))
                    tag_linha.setAttribute('base',str(int(to_decimal(line['base']))))
                    tag_linha.setAttribute('aces',str(int(to_decimal(line['aces']))))
                    tag_linha.setAttribute('isento',str(int(to_decimal(line['isento']))))                    
                    tag_linha.setAttribute('tipologia',str(line['tipologia']))                    
                    tag_linha.setAttribute('ir_teu',str(int(to_decimal(line['ir_teu']))))                
                    tag_linha.setAttribute('inps',str(int(to_decimal(line['inps']))))
                    tag_linha.setAttribute('outros',str(int(to_decimal(line['outros']))))
                    tag_linha.setAttribute('trib',str(int(to_decimal(line['trib']))))
                    tag_linha.setAttribute('tp_oper',str(line['tp_oper']))
                    #adicionar a tag linha na tag linhas
                    tag_linhas.appendChild(tag_linha)               
                #GERANDO O XML
                conteudoXmlCriado= doc.toprettyxml()        
                #colocar o encoding
                conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>')           
        return conteudoFinalXml


    def getInfoRecibosSalario(self, key):
        self.kargs = get_model_record(model=self, key=key)
        salario = Salario(where="ano='{ano}' AND periodo='{periodo}' AND estado ='Pago' AND tipo_operacao = '{tipo}'".format(ano=self.kargs['ano'], periodo=self.kargs['periodo'], tipo=self.kargs['tipo_operacao'])).get()
        if salario:
            salario =salario[0]
            recibos = ReciboSalario(where="salario='{id}' AND estado = 'Pago'".format(id=salario['id'])).get()
            if recibos:
                #guadar o anexo_salario
                content={
                    'user':self.kargs['user'],
                    'modelo_dpr':str(key),
                    'nome':erp_config.enterprise,
                    'nif':erp_config.nif,
                    'ano':self.kargs['ano'],
                    'periodo':self.kargs['periodo'],
                    'cd_af':self.kargs['cd_af'],
                    'dec':self.kargs['dec'],
                    'dt_emissao':self.kargs['dt_emissao']
                }
                id_anexo = AnexoSalarioDPR(**content).put()
                for recibo in recibos:
                    if recibo['tipo']=='subsidio':
                        este_periodo=recibo['periodo_subsidio']
                    else:
                        este_periodo=recibo['periodo']

                    content={
                        'user':self.kargs['user'],
                        'anexo_salario_dpr': str(id_anexo),
                        'designacao':recibo['nome_funcionario'],
                        'nif':recibo['nif'],
                        'periodo':este_periodo,
                        'base':int(to_decimal(recibo['salario_base'])),
                        'aces':int(to_decimal(recibo['salario_aces'])),
                        'isento':int(to_decimal(recibo['salario_isento'])),
                        'trib':int(to_decimal(recibo['salario_trib'])),
                        'tipologia':recibo['tipologia'],
                        'ir_teu':int(to_decimal(recibo['valor_retido'])),
                        'inps':int(to_decimal(recibo['inps_funcionario']) + to_decimal(recibo['inps_entidade'])),
                        'outros':int(to_decimal(recibo['soat'])+to_decimal(recibo['sindicato'])+to_decimal(recibo['outros_retencoes'])),
                        'tp_oper':recibo['tipo_oper']                        
                    }
                    LinhaAnexoSalarioDPR(**content).put()
                self.kargs['g7']=AnexoSalarioDPR().get_ir_teu(id_anexo) 
                self.put()

