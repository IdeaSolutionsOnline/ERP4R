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

import os, sys
sys.path.append(os.getcwd())

from utils import *
from actions import *
import objs
from auth import verify_form_rights, require_auth
import bottle
import random
import base64
from dateutil.parser import parse

class View(object):

    def __init__(self, **kargs):
        self.kargs = kargs

    @bottle.view('base')
    @require_auth
    def form(self, action = None, key = None):
        #a ideia e o get_new_window_id criar um window_id e guarda-lo em context, manda-mos desde ja o window_id e ele associa-o ao window.name se nao existir window.name, existindo muda o window_id para o declarado pelo window_name. o base. tpl quando arranca faz esse trabalho e se nao tiver window.name requesita um
        #no load do base.tpl
        #verifica se existe window.name:
        #se nao existir requisita um ao get_window_id
        print('oi do form get')
        window_id = str(get_window_id())
        set_base_context(window_id)
        ctx_dict = get_context(window_id)
        #print('1')
        try:
            get_mail = Receive_POP3()
            get_mail.save_message()
        except:
            print("""atention!!! the user {user} it's not receiving emails!!!""".format(user = bottle.request.session['user_name']))
        #self.window_id = str(get_new_window_id())
        #print('my new window_id is {var1} and self.__title__ is {var2}'.format(var1=self.window_id, var2=self.__title__))
        #dados globais do formulario

        ctx_dict['window_id'] = window_id
        ctx_dict['name'] = self.__name__
        ctx_dict['title'] = self.__title__
        ctx_dict['cols'] = 12
        ctx_dict['model_name'] = self.__model_name__
        ctx_dict['main_key'] = key
        ctx_dict['redirect_url'] = '/' + self.__name__
        ctx_dict['window_status'] = 'list'#(pode ser list, edit, popup, calendar, gant, etc e representa o que ocupa a window nesse momento)
        #cria o dicionario que guarda os dados relativos a lista
        ctx_dict[self.__name__] = {}
        # povoa o dicionario da lista
        ctx_dict[self.__name__]['page'] = 0
        ctx_dict[self.__name__]['limit'] = 10
        ctx_dict[self.__name__]['title'] = self.__title__
        ctx_dict[self.__name__]['show_search'] = True
        set_context(window_id, ctx_dict)
        #print (ctx_dict)
        result = {}
        try:
            if key not in ['None', None] and 'get' not in key :
                ctx_dict['window_status'] = 'edit'
                set_context(window_id, ctx_dict)
                result['form'] = form_edit(key = key, window_id = window_id).show()
            elif action == 'New':
                result['form'] = ''
            elif self.__db_mode__ == 'None':
                ctx_dict['window_status'] = 'edit'
                set_context(window_id, ctx_dict)
                result['form'] = form_edit(window_id = window_id).show()
            elif action == 'OtherForm':
                #print('1---------------------------------------------------------------------', key)
                result['form'] = eval('self.{function_to_call}(window_id=window_id)'.format(function_to_call=key))
            else:
                #print('before form_list')
                result['form'] = form_list(window_id = window_id).show()
                #print('after form list')
            if hasattr(self,'__side_bar__'):
                result['side_bar'] = self.__side_bar__
            else:
                result['side_bar'] = {}
            #print('fim de get')
            result.update(ctx_dict)
            return result
        except:
            result['form'] =  error_message(traceback.format_exc())
            ctx_dict['side_bar'] = {}
            set_context(window_id, ctx_dict)
            result.update(ctx_dict)
            return result

    @bottle.view('base')
    @require_auth
    def submit(self, action, key):
        try:
            print('oi sou o post')
            window_id = bottle.request.forms.get('window_id')
            #print (get_context(window_id)[self.__name__])
            #print('{var1}'.format(var1=action))
            m_action = model_action(obj = self)
            #print('m_action is {var1}'.format(var1=m_action))
            option = ''
            if 'form_list_onchange' in action:
                option = action[18:]
                action = 'form_list_onchange'
            elif 'list_field_onchange' in action:
                print('sou um list_field_onchange a action is {var1}'.format(var1 = action))
                option = action[19:]
                action = 'list_field_onchange'
                #print(option, '-----', action)
            elif 'form_edit_dyn_atrs' in action:
                print('sou um edit_dyn_atrs')
                option = action[18:]
                action = 'form_edit_dyn_atrs'
            if option:
                option = "option='{option}'".format(option = option)
                #print('option:{var1}, action:{var2}, key:{var3}'.format(var1 = option, var2 = action, var3 = str(key)))
            if hasattr(self, action):
                print('o meu modelo tem esta funçao {var1} and key is {var2} and window_id is {var3}'.format(var1 = action, var2 = str(key), var3 = window_id))
                response = eval("""self.{action}(key = '{key}', window_id='{window_id}')""".format(action = action, key = str(key), window_id = window_id))
                #print(response)
            elif hasattr(model_action, action):
                print('as model_action , action e option são', model_action, action, option, 'bla')
                if option:
                    separator = ','
                else:
                    separator = ''
                print("""m_action.{action}(key='{key}'{separator} {option})""".format(action = action, key = key, separator=separator, option = option))
                response = eval("""m_action.{action}(key='{key}'{separator} {option})""".format(action = action, key = key, separator=separator, option = option))
                #print(response)

                if response[0] == 'string':
                    response = response[1]
                elif response[0] == 'form':
                    print('im in the final response')
                    response = eval(response[1])
                    #print(response)
                else:
                    print('fuck-----------------------------------------------------------')
            else:
                response = error_message('Not implemented yet, it\'s a shame... :-) ! -/'+ action + '/' + option + '/' + key)
            #print('response is {var1}'.format(var1=response))
            return response
        except:
            print('traceback.format_exc()----------------', traceback.format_exc())
            raise error_message(traceback.format_exc())


