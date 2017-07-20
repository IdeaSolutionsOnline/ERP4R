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
__model_name__ = 'contacto.Contacto'
import auth, base_models
from orm import *
from form import *

class Contacto(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'contacto'
        self.__title__= 'Contactos de Terceiros'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }
        #self.__get_options__ = ['nome']

        self.terceiro = parent_field(view_order=1 , name='Terceiro', hidden=True, nolabel=True, onlist=False, model_name='terceiro.Terceiro', column='nome')
        self.tipo = combo_field(view_order=2 , name='Tipo', args='required', size=40, options=[('defeito','Defeito'), ('facturacao','Facturação'), ('entrega','Entrega'),('funcionario','Funcionario'),('representante','Representante')])
        self.nome = string_field(view_order=3 , name='Nome', args='required', size=80)
        self.funcao = string_field(view_order=4 , name='Função', size=40)
        self.morada = string_field(view_order=5 , name='Morada', size=100)
        self.cidade = string_field(view_order=6 , name='Cidade', onlist=False, size=40)
        self.ilha = string_field(view_order=7 , name='Ilha', onlist=False, size=40)
        self.concelho = string_field(view_order=8 , name='Concelho', onlist=False, size=40)
        self.pais = string_field(view_order=9 , name='País', onlist=False, size=40)
        self.telefone = string_field(view_order=10 , name='Telefone', size=40)
        self.telemovel = string_field(view_order=11 , name='Telemóvel', size=40)
        self.fax = string_field(view_order=12 , name='Fax', onlist=False, size=40)
        self.email = string_field(view_order=13 , name='Email', onlist=False, size=100)
        self.www = string_field(view_order=14 , name='WWW', onlist=False, size=100)

    def get_options(self, terceiro=None):
        """Este get_options só devolve os contactos do terceiro em causa"""
        options = []
        opts = self.get()
        for f in get_model_fields(self):
            if f[0] == 'tipo':
                field=f
        for option in opts:
            if terceiro:
                if str(option['terceiro']) == str(terceiro):
                    tipo = get_field_value(record=option, field=field, model=self)['field_value'][1]
                    options.append((str(option['id']), '{tipo}: {nome}'.format(nome=option['nome'], tipo=tipo)))
            else:
                nome = get_field_value(record=option, field=field, model=self)['field_value']
                options.append((str(option['id']), '{nome}'.format(nome=nome)))
        return options
