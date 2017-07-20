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
__model_name__ = 'campos_modelo106.CamposModelo106'
import auth, base_models
from orm import *
from form import *
from modelo106 import Modelo106


class CamposModelo106(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'campos_modelo106'
        self.__title__ = 'Campos do Modelo106'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['modelo106']

        self.modelo106 = combo_field(view_order = 0, name = 'Modelo 106', onchange='modelo106_onchange',args='required', model_name = 'modelo106.Modelo106', onlist = True, options="model.get_opts('Modelo106().get_options()')")
        self.cp01 = string_field(view_order= 1, name ='Campo 01', args='required', size=45)
        self.cp02 = string_field(view_order= 2, name ='Campo 02', args='required', size=45)
        self.cp03 = string_field(view_order= 3, name ='Campo 03', args='required', size=45)
        self.cp04 = string_field(view_order= 4, name ='Campo 04', args='required', size=45)
        self.cp05 = string_field(view_order= 5, name ='Campo 05', args='required', size=45,onlist=False)
        self.cp06 = string_field(view_order= 6, name ='Campo 06', args='required', size=45,onlist=False)
        self.cp07 = string_field(view_order= 7, name ='Campo 07', args='required', size=45,onlist=False)
        self.cp08 = string_field(view_order= 8, name ='Campo 08', args='required', size=45,onlist=False)
        self.cp09 = string_field(view_order= 9, name ='Campo 09', args='required', size=45,onlist=False)
        self.cp10 = string_field(view_order=10, name ='Campo 10', args='required', size=45,onlist=False)
        self.cp11 = string_field(view_order=11, name ='Campo 11', args='required', size=45,onlist=False)
        self.cp12 = string_field(view_order=12, name ='Campo 12', args='required', size=45,onlist=False)
        self.cp13 = string_field(view_order=13, name ='Campo 13', args='required', size=45,onlist=False)
        self.cp14 = string_field(view_order=14, name ='Campo 14', args='required', size=45,onlist=False)
        self.cp15 = string_field(view_order=15, name ='Campo 15', args='required', size=45,onlist=False)
        self.cp16 = string_field(view_order=16, name ='Campo 16', args='required', size=45,onlist=False)
        self.cp17 = string_field(view_order=17, name ='Campo 17', args='required', size=45,onlist=False)
        self.cp18 = string_field(view_order=18, name ='Campo 18', args='required', size=45,onlist=False)
        self.cp19 = string_field(view_order=19, name ='Campo 19', args='required', size=45,onlist=False)
        self.cp20 = string_field(view_order=20, name ='Campo 20', args='required', size=45,onlist=False)
        self.cp21 = string_field(view_order=21, name ='Campo 21', args='required', size=45,onlist=False)
        self.cp22 = string_field(view_order=22, name ='Campo 22', args='required', size=45,onlist=False)
        self.cp23 = string_field(view_order=23, name ='Campo 23', args='required', size=45,onlist=False)
        self.cp24 = string_field(view_order=24, name ='Campo 24', args='required', size=45,onlist=False)
        self.cp25 = string_field(view_order=25, name ='Campo 25', args='required', size=45,onlist=False)
        self.cp26 = string_field(view_order=26, name ='Campo 26', args='required', size=45,onlist=False)
        self.cp27 = string_field(view_order=27, name ='Campo 27', args='required', size=45,onlist=False)
        self.cp28 = string_field(view_order=28, name ='Campo 28', args='required', size=45,onlist=False)
        self.cp29 = string_field(view_order=29, name ='Campo 29', args='required', size=45,onlist=False)
        self.cp30 = string_field(view_order=30, name ='Campo 30', args='required', size=45,onlist=False)
        self.cp31 = string_field(view_order=31, name ='Campo 31', args='required', size=45,onlist=False)
        self.cp32 = string_field(view_order=32, name ='Campo 32', args='required', size=45,onlist=False)
        self.cp33 = string_field(view_order=33, name ='Campo 33', args='required', size=45,onlist=False)
        self.cp34 = string_field(view_order=34, name ='Campo 34', args='required', size=45,onlist=False)
        self.cp35 = string_field(view_order=35, name ='Campo 35', args='required', size=45,onlist=False)
        self.cp36 = string_field(view_order=36, name ='Campo 36', args='required', size=45,onlist=False)
        self.cp37 = string_field(view_order=37, name ='Campo 37', args='required', size=45,onlist=False)
        self.cp38 = string_field(view_order=38, name ='Campo 38', args='required', size=45,onlist=False)
        self.cp39 = string_field(view_order=39, name ='Campo 39', args='required', size=45,onlist=False)
        self.cp40 = string_field(view_order=40, name ='Campo 40', args='required', size=45,onlist=False)
        self.cp41 = string_field(view_order=41, name ='Campo 41', args='required', size=45,onlist=False)
        self.cp42 = string_field(view_order=42, name ='Campo 42', args='required', size=45,onlist=False)
        self.cp43 = string_field(view_order=43, name ='Campo 43', args='required', size=45,onlist=False)
        self.cp44 = string_field(view_order=44, name ='Campo 44', args='required', size=45,onlist=False)
        self.cp45 = string_field(view_order=45, name ='Campo 45', args='required', size=45,onlist=False)
        self.cp46 = string_field(view_order=46, name ='Campo 46', args='required', size=45,onlist=False)
        self.cp47 = string_field(view_order=47, name ='Campo 47', args='required', size=45,onlist=False)
        self.cp48 = string_field(view_order=48, name ='Campo 48', args='required', size=45,onlist=False)
        self.cp49 = string_field(view_order=49, name ='Campo 49', args='required', size=45,onlist=False)
        self.cp50 = string_field(view_order=50, name ='Campo 50', args='required', size=45,onlist=False)



    def get_opts(self, get_str):       
        return eval(get_str)