class form(object):
    """Classe base para formulários"""
    def __init__():
        pass

class side_bar(object):
    """Construtor do side bar"""
    def __init__(self):
        pass

    def show(model, options_dict):
        code = ''
        for opt in options_dict:
            code += """
            <div onclick="call_post_method('{url}');" class="base_color">{description}</div>
            """.format(url = model + '/' + options_dict[opt] + '/None', description = opt)
        return code


@verify_form_rights
class form_list(form):
    def __init__(self, window_id):
        #print('in init')
        self.window_id = window_id
        self.ctx_dict = get_context(self.window_id)
        self.result_dict = {}

    def show(self):
        print('in show do form_list')
        forms = '/var/www/core/forms/'
        widgets = '/var/www/core/widgets/'
        ctx_key = None
        #print('before model')
        if self.ctx_dict.get('window_status') == 'popup': # e se decidirmos depois carregar um list_form num popup sem ser no caso do choice_field????
            model_name = self.ctx_dict.get('popup_model_name')
            field_name = self.ctx_dict.get('popup_field_name')
            ctx_key = field_name  #a ctx_key é onde o prepare_list_data deve ir buscar a informação para completar a lista, se vem de um choise é o nome do campo e se vem de um formulário é o nome do modelo
        else:
            model_name = self.ctx_dict.get('model_name')
        model = eval("""objs.{model_name}()""".format(model_name = model_name))

        if not ctx_key:
            ctx_key = model.__name__
        #print(model_name, model.__name__)
        #print('after model')
        self.ctx_dict[ctx_key]['list_edit_mode'] = model.__list_edit_mode__
        self.ctx_dict[ctx_key]['list_field'] = False
        self.ctx_dict[ctx_key]['side_menu'] = model.__side_menu__
        self.ctx_dict[ctx_key]['breadcrumbs_navigation'] = model.__breadcrumbs_navigation__

        set_context(self.window_id, self.ctx_dict)
        #print('antes de list_data')
        list_data = prepare_list_data(model = model, ctx_dict = self.ctx_dict, list_name = ctx_key)
        list_data['recalled'] = False#se foi chamado (refrescado) por alguma funçao interna
        #print('depois de list_data')
        self.ctx_dict[ctx_key].update(list_data)
        #print (self.ctx_dict)
        set_context(self.window_id, self.ctx_dict)
        #print (2)
        #print(model.__name__, str(list_data))
        #print (self.ctx_dict[model.__name__], self.window_id)
        self.result_dict.update(self.ctx_dict)
        self.result_dict['list'] = bottle.SimpleTemplate(name = widgets + 'list_field').render(list_data)
        #print('after render the list')
        return bottle.SimpleTemplate(name = forms + 'list').render(self.result_dict)

