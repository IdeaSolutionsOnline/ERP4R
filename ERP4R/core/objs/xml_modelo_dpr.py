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
__model_name__ = 'xml_modelo_dpr.XMLModeloDPR'

import auth, base_models
from orm import *
from form import *
import erp_config

try:
    from my_area_fiscal import AreaFiscal
except:
    from area_fiscal import AreaFiscal
try:
    from my_anexo_cliente_dpr import XMLAnexoClienteDPR
except:
    from xml_anexo_cliente_dpr import XMLAnexoClienteDPR
try:
    from my_linha_anexo_cliente_dpr import XMLLinhaAnexoClienteDPR
except:
    from xml_linha_anexo_cliente_dpr import XMLLinhaAnexoClienteDPR
try:
    from my_anexo_fornecedor_dpr import XMLAnexoFornecedorDPR
except:
    from xml_anexo_fornecedor_dpr import XMLAnexoFornecedorDPR
try:
    from my_linha_anexo_fornecedor_dpr import XMLLinhaAnexoFornecedorDPR
except:
    from xml_linha_anexo_fornecedor_dpr import XMLLinhaAnexoFornecedorDPR
try:
    from my_anexo_salario_dpr import XMLAnexoSalarioDPR
except:
    from xml_anexo_salario_dpr import XMLAnexoSalarioDPR
try:
    from my_linha_anexo_salario_dpr import XMLLinhaAnexoSalarioDPR
except:
    from xml_linha_anexo_salario_dpr import XMLLinhaAnexoSalarioDPR
try:
    from my_rh_folha_salario import RHFolhaSalario
except:
    from rh_folha_salario import RHFolhaSalario
try:
    from my_rh_recibo_salario import RHReciboSalario
except:
    from rh_recibo_salario import RHReciboSalario
try:
    from my_rh_linha_recibo_salario import RHLinhaReciboSalario
except:
    from rh_linha_recibo_salario import RHLinhaReciboSalario
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro
try:
    from my_factura_cli import FacturaCliente
except:
    from factura_cli import FacturaCliente
try:
    from my_linha_factura_cli import LinhaFacturaCliente
except:
    from linha_factura_cli import LinhaFacturaCliente
try:
    from my_factura_forn import FacturaFornecedor
except:
    from factura_forn import FacturaFornecedor
try:
    from my_linha_factura_forn import LinhaFacturaFornecedor
except:
    from linha_factura_forn import LinhaFacturaFornecedor
try:
    from my_produto import Produto
except:
    from produto import Produto

