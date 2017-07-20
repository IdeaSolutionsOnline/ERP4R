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
__model_name__='contrato.Contrato'
import base_models
from orm import *
from form import *
try:
    from my_terceiro import Terceiro
except:
    from terceiro import Terceiro
try:
    from my_zona import Zona
except:
    from zona import Zona

class Contrato(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'contrato'
        self.__title__= 'Contratos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(contrato.numero)'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['Gestor']
            }
        self.__get_options__ = ['numero']
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Inspecionar'], 'Inspecionado':['Imprimir', 'Activar'], 'Activo':['Imprimir', 'Suspender', 'Cancelar'], 'Suspenso':['Reactivar','Cancelar'], 'Cortado':['Reactivar','Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Vendedor'],
            'Inspecionar':['Inspector'],
            'Imprimir':['All'],
            'Activar':['Vendedor'],
            'Reactivar':['Vendedor'],
            'Suspender':['Vendedor'],
            'Cancelar':['Gestor'],
            'Rascunho':['Gestor'],
            'full_access':['Gestor'],
            }
        self.__workflow_context__ = {
            }
        self.__no_edit__ = [
            ('estado', ['Activo','Cancelado','Suspenso', 'Cortado'])
            ]

        self.numero = info_field(view_order=1, name='Número', )
        self.data_pedido = date_field(view_order=2, name='Data Pedido', args='required', onlist=False, default=datetime.date.today())
        self.cliente = choice_field(view_order=3, name='Cliente', args='required', size=60, model='terceiro', column='nome', options='model.get_clientes()')
        self.data_aprovacao = date_field(view_order=4, name='Data Aprovação', onlist=False)
        self.data_assinatura = date_field(view_order=5, name='Data Assinatura', onlist=False)
        self.zona = choice_field(view_order=6, name='Zona', args='required', size=60, model='zona', column='nome', options='model.get_zonas()')
        self.data_instalacao = date_field(view_order=7, name='Data Instalação', onlist=False)
        self.responsabilidade = combo_field(view_order=8, name='Responsabilidade', onlist=False, default='proprietario', args='required', size=60, options=[('inquilino','Inquilino'),('proprietario','Proprietário'),('instituicao','Instituição'),('outro','Outro')])
        self.estado = info_field(view_order=9, name='Estado', default='Rascunho')
        self.tipo = combo_field(view_order=10, name='Tipo', args='required', default='domiciliar', size=60, options=[('domiciliar','Domiciliar'),('alagamento','Agricula P/Alagamento'),('gotagota','Agricola Gota-a-Gota'),('industrial','Industrial'),('instituicao','Instituição'),('social','Social')])
        self.documento = combo_field(view_order=11, name='Documento', size=60, search=False, onlist=False, options=[('bi','Bilhete ID'), ('passaporte', 'Passaporte'), ('outro','Outro')])
        self.numero_documento = string_field(view_order=12, name ='NºDocumento', size=60, onlist=False, search=False)
        self.contactos = list_field(view_order=13, name='Endereços', model_name='contacto.Contacto', condition="contrato={id}", fields=['tipo', 'nome', 'morada'], show_footer=False, simple=True, list_edit_mode='inline')#, colspan=2, field_filter=("terceiro='{value}'",'cliente'),
        #ainda não é possivel fazer estes tipos de campos required :-(
        self.contador_contrato = list_field(view_order=14, name='Contadores', fields=['contador', 'estado'], show_footer=False, model_name='contador_contrato.ContadorContrato', condition="contrato='{id}'", list_edit_mode='inline')#colspan=2, 
        self.informacao_tecnica = text_field(view_order=15, name='Informação Técnica', args='rows=3', size=80, onlist=False, search=False)#, colspan=3
        self.inspeccao = list_field(view_order=16, name='Inspecções', model_name='inspeccao.Inspeccao', condition="contrato='{id}'", list_edit_mode='inline')

    def get_clientes(self):
        return Terceiro().get_clientes()

    def get_zonas(self):
        return Zona().get_options()

    def Imprimir(self, key, window_id):
        """Imprime o Contrato para assinatura!!!"""
        self.kargs = get_model_record(model=self, key=key)
        # Ver como Fazer isto da melhor maneira e pensando já no futuro!!!
        #self.kargs['estado'] = 'Inspecionado'
        #self.put()
        return form_edit(window_id = window_id).show()

    def Inspecionar(self, key, window_id):
        """verificar se o contrato tem pelo menos uma linha de inspecção no estado 'Aprovado'!!!, se sim muda o estado e se não tiver data de aprovação preenche com a data de hoje"""
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_inspeccao import Inspeccao
        except:
            from inspeccao import Inspeccao
        inspeccoes = Inspeccao(where = "contrato = '{contrato_id}'".format(contrato_id=self.kargs['id'])).get()
        inspeccao_aprovada = False
        if len(inspeccoes) > 0:
            for inspeccao in inspeccoes:
                if inspeccao['resultado'] == 'aprovado':
                    inspeccao_aprovada = True
        if inspeccao_aprovada:
            self.kargs['estado'] = 'Inspecionado'
            if not self.kargs['data_aprovacao']:
                self.kargs['data_aprovacao'] = datetime.date.today()
            self.put()
            return form_edit(window_id = window_id).show()
        else:
            return error_message('Não pode aprovar um contrato sem ter uma Inspecção Aprovada!')

    def Activar(self, key, window_id):
        """verificar se temos um contador activo, e caso as datas de instalação e assinatura estiverem vazias preenche com a data de hoje, a partir daqui o contrato fica read-only"""
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_contador_contrato import ContadorContrato
        except:
            from contador_contrato import ContadorContrato
        contadores = ContadorContrato(where = "contrato = '{contrato_id}'".format(contrato_id=self.kargs['id'])).get()
        contador_activo = False
        if len(contadores) > 0:
            for contador in contadores:
                if contador['estado'] == 'activo':
                    contador_activo = True
        if contador_activo:
            if not self.kargs['data_instalacao']:
                self.kargs['data_instalacao'] = datetime.date.today()
            if not self.kargs['data_assinatura']:
                self.kargs['data_assinatura'] = datetime.date.today()
            self.kargs['estado'] = 'Activo'
            self.put()
            return form_edit(window_id = window_id).show()
        else:
            return error_message('Não pode activar um contrato sem ter um contador activo!')

    def Reactivar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Activo'
        self.put()
        return form_edit(window_id = window_id).show()

    def Suspender(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Suspenso'
        self.put()
        return form_edit(window_id = window_id).show()

    def Confirmar(self, key, window_id):
        """verificar se o campo contactos está preenchido, tem que ter um contacto do tipo consumo e outro facturação ou então um do tipo defeito, se sim muda o estado para confirmado e atribui-lhe um numero novo utilizando as sequencias!"""
        if key in ['None', None]:
            m_action = model_action(obj=self)
            m_action.save(key=None, internal=True)
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_contacto import Contacto
        except:
            from contacto import Contacto
        contactos = Contacto(where = "contrato = '{contrato_id}'".format(contrato_id=self.kargs['id'])).get()
        contacto_facturacao = False
        contacto_consumo = False
        if len(contactos) > 0:
            for contact in contactos:
                if contact['tipo'] == 'facturacao' or contact['tipo'] == 'defeito':
                    contacto_facturacao = True
                if contact['tipo'] == 'consumo' or contact['tipo'] == 'defeito':
                    contacto_consumo = True
        if contacto_facturacao and contacto_consumo:
            if not self.kargs['numero']:
                self.kargs['numero'] = base_models.Sequence().get_sequence('contrato')
            self.kargs['estado'] = 'Confirmado'
            self.put()
            return form_edit(window_id = window_id).show()
        else:
            return error_message('Não pode confirmar contratos sem Moradas de Facturação e Consumo ou então uma do Tipo "Por Defeito!"!')

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