@verify_form_rights
class form_edit(form):

    def __init__(self,  window_id):
        print('in form_edit  o window_id é ', window_id)
        self.window_id = window_id
        self.ctx_dict = get_context(window_id)
        if self.ctx_dict['window_status'] == 'edit':
            self.title = self.ctx_dict.get('title')
            self.name = self.ctx_dict.get('name')
            self.model_name = self.ctx_dict.get('model_name')
            self.main_key = self.ctx_dict.get('main_key')# o id do registo que estamos a editar
        #print('1')
        self.popup = False
        if self.ctx_dict.get('window_status') == 'popup':
            self.popup = True
            #print('Im a popup {var1}'.format(var1=self.popup))
            self.title = self.ctx_dict.get('popup_title')
            self.name = self.ctx_dict.get('popup_name')
            self.main_key = self.ctx_dict.get('popup_main_key')
            self.model_name = self.ctx_dict.get('popup_model_name')
        #print('2')
        self.cols = self.ctx_dict.get('cols')
        #print('my self.main_key in init {var1}'.format(var1=str(self.main_key)))
        self.parent_name = self.ctx_dict.get('parent_name')# caso seja chamado por outro registo esta informação é sobre esse registo pai
        self.parent_key = self.ctx_dict.get('parent_key')# id do registo pai
        #print('3')
        self.rights = self.ctx_dict.get('rights')
        #self.dynamic_atrs = self.ctx_dict.get('dynamic_atrs')
        #print('my dynamic_atrs é ', self.dynamic_atrs)

    def show(self):
        print('Inicio do form_edit')
        #print("here 2 edit")
        forms = '/var/www/core/forms/'
        widgets = '/var/www/core/widgets/'
        fields = []# guarda todos os campos menos os das tabelas
        tabs = []# guarda o centeudo das tabs
        #tab_labels = []# guarda as labels das tabs
        tab_fields = []# guarda todos os campos de todas as tabs
        workflow = []# guarda os botões do workflow
        #print('inicio o modelo')
        model = eval("""objs.{model_name}()""".format(model_name=self.model_name))
        #Utilizado nas permissões ou seja define o que o utilizador pode fazer
        add_ok = False
        add_rights = ['create', 'full_access']
        edit_ok = False
        edit_rights = ['write', 'full_access']
        delete_ok = False
        delete_rights = ['delete', 'full_access']
        #aqui já temos a lista dos direitos e assim podemos alimentar a variavel (flag) para cada autorização
        for right in self.rights[0]:
            if right in add_rights:
                add_ok = True
            if right in edit_rights:
                edit_ok = True
            if right in delete_rights:
                delete_ok = True
        #print(str(edit_ok) + str(delete_ok))
        #aqui vou pedir o record com a totalidade dos campos pois assim garanto que se algum foi acrescentado á posterior no modelo o sync_model ira actualiza-lo!!!
        select_fields = get_select_fields(model) # neste caso são todos dado que não lhe passo o argumento fields=[]
        #print('my model_fields are' + model_fields)
        #vai buscar o registo em si que ira alimentar o formulário
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        record = model.get(key=self.main_key, fields=select_fields)# Registo a ser apresentado
        #print('my record is' + record)
        if record:
            record = record[0]
        #if record:
        #   record = record[0]#o record é um tuple com os dados em si e...
        #print('my record is' + record)
        #new_atrs = False
        #print('2')
        #Utilizado na inibição dos formulários para que não seja modificavel mediante o valor de um determinado campo
        #print('record {var1}'.format(var1=record))
        if hasattr(model, '__no_edit__') and len(model.__no_edit__) > 0:
            #print('no edit')
            if record:
                for no_edit in model.__no_edit__:
                    if record[no_edit[0]] in no_edit[1]:
                        edit_rights = []
                        edit_ok = False
                        delete_rights = []
                        delete_ok = False
                        #print('edit_rights ', edit_rights, ' delete_rights ', delete_rights, ' edit_ok ', edit_ok, ' delete_ok ', delete_ok)
        #print('3')
        #print ('my model_name is', model.__name__, self.name)
        #print('o self name do ctx_dict é: ', self.ctx_dict[self.name])
        selected_ids = self.ctx_dict[self.name].get('selected_ids')
        #print('selected_ids', selected_ids)
        if not selected_ids:
            #print('não tenho selected ids por isso atribui o do main_key', self.main_key)
            selected_ids = [(0, str(self.main_key))]
        rows_count = len(selected_ids)# numero de registos que respeitam as regras de filtro e search
        record_num = 0 #aqui tenho que ver o caso dos novos registos, pois o index começa por 0 tambem
        #print('selected_ids', selected_ids)
        for rec_id in selected_ids:
            if str(rec_id[1]) == str(self.main_key):
                record_num = rec_id[0]
                #print('my record_num e', record_num)
        #print('4')
        #penso que podemos substituir esta merda aqui pelo index da lista, ver depois
        #for record_id in record_ids:
        #   index[order_number] = str(record_id)
        #   if str(record_id) == str(self.main_key):
        #       record_num = order_number
        #   order_number += 1
        #print(index + self.main_key + bottle.SimpleTemplate.defaults['main_key'])
        try:
            first = selected_ids[0][1]
        except:
            first = 'None'
        try:
            last = selected_ids[-1][1]
        except:
            last = 'None'
        if record_num > 1:
            back = selected_ids[record_num-1][1]
        else:
            try:
                back = selected_ids[record_num][1]
            except:
                back = 'None'
        try:
            forward = selected_ids[record_num +1][1]
        except:
            forward = 'None'#selected_ids[record_num][1]
        #print('first, back, forward, last', first, back, forward, last)
        #print('5')
        #Caso seja chamado sem ser por onchange verifica os valores e define os atributos de acordo a eles
        #if self.dynamic_atrs == False: # os atributos dinamicos são ao nivel do campo e não do form por isso não entendi o que isto está a fazer aqui
        if record:
            values = record
        else:
            values = {}
            for field in get_model_fields(model):
                if hasattr(field[1], 'default') and field[1].default:
                    #print('o default e:' + field[1].default)
                    default = field[1].default
                    if type(default) == str:
                        if 'session' in default:
                            default = eval('bottle.request.' + default)
                        elif 'get_' in default:
                            default = eval('model.' + default)
                        else:
                            default = str(default)
                    else:
                        default = str(default)
                    #print('my default is ' + default)
                    if field[1].__class__.__name__ == 'parent_field':
                        #print('Im a parent field')
                        options = eval('objs.{model_name}().get_options()'.format(model_name = field[1].model_name))
                        values[field[0]] = parent2HTML(value = default, options = options)
                        #print ('values', values[field[0]])
                    else:
                        values[field[0]] = default
            #print('values:' + values)
            #new_atrs = run_dyn_atrs_function(values = values, model = model, field_name = None)
        #print('6')
        #Verifica se tem tabs e se tiver preenche a lista de campos que pertencem a tabs
        tab_field_names = []
        if hasattr(model, '__tabs__') and model.__tabs__ != []:
            for tab in model.__tabs__:
                for f in tab[1]:
                    tab_field_names.append(f)
        #print('tab_field_names--------', tab_field_names)
        values_record = {}#dicionário utilizado para registar os valores dos campos do registo escolhido
        #print('7')
        #print (model)

        dynamic_atrs_result = {}
        dynamic_atrs_args = {}

        for field in get_model_fields(model):
           #caso tenha onchange ou dynamic_atrs nos argumentos deve passar a função para os kargs para que possa passar para o JS via HTML5, assim o JS poderá invocar a função que existe no objecto, receber o result que é um dicionário com campos e valores ou atributos html5 e mudar os valores ou atributos de acordo com o resultado da função, esta abordagem só funciona quando o utilizador muda o valor do campo e não quando o campo é mudado por um botão de workflow, temos também que assegurar que quando abrimos o form se as condições se manifestarem devem ser cumpridas

            onchange_function = ''
            dynamic_atrs_function = ''

            if field[1].dynamic_atrs in ['False', False]:
                del field[1].dynamic_atrs
            if field[1].onchange in ['False', False]:
                del field[1].onchange

            if hasattr(field[1], 'dynamic_atrs'):
                #print('Tenho dynamic_atrs', field[1].dynamic_atrs)
                dynamic_atrs_function = field[1].dynamic_atrs

            if hasattr(field[1],  'onchange'):
                onchange_function = field[1].onchange

            if hasattr(field[1], 'dynamic_atrs') or hasattr(field[1],  'onchange'):
                print('vou acrescentar os argumentos da função')
                dynamic_atrs_args[field[0]] = """ onChange="runEditOnchange('{key}', '{name}', '{onchange_function}', '{dynamic_atrs_function}')" """.format(key=self.main_key, name=self.name, onchange_function=onchange_function, dynamic_atrs_function=dynamic_atrs_function)
        #         #print(field[1].args)
        #         #vou correr a função definida para adaptar os atributos
                if hasattr(field[1], 'dynamic_atrs'):
                    from ujson import loads
        #             #print(dynamic_atrs_function)
        #             #print(record)
                    if record:
                        rec_to_pass = record
                    else:
                        rec_to_pass = {}
                        for sf in select_fields:
                            rec_to_pass[sf] = ''
                    dynamic_atrs_result =  loads(eval("model.{function}(record={record}, internal=True)".format(function=dynamic_atrs_function, record=rec_to_pass)))
        #print('o resultado dos meus atributos dinamicos é vindos da função', dynamic_atrs_result)
        #print(type(dynamic_atrs_result))
        # print('as funções onchange que vou acrescentar ao codigo ', dynamic_atrs_args)

        for field in get_model_fields(model):
            #print('8' + field[0])
            kargs = {}#dicionário que guarda os dados necessários para passar para o template de cada campo (field)
            #print(str(edit_ok))
            if field[1].__class__.__name__ in ['list_field', 'many2many']:
                if field[1].__class__.__name__ == 'list_field':
                    field_model = eval("""objs.{model_name}()""".format(model_name=field[1].model_name))
                    print('before filter_expression')
                    self.ctx_dict[field[0]] = {}
                    #print('condition do list_field', get_condition(condition=field[1].condition, record=record))
                    self.ctx_dict[field[0]]['filter_expression'] = get_condition(condition=field[1].condition, record=record)
                    self.ctx_dict[field[0]]['page'] = 0
                    self.ctx_dict[field[0]]['limit'] = 1000
                    self.ctx_dict[field[0]]['show_search'] = False
                    self.ctx_dict[field[0]]['title'] = field[1].name
                    set_context(self.window_id, self.ctx_dict)
                    #print('window_status is {var1}'.format(var1 = self.ctx_dict['window_status']))
                    #print('filter_expression is {var1}'.format(var1 = self.ctx_dict[field[0]]['filter_expression']))
                    if hasattr(field[1], 'list_edit_mode'):
                        self.ctx_dict[field[0]]['list_edit_mode'] = field[1].list_edit_mode
                    else:
                        self.ctx_dict[field[0]]['list_edit_mode'] = field_model.model.__list_edit_mode__
                    self.ctx_dict[field[0]]['list_field'] = True
                    set_context(self.window_id, self.ctx_dict)
                    print('antes de list_data')
                    list_data = prepare_list_data(model=field_model, ctx_dict=self.ctx_dict, list_name=field[0])
                    if hasattr(field[1], 'size') and field[1].size > 10:
                        size = field[1].size
                    else:
                        size = 300
                    cols = round(size / 25)
                    if cols > 12:
                        cols = 12
                    list_data['size'] = size
                    list_data['cols'] = cols
                    list_data['recalled'] = False # o recalled ´e utilizado para eu saber se estou a carregar a lista pela 1ª vez ou a rechama-la
                    #print('depois de list_data')
                    #print('after prepare_list_data')
                    #print(str(list_data))
                elif field[1].__class__.__name__ == 'many2many':
                    #print('im a m2m')
                    parent_ids = model.get_m2m_ids(field_name=field[0], record=record)
                    #print('parent_ids is {var1}'.format(var1=str(parent_ids)))
                    condition = ""
                    if parent_ids:
                        parent_ids_str = '('
                        for parent_id in parent_ids:
                            parent_ids_str += "'" + str(parent_id) + "',"
                        parent_ids_str = parent_ids_str[:-1] + ')'
                        #print('a minha parent_ids_str do many2many é ', parent_ids_str)
                        condition = 'where="id in {parent_ids}"'.format(parent_ids=str(parent_ids_str))
                    #print('before eval_model')
                    field_model = eval("""objs.{model_name}({condition})""".format(model_name=field[1].model_name, condition=condition))
                    #print('after eval_model field_model is {var1}'.format(var1 = str(field_model)))
                    field_fields = []
                    if hasattr(field[1], 'fields'):
                        field_fields = field[1].fields
                    list_data = prepare_m2m_data(model=field_model, ctx_dict=self.ctx_dict, fields=field_fields, parent_ids=parent_ids)
                    self.ctx_dict[field[0]] = {}
                #print('8.1.1.2')
                #print('list_data {var1}'.format(var1=str(list_data)))
                self.ctx_dict[field[0]].update(list_data)
                set_context(self.window_id, self.ctx_dict)
                kargs.update(list_data)
                #print('kargs is {var1}'.format(var1=str(kargs)))
                #kargs['show_search'] = False
                #kargs['list_edit_mode'] = field_model.__list_edit_mode__
            #print('8.1.2')
            #print('self.main_key, field[1].__class__.__name__' + self.main_key + field[1].__class__.__name__)
            if self.main_key not in ['None', None] and field[1].__class__.__name__ not in ['separator', 'newline', 'link','label','hrline']:
                field_values = get_field_value(record, field, model)
                #aqui se for popup tenho que procurar no request por popup_fieldname
                #print(field[0], '--------------------------------------------------------------------------------------------')
                #print(field_values['field_value'], type(field_values['field_value']))
                if field_values['field_value']:
                    #print('we do have field_value', kargs)
                    #if isinstance(field_values['field_value'], Decimal):
                    #    kargs['value'] = field_values['field_value']#str(format_number(field_values['field_value']))
                    #else:
                     #   print('sou outro que não decimal')
                    kargs['value'] = field_values['field_value']
                    #print(kargs['value'])
            #elif field[1].__class__.__name__ in ['separator', 'newline']:
            #   pass
            else:
                if hasattr(field[1], 'default') and field[1].default:
                    default = field[1].default
                    if type(default) == str:
                        if 'session' in default:
                            default = default[7:]
                            try:
                                default = eval('self.ctx_dict{default}'.format(default = default, window_id = self.window_id))
                            except:
                                default = 'ERROR'
                        elif 'get_' in default:
                            default = eval('model.' + default)
                    else:
                        default = str(default)
                    if field[1].__class__.__name__ == 'parent_field':
                        #print('im a parent_field')
                        options = eval('objs.{model_name}().get_options()'.format(model_name = field[1].model_name))
                        #print('1')
                        #kargs['parent_name'] = eval('objs.{model_name}().__name__'.format(model_name=field[1].model_name))
                        #options = model.options[field[0]]
                        #print('2', kargs['parent_name'])
                        kargs['value'] = parent2HTML(value = default, options = options)
                        #print('3', kargs['value'])
                    else:
                        kargs['value'] = default
                        #print('valor por defeito is {var1}'.format(var1=kargs['value']))

            if field[1].__class__.__name__ == 'parent_field':
                kargs['parent_name'] = eval('objs.{model_name}().__name__'.format(model_name=field[1].model_name))

            #print('8.1.3')
            if field[1].__class__.__name__ in ['combo_field', 'choice_field']:
                #print('sou combo ou choice ', field[0])
                if isinstance(field[1].options, list):
                    kargs['options'] = field[1].options
                else:
                    kargs['options'] = eval(field[1].options)
                #print('validando as options do choice', kargs['options'])
                if field[1].__class__.__name__ in ['choice_field']:
                    option_ids = []
                    for o in kargs['options']:
                        option_ids.append(o[0])
                    option_ids = to_tuple(option_ids)
                    #não podemos guardar a filter exprecion e outras variaveis no modelo pois podemos facilmente ter dois choice que se alimentam do mesmo modelo por isso mudamos para guardar com o nome do campo como key, claro que depois temos que ver como fazer relativamente à list_data dado que está a ir buscar ao ctx_dict com o modelo como key
                    self.ctx_dict[field[0]] = {}
                    self.ctx_dict[field[0]]['filter_expression'] = 'id ' + str(option_ids)
                    self.ctx_dict[field[0]]['filter_expr_choice_restrict'] = 'id ' + str(option_ids) # esta entrada serve para garantir que nas choice_field quando carregamos no botão de filter jamais devolve valores que não constem desta lista.
                    #print('modelo', field[1].model)
                    #print ('my filter expression', self.ctx_dict[field[0]]['filter_expression'])
                    self.ctx_dict[field[0]]['page'] = 0
                    self.ctx_dict[field[0]]['limit'] = 1000
                    self.ctx_dict[field[0]]['show_search'] = False
                    set_context(self.window_id, self.ctx_dict)
            #print('8.1.4')
            if dynamic_atrs_result:
                #Significa que os args serão modificados pela dicionário alterando os atributos retornados pela função dynamic_atrs do campo, corremos o risco de fazer overwrite de atributos, depois temos que ver essa questão
                if field[0] in dynamic_atrs_result:
                    print('estou no dynamic_atrs_result', field[0])
                    print(dynamic_atrs_result[field[0]])
                    for arg in dynamic_atrs_result[field[0]]:
                        if arg == 'atrs':
                            field[1].args = field[1].args + ' ' + dynamic_atrs_result[field[0]]['atrs']
                        else:
                            exec("kargs['{arg}'] = dynamic_atrs_result['{field_name}']['{arg}']".format(arg=arg, field_name=field[0]))
                    print('os argumentos a passar ao html são', field[1].args)
            if dynamic_atrs_args:
                #Significa que os args serão modificados pela dicionário acrescentando a função onchange aos campos que tem o atributo dynamic_atrs, só terá efeito se o utilizador mudar o valor mas se for através de um botão de workflow o próprio botão tem que chamar o onchange
                if field[0] in dynamic_atrs_args:
                    field[1].args = field[1].args + dynamic_atrs_args[field[0]]

            if hasattr(field[1], 'size') and field[1].size > 10:
                size = field[1].size
            else:#se não receber argumento para size define aqui um default
                if field[1].__class__.__name__ in ['list_field', 'many2many']:
                    size = 300
                elif field[1].__class__.__name__ in ['image_field']:
                    size = 100
                    #kargs['obj'] = self.main_key
                else:
                    size = 50
            #print(field[0], size)
            cols = round(size / 25)
            if cols > 12:
                cols = 12

            if edit_ok == False:
                if field[1].__class__.__name__ not in ['combo_field', 'many2many', 'list_field']:#aqui tenho que definir outras formas de ser read_only
                    field[1].args = field[1].args + ' readonly'
                    kargs['edit_ok'] = False # depois desta forma podemos passar o controlo do edit para o html em todos os widget, desta forma ganhamos flexibilidade sobre de que forma o widget implementa o edit_ok = False
                else:
                    kargs['edit_ok'] = False
                    kargs['add_ok'] = False
                    kargs['delete_ok'] = False

            for d_key in vars(field[1]):
                if d_key not in ['name', 'type', 'sum', 'source', 'rowspan',  'onlist', 'condition', 'value', 'search', 'default', 'onchange', 'dynamic_atrs', 'view_order', 'parent_model', 'options', 'record', 'list_edit_mode', 'show_search', 'edit_ok','nolabel']:
                    kargs[d_key] = eval('field[1].' + d_key)
             #kargs['source'] = 'edit'#define a origem, ou seja de onde vem (quem o chamou) acho que ja nao faz falta, confirmar!
            #print('8.1.5')
            if field[1].__class__.__name__ in ['image_field', 'upload_field']:
                kargs['obj'] = self.model_name
                kargs['obj_key'] = self.main_key
            if field[1].__class__.__name__ not in ['separator', 'newline', 'link','label','hrline']:
                field_name = field[1].name
            else:
                field_name = field[0]
            #print('8.1.6')
            kargs['field_name'] = field_name#legenda
            kargs['name'] = field[0]#nome de campo
            kargs['size'] = size
            kargs['cols'] = cols
            #print(kargs)
            #print(field[1].__class__.__name__)
            #print('8.2' + str(field))
            #print(widgets + field[1].__class__.__name__)
            #print(bottle.SimpleTemplate(name=widgets + field[1].__class__.__name__).render(kargs))
            field_code = bottle.SimpleTemplate(name = widgets + field[1].__class__.__name__).render(kargs)
            #print('8.3')
            #eval(field[1].__class__.__name__+ '(**kargs).show()')-----------aqui gero o campo
            #print('o meu cols e' + cols)
            #print(field_code)
            if field[0] in tab_field_names:
                #print ('tab field_code', field_code)
                tab_fields.append((field[0], field_code, cols))#------ lista de tab_fields
            else:
                fields.append((field[0], field_code, cols))#, rowspan#, source----------------lista de fields---
            #print('8.4')
            if 'value' in kargs:
                values_record[field[0]] = kargs['value']
            else:
                values_record[field[0]] = ''
            #print('8.5')
        #print('9')
        #print(tab_fields)
        #Caso tenhamos tabs montar o formulário de cada tab
        if hasattr(model, '__tabs__') and model.__tabs__ != []:
            #print('model.__tabs__ is {var1}'.format(var1=model.__tabs__))
            for tab in model.__tabs__:
                tab_fields_code = ''
                col = 0
                #print('tab[0] is {var1}, tab[1] is {var2}'.format(var1=tab[0], var2=tab[1]))
                for f_name in tab[1]:
                    for field in tab_fields:
                        #print(field[0])
                        if field[0] == f_name:
                            #print('field[0] is {var1}, field[2] is {var2}, self.cols is {var3}'.format(var1=field[0], var2=field[2], var3=str(self.cols)))
                            #print (field[1])
                            if col >= self.cols:
                                col = 0
                            tab_fields_code += field[1]
                            col += int(field[2])
                            #print(tab_fields_code)
                #print(tab[0])
                col = 0
                #print('before tab name')
                tab_name = make_function_name(tab[0])
                #print('after tab name {var1}'.format(var1=tab_name))
                tabs.append((tab[0], tab_name, tab_fields_code))
                #print(str(tabs))
        #print('10')
        #Montagem dos botões de workflow
        wf_auth_buttons = {}
        if hasattr(model, '__workflow__') and model.__workflow__ != ():
            #print('main_ key' + self.main_key + type(self.main_key))
            #print(record, model.__workflow__)
            if self.main_key not in [None, 'None']:
                workflow_value = record[model.__workflow__[0]]
            else:
                for field in get_model_fields(model):
                    #print(field[0] + model.__workflow__[0])
                    if field[0] == model.__workflow__[0]:
                        #Aqui terei eventualmente que verificar se tem context por exemplo ou se é uma função, esse tipo de coisas
                        workflow_value = field[1].default
            if workflow_value in model.__workflow__[1]:
                for workflow_button in model.__workflow__[1][workflow_value]:
                    #print('workflow_button' + workflow_button)
                    #Aqui valida se mediante a condição o botão deve ou não aparecer e se é suposto aparecer valida se o utilizador tem autorização ou não
                    if hasattr(model, '__workflow_auth__'):
                        if workflow_button in model.__workflow_auth__:
                            for right in self.rights[1]:
                                if right in model.__workflow_auth__[workflow_button] or right == 'Administrator' or 'All' in model.__workflow_auth__[workflow_button]:
                                    if workflow_button not in wf_auth_buttons:
                                        #print(workflow_button)
                                        wf_auth_buttons[workflow_button] = make_function_name(workflow_button)
                    #Valida a condição para que o botão do workflow apareça!
                    if hasattr(model, '__workflow_context__'):
                        if workflow_button in model.__workflow_context__:
                            condition = model.__workflow_context__[workflow_button]
                            #print(condition)
                            #print(values_record)
                            if condition[0] in values_record:
                                val1 = values_record[condition[0]]
                            else:
                                val1 = condition[0]
                            if condition[2] in values_record:
                                val2 = values_record[condition[2]]
                            else:
                                val2 = condition[2]
                            if not val1:
                                val1 = '0'
                            if not val2:
                                val2 = '0'
                            #print(condition + val1 + val2)
                            condition_value = eval(str(val1) + str(condition[1]) + str(val2))
                            #print(condition_value)
                            if not condition_value:
                                del wf_auth_buttons[workflow_button]
        #print('record_num is {var1}, back is {var2}, forward is {var3}, last is {var4}, first is {var5}'.format(var1=str(record_num), var2=str(back), var3=str(forward), var4=str(last), var5=str(first)))
        result = {
            'title':self.title,
            'db_mode':model.__db_mode__,
            'add_ok':add_ok,
            'delete_ok':delete_ok,
            'edit_ok':edit_ok,
            'name':self.name,
            'main_key':self.main_key,
            'rows_count':rows_count,
            'record_num':record_num,
            'state':'',
            'fields':fields,
            'tabs':tabs,
            #'tab_labels':tab_labels,
            'wf_auth_buttons':wf_auth_buttons,
            'first':first,
            'back':back,
            'last':last,
            'forward':forward,
            'popup_name':self.name,
            'popup_main_key':self.main_key,
            'popup_model_name':self.model_name,
            'popup_title':self.title,
            #'window_id':self.window_id,
            }

        #print('o result é: ', result)
        result.update(self.ctx_dict)
        print('Fim do form_edit')
        #print(bottle.SimpleTemplate(name = forms + 'edit').render(result))
        return bottle.SimpleTemplate(name = forms + 'edit').render(result)

