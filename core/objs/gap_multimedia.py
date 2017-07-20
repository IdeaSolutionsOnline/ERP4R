# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVTek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_multimedia.GAPMultimedia'
import auth, base_models
from orm import *
from form import *

class GAPMultimedia(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_multimedia'
        self.__title__ = 'Multimedia'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'int8(gap_multimedia.ordem)'
        self.__get_options__ = ['nome']
        self.__workflow__ = (
            'estado', {'Activo':['GerarMD5']}
                )
        self.__workflow_auth__ = {
            'GerarMD5':['All'],
            'full_access':['Gestor de Atendimento']
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order = 1, name = 'Nome', size = 50)
        self.ficheiro = image_field(view_order=2, name='UploadFicheiro', size=30, onlist=False)
        self.data_ini = date_field(view_order=3, name ='Data Inicio',size = 40, args='required',  default=datetime.date.today())
        self.data_fim = date_field(view_order=4, name ='Data Fim',size = 40, args='required',  default=datetime.date.today())
        self.duracao_imagem = time_field(view_order=5, name ='Duraçao Imagem', size=40, onlist=False, default=time.strftime('%H:%M:%S'))
        self.tipo = combo_field(view_order = 6, name = 'Tipo', size = 50, args='required', default = 'image', options = [('image','Imagem'), ('video','Video')], onlist = True)
        self.ordem = integer_field(view_order = 7, name = 'Ordem', size = 40)
        self.terminal = many2many(view_order = 8, name = 'Loja', size = 50, fields=['name'], model_name = 'terminal.Terminal', condition = "gap_multimedia='{id}'", onlist=False)
        self.md5 = string_field(view_order = 9, name = 'MD5', args='readonly', onlist=False, size = 80)
        self.estado = info_field(view_order=10, name='Estado', hidden=True, onlist=False, default='Activo')



    #Apanha toda a multimedia disponivel
    def get_self(self):
        return self.get_options()


    def get_opts(self, get_str):
        return eval(get_str)


    #Apanha a lista multimedia disponivel para reproduzir para uma determinada loja
    def get_playlist_loja(self,loja=None):
        from my_terminal import Terminal
        #Para sabermos o ID da loja onde nos encontramos
        lojaID = Terminal().get_lojaID(loja=loja)
        self.kargs['join'] = ",gap_multimedia_terminal"
        self.where ="gap_multimedia_terminal.terminal = '{id}' and gap_multimedia_terminal.gap_multimedia= gap_multimedia.id".format(id=str(lojaID))
        options = []
        opts = self.get(order_by='int8(gap_multimedia.ordem)')
        data_hoje = datetime.date.today()
        for option in opts:
                data_inicio = str(option['data_ini']).split("-")
                if  (data_hoje >= datetime.date(int(data_inicio[0]),int(data_inicio[1]), int(data_inicio[2]))) and (option['md5'] != None) and (option['active'] == True):
                            options.append(option['nome']+';'+str(option['ficheiro'])+';'+option['tipo']+";"+str(option['duracao_imagem'])+";")
        #Retorna a playlist para uma loja xpto :)
        return options



    #Descartar ficheiros multimedia com data limite expirada para uma loja especifica
    def descartar_multimedia(self,loja=None):
        try:
            from my_terminal import Terminal
            #Para sabermos o ID da loja onde nos encontramos
            lojaID = Terminal().get_lojaID(loja=loja)
            #Descartar a musica ou imagem cujo a data final <= data hoje
            self.kargs['join'] = ",gap_multimedia_terminal"
            self.where ="gap_multimedia_terminal.terminal = '{id}' and gap_multimedia_terminal.gap_multimedia= gap_multimedia.id".format(id=str(lojaID))
            args = self.get(order_by='int8(gap_multimedia.ordem)')
            data_hoje = datetime.date.today()
            for self.kargs in args:
                data_fim = str(self.kargs['data_fim']).split("-")
                if (datetime.date(int(data_fim[0]),int(data_fim[1]), int(data_fim[2])) <= data_hoje) and (self.kargs['active'] == True):
                       #Muda o estado do ficheiro multimedia para false fazendo com que o mesmo nao apareça mais na playlist
                        self.kargs['user'] = bottle.request.session['user']
                        self.kargs['where'] = "id='{id}'".format(id=str(self.kargs['gap_multimedia']))
                        self.delete()
            return True
        except:
            return False

    #Essa funçao server para procurar pelos ficheiros de audio
    def find(self, name, path):
        import os
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join("/static/audio", name)
        return None

    #Apanha a lista multimedia disponivel para reproduzir e apenas imagens
    def get_playlist_type_Image(self):
        #retorna a lista do playlist com apenas imagens
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_multimedia.ordem)')
            for option in opts:
                if option['tipo'] == 'imagem':
                     options.append(option['nome']+' - '+ option['ficheiro']+ ' - ' + option['duracao_imagem'])
            return options
        return erp_cache.get(key=self.__model_name__ + '_playlist_type_Image', createfunc=get_results)


    #Apanha a lista multimedia disponivel para reproduzir e apenas videos
    def get_playlist_type_video(self):
        #retorna a lista do playlist com apenas videos
        def get_results():
            options = []
            opts = self.get(order_by='int8(gap_multimedia.ordem)')
            for option in opts:
                if option['tipo'] == 'video':
                     options.append(option['nome'] + ' - ' + option['ficheiro'])
            return options
        return erp_cache.get(key=self.__model_name__ + '_playlist_type_video', createfunc=get_results)


    #Gerar o MD5 somente vai gerar caso o utilizador fassa o upload do ficheiro xpto
    def GerarMD5(self, key, window_id):
            ficheiro = bottle.request.forms.getunicode('ficheiro')
            if ficheiro:
                import hashlib
                ficheiro_md5 = hashlib.md5(str(ficheiro).encode('utf-8')).hexdigest()
                fields_values= "md5='{md5}',user_change='{user}',date_change='{date}'".format(md5=str(ficheiro_md5), user=str(bottle.request.session['user']), date=str(datetime.datetime.today()))
                sql = "UPDATE gap_multimedia SET {values} where ficheiro='{ficheiro}'".format(values=fields_values, ficheiro=ficheiro)
                try:
                   run_sql(sql)
                except:
                    #cai no except nao sei pq mesmo efectuando o update corretamente :(
                    print("except --------")
                return form_edit(window_id=window_id).show()
            return error_message("Por favor faça o Upload do ficheiro e volte a tentar gerar o md5")