class XMLModeloDPR(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'xml_modelo_dpr'
        self.__title__ = 'Modelo DPR'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
                      

        self.__auth__ = {
            'read':['All'],
            'write':['Contabilista'],
            'create':['Contabilista'],
            'delete':['Contabilista'],
            'full_access':['Gestor']
            }

        self.__workflow__ = (
            'estado', {'Rascunho':['Verificar'],'Verificado':['Cancelar', 'Confirmar'], 'Confirmado':['Gerar XML'], 'Gerado':['Exportar_Anexo_Salario','Exportar_XML_DPR','Exportar_Anexo_Fornecedor','Exportar_Anexo_Cliente']}
            )

        self.__workflow_auth__ = {             
            'Exportar_Anexo_Fornecedor':['All'],
            'Exportar_Anexo_Cliente':['All'],
            'Exportar_Anexo_Salario':['All'],
            'Exportar_XML_DPR':['All'],
            'Gerar XML':['All'],
            'Confirmar':['All'],
            'Cancelar':['All'],
            'Verificar':['All'],
            'Rascunho':['All'],
            'full_access':['Gestor']
            }

        self.__no_edit__ = [('estado', ['Gerado', 'Cancelado'])]

        self.__tabs__ = [('XML DPR',['xml_dpr']),
                        ('XML Cliente',['xml_cliente']),
                        ('XML Fornecedor',['xml_fornecedor']),
                        ('XML Salário',['xml_salario']),]

        self.dec = combo_field(view_order = 1, name = 'Tipo Declaração', size = 70, default = '1', options = [('1','No Prazo'), ('2','Fora de Prazo'),('4', 'Substituição')], onlist = False)

        self.tipo_operacao = combo_field(view_order = 2, name='Tipo Operação',size=70, default='N', options=[('N','Normal'),('O','Omissão'),('C','Correção Fav. Contribuinte'),('E','Correção Fav. Estado'),('A','Anulado')])

        self.cli = combo_field(view_order = 3, name = 'Anexos Cliente', size=50,args='required',default='1',options=[('0','NAO'),('1','SIM')])

        self.forn = combo_field(view_order = 4, name = 'Anexos Fornecedor', size=45,args='required',default='1',options=[('0','NAO'),('1','SIM')])

        self.sal = combo_field(view_order = 5, name = 'Anexo Salario',size=45,args='required',default='1',options=[('0','NAO'),('1','SIM')])

        self.ano = combo_field(view_order = 6, name ='Ano', args = 'required', size=70, default = datetime.date.today().year, options='model.getAno()')
        
        self.periodo = combo_field(view_order = 7, size=70, name ='Periodo', args = 'required', default = datetime.date.today().strftime("%m"), options='model.getPeriodo()')

        self.cd_af = combo_field(view_order = 8, name = 'Repartição Finanças', size = 70, model = 'area_fiscal', args = 'required', onlist = False, search = False, column = 'local', default='223', options = "model.get_opts('AreaFiscal().get_options_buyable()')")
        
        self.nif = string_field(view_order = 9, name = 'Nif', size = 70, default=erp_config.nif, onlist=False)

        self.nome = string_field(view_order = 10, name = 'Nome', size = 230, default=erp_config.enterprise, onlist=False)

        self.dt_emissao = date_field(view_order = 11, size=70, name ='Data de Emissão', args='required ', default=datetime.date.today())

        self.g1 = currency_field(view_order = 12, name ='G1 Retenções da Categoria A', args='required',size=90,onlist=False)
        self.g2 = currency_field(view_order = 13, name ='G2 Retenções da Categoria B', args='required',size=90,onlist=False)
        self.g3 = currency_field(view_order = 14, name ='G3 Retenções da Categoria C', args='required',size=90,onlist=False)
        self.g4 = currency_field(view_order = 15, name ='G4 Retenções da Categoria D', args='required',size=90,onlist=False)
        self.g5 = currency_field(view_order = 16, name ='G5 Retenções da Categoria D(Pessoa Colectiva)', args='required',size=90,onlist=False)
        self.g6 = currency_field(view_order = 17, name ='G6 Retenções da Categoria E', args='required',size=90,onlist=False)
        self.g7 = currency_field(view_order = 18, name ='G7 Retenções TEU', args='required',size=90,onlist=False)

        self.tp = function_field(view_order = 19, name='Total a Pagar', args='required',size=90,default=0)
        self.obs = text_field(view_order = 20, name='Observações', size = 90, onlist=False, args='rows="1"')
        
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

    def get_tipologiaFuncionario(self, tipoFunc):
        if tipoFunc=='dependente':
            return 'A.1'
        elif tipoFunc=='pensionista':
            return 'A.2'
        elif tipoFunc=='isento':
            return 'A.3'
        else:
            return 'A.4'


    
    def Gerar_XML(self, key, window_id, internal = False):
        """ 
        Metodo para a confirmacao do modelo
        """
        self.kargs = get_model_record(model = self, key = key)
        if self.kargs['estado'] == 'Confirmado':

            xml_sal = self.gerar_xml_salario_dpr(key=key)              
            self.kargs['xml_salario']=xml_sal

            xml_forn = self.gerar_xml_fornecedor_dpr(key=key)              
            self.kargs['xml_fornecedor']=xml_forn 

            xml_cli = self.gerar_xml_cliente_dpr(key=key)
            self.kargs['xml_cliente']=xml_cli

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
        """ Metodo que faz a verificao e geração das informaçoes dos anexos e do proprio modelo 106"""
        self.kargs = get_model_record(model = self, key = key)
        if self.kargs['estado'] == 'Rascunho':            
            #mostrar os anexos desse periodo
            if self.kargs['cli']=='1':
                print("\n\n\n\n\n..................inicio anx cliente......................\n\n\n\n\n")
                self.get_informacao_cliente(key=key)
                print("\n\n\n\n\n..................fim anx cliente......................\n\n\n\n\n")                
                
            if self.kargs['forn']=='1':
                print("\n\n\n\n\n..................inicio anx forn......................\n\n\n\n\n")
                self.get_informacao_fornecedor(key=key)
                print("\n\n\n\n\n..................fim anx forn......................\n\n\n\n\n")                             

            if self.kargs['sal']=='1':
                print("\n\n\n\n\n..................inicio salario......................\n\n\n\n\n")
                self.get_informacao_salario(key=key)
                print("\n\n\n\n\n..................fim salario......................\n\n\n\n\n")
            self.put_informacao_modelo(key=key)               
                
            self.kargs['estado'] = 'Verificado'
            self.put()

            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result

    def put_informacao_modelo(self, key):
        """metodo que coloca as informações dos anexos no modelo dpr"""
        self.kargs = get_model_record(model=self, key=key)
        anexoSal = XMLAnexoSalarioDPR(where="xml_modelo_dpr='{id}'".format(id=key)).get()
        if anexoSal:
            self.kargs['g1']=XMLAnexoSalarioDPR().get_ir_teu(key=anexoSal[0]['id'])

        anexoForn = XMLAnexoFornecedorDPR(where="xml_modelo_dpr='{id}'".format(id=key)).get()
        if anexoForn:
            linhas = XMLLinhaAnexoFornecedorDPR(where="xml_anexo_fornecedor_dpr='{id}'".format(id=anexoForn[0]['id'])).get()
            for linha in linhas:
                if linha['tipologia'] in ('B.1','B.2','B.3','B.4','B.5'):
                    self.kargs['g2']= to_decimal(self.kargs['g2']) + to_decimal(linha['ir_teu'])
                elif linha['tipologia'] in ('C.1','C.2','C.3','C.4'):
                    self.kargs['g3']= to_decimal(self.kargs['g3']) + to_decimal(linha['ir_teu'])
                elif linha['tipologia'] in ('D.1','D.2'):
                    terceiro = Terceiro(where="nome='{nome}' AND nif='{nif}'".format(nome=linha['designacao'], nif=linha['nif'])).get()
                    if terceiro:
                        if terceiro[0]['tipo_entidade']=='pessoa_colectiva':
                            self.kargs['g5']= to_decimal(self.kargs['g5']) + to_decimal(linha['ir_teu'])
                        else:
                            self.kargs['g4']= to_decimal(self.kargs['g4']) + to_decimal(linha['ir_teu'])
                else:
                    self.kargs['g6']= to_decimal(self.kargs['g6']) + to_decimal(linha['ir_teu'])

        anexoCli = XMLAnexoClienteDPR(where="xml_modelo_dpr='{id}'".format(id=key)).get()
        if anexoCli:
            linhas = XMLLinhaAnexoClienteDPR(where="xml_anexo_cliente_dpr='{id}'".format(id=anexoCli[0]['id'])).get()
            for linha in linhas:
                if linha['tipologia'] in ('B.1','B.2','B.3','B.4','B.5'):
                    self.kargs['g2']= to_decimal(self.kargs['g2']) + to_decimal(linha['ir_teu'])
                elif linha['tipologia'] in ('C.1','C.2','C.3','C.4'):
                    self.kargs['g3']= to_decimal(self.kargs['g3']) + to_decimal(linha['ir_teu'])
                elif linha['tipologia'] in ('D.1','D.2'):
                    terceiro = Terceiro(where="nome='{nome}' AND nif='{nif}'".format(nome=linha['designacao'], nif=linha['nif'])).get()
                    if terceiro:
                        if terceiro[0]['tipo_entidade']=='pessoa_colectiva':
                            self.kargs['g5']= to_decimal(self.kargs['g5']) + to_decimal(linha['ir_teu'])
                        else:
                            self.kargs['g4']= to_decimal(self.kargs['g4']) + to_decimal(linha['ir_teu'])
                else:
                    self.kargs['g6']= to_decimal(self.kargs['g6']) + to_decimal(linha['ir_teu'])
        #guardar tudo
        self.put()


    def Exportar_XML_DPR(self, key, window_id):
        modelo = XMLModeloDPR(where="id='{id}'".format(id=key)).get()
        if modelo:
            modelo=modelo[0]            
            return data_to_xml(modelo['xml_dpr'], 'Download', "ModeloDPR_{ano}-{mes}".format(ano=modelo['ano'],mes=modelo['periodo']))
            

    def Exportar_Anexo_Salario(self, key, window_id):
        modelo = XMLModeloDPR(where="id='{id}'".format(id=key)).get()
        if modelo:
            modelo=modelo[0]            
            return data_to_xml(modelo['xml_salario'], 'Download', "AnexoDPR_Salario_{ano}-{mes}".format(ano=modelo['ano'],mes=modelo['periodo']))
            

    def Exportar_Anexo_Fornecedor(self, key, window_id):
        modelo = XMLModeloDPR(where="id='{id}'".format(id=key)).get()
        if modelo:
            modelo=modelo[0]            
            return data_to_xml(modelo['xml_fornecedor'], 'Download', "AnexoDPR_Fornecedor_{ano}-{mes}".format(ano=modelo['ano'],mes=modelo['periodo']))
            

    def Exportar_Anexo_Cliente(self, key, window_id):
        modelo = XMLModeloDPR(where="id='{id}'".format(id=key)).get()
        if modelo:
            modelo=modelo[0]            
            return data_to_xml(modelo['xml_cliente'], 'Download', "AnexoDPR_Cliente_{ano}-{mes}".format(ano=modelo['ano'],mes=modelo['periodo']))
            
    
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

    def Cancelar(self, key, window_id, internal = False):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado']='Cancelado'
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
            #CRIACAO DO XML DO MODELO DPR       
            import xml.dom.minidom
            doc = xml.dom.minidom.Document()
            # Cria os elementos
            tag_dpr_mod = doc.createElement('dpr_mod')
            tag_header = doc.createElement('header')
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
            
            doc.appendChild(tag_dpr_mod)
            tag_dpr_mod.appendChild(tag_header)               
            for campo in ('g1','g2','g3','g4','g5','g6','g7'):
                tag = doc.createElement(campo)
                if int(to_decimal(modelo[campo]))!=0:
                    tag.appendChild(doc.createTextNode(str(int(to_decimal(modelo[campo])))))
                tag_dpr_mod.appendChild(tag)

            tag_tp.appendChild(doc.createTextNode(str(self.get_tp(key=key))))
            tag_obs.appendChild(doc.createTextNode(str(modelo['obs'])))         
            tag_dt_emissao.appendChild(doc.createTextNode(str(modelo['dt_emissao'])))
             
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
        anexoCliDPR = XMLAnexoClienteDPR(where="xml_modelo_dpr='{id}'".format(id=key)).get()        
        if anexoCliDPR:
            anexoClienteDPR = anexoCliDPR[0]
            linhaAnexoCliDPR = XMLLinhaAnexoClienteDPR(where="xml_anexo_cliente_dpr='{id}'".format(id=anexoClienteDPR['id'])).get()            
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
                tag_totais.setAttribute('vl_recibo', str(int(to_decimal(XMLAnexoClienteDPR().get_vl_recibo(key=anexoClienteDPR['id'])))))
                tag_totais.setAttribute('ir_teu', str(int(to_decimal(XMLAnexoClienteDPR().get_ir_teu(key=anexoClienteDPR['id'])))))

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
        anexoFornDPR = XMLAnexoFornecedorDPR(where="xml_modelo_dpr='{id}'".format(id=key)).get()        
        if anexoFornDPR:              
            anexoFornecedorDPR = anexoFornDPR[0]
            linhaAnexoFornDPR = XMLLinhaAnexoFornecedorDPR(where="xml_anexo_fornecedor_dpr='{id}'".format(id=anexoFornecedorDPR['id'])).get()            
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
                tag_totais.setAttribute('vl_recibo', str(int(to_decimal(XMLAnexoFornecedorDPR().get_vl_recibo(key=anexoFornecedorDPR['id'])))))
                tag_totais.setAttribute('ir_teu', str(int(to_decimal(XMLAnexoFornecedorDPR().get_ir_teu(key=anexoFornecedorDPR['id']))))) 

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
        anexoSalDPR = XMLAnexoSalarioDPR(where="xml_modelo_dpr='{id}'".format(id=key)).get()           
        if anexoSalDPR:                          
            anexoSalarioDPR = anexoSalDPR[0]
            linhaAnexoSalDPR = XMLLinhaAnexoSalarioDPR(where="xml_anexo_salario_dpr='{id}'".format(id=anexoSalarioDPR['id'])).get()            
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
                tag_totais.setAttribute('base', str(int(to_decimal(XMLAnexoSalarioDPR().get_base(key=anexoSalarioDPR['id'])))))
                tag_totais.setAttribute('aces', str(int(to_decimal(XMLAnexoSalarioDPR().get_aces(key=anexoSalarioDPR['id'])))))
                tag_totais.setAttribute('isento', str(int(to_decimal(XMLAnexoSalarioDPR().get_isento(key=anexoSalarioDPR['id'])))))
                tag_totais.setAttribute('trib', str(int(to_decimal(XMLAnexoSalarioDPR().get_trib(key=anexoSalarioDPR['id'])))))
                tag_totais.setAttribute('ir_teu', str(int(to_decimal(XMLAnexoSalarioDPR().get_ir_teu(key=anexoSalarioDPR['id'])))))
                tag_totais.setAttribute('inps', str(int(to_decimal(XMLAnexoSalarioDPR().get_inps(key=anexoSalarioDPR['id'])))))
                tag_totais.setAttribute('outros', str(int(to_decimal(XMLAnexoSalarioDPR().get_outros(key=anexoSalarioDPR['id'])))))
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


    def get_informacao_salario(self, key):
        self.kargs = get_model_record(model=self, key=key)
        salarios = RHFolhaSalario(where="to_char(date_create,'YYYY-MM')='{ano}-{periodo}' AND (estado='Recibos Confirmado' OR estado='Pago')".format(ano=self.kargs['ano'], periodo=self.kargs['periodo'])).get()
        if salarios:            
            #guadar o anexo_salario
            content={
                'user':self.kargs['user'],
                'xml_modelo_dpr':str(key),
                'nome':erp_config.enterprise,
                'nif':erp_config.nif,
                'ano':self.kargs['ano'],
                'periodo':self.kargs['periodo'],
                'cd_af':self.kargs['cd_af'],
                'dec':self.kargs['dec'],
                'dt_emissao':self.kargs['dt_emissao']
            }
            id_anexo = XMLAnexoSalarioDPR(**content).put()
            for salario in salarios:
                recibos = RHReciboSalario(where="rh_folha_salario='{id}' AND (estado='Confirmado' OR estado='Pago')".format(id=salario['id'])).get()
                if recibos:
                    for recibo in recibos:
                        terceiro = Terceiro(where="id='{ter}'".format(ter=recibo['terceiro'])).get()
                        content={
                            'user':self.kargs['user'],
                            'xml_anexo_salario_dpr': str(id_anexo),
                            'designacao':terceiro[0]['nome'],
                            'nif':terceiro[0]['nif'],
                            'periodo':"{ano}-{mes}".format(ano=recibo['ano'], mes=recibo['periodo']),
                            'base':int(RHReciboSalario().get_salario(key=recibo['id'])),
                            'aces':int(RHReciboSalario().get_rendimentosAcessorios(key=recibo['id'])),
                            'isento':int(RHReciboSalario().get_rendimentosIsentos(key=recibo['id'])),
                            'trib':int(RHReciboSalario().get_rendimentosTributaveis(key=recibo['id'])),
                            'tipologia':self.get_tipologiaFuncionario(tipoFunc=recibo['tipo_funcionario']),
                            'ir_teu':int(RHReciboSalario().get_retencao(key=recibo['id'])),
                            'inps':int(RHReciboSalario().get_segurancaSocial(key=recibo['id'])),
                            'outros':int(RHReciboSalario().get_outrosRetencoes(key=recibo['id'])),
                            'tp_oper':self.kargs['tipo_operacao']                        
                        }
                        XMLLinhaAnexoSalarioDPR(**content).put()


    def get_tipologiaCliFornecedor(self, rendimento, entidade):
        """RETORNA A INFORMACAO DA TIPOLOGIA DO ANEXO DE CLIENTE OU FORNECEDOR"""
        if rendimento == 'rend_predial':
            if entidade=='singular_sem_contab':
                return 'C.1'
            elif entidade=='singular_com_contab':
                return 'C.2'
            elif entidade =='regime_simplificado':
                return 'C.3'
            else:
                return 'C.4'
        elif rendimento=='rend_de_capitais':
            return 'D.1'
        elif rendimento =='ganhos_patrimoniais':
            return 'E.1'
        else:
            if entidade=='nao_residente':
                return 'B.5'
            elif entidade=='singular_com_contab':
                return 'B.2'
            elif entidade =='regime_simplificado':
                return 'B.3'
            elif entidade == 'pessoa_colectiva':
                return 'B.4'
            else:
                #pessoa singular sem contabilidade organizada
                return 'B.1'


    def get_informacao_fornecedor(self, key):
        self.kargs = get_model_record(model=self, key=key)
        if self.kargs['forn']=='1':
            facturas = FacturaFornecedor(where="retencao='SIM' AND to_char(date_create,'YYYY-MM')='{ano}-{mes}'".format(ano=self.kargs['ano'], mes=self.kargs['periodo'])).get()
            if facturas: 
                print("\n\n\n\nRRRRRRRRRRRRRRRRRRRRRR\n\n", facturas,"\nRRRRRRRRRRRRRRRRRRRRR\n\n\n\n")              
                content={
                    'user':self.kargs['user'],
                    'xml_modelo_dpr':str(key),
                    'estado':'Gerado',
                    'nome':erp_config.enterprise,
                    'nif':erp_config.nif,
                    'ano':self.kargs['ano'],
                    'periodo':self.kargs['periodo'],
                    'cd_af':self.kargs['cd_af'],
                    'dec':self.kargs['dec'],
                    'dt_emissao':self.kargs['dt_emissao']
                }
                id_anexo = XMLAnexoFornecedorDPR(**content).put()

                for factura in facturas:                        
                    terceiro = Terceiro(where="id='{id}'".format(id=factura['fornecedor'])).get()
                    if terceiro:
                        terceiro =terceiro[0]
                        linhas = LinhaFacturaFornecedor(where="factura_forn='{id}'".format(id=factura['id'])).get()
                        if linhas:
                            produto = Produto(where="id='{id}'".format(id=linhas[0]['produto'])).get()
                            if produto:                        
                                content={
                                    'user':self.kargs['user'],
                                    'xml_anexo_fornecedor_dpr': str(id_anexo),
                                    'origem':terceiro['origem'],
                                    'designacao':terceiro['nome'],
                                    'nif':terceiro['nif'],
                                    'tp_doc':'FT',
                                    'serie':factura['serie'],
                                    'num_doc':factura['numero'],
                                    'dt_recibo':factura['data'],
                                    'vl_recibo':factura['total'],
                                    'tipologia':self.get_tipologiaCliFornecedor(rendimento=produto[0]['tipologia'],entidade=terceiro['tipo_entidade']),
                                    'tx_ret':int(to_decimal(factura['taxa_retencao'])),
                                    'ir_teu':factura['valor_retido'],
                                    'tp_oper':self.kargs['tipo_operacao']                        
                                }
                                XMLLinhaAnexoFornecedorDPR(**content).put()
                


    def get_informacao_cliente(self, key):        
        self.kargs = get_model_record(model=self, key=key)
        if self.kargs['cli']=='1':
            facturas = FacturaCliente(where="retencao='SIM' AND to_char(date_create,'YYYY-MM')='{ano}-{mes}'".format(ano=self.kargs['ano'], mes=self.kargs['periodo'])).get()
            if facturas:
                print("\n\n\n\n\n..................",facturas,"......................\n\n\n\n\n")            
                content={
                    'user':self.kargs['user'],
                    'xml_modelo_dpr':str(key),
                    'estado':'Gerado',
                    'nome':erp_config.enterprise,
                    'nif':erp_config.nif,
                    'ano':self.kargs['ano'],
                    'periodo':self.kargs['periodo'],
                    'cd_af':self.kargs['cd_af'],
                    'dec':self.kargs['dec'],
                    'dt_emissao':self.kargs['dt_emissao']
                }
                id_anexo = XMLAnexoClienteDPR(**content).put()
                for factura in facturas:                    
                    print(factura)                      
                    terceiro = Terceiro(where="id='{id}'".format(id=factura['cliente'])).get()
                    if terceiro:                        
                        terceiro =terceiro[0]
                        linhas = LinhaFacturaCliente(where="factura_cli='{id}'".format(id=factura['id'])).get()
                        if linhas:
                            produto = Produto(where="id='{id}'".format(id=linhas[0]['produto'])).get()
                            if produto:                        
                                content={
                                    'user':self.kargs['user'],
                                    'xml_anexo_cliente_dpr': str(id_anexo),
                                    'origem':terceiro['origem'],
                                    'designacao':terceiro['nome'],
                                    'nif':terceiro['nif'],
                                    'tp_doc':'FT',
                                    'serie':factura['serie'],
                                    'num_doc':factura['numero'],
                                    'dt_recibo':factura['data'],
                                    'vl_recibo':factura['total'],
                                    'tipologia':self.get_tipologiaCliFornecedor(rendimento=produto[0]['tipologia'],entidade=terceiro['tipo_entidade']),
                                    'tx_ret':int(to_decimal(factura['taxa_retencao'])),
                                    'ir_teu':factura['valor_retido'],
                                    'tp_oper':self.kargs['tipo_operacao']                        
                                }
                                XMLLinhaAnexoClienteDPR(**content).put()