@verify_form_rights
class form_calendar(form):

    def __init__(self, month, year, window_id):
        self.window_id = window_id
        self.ctx_dict = get_context(window_id)
        self.name = self.ctx_dict.get('name')#name
        self.model_name = self.ctx_dict.get('model_name')#model_name
        self.cols = self.ctx_dict.get('cols')
        self.main_key = self.ctx_dict.get('main_key')
        self.parent_name = self.ctx_dict.get('parent_name')
        self.parent_key = self.ctx_dict.get('parent_key')
        self.rights = self.ctx_dict.get('rights')
        #self.dynamic_atrs = self.ctx_dict.get('dynamic_atrs')
        self.month = month
        self.year = year

def list_report(name, data, cols):
    code = """<div class="list_report">
        <table>
            <tr>
            """
    for col in cols:
        code += """<th>{col}</th>
        """.format(col=col)
    code += """     </tr>
    <tbody>
    """
    for d in data:
        code += """<tr>
        """
        for col in cols:
            code += """<td>{val}</td>
        """.format(val=d[col])
        code += """</tr>
        """
    code +="""
            </tbody>
        </table>
    </div>
    """
    return code


@verify_form_rights
class form_gap_atendedor(form):
    def __init__(self, window_id):
        self.window_id = window_id
        self.ctx_dict = get_context(self.window_id)
        self.result_dict = {}

    def show(self):
        #print('aqui no gap atendedor-------------------------------------------------------------------')
        from gap_faq import GAPFaq
        from gap_atendimento import GAPAtendimento
        from gap_servico import GAPServico
        from gap_checklist import GAPChecklist
        from gap_timeAtendimento import  GAPTimeAtendimento
        from gap_balcao import GAPBalcao
        from my_users import Users
        import erp_config as ec

        forms = '/var/www/core/forms/'
        widgets = '/var/www/core/widgets/'

        faqs = []# guarda todos os faqs
        checklists = []# guarda todos os checklist
        fluxos = []# guarda todos os fluxos
        servicos = []# guarda todos os servicos

        clientes_espera = [] # guarda os clientes em espera pelo atendedor xpto

        #apanha o servico em atendimento no utilizador logado actualmente no sistema
        servico_em_Atendimento = GAPTimeAtendimento().getServicoAtendimento(loja=ec.terminal_name)
        faqs = GAPFaq().get_faqs()
        fluxos = GAPAtendimento().get_fluxos()
        servicos = GAPServico().get_servico()
        checklists = GAPChecklist().get_checklist()

        clientes_espera = GAPTimeAtendimento().getClienteEspera(loja=ec.terminal_name)

        user_balcao = GAPBalcao().get_balcao(loja=ec.terminal_name) # guarda o numero do balcao do atendedor
        user_estado = Users().get_estado() # guarda estado do atendedor
        if self.ctx_dict.get('window_status') == 'popup':
            model_name = self.ctx_dict.get('popup_model_name')
        else:
            model_name = self.ctx_dict.get('model_name')
        model = eval("""objs.{model_name}()""".format(model_name = model_name))
        self.ctx_dict[model.__name__]['list_edit_mode'] = model.__list_edit_mode__
        self.ctx_dict[model.__name__]['list_field'] = False
        set_context(self.window_id, self.ctx_dict)
        list_data = prepare_list_data(model = model, ctx_dict = self.ctx_dict, list_name = model.__name__)
        list_data['recalled'] = False#se foi chamado (refrescado) por alguma funçao interna
        #print('depois de list_data')
        self.ctx_dict[model.__name__].update(list_data)
        set_context(self.window_id, self.ctx_dict)
        result = {
            'checklists':checklists,
            'faqs':faqs,
            'servicos':servicos,
            'fluxos':fluxos,
            'user_balcao':user_balcao,
            'user_estado':user_estado,
            'clientes_espera':clientes_espera,
            'servico_em_Atendimento':servico_em_Atendimento,
        }
        result.update(self.ctx_dict)
        #print("no end form atendedor--------------------------------------------------------------------  ")
        return bottle.SimpleTemplate(name = forms + 'gap_atendedor').render(result)