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
__model_name__ = 'modelo106.Modelo106'
import auth, base_models
from orm import *
from form import *
from area_fiscal import AreaFiscal
import erp_config
from anexo_clientes import AnexoClientes
from linha_anexo_cliente import LinhaAnexoCliente
from anexo_fornecedor import AnexoFornecedor
from linha_anexo_fornecedor import LinhaAnexoFornecedor
from factura_cli import FacturaCliente
from factura_forn import FacturaFornecedor
from terceiro import Terceiro
from codigo_pais import CodigoPais
from linha_factura_cli import LinhaFacturaCliente
from linha_factura_forn import LinhaFacturaFornecedor
from anexo_reg_fornecedor import AnexoRegFornecedor
from linha_anexo_reg_fornecedor import LinhaAnexoRegFornecedor

from anexo_reg_cliente import AnexoRegCliente
from linha_anexo_reg_cliente import LinhaAnexoRegCliente

class Modelo106(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'modelo106'
        self.__title__ = 'Modelo 106'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']

        self.__workflow__ = (
            'estado', {'Rascunho':['Verificar'],'Verificado':['Rascunho', 'Confirmar'], 'Confirmado':['Gerar Mod106']}
            )

        self.__workflow_auth__ = {
            'Gerar Mod106':['All'],
            'Confirmar':['All'],
            'Verificar':['All'],
            'Rascunho':['All'],
            'full_access':['Gestor']
            }       

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.__tabs__ = [ 
            ('Regularização Fornecedor', ['anexo_reg_fornecedor',]),     
            ('Anexo Cliente', ['anexo_clientes']), 
            ('Anexo Fornecedor', ['anexo_fornecedor']),
            ('Regularização Cliente', ['anexo_reg_cliente']),
            ('Campos do Modelo',['cp01','cp02','cp03','cp04','cp05','cp06','cp07','cp08','cp09','cp10','cp11','cp12','cp13','cp14','cp15','cp16','cp17','cp18','cp19','cp20','cp21','cp22','cp23','cp24','cp25','cp26','cp27','cp28','cp29','cp30','cp31','cp32','cp33','cp34','cp35','cp36','cp37','cp38','cp39','cp40','cp41','cp42','cp43','cp44','cp45','cp46','cp47','cp48','cp49','cp50']),
            ('XML',['xml'])]


        self.nome = string_field(view_order = 1, name = 'Nome', size = 70, default='modelo106_{data}'.format(data=datetime.date.today()))

       	self.tipo_declaracao = combo_field(view_order = 2, name = 'Tipo Declaração', size = 65, default = '1', options = [('1','No Prazo'), ('2','Fora de Prazo'),('4', 'Substituição')], onlist = False)        
        
        self.nif=string_field(view_order=3, name='Nif', size=55, default=erp_config.nif)

        self.ano = combo_field(view_order = 4, name ='Ano', args = 'required', size = 50, default = datetime.date.today().year, options='model.getAno()')

        self.mes = combo_field(view_order = 5, name ='Mês',args = 'required', default=datetime.date.today().strftime("%m"), options =[('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Novembro'),('12','Dezembro')])

        self.anexo_cli = combo_field(view_order = 6, name = 'Anexos Cliente',onlist=False, size=75, args='required',default='0',options=[('0','--NÃO--'),('1','--SIM--')])

        self.anexo_forn = combo_field(view_order = 7, name = 'Anexos Fornecedor',onlist=False, size=65,args='required',default='0',options=[('0','--NÃO--'),('1','--SIM--')])

        self.anexo_reg_cli = combo_field(view_order = 8, name = 'Regularização Cliente',onlist=False,size=50,args='required',default='0',options=[('0','--NÃO--'),('1','--SIM--')])

        self.anexo_reg_forn = combo_field(view_order = 9, name = 'Regularização Fornecedor',onlist=False,size=50,args='required',default='0',options=[('0','--NÃO--'),('1','--SIM--')])

        self.area_fiscal = combo_field(view_order = 10, name = 'Área Fiscal', size = 50, model = 'area_fiscal',args = 'required', onlist = False, search = True, column = 'codigo', options = "model.get_opts('AreaFiscal().get_options_buyable()')")
        
        self.operacoes = combo_field(view_order = 11, name = 'Tipo de Operacoes', args='required', size = 75, default = '1', options = [('0','Activas e/ou Passivas'), ('1','Inexistência de operações'),('2', 'Unica Operação 1ª vez')], onlist = False)
        
        self.nif_tecnico = string_field(view_order = 12, name = 'Nif do Técnico O.C.', onlist=False,size = 65)

        self.num_reg_tec_ordem = string_field(view_order = 13, name = 'Nº Técnico O.C.',onlist=False, size = 55)

        self.data_apresentacao = date_field(view_order=14, size=62, name ='Data de Apresentação', args='required ', default=datetime.date.today())

        self.data_recepcao = date_field(view_order=15, size=60, name ='Data de Recepção', default=datetime.date.today())       
        
        

        self.local_apresentacao = combo_field(view_order = 16, name = 'Local de Apresentação', size = 75, model = 'area_fiscal', args = 'required', onlist = False, search = False, column = 'local', options = "model.get_opts('AreaFiscal().get_options()')")

        self.observacoes = text_field(view_order=17, name='Observações', size = 235,onlist=False)
        
        #50 campos do modelo
        self.cp01 = currency_field(view_order= 18, name ='[01] Base Tributavel Taxa Normal', args='required', size=70,onlist=False)
        self.cp02 = currency_field(view_order= 19, name ='[02] Imp. Favor Estado Taxa Normal', args='required',size=70,onlist=False)
        
        self.cp03 = currency_field(view_order= 20, name ='[03] Base Tributavel Taxa Especial', args='required',size=70,onlist=False)
        self.cp04 = currency_field(view_order= 21, name ='[04] Imp. Favor Estado Taxa Especial', args='required',size=70,onlist=False)

        self.cp05 = currency_field(view_order= 22, name ='[05] Base Trib. IVA Liq. Operaçoes(Dec. - Lei nº 16/2004)', args='required',size=90,onlist=False)
        self.cp06 = currency_field(view_order= 23, name ='[06] IVA Favor Estado', args ='required',size=90,onlist=False)
        
        self.cp07 = currency_field(view_order= 24, name ='[07] IVA Liquidado pelo Contratante', args='required',size=90,onlist=False)
        
        self.cp08 = currency_field(view_order= 25, name ='[08] Bens/Serv Isentas Com Direito a Dedução', args='required',size=90,onlist=False)
        
        self.cp09 = currency_field(view_order= 26, name ='[09] Bens/Serv Isentas Sem Direito a Dedução', args='required',size=90,onlist=False)
        
        self.cp10 = currency_field(view_order= 27, name ='[10] Bens/Serv Não tributados (art. 6º, nº 7 do RIVA)', args='required',size=90,onlist=False)
        
        self.cp11 = currency_field(view_order= 28, name ='[11] Base Tributavel - Prestador Serviço Estrageiro', args='required',size=90,onlist=False)
        self.cp12 = currency_field(view_order= 29, name ='[12] Imp. Liq. Favor Sujeito - Prestador Serviço Estrageiro', args='required',size=90,onlist=False)
        self.cp13 = currency_field(view_order= 30, name ='[13] Imp. Liq. Favor Estado - Prestador Serviço Estrageiro', args='required',size=90,onlist=False)
        
        self.cp14 = currency_field(view_order= 31, name ='[14] Base Tributavel - Serviços Costrução. Civil', args='required',size=90,onlist=False)
        self.cp15 = currency_field(view_order= 32, name ='[15] IVA Favor Sujeito - Serviços Costrução. Civil', args='required',size=90,onlist=False)
        self.cp16 = currency_field(view_order= 33, name ='[16] IVA Favor Estado - Serviços Costrução. Civil', args='required',size=90,onlist=False)
        
        self.cp17 = currency_field(view_order= 34, name ='[17] Base Trib. Bens/Serv - Investimentos', args='required',size=90,onlist=False)
        self.cp18 = currency_field(view_order= 35, name ='[18] Imposto Favor Sujeito - Investimentos', args='required',size=120,onlist=False)
        
        self.cp19 = currency_field(view_order= 36, name ='[19] Base Trib. Bens/Serv - Inventários', args='required',size=90,onlist=False)
        self.cp20 = currency_field(view_order= 37, name ='[20] Imposto Favor Sujeito - Inventários', args='required',size=120,onlist=False)
        
        self.cp21 = currency_field(view_order= 38, name ='[21] Base Trib. Bens/Serv - O.Bens de Consumo', args='required',size=90,onlist=False)
        self.cp22 = currency_field(view_order= 39, name ='[22] Imposto Favor Sujeito - O.Bens de Consumo', args='required',size=120,onlist=False)
        
        self.cp23 = currency_field(view_order= 40, name ='[23] Base Trib. Bens/Serv - Serviços', args='required',size=90,onlist=False)
        self.cp24 = currency_field(view_order= 41, name ='[24] Imposto Favor Sujeito - Serviços', args='required',size=120,onlist=False)
        
        self.cp25 = currency_field(view_order= 42, name ='[25] Base Trib. Import. Bens efectuados pelo SP', args='required',size=90,onlist=False)
        self.cp26 = currency_field(view_order= 43, name ='[26] Imp. Favor Sujeito- Import. Bens efectuados pelo SP', args='required',size=120,onlist=False)
        
        self.cp27 = currency_field(view_order= 44, name ='[27] Regularização F.Sujeito- Comunicada pela Adm.Fiscal.', args='required',size=120,onlist=False)
        self.cp28 = currency_field(view_order= 45, name ='[28] Regularização F.Estado- Comunicada pela Adm.Fiscal', args='required',size=120,onlist=False)
        
        self.cp29 = currency_field(view_order= 46, name ='[29] Regularização F.Sujeito-Comunicada pelo Contribuinte', args='required',size=120,onlist=False)
        self.cp30 = currency_field(view_order= 47, name ='[30] Regularização F.Estado-Comunicada pelo Contribuinte', args='required',size=120,onlist=False)
        
        self.cp31 = currency_field(view_order= 48, name ='[31] Percentagem Estimada ( dedução parcial pro rata )', args='required',size=270,onlist=False)

        self.cp32 = currency_field(view_order= 49, name ='[32] Soma B.T.(01+03+05+07+08+09+10+11+14+17+19+21+23+25)', args='readonly',size=120,onlist=False)
        self.cp33 = currency_field(view_order= 50, name ='[33] Soma I.F.S.(12+15+18+20+22+24+26+27+29)', args='readonly',size=90,onlist=False)
        self.cp34 = currency_field(view_order= 51, name ='[34] Soma I.F.E.(02+04+06+13+16+28+30)', args='readonly',size=70,onlist=False)

        self.cp35 = currency_field(view_order= 52, name ='[35] Apuramento F. Estado(34-33)', args='readonly',size=70,onlist=False)
        self.cp36 = currency_field(view_order= 53, name ='[36] Apuramento F. Sujeito(33-34)', args='readonly',size=70,onlist=False)
        
        self.cp37 = currency_field(view_order= 54, name ='[37] Excesso a Reportar P.Anteriores', args='required',size=70,onlist=False)
        self.cp38 = currency_field(view_order= 55, name ='[38] Imp. a Pagar ao Estado', args='readonly',size=70,onlist=False)
        self.cp39 = currency_field(view_order= 56, name ='[39] Crédito de Imposto', args='required',size=70,onlist=False)
        self.cp40 = currency_field(view_order= 57, name ='[40] Reporte p/ Periodo Seg.', args='required',size=70,onlist=False)
        self.cp41 = currency_field(view_order= 58, name ='[41] Pedido de Reembolso', args='required',size=70,onlist=False)
        self.cp42 = currency_field(view_order= 59, name ='[42] Adiant./trans.bens e serv tributadas', args='required',size=70,onlist=False)
        self.cp43 = currency_field(view_order= 60, name ='[43] Amostras/ofertas além limite legal', args='required',size=70,onlist=False)
        self.cp44 = currency_field(view_order= 61, name ='[44] Op. sujeitas a tributação da margem', args='required',size=70,onlist=False)
        self.cp45 = currency_field(view_order= 62, name ='[45] Outras Operações- art. 3º e 4º RIVA', args='required',size=70,onlist=False)
        self.cp46 = currency_field(view_order= 63, name ='[46] Op. Destinadas a Exportação', args='required',size=70,onlist=False)
        self.cp47 = currency_field(view_order= 64, name ='[47] Oper.efetuadas-Decreto-Lei 88/2005', args='required',size=70,onlist=False)
        self.cp48 = currency_field(view_order= 65, name ='[48] Bens da Lista Anexa', args='required',size=70,onlist=False)
        self.cp49 = currency_field(view_order= 66, name ='[49] Faturas de prest.serviços emitadas', args='required',size=70,onlist=False)
        self.cp50 = currency_field(view_order= 67, name ='[50] Recibos de prest.serviços faturados', args='required',size=70,onlist=False)
        
        self.estado = info_field(view_order = 68, name ='Estado', hidden = True, default='Rascunho')

        self.anexo_clientes = list_field(view_order = 69, name= '', nolabel =True, args ='readonly', condition = "modelo106='{id}'", model_name = 'anexo_clientes.AnexoClientes', list_edit_mode = 'edit', onlist = False)        

        self.anexo_fornecedor = list_field(view_order = 70, name= '', nolabel =True, args ='readonly', condition = "modelo106='{id}'", model_name = 'anexo_fornecedor.AnexoFornecedor', list_edit_mode = 'edit', onlist = False)

        self.anexo_reg_fornecedor = list_field(view_order = 71, name= '', nolabel =True, args ='readonly', condition = "modelo106='{id}'", model_name = 'anexo_reg_fornecedor.AnexoRegFornecedor', list_edit_mode = 'edit', onlist = False)

        self.anexo_reg_cliente = list_field(view_order = 72, name= '', nolabel =True, args ='readonly', condition = "modelo106='{id}'", model_name = 'anexo_reg_cliente.AnexoRegCliente', list_edit_mode = 'edit', onlist = False)

        self.xml = text_field(view_order = 73, name="XML", size = 320, onlist = False, args='rows=20')


    def get_opts(self, get_str):       
        return eval(get_str)


    def getAno(self):
        options = []
        opts = range(2014,2051)
        for option in opts:
            options.append((str(option), str(option)))
        return options


    def Verificar(self, key, window_id, internal = False):
        """ 
        Metodo que faz a verificao e geração dos anexos do modelo 106
        """
        self.kargs = get_model_record(model = self, key = key)
        if self.kargs['estado'] == 'Rascunho':            
            #gerar os anexos
            if self.kargs['anexo_cli']=='1':
                self.Gerar_Anexo_Cliente(key=key)

            if self.kargs['anexo_forn']=='1':
                self.Gerar_Anexo_Fornecedor(key=key)

            if self.kargs['anexo_reg_cli']=='1':
                self.Gerar_Anexo_Reg_Cliente(key=key)

            if self.kargs['anexo_reg_forn']=='1':
                self.Gerar_Anexo_Reg_Fornecedor(key=key)

            #calcular os totais
            self.put()
            self.kargs['cp32'] = str(int(self.get_cp32(key=key)))
            self.kargs['cp33'] = str(int(self.get_cp33(key=key)))
            self.kargs['cp34'] = str(int(self.get_cp34(key=key)))
            #é preciso guardar estes calculos para poder assim efectuar os novos (35 e 36)
            self.put()
            self.kargs['cp35'] = str(int(self.get_cp35(key=key)))
            self.kargs['cp36'] = str(int(self.get_cp36(key=key)))            
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
            self.kargs['cp38'] = str(int(self.get_cp38(key=key)))
            self.kargs['estado'] = 'Confirmado'
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result


    def Rascunho(self, key, window_id, internal = False):
        self.kargs = get_model_record(model=self, key=key)
        if self.kargs['estado'] == 'Verificado':            
            for x in range(1,51):
                if x<10:
                    campo="cp0{num}".format(num=x)
                else:
                    campo="cp{num}".format(num=x)
                try:                
                    self.kargs[campo]=to_decimal(0)
                except:
                    pass
            self.kargs['estado']='Rascunho'
            self.put() 

            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result


    def get_record_info(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            record = Modelo106(where="id = '{id}'".format(id=key)).get()
            return record[0]
        return erp_cache.get(key=self.__model_name__ + str(key), createfunc=get_results)

    def get_record_info_to3536(self, key):
        #esta função é uma função intermédia para evidar multiplos hit's na base de dados, desta forma só fazemos o request uma unica vez para todas as funções
        def get_results():
            record = Modelo106(where="id = '{id}'".format(id=key)).get()
            return record[0]
        return erp_cache.get(key=self.__model_name__ +'3536'+ str(key), createfunc=get_results)


    def get_cp32(self, key):
        record = self.get_record_info(key=key)
        soma=to_decimal(0)
        try:
            for x in ('01','03','05','07','08','09','10','11','14','17','19','21','23','25'):
                campo = "cp{x}".format(x=x)
                if record[campo] not in(None,'','None',0):
                    soma += to_decimal(int(record[campo]))
            return int(soma)
        except:
            return int(to_decimal(0))
        

    def get_cp33(self, key):
        record = self.get_record_info(key=key)
        soma=to_decimal(0)
        try:
            for x in ('12','15','18','20','22','24','26','27','29'):
                campo = "cp{x}".format(x=x)
                if record[campo] not in(None,'','None',0):
                    soma += to_decimal(int(record[campo]))
            return int(soma)
        except:
            return int(to_decimal(0))


    def get_cp34(self, key):
        record = self.get_record_info(key=key)
        soma=to_decimal(0)
        try:
            for x in ('02','04','06','13','16','28','30'):
                campo = "cp{x}".format(x=x)
                if record[campo] not in(None,'','None',0):
                    soma += to_decimal(int(record[campo]))
            return int(soma)
        except:
            return int(to_decimal(0))


    def get_cp35(self, key):
        record = self.get_record_info_to3536(key=key)
        diferenca =to_decimal(0)
        if to_decimal(record['cp34']) > to_decimal(record['cp33']):
            diferenca = to_decimal(record['cp34']) - to_decimal(record['cp33'])
        return int(diferenca)

    def get_cp36(self, key):
        record = self.get_record_info_to3536(key=key)
        diferenca =to_decimal(0)
        if to_decimal(record['cp34']) < to_decimal(record['cp33']):
            diferenca = to_decimal(record['cp33']) - to_decimal(record['cp34'])
        return int(diferenca)

    def get_cp38(self, key):
        self.kargs = get_model_record(model=self,key=key)
        diferenca = to_decimal(0)
        if self.kargs['tipo_declaracao']=='1':
            if to_decimal(self.kargs['cp35']) >= to_decimal(self.kargs['cp37']):
                diferenca = to_decimal(self.kargs['cp35']) - to_decimal(self.kargs['cp37'])
        return int(diferenca)

    #define a tipologia do anexo de regularizacao segundo o tipo de produto da linha de factura
    def getTipologia(self, tipo_produto):
        """
        retorna a tipologia da linha de anexo regularizacao baseado no tipo de produto
        """
        if tipo_produto in ('servico','','None',None):
            #servico
            return 'SRV'
        elif tipo_produto == 'consumivel':
            #outros bens de consumo
            return 'OBC'
        elif tipo_produto == 'imobilizado':
            #investimento
            return 'IMO'
        elif tipo_produto in ('armazenavel','produzido'):
            #inventario
            return 'INV'



    """Metodo para gerar o anexo fornecedor"""  
    def Gerar_Anexo_Fornecedor(self, key):
        informacoes = self.get_info_anexo_forn(key)
        if len(informacoes) > 0:
            self.guardar_anexo_forn(key=key, info_anexo=informacoes[0]['info_anexo'], info_linhas=informacoes[0]['info_linhas'])


    """ Metodo para gerar o anexo cliente """
    def Gerar_Anexo_Cliente(self, key):
        informacoes = self.get_info_anexo_cli(key)
        if len(informacoes) > 0:
            self.guardar_anexo_cli(key=key, info_anexo=informacoes[0]['info_anexo'], info_linhas=informacoes[0]['info_linhas'])



    def Gerar_Anexo_Reg_Fornecedor(self, key):        
        self.guardar_regularizacao_forn(key=key)
        #gerar o xml
        self.gerar_xml_reg_forn(key=key)



    def Gerar_Anexo_Reg_Cliente(self, key):
        self.guardar_regularizacao_cli(key=key)
        #gerar o xml        
        self.gerar_xml_reg_cli(key=key)



    """ Metodo para gerar o arquivo xml do modelo 106 """
    def Gerar_Mod106(self, key, window_id):
        
        self.kargs = get_model_record(model=self, key=key)        

        areaFiscal = AreaFiscal(where="id='{id}'".format(id=self.kargs['local_apresentacao'])).get()
        nome_local_apresentacao = areaFiscal[0]['local']        
        import xml.dom.minidom
        doc = xml.dom.minidom.Document()
        tag_modelo106 = doc.createElement('modelo106')
        tag_tp_dec_anx = doc.createElement('tp_dec_anx')
        tag_nif = doc.createElement('nif')
        tag_periodo = doc.createElement('periodo')
        tag_cd_af = doc.createElement('cd_af')
        tag_exist_oper = doc.createElement('exist_oper')
        tag_dt_apresentacao = doc.createElement('dt_apresentacao')
        tag_loc_apresentacao = doc.createElement('loc_apresentacao')
        tag_nif_toc = doc.createElement('nif_toc')
        tag_num_ordem_toc = doc.createElement('num_ordem_toc')
        tag_dt_recepcao = doc.createElement('dt_recepcao')
        tag_obs = doc.createElement('obs')
        tag_tp_dec_anx.setAttribute('dec', str(self.kargs['tipo_declaracao']))
        tag_tp_dec_anx.setAttribute('cli', str(self.kargs['anexo_cli']))
        tag_tp_dec_anx.setAttribute('for', str(self.kargs['anexo_forn']))
        tag_tp_dec_anx.setAttribute('cli_reg', str(self.kargs['anexo_reg_cli']))
        tag_tp_dec_anx.setAttribute('for_reg', str(self.kargs['anexo_reg_forn']))
        tag_periodo.setAttribute('ano', str(self.kargs['ano']))
        tag_periodo.setAttribute('mes', str(self.kargs['mes']))
        ######################################        
        # Cria a estrutura
        doc.appendChild(tag_modelo106)
        tag_modelo106.appendChild(tag_tp_dec_anx)
        tag_modelo106.appendChild(tag_nif)
        tag_modelo106.appendChild(tag_periodo)
        tag_modelo106.appendChild(tag_cd_af)
        tag_modelo106.appendChild(tag_exist_oper)
        ######################################                
        for x in range(1,51):
            if x<10:
                campo="cp0{num}".format(num=x)
            else:
                campo="cp{num}".format(num=x)
            try:         
                if self.kargs[campo] not in (None,'','None',0,'0'):                    
                    tags = doc.createElement(campo)
                    tag_modelo106.appendChild(tags)
                    tags.appendChild(doc.createTextNode(str(int(to_decimal(self.kargs[campo])))))
            except:
                pass

        tag_modelo106.appendChild(tag_dt_apresentacao)
        tag_modelo106.appendChild(tag_loc_apresentacao)
        tag_modelo106.appendChild(tag_nif_toc)
        tag_modelo106.appendChild(tag_num_ordem_toc)
        tag_modelo106.appendChild(tag_dt_recepcao)
        tag_modelo106.appendChild(tag_obs)
        #####################################################################################        
        tag_nif.appendChild(doc.createTextNode(str(self.kargs['nif'])))
        tag_cd_af.appendChild(doc.createTextNode(str(self.kargs['area_fiscal'])))
        tag_exist_oper.appendChild(doc.createTextNode(str(self.kargs['operacoes'])))
        tag_dt_apresentacao.appendChild(doc.createTextNode(str(self.kargs['data_apresentacao'])))
        tag_loc_apresentacao.appendChild(doc.createTextNode(str(nome_local_apresentacao)))
        
        tag_dt_recepcao.appendChild(doc.createTextNode(str(self.kargs['data_recepcao'])))
        tag_nif_toc.appendChild(doc.createTextNode(str(self.kargs['nif_tecnico'])))
        tag_num_ordem_toc.appendChild(doc.createTextNode(str(self.kargs['num_reg_tec_ordem'])))
        tag_obs.appendChild(doc.createTextNode(str(self.kargs['observacoes'])))
        #####################################################################################        
        conteudoXmlCriado= doc.toprettyxml()
        conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')
        self.kargs['xml']=str(conteudoFinalXml)
        self.kargs['estado']='Gerado'
        self.put()
        return form_edit(window_id=window_id).show()




    def guardar_anexo_cli(self, key, info_anexo, info_linhas):
        #GUARDANDO OS DADOS
        self.kargs = get_model_record(model=self, key=key)
        if len(info_linhas)!=0:
            conteudoFinalXml = self.gerar_XML_anexo_cli(info_anexo=info_anexo, info_linhas=info_linhas)            
            content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'ano': str(info_anexo['anx_cli_ano']),
                'mes': str(info_anexo['anx_cli_mes']),
                'area_fiscal': str(info_anexo['anx_cli_area_fiscal']),
                'nif_contribuinte': str(info_anexo['anx_cli_nif_contr']),
                'data_entrega': str(info_anexo['anx_cli_dt_entrega']),
                'modelo106':str(info_anexo['anx_cli_modelo106']),
                'nome':str(info_anexo['anx_cli_nome']),
                'estado':'Gerado',
                'total_factura':str(info_anexo['anx_cli_total_fact']),
                'total_base_incidencia':str(info_anexo['anx_cli_total_bs_incid']),
                'total_liquidado':str(info_anexo['anx_cli_total_liq']), 
                'xml_gerado':str(conteudoFinalXml)                                  
            }
            id_anxCli = AnexoClientes(**content).put()            
            #guardandos as linhas do anexo
            for line in info_linhas:
                content={
                    'user': '{user}'.format(user=bottle.request.session['user']),
                    'factura_cliente':str(line['ln_anx_cli_factura']),
                    'designacao':str(line['ln_anx_cli_designacao']),
                    'nif_cliente':str(line['ln_anx_cli_nif']),
                    'origem':str(line['ln_anx_cli_origem']),
                    'serie':str(line['ln_anx_cli_serie']),
                    'tipo_doc':str(line['ln_anx_cli_tipoDoc']),
                    'numero_doc':str(line['ln_anx_cli_num_doc']),
                    'data':str(line['ln_anx_cli_data']),
                    'valor_factura':str(int(line['ln_anx_cli_vl_fatura'])),
                    'valor_base_incidencia':str(int(line['ln_anx_cli_Incidencia'])),
                    'taxa_iva':str(line['ln_anx_cli_taxa_iva']),
                    'iva_liquidado':str(int(line['ln_anx_cli_total_Liq'])),
                    'nao_liq_imposto':str(line['ln_anx_cli_nao_liq_imp']),
                    'linha_mod106':str(line['ln_anx_cli_linha_MOD106']),
                    'anexo_clientes':str(id_anxCli)                
                }
                LinhaAnexoCliente(**content).put()
                ###adicionar as informaçoes ao modelo106
                if str(line['ln_anx_cli_linha_MOD106'])=='01':
                    self.kargs['cp01']= to_decimal(to_decimal(self.kargs['cp01']) + to_decimal(line['ln_anx_cli_Incidencia']))
                    self.kargs['cp02']= to_decimal(to_decimal(self.kargs['cp02']) + to_decimal(line['ln_anx_cli_total_Liq']))                
                
                elif str(line['ln_anx_cli_linha_MOD106'])=='03':
                    self.kargs['cp03']= to_decimal(to_decimal(self.kargs['cp03']) + to_decimal(line['ln_anx_cli_Incidencia']))
                    self.kargs['cp04']= to_decimal(to_decimal(self.kargs['cp04']) + to_decimal(line['ln_anx_cli_total_Liq']))
                
                elif str(line['ln_anx_cli_linha_MOD106'])=='05':
                    self.kargs['cp05']= to_decimal(to_decimal(self.kargs['cp05']) + to_decimal(line['ln_anx_cli_Incidencia']))
                    self.kargs['cp06']= to_decimal(to_decimal(self.kargs['cp06']) + to_decimal(line['ln_anx_cli_total_Liq']))
                
                elif str(line['ln_anx_cli_linha_MOD106'])=='07':
                    self.kargs['cp07']= to_decimal(to_decimal(self.kargs['cp07']) + to_decimal(line['ln_anx_cli_Incidencia']))                    

                elif str(line['ln_anx_cli_linha_MOD106'])=='08':
                    self.kargs['cp08']= to_decimal(to_decimal(self.kargs['cp08']) + to_decimal(line['ln_anx_cli_Incidencia']))                    

                elif str(line['ln_anx_cli_linha_MOD106'])=='09':
                    self.kargs['cp09']= to_decimal(to_decimal(self.kargs['cp09']) + to_decimal(line['ln_anx_cli_Incidencia']))                    

                elif str(line['ln_anx_cli_linha_MOD106']) =='10':
                    self.kargs['cp10']= to_decimal(to_decimal(self.kargs['cp10']) + to_decimal(line['ln_anx_cli_Incidencia']))
                    
            #guadar a informaçoes
            self.put()


    def gerar_XML_anexo_cli(self, info_anexo, info_linhas):      
        conteudoFinalXml=''
        if len(info_linhas)!=0:
            #CRIACAO DO MODELO XML        
            import xml.dom.minidom
            doc = xml.dom.minidom.Document()

            # Cria os elementos
            tag_anexo_cli = doc.createElement('anexo_cli')
            tag_header = doc.createElement('header')
            tag_linhas = doc.createElement('linhas')
            tag_dt_entrega = doc.createElement('dt_entrega')
            tag_total_fatura = doc.createElement('total_fatura')
            tag_total_base_incid = doc.createElement('total_base_incid')
            tag_total_liquidado = doc.createElement('total_liquidado')

            # Cria os atributos de header, os mesmos do modelo106
            # é necessario guardar as informacaoes            
            tag_header.setAttribute('ano', str(info_anexo['anx_cli_ano']))
            tag_header.setAttribute('mes', str(info_anexo['anx_cli_mes']))
            tag_header.setAttribute('cd_af', str(info_anexo['anx_cli_area_fiscal']))
            tag_header.setAttribute('nif', str(info_anexo['anx_cli_nif_contr']))

            # Cria a estrutura
            doc.appendChild(tag_anexo_cli)
            tag_anexo_cli.appendChild(tag_header)
            tag_anexo_cli.appendChild(tag_linhas)
            tag_anexo_cli.appendChild(tag_dt_entrega)
            tag_anexo_cli.appendChild(tag_total_fatura)
            tag_anexo_cli.appendChild(tag_total_base_incid)
            tag_anexo_cli.appendChild(tag_total_liquidado)

            #colocar os valores
            for line in info_linhas:
                #criar a tag linha
                tag_linha = doc.createElement('linha')
                #colocar os valor da linnha
                tag_linha.setAttribute('designacao',str(line['ln_anx_cli_designacao']))
                tag_linha.setAttribute('nif_cliente',str(line['ln_anx_cli_nif']))
                tag_linha.setAttribute('origem',str(line['ln_anx_cli_origem']))
                tag_linha.setAttribute('serie',str(line['ln_anx_cli_serie']))
                tag_linha.setAttribute('tipo_doc',str(line['ln_anx_cli_tipoDoc']))
                tag_linha.setAttribute('numero_doc',str(line['ln_anx_cli_num_doc']))
                tag_linha.setAttribute('data',str(line['ln_anx_cli_data']))
                tag_linha.setAttribute('valor_factura',str(int(line['ln_anx_cli_vl_fatura'])))
                tag_linha.setAttribute('valor_base_incidencia',str(int(line['ln_anx_cli_Incidencia'])))
                tag_linha.setAttribute('taxa_iva',str(line['ln_anx_cli_taxa_iva']))
                tag_linha.setAttribute('iva_liquidado',str(int(line['ln_anx_cli_total_Liq'])))
                tag_linha.setAttribute('nao_liq_imposto',str(line['ln_anx_cli_nao_liq_imp']))
                tag_linha.setAttribute('linha_mod106',str(line['ln_anx_cli_linha_MOD106']))

                #adicionar a tag linha na tag linhas
                tag_linhas.appendChild(tag_linha)

            tag_dt_entrega.appendChild(doc.createTextNode(str(info_anexo['anx_cli_dt_entrega'])))
            tag_total_fatura.appendChild(doc.createTextNode(str(info_anexo['anx_cli_total_fact'])))
            tag_total_base_incid.appendChild(doc.createTextNode(str(info_anexo['anx_cli_total_bs_incid'])))
            tag_total_liquidado.appendChild(doc.createTextNode(str(info_anexo['anx_cli_total_liq'])))
            # GERANDO O XML
            conteudoXmlCriado= doc.toprettyxml()        
            #colocar o encoding
            conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')           
        
        return conteudoFinalXml

   

    def get_info_anexo_cli(self, key):              
        self.kargs = get_model_record(model=self, key=key)        
        informacoes=[]
        #inicializar os totais
        
        anx_cli_total_fact =0
        anx_cli_total_bs_incid = 0
        anx_cli_total_liq = 0
        #array de linhas
        info_linhas =[]

        #buscar as facturas de cliente do periodo
        facturas_clientes = FacturaCliente(where = "estado='Confirmado' and to_char(data,'yyyy')='{ano}' and to_char(data,'mm')='{mes}'".format(ano=str(self.kargs['ano']), mes =str(self.kargs['mes']))).get()
        if len(facturas_clientes) > 0:                                
            for facturaCli in facturas_clientes:                
                
                terceiro = Terceiro(where="id = '{id}'".format(id=facturaCli['cliente'])).get()
                #criar os atributos das linhas
                ln_anx_cli_origem=terceiro[0]['origem']
                ln_anx_cli_designacao=terceiro[0]['nome']
                ln_anx_cli_nif = ""
                if terceiro[0]['nif'] not in ('', None,'None'):                        
                    ln_anx_cli_nif= terceiro[0]['nif']
                else:
                    ln_anx_cli_nif= '000000000'
                ln_anx_cli_serie = facturaCli['serie']
                ln_anx_cli_tipoDoc = 'FT'                
                
                ###############################################                
                ln_anx_cli_num_doc = facturaCli['numero']
                ln_anx_cli_data = facturaCli['data']
                ln_anx_cli_vl_fatura = facturaCli['total']
                ln_anx_cli_factura = facturaCli['id']

                #para cada factura buscar as taxas de iva existente nela                
        
                sql="""SELECT DISTINCT l.iva, p.deducao, p.nao_liq_imposto FROM linha_factura_cli l, Produto p
                where (l.active = True OR l.active is NULL) 
                AND (p.active = True OR p.active is NULL)
                AND l.produto = p.id
                AND l.factura_cli = '{idFactura}'""".format(idFactura = facturaCli['id'])

                taxas = run_sql(sql)
                for taxa in taxas:
                    ln_anx_cli_linha_MOD106 = self.getLinhaM106AnexCli(taxa=taxa)
                    if taxa['nao_liq_imposto'] not in (None,'None'):
                        sql="""SELECT l.* FROM linha_factura_cli l, Produto p
                        where (l.active = True OR l.active is NULL) 
                        AND (p.active = True OR p.active is NULL)
                        AND l.produto = p.id
                        AND l.iva='{esteIva}' 
                        AND p.deducao = '{esteDeducao}' 
                        AND p.nao_liq_imposto = '{naoLiqImp}' 
                        AND l.factura_cli = '{idFactura}'""".format(esteIva=taxa['iva'],esteDeducao=taxa['deducao'],naoLiqImp=str(taxa['nao_liq_imposto']),idFactura = facturaCli['id'])                   
                    else:
                        sql="""SELECT l.* FROM linha_factura_cli l, Produto p
                        where (l.active = True OR l.active is NULL) 
                        AND (p.active = True OR p.active is NULL)
                        AND l.produto = p.id
                        AND l.iva='{esteIva}' 
                        AND p.deducao = '{esteDeducao}' 
                        AND p.nao_liq_imposto is NULL 
                        AND l.factura_cli = '{idFactura}'""".format(esteIva=taxa['iva'],esteDeducao=taxa['deducao'],idFactura = facturaCli['id'])                  
                    linhas_fact_cli = run_sql(sql)
                    #calcular a nova base incidencia e novo total de iva
                    ln_anx_cli_Incidencia = FacturaCliente().get_total_incidencia_por_taxa(record_lines=linhas_fact_cli)                    
                    ln_anx_cli_total_Liq = FacturaCliente().get_total_iva_por_taxa(record_lines=linhas_fact_cli)

                    ln_anx_cli_nao_liq_imp = taxa['nao_liq_imposto']                   
                    
                    ###para cada linha do anexo, é necessario somar os totais ao totais no anexo
                   
                    anx_cli_total_fact += int(facturaCli['total'])
                    anx_cli_total_liq += int(ln_anx_cli_total_Liq)
                    anx_cli_total_bs_incid += int(ln_anx_cli_Incidencia)             
                    ###############
                    ln_anx_cli_taxa_iva =""
                    if str(taxa['iva']) in ('None', None,'',0):
                        ln_anx_cli_taxa_iva=str(0)
                    elif '.5' in str(taxa['iva']):
                        ln_anx_cli_taxa_iva= str(round(to_decimal(taxa['iva']),1))
                    else:
                        ln_anx_cli_taxa_iva = str(int(taxa['iva']))
                    #adicionar as informacoes das linhas
                    linha = {
                        'ln_anx_cli_Incidencia':ln_anx_cli_Incidencia,
                        'ln_anx_cli_nif':ln_anx_cli_nif,
                        'ln_anx_cli_data':ln_anx_cli_data,
                        'ln_anx_cli_serie':ln_anx_cli_serie,
                        'ln_anx_cli_tipoDoc':ln_anx_cli_tipoDoc,
                        'ln_anx_cli_designacao':ln_anx_cli_designacao,
                        'ln_anx_cli_origem':ln_anx_cli_origem,
                        'ln_anx_cli_taxa_iva':ln_anx_cli_taxa_iva,
                        'ln_anx_cli_total_Liq':ln_anx_cli_total_Liq,
                        'ln_anx_cli_vl_fatura':ln_anx_cli_vl_fatura,
                        'ln_anx_cli_num_doc':ln_anx_cli_num_doc,
                        'ln_anx_cli_linha_MOD106':ln_anx_cli_linha_MOD106,
                        'ln_anx_cli_nao_liq_imp':ln_anx_cli_nao_liq_imp,
                        'ln_anx_cli_factura':ln_anx_cli_factura
                    }
                    info_linhas.append(linha)
            #adiconar as info do anexo cliente
            info_anexo={
                'anx_cli_ano':self.kargs['ano'],
                'anx_cli_mes':self.kargs['mes'],
                'anx_cli_area_fiscal': self.kargs['area_fiscal'],
                'anx_cli_nif_contr': self.kargs['nif'],
                'anx_cli_dt_entrega':self.kargs['data_apresentacao'],
                'anx_cli_modelo106': key,
                'anx_cli_nome': 'Anexo clientes_{ano}-{mes}'.format(ano=self.kargs['ano'], mes=self.kargs['mes']),
                'anx_cli_estado': 'Gerado',
                'anx_cli_total_fact':anx_cli_total_fact,
                'anx_cli_total_bs_incid':anx_cli_total_bs_incid,
                'anx_cli_total_liq':anx_cli_total_liq
            }
            informacoes.append({'info_anexo':info_anexo, 'info_linhas':info_linhas})
            print('\n\n\n\n\n#############################\nvou retornar:\n',informacoes,'\n#################\n\n\n\n\n')
        return informacoes


    def getLinhaM106AnexCli(self, taxa):
        """
            determina a linha do modelo106 que entra a informação do anexo de cliente
            obs: ficou por determinar a situaçao da linhha 5 (Operações em que liquidou o 
            IVA nos termos do Decreto - Lei nº 16/2004 de 20 de Maio (valor recebido))           
        """                           
        if str(to_decimal(taxa['iva'])) == str(to_decimal(15.5)):
            #taxa normal em vigor
            return '01'
        if str(to_decimal(taxa['iva'])) in (str(to_decimal(0)),'',None,'None'):                         
            #isento de iva
            if taxa['deducao']  in ('0',0):
                #sem direito a deducao
                return '09'
            elif taxa['deducao'] in ('50',50,'100',100):
                #com direito a deducao
                return '08'
            else:
                #nao tributados
                return '10'
        else:
            #taxa especial           
            return '03'
        


    
    def get_info_anexo_forn(self, key):
        #array contendo toda a informacao do anexo fornecedor
        informacoes=[]         
        self.kargs = get_model_record(model=self, key=key)
        #criar os dicionarios de dados      
        anx_forn_total_fact = 0
        anx_forn_total_bs_incid = 0
        anx_forn_total_ded = 0
        anx_forn_total_sup = 0

        #array de linhas de anexo
        info_linhas = []
        #buscar as facturas de fornecedor do periodo
        facturas_fornecedores = FacturaFornecedor(where = "estado='Confirmado' and to_char(data,'yyyy')='{ano}' and to_char(data,'mm')='{mes}'".format(ano=str(self.kargs['ano']), mes =str(self.kargs['mes']))).get()
        if len(facturas_fornecedores) > 0:                                 
            for facturaForn in facturas_fornecedores:                
                terceiro = Terceiro(where="id = '{id}'".format(id=facturaForn['fornecedor'])).get()
                #criar os atributos das linhas
                ln_anx_forn_origem=terceiro[0]['origem']
                ln_anx_forn_designacao=terceiro[0]['nome']
                ln_anx_forn_nif= terceiro[0]['nif']                
                ln_anx_forn_tipoDoc = 'FT'                               
                ###############################################                
                ln_anx_forn_num_doc = facturaForn['numero']
                ln_anx_forn_data = facturaForn['data']
                ln_anx_forn_vl_fatura = facturaForn['total']
                ln_anx_forn_factura = facturaForn['id']
                
                #para cada factura buscar as taxas de iva e deducao existente nela               
                
                sql ="""SELECT DISTINCT l.iva, l.direito_deducao AS deducao, p.tipo 
                FROM linha_factura_forn l, produto p 
                WHERE (l.active=True OR l.active IS NULL)
                AND (p.active=True OR p.active IS NULL)
                AND l.produto = p.id
                AND l.factura_forn = '{idFactura}'""".format(idFactura = facturaForn['id'])
                
                taxas = run_sql(sql)        
                for taxa in taxas:                    
                    #colocar a tipologia
                    ln_anx_forn_tipologia = self.getTipologia(taxa['tipo'])
                    #buscar as linhas de factura_forn que contem a taxa de iva, de deducao  e o tipo de produto 
                    sql ="""SELECT  l.* FROM linha_factura_forn l, produto p 
                    WHERE (l.active=True OR l.active IS NULL)
                    AND (p.active=True OR p.active IS NULL)
                    AND l.produto = p.id 
                    AND l.iva = '{esteIva}' 
                    AND l.direito_deducao ='{esteDeducao}' 
                    AND p.tipo = '{esteTipo}' 
                    AND l.factura_forn = '{idFactura}'""".format(esteIva=taxa['iva'], esteDeducao=taxa['deducao'],esteTipo=taxa['tipo'],idFactura = facturaForn['id'])                                                  
                    
                    linhas_fact_forn = run_sql(sql)

                    #calcular a nova base incidencia, novo total de iva suportado e novo total deducao
                    ln_anx_forn_Incidencia = FacturaFornecedor().get_total_incidencia_por_taxa(record_lines=linhas_fact_forn)
                    ln_anx_forn_total_sup = round(to_decimal(to_decimal(ln_anx_forn_Incidencia)*to_decimal(taxa['iva'])/100),0)               
                    ln_anx_forn_total_ded = FacturaFornecedor().get_total_dedutivel_por_taxa(record_lines=linhas_fact_forn)                  
                    
                    ###para cada linha do anexo, é necessario somar os totais ao totais no anexo
                    anx_forn_total_fact += int(facturaForn['total'])
                    anx_forn_total_sup += int(ln_anx_forn_total_sup)
                    anx_forn_total_bs_incid += int(ln_anx_forn_Incidencia)
                    anx_forn_total_ded += int(ln_anx_forn_total_ded)         
                    ###############

                    ln_anx_forn_taxa_iva =""
                    if str(taxa['iva']) in ('None', None,''):
                        ln_anx_forn_taxa_iva=0
                    elif '.5' in str(taxa['iva']):
                        ln_anx_forn_taxa_iva= round(to_decimal(taxa['iva']),1)
                    else:
                        ln_anx_forn_taxa_iva = int(taxa['iva'])
                    ln_anx_forn_direito_ded = str(taxa['deducao'])
                    #defenir a linha do modelo106 que entra a informação
                    ln_anx_forn_linha_MOD106 = self.getLinhaM106AnexForn(tipologia = ln_anx_forn_tipologia, origem = ln_anx_forn_origem)                   
                    
                    #adicionar as informacoes das linhas
                    linha = {
                        'ln_anx_forn_Incidencia':ln_anx_forn_Incidencia,
                        'ln_anx_forn_nif':ln_anx_forn_nif,
                        'ln_anx_forn_data':ln_anx_forn_data,                        
                        'ln_anx_forn_tipoDoc':ln_anx_forn_tipoDoc,
                        'ln_anx_forn_designacao':ln_anx_forn_designacao,
                        'ln_anx_forn_origem':ln_anx_forn_origem,
                        'ln_anx_forn_taxa_iva':ln_anx_forn_taxa_iva,
                        'ln_anx_forn_total_sup':ln_anx_forn_total_sup,
                        'ln_anx_forn_direito_ded':ln_anx_forn_direito_ded,
                        'ln_anx_forn_total_ded':ln_anx_forn_total_ded,
                        'ln_anx_forn_vl_fatura':ln_anx_forn_vl_fatura,
                        'ln_anx_forn_num_doc':ln_anx_forn_num_doc,
                        'ln_anx_forn_linha_MOD106':ln_anx_forn_linha_MOD106,
                        'ln_anx_forn_tipologia':ln_anx_forn_tipologia,
                        'ln_anx_forn_factura':ln_anx_forn_factura
                    }                    
                    info_linhas.append(linha)
                    
            #adicionar as info do anexo
            info_anexo ={
                'anx_forn_ano': self.kargs['ano'],
                'anx_forn_mes': self.kargs['mes'],
                'anx_forn_area_fiscal': self.kargs['area_fiscal'],
                'anx_forn_nif_entidade': self.kargs['nif'],
                'anx_forn_dt_entrega': self.kargs['data_apresentacao'],
                'anx_forn_modelo106': key,
                'anx_forn_nome' :'Anexo fornecedor_{ano}-{mes}'.format(ano=self.kargs['ano'], mes=self.kargs['mes']),
                'anx_forn_estado':'Gerado',
                'anx_forn_total_fact' : anx_forn_total_fact,
                'anx_forn_total_bs_incid': anx_forn_total_bs_incid,
                'anx_forn_total_ded': anx_forn_total_ded,
                'anx_forn_total_sup': anx_forn_total_sup           
            }       
            informacoes.append({'info_anexo':info_anexo,'info_linhas':info_linhas})         
        return informacoes



    def getLinhaM106AnexForn(self, tipologia, origem):
        """
            determina a linha do modelo106 que entra a informação.
            obs: ficou por determinar a linha 25(Imposto Dedutível nas importações de bens efetuadas pelo SP)
        """
        if origem=='CV':
            #fornecedor com sede nacional
            if tipologia=='IMO':
                return '17'
            elif tipologia=='INV':
                return '19'
            elif tipologia=='OBC':
                return '21'
            else:
                return '23'
        else:
            #fornecedor com sede no estrangeiro
            return '11'



    def gerar_XML_anexo_forn(self, info_anexo, info_linhas):
        conteudoFinalXml=''         
        if len(info_linhas)!=0:         
            #CRIACAO DO MODELO XML        
            import xml.dom.minidom
            doc = xml.dom.minidom.Document()
            # Cria os elementos
            tag_anexo_for = doc.createElement('anexo_for')
            tag_header = doc.createElement('header')
            tag_linhas = doc.createElement('linhas')
            tag_dt_entrega = doc.createElement('dt_entrega')
            tag_total_fatura = doc.createElement('total_fatura')
            tag_total_base_incid = doc.createElement('total_base_incid')
            tag_total_suportado = doc.createElement('total_suportado')
            tag_total_dedutivel = doc.createElement('total_dedutivel')

            # Cria os atributos de header
            tag_header.setAttribute('ano', str(info_anexo['anx_forn_ano']))
            tag_header.setAttribute('mes', str(info_anexo['anx_forn_mes']))
            tag_header.setAttribute('cd_af', str(info_anexo['anx_forn_area_fiscal']))
            tag_header.setAttribute('nif', str(info_anexo['anx_forn_nif_entidade']))
            

            # Cria a estrutura
            doc.appendChild(tag_anexo_for)
            tag_anexo_for.appendChild(tag_header)
            tag_anexo_for.appendChild(tag_linhas)
            tag_anexo_for.appendChild(tag_dt_entrega)
            tag_anexo_for.appendChild(tag_total_fatura)
            tag_anexo_for.appendChild(tag_total_base_incid)
            tag_anexo_for.appendChild(tag_total_suportado)
            tag_anexo_for.appendChild(tag_total_dedutivel)

            #colocar os valores
            for line in info_linhas:
                #criar a tag linha
                tag_linha = doc.createElement('linha')
                #colocar os valor da linnha                              
                tag_linha.setAttribute('designacao',str(line['ln_anx_forn_designacao']))
                tag_linha.setAttribute('nif',str(line['ln_anx_forn_nif']))
                tag_linha.setAttribute('origem',str(line['ln_anx_forn_origem']))                
                tag_linha.setAttribute('tp_doc',str(line['ln_anx_forn_tipoDoc']))
                tag_linha.setAttribute('num_doc',str(line['ln_anx_forn_num_doc']))
                tag_linha.setAttribute('data',str(line['ln_anx_forn_data']))
                tag_linha.setAttribute('vl_fatura',str(int(line['ln_anx_forn_vl_fatura'])))
                tag_linha.setAttribute('vl_base_incid',str(int(line['ln_anx_forn_Incidencia'])))
                tag_linha.setAttribute('tx_iva',str(line['ln_anx_forn_taxa_iva']))
                tag_linha.setAttribute('iva_sup',str(int(line['ln_anx_forn_total_sup'])))
                tag_linha.setAttribute('direito_ded',str(int(to_decimal(line['ln_anx_forn_direito_ded']))))         
                tag_linha.setAttribute('iva_ded',str(line['ln_anx_forn_total_ded']))
                tag_linha.setAttribute('tipologia',str(line['ln_anx_forn_tipologia']))
                tag_linha.setAttribute('linha_dest_mod',str(line['ln_anx_forn_linha_MOD106']))
                #adicionar a tag linha na tag linhas
                tag_linhas.appendChild(tag_linha)

            #adicionar os totais
            tag_dt_entrega.appendChild(doc.createTextNode(str(info_anexo['anx_forn_dt_entrega'])))
            tag_total_fatura.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_fact'])))
            tag_total_base_incid.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_bs_incid'])))
            tag_total_suportado.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_sup'])))
            tag_total_dedutivel.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_ded'])))
            
            # GERANDO O XML
            conteudoXmlCriado = doc.toprettyxml()        
            #colocar o encoding
            conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')       
           
        return conteudoFinalXml




    def guardar_anexo_forn(self, key, info_anexo, info_linhas):
        #gerar o xml
        self.kargs= get_model_record(model=self,key=key)        
        conteudoFinalXml = self.gerar_XML_anexo_forn(info_anexo, info_linhas)
        #GUARDANDO OS DADOS
        content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'ano': str(info_anexo['anx_forn_ano']),
                'mes': str(info_anexo['anx_forn_mes']),
                'area_fiscal': str(info_anexo['anx_forn_area_fiscal']),
                'nif_entidade': str(info_anexo['anx_forn_nif_entidade']),
                'data_entrega': str(info_anexo['anx_forn_dt_entrega']),
                'modelo106':str(info_anexo['anx_forn_modelo106']),
                'nome':str(info_anexo['anx_forn_nome']),
                'estado':'Gerado',
                'total_factura':str(info_anexo['anx_forn_total_fact']),
                'total_base_incidencia':str(info_anexo['anx_forn_total_bs_incid']),
                'total_suportado':str(info_anexo['anx_forn_total_sup']),
                'total_dedutivel':str(info_anexo['anx_forn_total_ded']),
                'xml_gerado':str(conteudoFinalXml)                                      
        }           
        id_anxForn = AnexoFornecedor(**content).put()        
        #guardandos as linhas do anexo
        for line in info_linhas:
            content={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'factura_fornecedor':str(line['ln_anx_forn_factura']),
                'anexo_fornecedor':str(id_anxForn),
                'designacao':str(line['ln_anx_forn_designacao']),
                'nif_fornecedor':str(line['ln_anx_forn_nif']),
                'origem':str(line['ln_anx_forn_origem']),
                'tipologia':str(line['ln_anx_forn_tipologia']),
                'tipo_doc':str(line['ln_anx_forn_tipoDoc']),
                'numero_doc':str(line['ln_anx_forn_num_doc']),
                'data':str(line['ln_anx_forn_data']),
                'valor_factura':str(int(line['ln_anx_forn_vl_fatura'])),
                'valor_base_incid':str(int(line['ln_anx_forn_Incidencia'])),
                'taxa_iva':str(line['ln_anx_forn_taxa_iva']),
                'iva_suportado':str(int(line['ln_anx_forn_total_sup'])),
                'direito_ded':str(int(to_decimal(line['ln_anx_forn_direito_ded']))),
                'iva_dedutivel':str(line['ln_anx_forn_total_ded']),
                'linha_mod106':str(line['ln_anx_forn_linha_MOD106'])                                   
            }
            LinhaAnexoFornecedor(**content).put()
            ###adicionar as informaçoes ao modelo106
            if str(line['ln_anx_forn_linha_MOD106'])=='11':
                self.kargs['cp11']= to_decimal(to_decimal(self.kargs['cp11']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp12']= to_decimal(to_decimal(self.kargs['cp12']) + to_decimal(line['ln_anx_forn_total_ded']))
            
            elif str(line['ln_anx_forn_linha_MOD106'])=='14':
                self.kargs['cp14']= to_decimal(to_decimal(self.kargs['cp14']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp15']= to_decimal(to_decimal(self.kargs['cp15']) + to_decimal(line['ln_anx_forn_total_ded']))

            elif str(line['ln_anx_forn_linha_MOD106'])=='17':
                self.kargs['cp17']= to_decimal(to_decimal(self.kargs['cp17']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp18']= to_decimal(to_decimal(self.kargs['cp18']) + to_decimal(line['ln_anx_forn_total_ded']))

            elif str(line['ln_anx_forn_linha_MOD106'])=='19':
                self.kargs['cp19']= to_decimal(to_decimal(self.kargs['cp19']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp20']= to_decimal(to_decimal(self.kargs['cp20']) + to_decimal(line['ln_anx_forn_total_ded']))

            elif str(line['ln_anx_forn_linha_MOD106'])=='21':
                self.kargs['cp21']= to_decimal(to_decimal(self.kargs['cp21']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp22']= to_decimal(to_decimal(self.kargs['cp22']) + to_decimal(line['ln_anx_forn_total_ded']))

            elif str(line['ln_anx_forn_linha_MOD106'])=='23':
                self.kargs['cp23']= to_decimal(to_decimal(self.kargs['cp23']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp24']= to_decimal(to_decimal(self.kargs['cp24']) + to_decimal(line['ln_anx_forn_total_ded']))

            elif str(line['ln_anx_forn_linha_MOD106']) =='25':
                self.kargs['cp25']= to_decimal(to_decimal(self.kargs['cp25']) + to_decimal(line['ln_anx_forn_Incidencia']))
                self.kargs['cp26']= to_decimal(to_decimal(self.kargs['cp26']) + to_decimal(line['ln_anx_forn_total_ded']))
            
        #guadar a informaçoes
        self.put()



    def get_alteracoes_forn(self, key):
        """
        metodo que verifica a existencia de alteracoes nas facturas de fornecdor, e retorna um array de dados
        informando a accao a tomar e os dados (informacao das linhas de anexo actuais e anteriores) a utilizar na acao.
        """
        self.kargs = get_model_record(model=self, key=key)
        #informacao das facturas anteriores
        anterior =[]
        info_anexo = AnexoFornecedor(where="ano='{ano}' AND mes='{mes}'".format(ano=self.kargs['ano'],mes =self.kargs['mes'])).get()
        if len(info_anexo)!=0:
            info_linhas = LinhaAnexoFornecedor(where="anexo_fornecedor='{id}'".format(id=info_anexo[0]['id'])).get()
            if len(info_linhas)!=0:
                anterior.append({'info_linhas':info_linhas})               

        #informacao das factuaras actuais        
        actual = self.get_info_anexo_forn(key)        

        #TOMAR DECISAO SOBRE AS INFORMACOES EXISTENTES (actual e anterior)
        
        if (len(actual)==0) & (len(anterior)==0):
            #nao existe facturas (actuais ou anteriro) logo nao existe alteracoes            
            return []

        elif (len(actual)> 0) & (len(anterior)==0):
            #todos as facturas actuais foram adicionadas (criar anexo reg. fornecedor de adicão de facturas)
            alteracoes = []
            alteracoes.append({'accao':'Adicionar','info_linhas_act':actual[0]['info_linhas']})
            return alteracoes

        elif (len(actual)==0) & (len(anterior)>0):
            #todas as facturas do periodo foram eliminadas, logo deve-se criar anexo regularizacao com ação de "eliminar" todas
            alteracoes = []
            alteracoes.append({'accao':'Eliminar','info_linhas_ant':anterior[0]['info_linhas']})
            return alteracoes

        elif (len(actual)>0) & (len(anterior)>0):
            #existe facturas anterior e actuais, porem podera existir adicao, eliminacao e alteracoes de factura, logo é preciso a analise factura a factura
            act = actual[0]
            ant = anterior[0]
            linhasAlterar = []            
            linhasAdicionar=[]
            linhasEliminar=[]

            for line_act in act['info_linhas']:                
                existe = False
                for line_ant in ant['info_linhas']:
                    #detectar os iguais 
                    if ((str(line_act['ln_anx_forn_factura']) == line_ant['factura_fornecedor'])
                        & (str(line_act['ln_anx_forn_taxa_iva']) == line_ant['taxa_iva'])
                        & (str(line_act['ln_anx_forn_direito_ded']) == line_ant['direito_ded'])
                        & (str(int(line_act['ln_anx_forn_total_sup'])) == line_ant['iva_suportado'])
                        & (str(int(line_act['ln_anx_forn_total_ded'])) == line_ant['iva_dedutivel'])
                        & (str(int(line_act['ln_anx_forn_vl_fatura'])) == line_ant['valor_factura'])
                        & (str(line_act['ln_anx_forn_num_doc']) == line_ant['numero_doc'])):
                        
                        ant['info_linhas'].remove(line_ant)
                        existe = True
                        break
                    # detectar os modificados que sao para alterar
                    elif ((str(line_act['ln_anx_forn_factura']) == line_ant['factura_fornecedor'])
                        & (str(line_act['ln_anx_forn_num_doc']) == line_ant['numero_doc'])):                       
                        linhasAlterar.append({'info_linhas_act':line_act,'info_linhas_ant':line_ant})                        
                        #remover esta linha do ant['info_linhas']
                        ant['info_linhas'].remove(line_ant)
                        existe = True
                        break
                       
                #caso nao existe em ambas deve adiciona-la
                if not existe:
                    linhasAdicionar.append(line_act)
                # o que restou das linhas anteriores sao para eliminar
                linhasEliminar = ant['info_linhas']

            alteracoes = []
            # caso exista alguma linha no linhaAlterar esta é para a acção de Corrigir
            if len(linhasAlterar)>0:                    
                alteracoes.append({'accao':'Corrigir', 'info_linhas':linhasAlterar})
                
            # caso continua existindo linhas no linhasAdicionar, essas devem ser da acção Adicionar
            if len(linhasAdicionar)>0:                    
                alteracoes.append({'accao':'Adicionar', 'info_linhas_act':linhasAdicionar})
                
            # caso continua existindo linhas no linhasEliminar, essas devem ser da acção Eliminar
            if len(linhasEliminar)>0:                    
                alteracoes.append({'accao':'Eliminar', 'info_linhas_ant':linhasEliminar})
            
            return alteracoes



    def get_alteracoes_cli(self, key):
        """
        metodo que verifica a existencia de alteracoes nas facturas de clientes, e retorna um array de dados
        informando a accao a tomar e os dados (informacao das linhas de anexo actuais e anteriores) a utilizar na acao.
        """
        self.kargs = get_model_record(model=self, key= key)
        #informacao das facturas anteriores
        anterior =[]
        info_anexo = AnexoClientes(where="ano='{ano}' AND mes='{mes}'".format(ano=self.kargs['ano'],mes =self.kargs['mes'])).get()
        if len(info_anexo)!=0:
            info_linhas = LinhaAnexoCliente(where="anexo_clientes='{id}'".format(id=info_anexo[0]['id'])).get()
            if len(info_linhas)!=0:
                anterior.append({'info_linhas':info_linhas})               

        #informacao das factuaras actuais        
        actual = self.get_info_anexo_cli(key)
        #TOMAR DECISAO SOBRE AS INFORMACOES EXISTENTES (actual e anterior)
        
        if (len(actual)==0) & (len(anterior)==0):
            #nao existe facturas (actuais ou anteriro) logo nao existe alteracoes
            return []

        elif (len(actual)> 0) & (len(anterior)==0):
            #todos as facturas actuais foram adicionadas (criar anexo reg. fornecedor de adicão de facturas)
            alteracoes = []
            alteracoes.append({'accao':'Adicionar','info_linhas_act':actual[0]['info_linhas']})
            return alteracoes

        elif (len(actual)==0) & (len(anterior)>0):
            #todas as facturas do periodo foram eliminadas, logo deve-se criar anexo regularizacao com ação de "eliminar" todas
            alteracoes = []
            alteracoes.append({'accao':'Eliminar','info_linhas_ant':anterior[0]['info_linhas']})
            return alteracoes

        elif (len(actual)>0) & (len(anterior)>0):
            #existe facturas anterior e actuais, porem podera existir adicao, eliminacao e alteracoes de factura, logo é preciso a analise factura a factura
            act = actual[0]
            ant = anterior[0]

            linhasAlterar = []            
            linhasAdicionar=[]
            linhasEliminar=[]

            for line_act in act['info_linhas']:                
                existe = False
                for line_ant in ant['info_linhas']:
                    #detectar os iguais 
                    if ((str(line_act['ln_anx_cli_factura']) == str(line_ant['factura_cliente']))
                        & (str(line_act['ln_anx_cli_taxa_iva']) == str(line_ant['taxa_iva']))
                        & (str(int(line_act['ln_anx_cli_Incidencia'])) == str(line_ant['valor_base_incidencia']))
                        & (str(int(line_act['ln_anx_cli_total_Liq'])) == str(line_ant['iva_liquidado']))
                        & (str(int(line_act['ln_anx_cli_vl_fatura'])) == str(line_ant['valor_factura']))):
                        
                        ant['info_linhas'].remove(line_ant)
                        existe = True
                        break
                    # detectar os modificados que sao para alterar
                    elif ((str(line_act['ln_anx_cli_factura']) == line_ant['factura_cliente'])
                        & (str(line_act['ln_anx_cli_num_doc']) == line_ant['numero_doc'])):
                        linhasAlterar.append({'info_linhas_act':line_act,'info_linhas_ant':line_ant})                        
                        #remover esta linha do ant['info_linhas']
                        ant['info_linhas'].remove(line_ant)
                        existe = True
                        break

                       
                #caso nao existe em ambas deve adiciona-la
                if not existe:
                    linhasAdicionar.append(line_act)
                # o que restou das linhas anteriores sao para a accao de eliminar
                linhasEliminar = ant['info_linhas']

            alteracoes = []
            # caso exista alguma linha no linhaAlterar esta é para a acção de Corrigir
            if len(linhasAlterar)>0:                    
                alteracoes.append({'accao':'Corrigir', 'info_linhas':linhasAlterar})
                
            # caso continua existindo linhas no linhasAdicionar, essas devem ser da acção Adicionar
            if len(linhasAdicionar)>0:                    
                alteracoes.append({'accao':'Adicionar', 'info_linhas_act':linhasAdicionar})
                
            # caso continua existindo linhas no linhasEliminar, essas devem ser da acção Eliminar
            if len(linhasEliminar)>0:                    
                alteracoes.append({'accao':'Eliminar', 'info_linhas_ant':linhasEliminar})
            
            return alteracoes



    def gerar_xml_reg_forn(self, key):
        """
        gera o xml de anexo regularizacao fornecedor com as 
        infomaçoes das linhas ja armazenadas na base dados
        """        
        self.kargs = get_model_record(model=self, key=key)
        anexo = AnexoRegFornecedor(where="modelo106='{modelo}'".format(modelo=key)).get()
        if len(anexo)!=0:
            info_anexo =anexo[0]
            linhasAnexo = LinhaAnexoRegFornecedor(orderby="posicao",where="anexo_reg_fornecedor='{anexo_reg}'".format(anexo_reg=info_anexo['id'])).get()                
            if len(linhasAnexo)!=0:
                #CRIACAO DO MODELO XML
                import xml.dom.minidom
                doc = xml.dom.minidom.Document()
                # Cria os elementos
                tag_anexo_for = doc.createElement('anexo_for_reg')
                tag_header = doc.createElement('header')
                tag_linhas = doc.createElement('linhas')
                tag_linha = doc.createElement('linha')
                tag_dt_entrega = doc.createElement('dt_entrega')
                tag_total_fatura = doc.createElement('total_fatura')
                tag_total_base_incid = doc.createElement('total_base_incid')
                tag_total_suportado = doc.createElement('total_suportado')
                tag_total_dedutivel = doc.createElement('total_dedutivel')     

                # setar os atributos de header
                tag_header.setAttribute('ano', info_anexo['ano'])
                tag_header.setAttribute('mes', info_anexo['mes'])
                tag_header.setAttribute('cd_af', info_anexo['area_fiscal'])
                tag_header.setAttribute('nif', info_anexo['nif_entidade'])
                

                # Cria a estrutura
                doc.appendChild(tag_anexo_for)
                tag_anexo_for.appendChild(tag_header)
                tag_anexo_for.appendChild(tag_linhas)       
                tag_anexo_for.appendChild(tag_dt_entrega)
                tag_anexo_for.appendChild(tag_total_fatura)
                tag_anexo_for.appendChild(tag_total_base_incid)
                tag_anexo_for.appendChild(tag_total_suportado)
                tag_anexo_for.appendChild(tag_total_dedutivel)

                #buscar as linhas do anexo para inserir
                #como as linhas estao aos pares a cada duas linhas percorridas uma nova "tag_linha" e inserida
                x=1
                for linhA in linhasAnexo:
                    if linhA['accao'] == 'Adicionar':
                        if linhA['tipo'] != 'decl_anterior':
                            tag_reg_or_ant = doc.createElement(linhA['tipo'])                      
                            tag_reg_or_ant.setAttribute('num_doc', linhA['valor_factura'])                              
                            tag_reg_or_ant.setAttribute('origem', linhA['origem'])                    
                            tag_reg_or_ant.setAttribute('nif', linhA['nif_fornecedor'])
                            tag_reg_or_ant.setAttribute('iniciativa', linhA['iniciativa'])                
                            tag_reg_or_ant.setAttribute('tp_doc', linhA['tipo_doc'])             
                            tag_reg_or_ant.setAttribute('data', linhA['data'])                    
                            tag_reg_or_ant.setAttribute('vl_fatura', linhA['valor_factura'])
                            tag_reg_or_ant.setAttribute('vl_base_incid', linhA['valor_base_incid'])
                            tag_reg_or_ant.setAttribute('tx_iva', linhA['taxa_iva'])
                            tag_reg_or_ant.setAttribute('iva_sup', linhA['iva_suportado'])
                            tag_reg_or_ant.setAttribute('direito_ded', linhA['direito_ded'])
                            tag_reg_or_ant.setAttribute('iva_ded', linhA['iva_dedutivel'])
                            tag_reg_or_ant.setAttribute('tipologia', linhA['tipologia'])
                            tag_reg_or_ant.setAttribute('linha_dest_mod', linhA['linha_mod106'])
                            tag_reg_or_ant.setAttribute('periodo_ref',linhA['periodo_referencia'])
                    else:
                        tag_reg_or_ant = doc.createElement(linhA['tipo'])                      
                        tag_reg_or_ant.setAttribute('num_doc', linhA['valor_factura'])                              
                        tag_reg_or_ant.setAttribute('origem', linhA['origem'])                    
                        tag_reg_or_ant.setAttribute('nif', linhA['nif_fornecedor'])
                        tag_reg_or_ant.setAttribute('iniciativa', linhA['iniciativa'])                
                        tag_reg_or_ant.setAttribute('tp_doc', linhA['tipo_doc'])             
                        tag_reg_or_ant.setAttribute('data', linhA['data'])                    
                        tag_reg_or_ant.setAttribute('vl_fatura', linhA['valor_factura'])
                        tag_reg_or_ant.setAttribute('vl_base_incid', linhA['valor_base_incid'])
                        tag_reg_or_ant.setAttribute('tx_iva', linhA['taxa_iva'])
                        tag_reg_or_ant.setAttribute('iva_sup', linhA['iva_suportado'])
                        tag_reg_or_ant.setAttribute('direito_ded', linhA['direito_ded'])
                        tag_reg_or_ant.setAttribute('iva_ded', linhA['iva_dedutivel'])
                        tag_reg_or_ant.setAttribute('tipologia', linhA['tipologia'])
                        tag_reg_or_ant.setAttribute('linha_dest_mod', linhA['linha_mod106'])
                        tag_reg_or_ant.setAttribute('periodo_ref',linhA['periodo_referencia'])

                    tag_linha.appendChild(tag_reg_or_ant)
                    if x==2:
                        x=0
                        tag_linhas.appendChild(tag_linha)
                        tag_linha = doc.createElement('linha')
                    x+=1
                # colocar os valores
                tag_dt_entrega.appendChild(doc.createTextNode(info_anexo['data_entrega']))
                tag_total_fatura.appendChild(doc.createTextNode(info_anexo['total_factura']))
                tag_total_base_incid.appendChild(doc.createTextNode(info_anexo['total_base_incidencia']))
                tag_total_suportado.appendChild(doc.createTextNode(info_anexo['total_suportado']))
                tag_total_dedutivel.appendChild(doc.createTextNode(info_anexo['total_dedutivel']))        
                # Gerar o conteudo xml
                conteudoXmlCriado= doc.toprettyxml()        
                #colocar o encoding
                conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')
                #guardar o xml
                content={
                    'user': '{user}'.format(user=bottle.request.session['user']),
                    'id':info_anexo['id'],
                    'xml_gerado':conteudoFinalXml
                }
                AnexoRegFornecedor(**content).put()


    def gerar_xml_reg_cli(self, key):
        """
        gera o xml de anexo regularizacao cliente com as 
        infomaçoes do anexo ja armazenadas na base dados
        """        
        self.kargs = get_model_record(model=self, key=key)
        anexo = AnexoRegCliente(where="modelo106='{modelo}'".format(modelo=key)).get()
        if len(anexo)!=0:
            info_anexo =anexo[0]
            linhasAnexo = LinhaAnexoRegCliente(orderby="posicao",where="anexo_reg_cliente='{anexo_reg}'".format(anexo_reg=info_anexo['id'])).get()                
            if len(linhasAnexo)!=0:
                #CRIACAO DO MODELO XML
                import xml.dom.minidom
                doc = xml.dom.minidom.Document()
                # Cria os elementos
                tag_anexo_cli = doc.createElement('anexo_for_cli')
                tag_header = doc.createElement('header')
                tag_linhas = doc.createElement('linhas')
                tag_linha = doc.createElement('linha')
                tag_dt_entrega = doc.createElement('dt_entrega')
                tag_total_fatura = doc.createElement('total_fatura')
                tag_total_base_incid = doc.createElement('total_base_incid')
                tag_total_liquidado = doc.createElement('total_liquidado')    

                # setar os atributos de header
                tag_header.setAttribute('ano', info_anexo['ano'])
                tag_header.setAttribute('mes', info_anexo['mes'])
                tag_header.setAttribute('cd_af', info_anexo['area_fiscal'])
                tag_header.setAttribute('nif', info_anexo['nif_entidade'])
                

                # Cria a estrutura
                doc.appendChild(tag_anexo_cli)
                tag_anexo_cli.appendChild(tag_header)
                tag_anexo_cli.appendChild(tag_linhas)       
                tag_anexo_cli.appendChild(tag_dt_entrega)
                tag_anexo_cli.appendChild(tag_total_fatura)
                tag_anexo_cli.appendChild(tag_total_base_incid)
                tag_anexo_cli.appendChild(tag_total_liquidado)

                #buscar as linhas do anexo para inserir
                #como as linhas estao aos pares a cada duas linhas percorridas uma nova "tag_linha" e inserida
                x=1
                for linhA in linhasAnexo:
                    if linhA['accao'] == 'Adicionar':
                        if linhA['tipo'] != 'decl_anterior':
                            tag_reg_or_ant = doc.createElement(linhA['tipo'])                      
                            tag_reg_or_ant.setAttribute('num_doc', linhA['valor_factura'])                              
                            tag_reg_or_ant.setAttribute('origem', linhA['origem'])                    
                            tag_reg_or_ant.setAttribute('nif', linhA['nif_cliente'])
                            tag_reg_or_ant.setAttribute('iniciativa', linhA['iniciativa'])                
                            tag_reg_or_ant.setAttribute('tp_doc', linhA['tipo_doc'])             
                            tag_reg_or_ant.setAttribute('data', linhA['data'])                    
                            tag_reg_or_ant.setAttribute('vl_fatura', linhA['valor_factura'])
                            tag_reg_or_ant.setAttribute('vl_base_incid', linhA['valor_base_incid'])
                            tag_reg_or_ant.setAttribute('tx_iva', linhA['taxa_iva'])
                            tag_reg_or_ant.setAttribute('iva_liq', linhA['iva_liquidado'])
                            tag_reg_or_ant.setAttribute('linha_dest_mod', linhA['linha_mod106'])
                            tag_reg_or_ant.setAttribute('periodo_ref',linhA['periodo_referencia'])
                    else:
                        tag_reg_or_ant = doc.createElement(linhA['tipo'])                      
                        tag_reg_or_ant.setAttribute('num_doc', linhA['valor_factura'])                              
                        tag_reg_or_ant.setAttribute('origem', linhA['origem'])                    
                        tag_reg_or_ant.setAttribute('nif', linhA['nif_cliente'])
                        tag_reg_or_ant.setAttribute('iniciativa', linhA['iniciativa'])                
                        tag_reg_or_ant.setAttribute('tp_doc', linhA['tipo_doc'])             
                        tag_reg_or_ant.setAttribute('data', linhA['data'])                    
                        tag_reg_or_ant.setAttribute('vl_fatura', linhA['valor_factura'])
                        tag_reg_or_ant.setAttribute('vl_base_incid', linhA['valor_base_incid'])
                        tag_reg_or_ant.setAttribute('tx_iva', linhA['taxa_iva'])
                        tag_reg_or_ant.setAttribute('iva_liq', linhA['iva_liquidado'])
                        tag_reg_or_ant.setAttribute('linha_dest_mod', linhA['linha_mod106'])
                        tag_reg_or_ant.setAttribute('periodo_ref',linhA['periodo_referencia'])

                    tag_linha.appendChild(tag_reg_or_ant)
                    if x==2:
                        x=0
                        tag_linhas.appendChild(tag_linha)
                        tag_linha = doc.createElement('linha')
                    x+=1
                # colocar os valores
                tag_dt_entrega.appendChild(doc.createTextNode(info_anexo['data_entrega']))
                tag_total_fatura.appendChild(doc.createTextNode(info_anexo['total_factura']))
                tag_total_base_incid.appendChild(doc.createTextNode(info_anexo['total_base_incidencia']))
                tag_total_liquidado.appendChild(doc.createTextNode(info_anexo['total_liquidado']))       
                # Gerar o conteudo xml
                conteudoXmlCriado= doc.toprettyxml()        
                #colocar o encoding
                conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')
                #guardar o xml
                content={
                    'user': '{user}'.format(user=bottle.request.session['user']),
                    'id':info_anexo['id'],
                    'xml_gerado':conteudoFinalXml
                }
                AnexoRegCliente(**content).put()



    def guardar_regularizacao_forn(self, key):
        """
            guarda as informaçoes de anexo de regularizacao de fornecedor na base dados
        """
        #get alteracoes
        alteracoes = self.get_alteracoes_forn(key=key)

        self.kargs = get_model_record(model=self,key=key)        
        
        if len(alteracoes)>0:
            #guardando o anexo reg
            tot_factura=0
            tot_incidencia=0
            tot_suportado=0
            tot_dedutivel=0

            content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'nome': 'anexo_reg_for_{ano}-{mes}'.format(ano=self.kargs['ano'], mes=self.kargs['mes']),
                'modelo106':str(key),
                'nif_entidade':str(self.kargs['nif']),
                'ano':str(self.kargs['ano']),
                'mes':str(self.kargs['mes']),
                'area_fiscal':str(self.kargs['area_fiscal']),
                'data_entrega':str(self.kargs['data_apresentacao']),
                'total_factura':str(0),
                'total_base_incidencia':str(0),
                'total_suportado':str(0),
                'total_dedutivel':str(0),
                'estado':'Gerado'
            }
            id_reg_forn = AnexoRegFornecedor(**content).put()
            #guardando as linhas
            #variavel "pos" server para guiar na colocacao de linha regulada e da linha reguladora
            pos=1
            for line in alteracoes:                
                if line['accao'] =='Adicionar':
                    # de acordo com as especificaçoes tecnicas, na acao de adicionar, somente a linha "regularizacao" é necessario,
                    # sendo a linha "decl_anterior" ignorada ou seja vazia
                    info_linhas = line['info_linhas_act']
                    #guardando as linhas do anexo
                    for linha in info_linhas:
                        tot_factura+=int(linha['ln_anx_forn_vl_fatura'])
                        tot_incidencia+=int(linha['ln_anx_forn_Incidencia'])
                        tot_suportado+=int(linha['ln_anx_forn_total_sup'])
                        tot_dedutivel+=int(linha['ln_anx_forn_total_ded'])
                        #linha "regularizacao"                 
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_fornecedor':str(id_reg_forn),
                            'tipo':'regularizacao',
                            'accao':str(line['accao']),
                            'factura':str(linha['ln_anx_forn_factura']),
                            'origem':str(linha['ln_anx_forn_origem']),
                            'nif_fornecedor':str(linha['ln_anx_forn_nif']),
                            'tipo_doc':str(linha['ln_anx_forn_tipoDoc']),
                            'numero_doc':str(linha['ln_anx_forn_num_doc']),
                            'data':str(linha['ln_anx_forn_data']),
                            'valor_factura':str(linha['ln_anx_forn_vl_fatura']),                            
                            'valor_base_incid':str(linha['ln_anx_forn_Incidencia']),
                            'taxa_iva':str(linha['ln_anx_forn_taxa_iva']),
                            'direito_ded':str(linha['ln_anx_forn_direito_ded']),
                            'iva_suportado':str(linha['ln_anx_forn_total_sup']),                            
                            'iva_dedutivel':str(linha['ln_anx_forn_total_ded']),
                            'tipologia':str(linha['ln_anx_forn_tipologia']),                            
                            'linha_mod106':str(29),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegFornecedor(**content).put()
                        #adicionar a informação ao modelo106
                        self.kargs['cp29']= to_decimal(to_decimal(self.kargs['cp29']) + to_decimal(linha['ln_anx_forn_total_ded']))
                        #linha "decl_anterior"
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_fornecedor':str(id_reg_forn),
                            'tipo':'decl_anterior',
                            'accao':str(line['accao']),
                            'factura':'',
                            'origem':'',
                            'nif_fornecedor':'',
                            'tipo_doc':'',
                            'numero_doc':'',
                            'data':'',
                            'valor_factura':'',
                            'valor_base_incid':'',
                            'taxa_iva':'',
                            'direito_ded':'',
                            'iva_suportado':'',
                            'iva_dedutivel':'',
                            'tipologia':'',
                            'linha_mod106':'',
                            'periodo_referencia':'',
                            'iniciativa':'',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegFornecedor(**content).put()
                        pos+=1
                elif line['accao']=='Eliminar':
                    # de acordo com as especificaçoes tecnicas, na acao de Eliminar, a linha "regularizacao" é preenchida com os totais a zero,
                    # sendo a linha "decl_anterior" preenchida exatamente como foi enviada anteriormente

                    info_linhas = line['info_linhas_ant']
                    #guardando as linhas do anexo
                    for linha in info_linhas:
                        tot_factura+=int(linha['valor_factura'])
                        tot_incidencia+=int(linha['valor_base_incid'])
                        tot_suportado+=int(linha['iva_suportado'])
                        tot_dedutivel+=int(linha['iva_dedutivel'])
                        #linha "regularizacao"                 
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_fornecedor':str(id_reg_forn),
                            'tipo':'regularizacao',
                            'accao':str(line['accao']),
                            'factura':str(linha['factura_fornecedor']),
                            'origem':str(linha['origem']),
                            'nif_fornecedor':str(linha['nif_fornecedor']),
                            'tipo_doc':str(linha['tipo_doc']),
                            'numero_doc':str(linha['numero_doc']),
                            'data':str(linha['data']),
                            'valor_factura':str(0),
                            'valor_base_incid':str(0),
                            'taxa_iva':str(linha['taxa_iva']),
                            'direito_ded':str(linha['direito_ded']),
                            'iva_suportado':str(0),
                            'iva_dedutivel':str(0),
                            'tipologia':str(linha['tipologia']),                            
                            'linha_mod106':str(linha['linha_mod106']),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegFornecedor(**content).put()
                        #linha "decl_anterior"
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_fornecedor':str(id_reg_forn),
                            'tipo':'decl_anterior',
                            'accao':str(line['accao']),
                            'factura':str(linha['factura_fornecedor']),
                            'origem':str(linha['origem']),
                            'nif_fornecedor':str(linha['nif_fornecedor']),
                            'tipo_doc':str(linha['tipo_doc']),
                            'numero_doc':str(linha['numero_doc']),
                            'data':str(linha['data']),
                            'valor_factura':str(linha['valor_factura']),
                            'valor_base_incid':str(linha['valor_base_incid']),
                            'taxa_iva':str(linha['taxa_iva']),
                            'direito_ded':str(linha['direito_ded']),
                            'iva_suportado':str(linha['iva_suportado']),
                            'iva_dedutivel':str(linha['iva_dedutivel']),
                            'tipologia':str(linha['tipologia']),                            
                            'linha_mod106':str(30),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegFornecedor(**content).put()
                        #adicionar a informação ao modelo106
                        self.kargs['cp30']= to_decimal(to_decimal(self.kargs['cp30']) + to_decimal(linha['iva_dedutivel']))
                        pos+=1
                elif line['accao']=='Corrigir':                   
                    
                    #guardando as linhas do anexo
                    for linha in line['info_linhas']:
                        linha_act = linha['info_linhas_act']
                        linha_ant = linha['info_linhas_ant']
                        #adicionar os totais do actual
                        tot_factura+=int(linha_act['ln_anx_forn_vl_fatura'])
                        tot_incidencia+=int(linha_act['ln_anx_forn_Incidencia'])
                        tot_suportado+=int(linha_act['ln_anx_forn_total_sup'])
                        tot_dedutivel+=int(linha_act['ln_anx_forn_total_ded'])
                        #adicionar os totais do anterior
                        tot_factura+=int(linha_ant['valor_factura'])
                        tot_incidencia+=int(linha_ant['valor_base_incid'])
                        tot_suportado+=int(linha_ant['iva_suportado'])
                        tot_dedutivel+=int(linha_ant['iva_dedutivel'])                        

                        num_linhaM106 = self.get_linhaM106_correcao_forn(linha_act, linha_ant)

                        #linha "regularizacao"                
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_fornecedor':str(id_reg_forn),
                            'tipo':'regularizacao',
                            'accao':str(line['accao']),
                            'factura':str(linha_act['ln_anx_forn_factura']),
                            'origem':str(linha_act['ln_anx_forn_origem']),
                            'nif_fornecedor':str(linha_act['ln_anx_forn_nif']),
                            'tipo_doc':str(linha_act['ln_anx_forn_tipoDoc']),
                            'numero_doc':str(linha_act['ln_anx_forn_num_doc']),
                            'data':str(linha_act['ln_anx_forn_data']),
                            'valor_factura':str(linha_act['ln_anx_forn_vl_fatura']),
                            'valor_base_incid':str(linha_act['ln_anx_forn_Incidencia']),
                            'taxa_iva':str(linha_act['ln_anx_forn_taxa_iva']),
                            'direito_ded':str(linha_act['ln_anx_forn_direito_ded']),
                            'iva_suportado':str(linha_act['ln_anx_forn_total_sup']),
                            'iva_dedutivel':str(linha_act['ln_anx_forn_total_ded']),
                            'tipologia':str(linha_act['ln_anx_forn_tipologia']),
                            #podera ser tanto 29 como 30 dependendo do total a dedutivel
                            'linha_mod106':str(num_linhaM106),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos),
                        }
                        LinhaAnexoRegFornecedor(**content).put()
                        #adicionar a informaçao ao modelo106
                        campo = "cp{num}".format(num=str(num_linhaM106))                                           
                        self.kargs[campo] = int(to_decimal(self.kargs[campo]) + to_decimal(linha_act['ln_anx_forn_total_ded']))
                        #linha "decl_anterior"
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_fornecedor':str(id_reg_forn),
                            'tipo':'decl_anterior',
                            'accao':str(line['accao']),
                            'factura':str(linha_ant['factura_fornecedor']),
                            'origem':str(linha_ant['origem']),
                            'nif_fornecedor':str(linha_ant['nif_fornecedor']),
                            'tipo_doc':str(linha_ant['tipo_doc']),
                            'numero_doc':str(linha_ant['numero_doc']),
                            'data':str(linha_ant['data']),
                            'valor_factura':str(linha_ant['valor_factura']),
                            'valor_base_incid':str(linha_ant['valor_base_incid']),
                            'taxa_iva':str(linha_ant['taxa_iva']),
                            'direito_ded':str(linha_ant['direito_ded']),
                            'iva_suportado':str(linha_ant['iva_suportado']),
                            'iva_dedutivel':str(linha_ant['iva_dedutivel']),
                            'tipologia':str(linha_ant['tipologia']),                            
                            'linha_mod106':str(linha_ant['linha_mod106']),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegFornecedor(**content).put()
                        #guadar alteraçoes do modelo106
                        campo = "cp{num}".format(num=str(linha_ant['linha_mod106'])) 
                        self.kargs[campo] = int(to_decimal(self.kargs[campo]) + to_decimal(linha_ant['iva_dedutivel']))
                        #self.kargs['cp{num}'.format(num=linha_ant['linha_mod106'])] = to_decimal(to_decimal(self.kargs['cp{num}'.format(num=linha_ant['linha_mod106'])]) + to_decimal(linha_ant['iva_dedutivel']))
                        pos+=1


            #apos inserir as linhas é necessario actualizar os totais do anexo
            content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'id':str(id_reg_forn),
                'total_factura':str(tot_factura),
                'total_base_incidencia':str(tot_incidencia),
                'total_suportado':str(tot_suportado),
                'total_dedutivel':str(tot_dedutivel),
            }
            AnexoRegFornecedor(**content).put()
            self.put()           



    def get_linhaM106_correcao_forn(self, linha_actual, linha_anterior):
        """
        determina qual a linha do modelo 106 que uma correcao de anexo regularizaçao de fornecedor pertence
        """
        if int(linha_actual['ln_anx_forn_total_ded']) > int(linha_anterior['iva_dedutivel']):
            return str(29)
        else:
            return str(30)


    def guardar_regularizacao_cli(self, key):
        """
            guarda todas as informaçoes de anexo regularização de cliente na base de dados
        """
        #get alteracoes
        alteracoes = self.get_alteracoes_cli(key=key)
        self.kargs = get_model_record(model=self,key=key)
        if len(alteracoes)>0:
            #guardando o anexo reg
            tot_factura=0
            tot_incidencia=0
            tot_liquidado=0

            content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'nome': 'anexo_reg_cli_{ano}-{mes}'.format(ano=self.kargs['ano'], mes=self.kargs['mes']),
                'modelo106':str(key),
                'nif_entidade':str(self.kargs['nif']),
                'ano':str(self.kargs['ano']),
                'mes':str(self.kargs['mes']),
                'area_fiscal':str(self.kargs['area_fiscal']),
                'data_entrega':str(self.kargs['data_apresentacao']),
                'total_factura':str(0),
                'total_base_incidencia':str(0),
                'total_liquidado':str(0),
                'estado':'Gerado'
            }
            id_reg_cli = AnexoRegCliente(**content).put()
            #guardando as linhas
            #variavel "pos" server para guiar na colocacao de linha regulada e da linha reguladora
            pos=1
            for line in alteracoes:                
                if line['accao'] =='Adicionar':
                    # de acordo com as especificaçoes tecnicas, na acao de adicionar, somente a linha "regularizacao" é necessario,
                    # sendo a linha "decl_anterior" ignorada ou seja vazia
                    info_linhas = line['info_linhas_act']
                    #guardando as linhas do anexo
                    for linha in info_linhas:
                        tot_factura+=int(linha['ln_anx_cli_vl_fatura'])
                        tot_incidencia+=int(linha['ln_anx_cli_Incidencia'])
                        tot_liquidado+=int(linha['ln_anx_cli_total_Liq'])
                        #linha "regularizacao"               
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_cliente':str(id_reg_cli),
                            'tipo':'regularizacao',
                            'accao':str(line['accao']),
                            'factura':str(linha['ln_anx_cli_factura']),
                            'origem':str(linha['ln_anx_cli_origem']),
                            'nif_cliente':str(linha['ln_anx_cli_nif']),
                            'tipo_doc':str(linha['ln_anx_cli_tipoDoc']),
                            'numero_doc':str(linha['ln_anx_cli_num_doc']),
                            'data':str(linha['ln_anx_cli_data']),
                            'valor_factura':str(linha['ln_anx_cli_vl_fatura']),                            
                            'valor_base_incid':str(linha['ln_anx_cli_Incidencia']),
                            'taxa_iva':str(linha['ln_anx_cli_taxa_iva']),
                            'iva_liquidado':str(linha['ln_anx_cli_total_Liq']),
                            #linha 30 pq o iva e favor ao estado                          
                            'linha_mod106':'30',
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegCliente(**content).put()
                        #adicionar a informação ao modelo106
                        self.kargs['cp30']= to_decimal(to_decimal(self.kargs['cp30']) + to_decimal(linha['ln_anx_cli_total_Liq']))
                        #linha "decl_anterior"
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_cliente':str(id_reg_cli),
                            'tipo':'decl_anterior',
                            'accao':str(line['accao']),
                            'factura':'',
                            'origem':'',
                            'nif_cliente':'',
                            'tipo_doc':'',
                            'numero_doc':'',
                            'data':'',
                            'valor_factura':'',                            
                            'valor_base_incid':'',
                            'taxa_iva':'',
                            'iva_liquidado':'',                          
                            'linha_mod106':'',
                            'periodo_referencia':'',
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegCliente(**content).put()
                        pos+=1
                elif line['accao']=='Eliminar':
                    # de acordo com as especificaçoes tecnicas, na acao de Eliminar, a linha "regularizacao" é preenchida com os totais a zero,
                    # sendo a linha "decl_anterior" preenchida exatamente como foi enviada anteriormente

                    info_linhas = line['info_linhas_ant']
                    #guardando as linhas do anexo
                    for linha in info_linhas:
                        tot_factura+=int(linha['valor_factura'])
                        tot_incidencia+=int(linha['valor_base_incidencia'])
                        tot_liquidado+=int(linha['iva_liquidado'])
                        #linha "regularizacao"                 
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_cliente':str(id_reg_cli),
                            'tipo':'regularizacao',
                            'accao':str(line['accao']),
                            'factura':str(linha['factura_cliente']),
                            'origem':str(linha['origem']),
                            'nif_cliente':str(linha['nif_cliente']),
                            'tipo_doc':str(linha['tipo_doc']),
                            'numero_doc':str(linha['numero_doc']),
                            'data':str(linha['data']),
                            'valor_factura':str(0),                            
                            'valor_base_incid':str(0),
                            'taxa_iva':str(0),
                            'iva_liquidado':str(0),                          
                            'linha_mod106':str(linha['linha_mod106']),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegCliente(**content).put()
                        #linha "decl_anterior"
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_cliente':str(id_reg_cli),
                            'tipo':'decl_anterior',
                            'accao':str(line['accao']),
                            'factura':str(linha['factura_cliente']),
                            'origem':str(linha['origem']),
                            'nif_cliente':str(linha['nif_cliente']),
                            'tipo_doc':str(linha['tipo_doc']),
                            'numero_doc':str(linha['numero_doc']),
                            'data':str(linha['data']),
                            'valor_factura':str(linha['valor_factura']),                            
                            'valor_base_incid':str(linha['valor_base_incidencia']),
                            'taxa_iva':str(linha['taxa_iva']),
                            'iva_liquidado':str(linha['iva_liquidado']),                          
                            'linha_mod106':str(linha['linha_mod106']),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT',
                            'posicao':str(pos)
                        }
                        LinhaAnexoRegCliente(**content).put()
                        #adicionar a informação ao modelo106
                        self.kargs['cp29']= to_decimal(to_decimal(self.kargs['cp29']) + to_decimal(linha['iva_liquidado']))
                        pos+=1
                elif line['accao']=='Corrigir':                   
                    
                    #guardando as linhas do anexo
                    for linha in line['info_linhas']:
                        linha_act = linha['info_linhas_act']
                        linha_ant = linha['info_linhas_ant']
                        #adicionar os totais do actual
                        tot_factura+=int(linha_act['ln_anx_cli_vl_fatura'])
                        tot_incidencia+=int(linha_act['ln_anx_cli_Incidencia'])
                        tot_liquidado+=int(linha_act['ln_anx_cli_total_Liq'])
                        #adicionar os totais do anterior
                        tot_factura+=int(linha_ant['valor_factura'])
                        tot_incidencia+=int(linha_ant['valor_base_incidencia'])
                        tot_liquidado+=int(linha_ant['iva_liquidado'])
                        #determinar a linha do modelo 106 que entre  esta alteração                       
                        num_linhaM106 = self.get_linhaM106_correcao_cli(linha_act=linha_act, linha_ant=linha_ant)
                        
                        #linha "regularizacao"                 
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'tipo':'regularizacao',
                            'accao':str(line['accao']),
                            'posicao':str(pos),
                            'anexo_reg_cliente':str(id_reg_cli),
                            'factura':str(linha_act['ln_anx_cli_factura']),
                            'origem':str(linha_act['ln_anx_cli_origem']),
                            'nif_cliente':str(linha_act['ln_anx_cli_nif']),
                            'tipo_doc':str(linha_act['ln_anx_cli_tipoDoc']),
                            'numero_doc':str(linha_act['ln_anx_cli_num_doc']),
                            'data':str(linha_act['ln_anx_cli_data']),
                            'valor_factura':str(linha_act['ln_anx_cli_vl_fatura']),                            
                            'valor_base_incid':str(linha_act['ln_anx_cli_Incidencia']),
                            'taxa_iva':str(linha_act['ln_anx_cli_taxa_iva']),
                            'iva_liquidado':str(linha_act['ln_anx_cli_total_Liq']),                          
                            'linha_mod106':str(num_linhaM106),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':'CT'                            
                        }

                        LinhaAnexoRegCliente(**content).put()
                        #adicionar a informaçao ao modelo106
                        campo = "cp{num}".format(num=str(num_linhaM106))                                           
                        self.kargs[campo] = int(to_decimal(self.kargs[campo]) + to_decimal(linha_act['ln_anx_cli_total_Liq']))                       
                        
                        #linha "decl_anterior"
                        content={
                            'user': '{user}'.format(user=bottle.request.session['user']),
                            'anexo_reg_cliente':str(id_reg_cli),
                            'tipo':'decl_anterior',
                            'accao':str(line['accao']),
                            'factura':str(linha_ant['factura_cliente']),
                            'origem':str(linha_ant['origem']),
                            'nif_cliente':str(linha_ant['nif_cliente']),
                            'tipo_doc':str(linha_ant['tipo_doc']),
                            'numero_doc':str(linha_ant['numero_doc']),
                            'data':str(linha_ant['data']),
                            'valor_factura':str(linha_ant['valor_factura']),                            
                            'valor_base_incid':str(linha_ant['valor_base_incidencia']),
                            'taxa_iva':str(linha_ant['taxa_iva']),
                            'iva_liquidado':str(linha_ant['iva_liquidado']),                          
                            'linha_mod106':str(linha_ant['linha_mod106']),
                            'periodo_referencia':'{ano}-{mes}'.format(ano=str(self.kargs['ano']),mes=str(self.kargs['mes'])),
                            'iniciativa':str('CT'),
                            'posicao':str(pos),
                        }
                        LinhaAnexoRegCliente(**content).put()
                        #adicionar a informação ao modelo1060
                        campo = "cp{num}".format(num=str(linha_ant['linha_mod106'])) 
                        self.kargs[campo] = int(to_decimal(self.kargs[campo]) + to_decimal(linha_ant['iva_liquidado']))
                        pos+=1
            #apos inserir as linhas é necessario actualizar os totais do anexo
            content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'id':str(id_reg_cli),
                'total_factura':str(tot_factura),
                'total_base_incidencia':str(tot_incidencia),
                'total_liquidado':str(tot_liquidado),
            }

            AnexoRegCliente(**content).put()
            #guardar alteraçoes do modelo 106
            self.put()            


    def get_linhaM106_correcao_cli(self, linha_act, linha_ant):
        """
        determina qual a linha do modelo 106 que uma correcao de anexo regularizaçao de cliente pertence
        """        
        if int(linha_act['ln_anx_cli_total_Liq']) > int(linha_ant['iva_liquidado']):            
            return str(30)
        else:
            return str(29)