# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
É utilizado na Restituição do IUR e permite ao Gestor do tesouro mudar cabimentos validados de um técnico para outro e assim gerir melhor os pagamentos
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__= 'sai_muda_user.SaiMudaUser'
#import auth, base_models
from orm import *
from form import *
try:
    from my_users import Users
except:
    from users import Users

class SaiMudaUser(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sai_muda_user'
        self.__title__= 'Redestribui validados para outro técnico'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'sai_muda_user.data DESC'
        self.__workflow__ = (
            'estado', {'Rascunho':['Executar'], 'Executado':[]}
            )
        self.__workflow_auth__ = {
            'Executar':['Gestor Tesouro'],
            'full_access':['Gestor Tesouro']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor Tesouro'],
            'create':['Gestor Tesouro'],
            'delete':['Administrador'],
            'full_access':['Administrador']
            }
        self.__no_edit__ = [('estado', ['Executado'])]
        self.__get_options__ = ['data']

        self.de_utilizador = combo_field(view_order=1, name='Do Utilizador', size=60, args='required', model='users', column='nome', options="model.get_opts('Users().get_options()')")
        self.para_utilizador = combo_field(view_order=2, name='Para Utilizador', size=60, args='required', model='users', column='nome', options="model.get_opts('Users().get_options()')")
        self.quantidade = integer_field(view_order=3, name='Quantidade', size=60)
        self.data = date_field(view_order=4, name='Data', size=60, args='readonly')
        self.estado = info_field(view_order=8, name='Estado', size=60, default='Rascunho')

    def Executar(self, key, window_id):
        print('in executar')
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Executado'
        self.kargs['data'] = datetime.datetime.today()
        quantidade = self.kargs['quantidade']
        de = self.kargs['de_utilizador']
        de = Users().get(key=de)[0]['nome']
        #print(de)
        para = self.kargs['para_utilizador']
        para = Users().get(key=para)[0]['nome']
        #print(para)
        sql = "update sai_rest_iur_validados set utilizador = '{para}' where cabimento in (select cabimento from sai_rest_iur_validados where utilizador = '{de}' and estado = 'Validado' limit {quantidade})".format(para=para, de=de, quantidade=quantidade)
        print(sql)
        run_sql(sql)
        self.put()
        return form_edit(window_id=window_id).show()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)