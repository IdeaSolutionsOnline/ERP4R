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
__model_name__='ano_fiscal.AnoFiscal'
import auth, base_models
from orm import *
from form import *

class AnoFiscal(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'ano_fiscal'
        self.__title__= 'Anos Fiscais'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'ano_fiscal.nome'
        self.__workflow__ = (
            'estado', {'Rascunho':['Activar', 'Gera Periodos'], 'Activo':['Encerrar', 'Cancelar'], 'Encerrado':['Cancelar'], 'Cancelado':['Rascunho']}
            )
        self.__workflow_auth__ = {
            'Gera Periodos':['Contabilista'],
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
        self.__no_edit__ = [
            ('estado', ['Encerrado','Cancelado'])
            ]
        self.__get_options__ = ['nome']

        self.nome = string_field(view_order=1, name='Nome', size=60)
        self.estado = info_field(view_order=2, name='Estado', size=60, default='Rascunho')
        self.periodos = list_field(view_order=3, name='Periodos', condition="ano_fiscal='{id}'", model_name='periodo.Periodo', list_edit_mode='inline', onlist=False)


    def Gera_Periodos(self, key, window_id):
        """Gera os periodos base para o Ano Fiscal"""
        #print('inicio de gera periodos')
        self.kargs = get_model_record(model=self, key=key)
        try:
            from my_periodo import Periodo
        except:
            from periodo import Periodo
        ano_fiscal = self.kargs['nome']
        #print('1')
        periodos = {
        'Abe':['abertura', '01/01/' + ano_fiscal, '01/01/' + ano_fiscal],
        'Enc':['encerramento', '31/12/' + ano_fiscal, '31/12/' + ano_fiscal],
        'Apu':['apuramento', '31/12/' + ano_fiscal, '31/12/' + ano_fiscal],
        'Jan':['normal', '01/01/' + ano_fiscal, '31/01/' + ano_fiscal],
        'Fev':['normal', '01/02/' + ano_fiscal, '28/02/' + ano_fiscal],
        'Mar':['normal', '01/03/' + ano_fiscal, '31/03/' + ano_fiscal],
        'Abr':['normal', '01/04/' + ano_fiscal, '30/04/' + ano_fiscal],
        'Mai':['normal', '01/05/' + ano_fiscal, '31/05/' + ano_fiscal],
        'Jun':['normal', '01/06/' + ano_fiscal, '30/06/' + ano_fiscal],
        'Jul':['normal', '01/07/' + ano_fiscal, '31/07/' + ano_fiscal],
        'Ago':['normal', '01/08/' + ano_fiscal, '31/08/' + ano_fiscal],
        'Set':['normal', '01/09/' + ano_fiscal, '30/09/' + ano_fiscal],
        'Out':['normal', '01/10/' + ano_fiscal, '31/10/' + ano_fiscal],
        'Nov':['normal', '01/11/' + ano_fiscal, '30/11/' + ano_fiscal],
        'Dez':['normal', '01/12/' + ano_fiscal, '31/12/' + ano_fiscal],
        }
        for p in periodos:
            Periodo(ano_fiscal=self.kargs['id'], nome=p+ano_fiscal, tipo=periodos[p][0], data_inicial=periodos[p][1], data_final=periodos[p][2], user=self.kargs['user']).put()
        #print('fim de gera periodos')
        return form_edit(window_id=window_id).show()

    def Activar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Activo'
        self.put()
        return form_edit(window_id=window_id).show()

    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Encerrar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Encerrado'
        self.put()
        return form_edit(window_id=window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()
