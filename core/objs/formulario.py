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
__model_name__ = 'formulario.Formulario'
import auth, base_models
from orm import *
from form import *

import random
import string
import time

class Formulario(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'formulario'
        self.__title__ ='Formulario da manifestação' 
        self.__model_name__ = __model_name__
        #self.__get_options__ = 'formulario.nomecompleto'
        self.__list_edit_mode__ = 'edit'
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['Funcionario'],
            'delete':['DGPOG'],
            'full_access':['DGPOG']
            }
        self.__get_options__ = ['nomecompleto']
        
        self.__workflow__ = (
            'estado',{'Rascunho':['Confirmar','Cancelar'], 'Confirmado':['Send_email']}
            )           
        self.__workflow_auth__ = {
            'Rascunho':['All'],
            'Confirmar':['All'],
            'Cancelar':['All'],            
            'Send_email':['estado'],
            'full_access':['estado']
            }

        self.nomecompleto = string_field(view_order=1 , name='Nome completo', size=80)
        self.email = email_field(view_order=2 , name='Correio eletrónico', size=80)
        self.utilizador = string_field(view_order = 3, name = 'Utilizador', size = 40)
        self.password = password_field(view_order = 4, name = 'Password', size = 40)
        self.estado = combo_field(view_order=5, name='Estado', hidden=True ,size=40,  default='Rascunho', onlist = True)
        #self.estado = combo_field(view_order=5, name='Estado', options=[('cancelado','Cancelado'), ('activo','Activo')], default='Activo', hidden= True, onlist = False)
        #self.fichainscricao = list_field(view_order=6, name='Ficha de inscricao ', simple=True, show_footer=False, fields=['email'], condition="formulario='{id}'", model_name='fichainscricao.Fichainscricao', list_edit_mode='inline', hidden= False, onlist = False)
        #self.residecom = choice_field(view_order=4, name='Reside com', size=70, model='residencia', column='residecom', options="model.get_opts('Residencia().get_self()')")
        #self.parentesco = list_field(view_order = 4, name = 'Parentesco', model_name = 'parentesco.Parentesco', condition = "formulario='{id}'", show_footer = False, list_edit_mode = 'edit', onlist = False)
 
    def get_self(self):
        return self.get_options()

    def get_opt(self, model):
        return eval(model + '().get_options()')

    def get_opts(self, get_str):
        return eval(get_str)

    def addForm(self,user=None,nomefun=None,emailfun=None,utilsistema=None,passutil=None):
        try:
            content = {
            'user':user,
            'nomecompleto':nomefun,
            'email':emailfun,
            'utilizador':utilsistema,
            'password':passutil,
            'estado':'Pendente',            
            }
            Formulario(**content).put()
            return True
        except:
            return False
    

    def get_formulario(self):

        result = [] 
        sql = "SELECT f.nomecompleto as nomefun, f.email as emailfun, f.utilizador as utilsistema, f.password as passutil FROM formulario"
        try:
           result = run_sql(sql)
           print('>>>>>>>>>>>>>>>>>>>>>>>>>>>> '+str(result))
        except:
           
           print("except-----------------------")        
        return result


    def Cancelar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Confirmar(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Confirmado'
        self.put()
        return form_edit(window_id = window_id).show()

    def Rascunho(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Rascunho'
        self.put()
        return form_edit(window_id=window_id).show()
    
    def Send_email(self, key, window_id):
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'send_email():'
        self.put()
        return form_edit(window_id = window_id).show()    

   
    def mkpass(size=16):
        chars = []
        chars.extend([i for i in string.ascii_letters])
        chars.extend([i for i in string.digits])
        chars.extend([i for i in '\'"!@#$%&*()-_=+[{}]~^,<.>;:/?'])
    
        password = ''
    
        for i in range(size):
            password += chars[random.randint(0,  len(chars) - 1)]
        
            random.seed = int(time.time())
            random.shuffle(chars)
        
        return password    

################## formulario login 

   # def addLogin(self,user=None,utilsistema=None,passutil=None):
    #    try:
     #       content = {
      #      'user':user,
       #     'utilizador':utilsistema,
        #    'password':passutil,
         #   'estado':'Pendente',            
          #  }
           # Formulario(**content).put()
           # return True
        #except:
         #   return False    