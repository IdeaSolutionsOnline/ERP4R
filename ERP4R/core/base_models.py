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

#import os, sys
#sys.path.append(os.getcwd())
#import bottle
from orm import *
from form import *

class Sequence(Model):
    """Este modelo serve para quardar as sequencias de numeração para documentos como facturas por exemplo!"""
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'sequence'
        self.__title__ = 'Sequences'
        self.__model_name__ = 'base_models.Sequence'

        self.domain = string_field(view_order=1, name='Dominio', size=60)
        self.number = integer_field(view_order=2, name='Número', size=60)
        
        self.__list_edit_mode__ = 'inline'
        self.__on_create_sql__ = ""
        self.__workflow__ = ()

    def get_options(self):
        options = []
        opts = self.get()
        for option in opts:
            options.append((str(option['id']), option['domain']))
        return options

    def get_sequence(self, domain):
        """cria sequencias para documentos, penso que tem que ser revisto, aparentemente por vezes não lê e depois inicia a sequencia de novo"""
        self.where = "domain = '{domain}'".format(domain=domain)
        self.kargs = self.get()
        #print (self.kargs)
        if self.kargs:
            self.kargs = self.kargs[0]
            self.kargs['number'] = self.kargs['number'] + 1
            self.kargs['user'] = bottle.request.session['user']
            self.put()
            return self.kargs['number']
        else:
            #try a few more times,this it's a temporary turn around for the problem
            for z in range(10):
                self.kargs = self.get()
                if self.kargs:
                    self.kargs = self.kargs[0]
                    self.kargs['number'] = self.kargs['number'] + 1
                    self.kargs['user'] = bottle.request.session['user']
                    self.put()
                    return self.kargs['number']
            self.kargs = {'domain':domain, 'number':1, 'user':bottle.request.session['user']}
            self.put()
            return self.kargs['number']

