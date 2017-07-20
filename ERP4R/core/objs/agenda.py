# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVtek dev"
__status__ = "Development"
__model_name__ = 'agenda.Agenda'
import auth, base_models
from orm import *
from form import *

class Agenda(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'agenda'
        self.__title__ ='Agenda de Tarefas'
        self.__model_name__ = __model_name__
        self.__get_options__ = ['numero']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'agenda.data_inicio'
        self.__auth__ = {
            'read':['All'],
            'write':['Gestor'],
            'create':['Gestor'],
            'delete':['Gestor'],
            'full_access':['Gestor']
        }
        self.data_inicio = date_field(view_order = 1, name = 'dataInicio', size=50, default = datetime.date.today())    
        self.hora_inicio = time_field(view_order=2, name ='horaInicio', size=50, default=time.strftime('%H:%M'))
        self.data_fim = date_field(view_order = 3, name = 'dataFim', size=50, default = datetime.date.today())    
        self.hora_fim = time_field(view_order=4, name ='horaFim', size=50, default=time.strftime('%H:%M'))
        self.descricao = text_field(view_order=5, name='descricao', size=70, args="rows=40", onlist=True, search=False)

    #Retornar agenda
    def get_agenda(self, window_id):
        return form_agenda(window_id=window_id).show()

    def validarDatas(self, dataInicio, horaInicio, dataFim, horaFim, descricao):
        
        from datetime import date, time 
        
        dia, mes, ano = str(dataInicio).split("-")
        dataI = datetime.date(int(ano), int(mes), int(dia))
        
        ano, mes, dia = str(dataFim).split("-")
        dataF = datetime.date(int(ano), int(mes), int(dia))
        
        hora, minuto = str(horaInicio).split(":")
        horaI = datetime.time(int(hora), int(minuto))

        hora, minuto = str(horaFim).split(":")
        horaF = datetime.time(int(hora), int(minuto))
        print("Hora inicio ##########"+str(dataI))
        print("Hora fim #############"+str(dataF))
        if(dataF < dataI):
            return "erroData"
        if(dataI == dataF) & (horaI > horaF):
            return "erroHora"

            #Aparentemente parece tudo bom
        option = []
        opts = self.get()

        for options in opts:
                
            DataInicioTeste = str(options['data_inicio'])
            DataFimTeste = str(options['data_fim'])
            
            ano,mes,dia = DataInicioTeste.split("-")
            dataI2 = datetime.date(int(ano), int(mes), int(dia))

            ano,mes,dia = DataFimTeste.split("-")
            dataF2 = datetime.date(int(ano), int(mes), int(dia))

            horaInicioTeste = str(options['hora_inicio'])
            horaFimTeste = str(options['hora_fim'])
            
            hora, minuto, segundos= horaInicioTeste.split(":")
            horaI2 = datetime.time(int(hora), int(minuto))

            hora, minuto, segundos = horaFimTeste.split(":")
            horaF2 = datetime.time(int(hora), int(minuto))

            if (dataI < dataI2 and dataF < dataI2) or (dataI > dataF2 and dataF > dataF2):
                print("Tudo Bem")
            elif (horaI < horaI2 and horaF < horaI2) or (horaI > horaF2 and horaF > horaF2):
                print("Tudo Bem")
            else:
                return "dataIndisponivel"
        return "dataDisponivel" 
        
    def guardarTarefa(self, dataInicio, horaInicio, dataFim, horaFim, descricao):
        result = self.validarDatas(dataInicio, horaInicio, dataFim, horaFim, descricao)
        
        if result != "dataDisponivel":
            return result
        else:     
            try:
                content = {
                'user': '{user}'.format(user=bottle.request.session['user']), 
                'data_inicio': dataInicio,  
                'hora_inicio': horaInicio, 
                'data_fim': dataFim,  
                'hora_fim': horaFim,  
                'descricao': descricao
                }
                Agenda(**content).put()
                return True
            except ValueException:
                return False
        return 'ok'

    def buscarTarefa(self, data):
        from datetime import date
        import time
        ndata = datetime.datetime.strptime(data, "%d-%m-%Y").strftime("%Y-%m-%d")
        option = []
        opts = self.get(order_by='hora_inicio')
        for options in opts:
            inicioTeste = str(options['data_inicio'])
            fimTeste = str(options['data_fim'])
            ano,mes,dia = inicioTeste.split("-")
            dataI = datetime.date(int(ano), int(mes), int(dia))
            ano,mes,dia = fimTeste.split("-")
            dataF = datetime.date(int(ano), int(mes), int(dia)) 
            if not ((inicioTeste > ndata and fimTeste > ndata) or (inicioTeste < ndata and fimTeste < ndata)):  
                option.append(str(options['data_inicio'])+";"+str(options['hora_inicio'])+";"+str(options['data_fim'])+";"+str(options['hora_fim'])+";"+str(options['descricao']))
            print(str(option))
        return option