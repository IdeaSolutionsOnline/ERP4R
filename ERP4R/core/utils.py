# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""ERP+"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"

import os
import sys
sys.path.append(os.getcwd())
import datetime
import time
#from bottle import *#bottle
import bottle
from orm import run_sql, traceback, get_context, set_context
from decimal import Decimal
import erp_config

""""""
def get_user_id(window_name=None, window_id=None):
    new_user_id = bottle.request.session.get('user')
    return str(new_user_id)


def get_window_id(window_name=None, window_id=None):
    """Atribui um novo window_id a nova janela"""
    #print('Im in get_window_id', window_name, window_id)
    if not window_name or window_name == '':
        #print('111')
        import random
        new_window_id = random.randint(1000000, 100000000000)
        #print('123')
        set_context(str(new_window_id), {})
        #print('222')
    else:
        #print (window_name, '---', window_id)
        window_id_dict = get_context(window_id)
        #print(1)
        #print('window_id', window_id_dict, window_id)
        try:
            window_name_dict = get_context(window_name)
            #print(2)
            window_name_dict.update(window_id_dict)
            window_name_dict['window_id'] = window_name
            #print('window_name', window_name_dict, window_name)
            #print(3)
            os.remove('../tmp/{window_id}ctx.json'.format(window_id=window_id))
            #print(4)
            new_dict = window_name_dict
        except:
            new_dict = window_id_dict
        new_window_id = window_name
        set_context(new_window_id, new_dict)
    #print ('end of get_window_id', new_window_id)
    return str(new_window_id)


def to_tuple(list_in):
    """
    transforma uma lista para o formato que pode ser utilizado em SQL
    """
    #print( 'im in to_tuple {var1}'.format(var1=list_in))
    result = tuple(list_in)
    #print( '{var1}'.format(var1=str(result)))
    if len(result) == 0:
        result = "in ('0')"
    elif len(result) > 1:
        result = "in {ids}".format(ids=result)
    else:
        result = "= '{ids}'".format(ids = result[0])
    return result

# def get_reports_path(report):
#   #print('{var1}'.format(var1=os.getcwd()))
#   path = os.path.join(os.getcwd(), "reports", "html" , report)#depois temos que ver os que s~ao pos e os que s~ao html
#   if not os.path.isfile(path):
#       path = os.path.join("../core", "reports", "html" , report)
#   return path

def get_records_to_print(key, model, force_db = False):
    """
    Transforma o record acrescentando-lhe os child ordenados pela opção de ordenação definida no modelos respectivo para que possa ser utilizado nos relatórios, e não só, lol
    o key espera a key relativamente aquele record
    o model espera uma instancia de modelo
    """
    #print('in get_records_to_print')
    #tem que tomar em conta combo, parent, list e many2many como child
    import objs
    record = get_model_record(model=model, key=key, force_db=force_db)
    #print( 'record do get_records_to_print {var1}, {var2}, {var3}, {var4}'.format(var1=str(record), var2=str(model), var3=str(key), var4=str(force_db)))
    final_record = {}
    for field in get_model_fields(model):
        #print('field {var1}'.format(var1=field))
        if field[1].__class__.__name__ in ['list_field', 'many2many', 'parent_field']:
        #'combo_field' ainda nao consigo mandar se nao o valor, tratar directo na funcao
            if field[1].__class__.__name__ != 'parent_field':
                #print('Im a List or a M2M')
                child_model = eval('objs.' + field[1].model_name + '(where="' + get_condition(field[1].condition, record) + '")')
            else:
                #print('Im a parent')
                if record[field[0]]:
                    child_model = eval("""objs.{model_name}(where = "id = '{key}'")""".format(model_name = field[1].model_name, key = record[field[0]]))
                else:
                    child_model = None
            child_records = []
            if child_model:
                child_records = child_model.get()
                # aqui tenho que modificar a função por forma a ordenar na listagem, neste momento não tenho tempo
            #print( 'child_records %', str(child_records))
            if len(child_records) != 0:
                final_child_records = []
                for child_record in child_records:
                    final_child_record = {}
                    for child_field in get_model_fields(child_model):
                        #print(str(child_record), str(child_field), str(child_model))
                        child_field_value = get_field_value(child_record, child_field, child_model)['field_value']
                        #if isinstance(child_field_value, tuple):
                        #   child_field_value = child_field_value[1]
                        final_child_record[child_field[0]] = child_field_value
                    final_child_record['id'] = child_record['id']
                    final_child_records.append(final_child_record)
                final_record[field[0]] = final_child_records
            else:
                final_record[field[0]] = []
        else:
            field_value = get_field_value(record, field, model)['field_value']
            #if isinstance(field_value, tuple):
            #   field_value = field_value[1]
            final_record[field[0]] = field_value
    final_record['id'] = key
    #print( 'final record do get_records_to_print {var1}'.format(var1=str(final_record)))
    return final_record


class Report(object):
    def __init__(self, record, report_template, printer='pos', only_html=True):
        """Se session['pos_printer'] = 'SYSTEM' gera html, se for 'ESC-POS' gera documento raw(ESC-POS)  sempre imforma qual template de report deve ser utilizado, se não encontra o template na pasta reports do projecto procura na geral (erp) e se não encontra devolve erro!!!
        records recebe uma lista de dicionarios contendo os registos a imprimir, nestes podem estar incluidas listas de registos filhos
        report_template é o nome do report sem extensão
        printer é o nome da impressora a utilizar nas impressoras esc_pos caso diferente de "pos"
        only_html por defeito True significa que ignora a entrada do erp_config e imprime sempre para html
        """
        self.record = record
        #print('Im in Report {var1}'.format(var1=str(self.record)))
        self.report_template = report_template
        self.printer = printer
        self.only_html = only_html

    def show(self):
        #print('Im in show de Report')
        if self.only_html:
            self.output_type = 'system'
            my_path = os.path.join(os.getcwd(), "reports", "html", self.report_template + '.html')
            base_path = os.path.join("/var/www/core", "reports", "html", self.report_template + '.html')
        else:
            self.output_type = bottle.request.session.get('pos_printer')
            if self.output_type == 'system':
                my_path = os.path.join(os.getcwd(), "reports", "html", self.report_template + '.html')
                base_path = os.path.join("/var/www/core", "reports", "html", self.report_template + '.html')
            else:
                my_path = os.path.join(os.getcwd(), "reports", "esc_pos", self.report_template + '.txt')
                base_path = os.path.join("/var/www/core", "reports", "esc_pos", self.report_template + '.txt')
        try:
            #print('vou abrir o template', my_path)
            tmpl_file = open(my_path, 'r', encoding='utf8')
            self.tmpl_string = tmpl_file.read()
            #print('abri o template')
        except:
            try:
                #print('vou abrir o template', base_path)
                tmpl_file = open(base_path, 'r', encoding='utf8')
                #print('tmpl_file')
                self.tmpl_string = tmpl_file.read()
                #print('abri o template 1')
            except:
                return error_message('O Template de Report escolhido não existe!!!')
        #print('{var1}'.format(var1=self.tmpl_string))

        #Se fizer uma função intermédia para imprimir várias instancias do report :
        #   se for esc_pos não tem problema pois é só mandar um atrás do outro
        #   se for system, tenho que ver como devolver, se for html puro, poderei eventualmente
        # modificar por forma a juntar tudo num html, ver a questão das páginas.
        #print ('self.' + self.output_type + '()')
        return eval('self.' + self.output_type + '()')

    def system(self):
        #print('Im in system')
        window_id = bottle.request.forms.get('window_id')
        #print (window_id)
        ctx_dict = get_context(window_id)
        self.record.update({'enterprise':ctx_dict.get('enterprise'), 'logotipo':ctx_dict.get('logotipo'), 'street':ctx_dict.get('street'), 'city':ctx_dict.get('city'), 'phone':ctx_dict.get('phone'), 'nif':ctx_dict.get('nif')})
        #print('after self.records.update')
        #print (self.tmpl_string)
        #print (self.record['linha_entrega'])#['rows']
        #print (bottle.template(self.tmpl_string, self.record))
        return bottle.template(self.tmpl_string, self.record)

    def esc_pos(self):
        from subprocess import Popen,PIPE
        lpr = Popen(["/usr/bin/lpr", "-P", self.printer], stdin = PIPE, shell = False, stdout = PIPE, stderr = PIPE)
        OpenDraw=chr(27) + chr(112) + chr(0) + chr(32) + chr(32)
        Now = time.strftime("%X")
        Today = datetime.date.today()
        Line = '----------------------------------------\n'
        VatLine = 'Iva Incluido a Taxa de 15,5%\n'#aqui pode ser 6%
        TanksLine = 'Obrigado pela sua visita\n'
        LineAdvance=chr(27) + chr(100) + chr(5)
        StartPrinter=chr(27)+ chr(61) + chr(1) + chr(27) + chr(64) + chr(27) + "" + chr(0) + chr(27)+ chr(73) + chr(0)
        CutPaper=chr(27) + chr(86) + chr(0)
        Enterprise = bottle.request.session.get('enterprise', None)
        street = bottle.request.session.get('street', None)
        street2 = bottle.request.session.get('street2', None) + '\n'
        Phone = bottle.request.session.get('phone', None)
        NIF = bottle.request.session.get('nif', None)
        Country = bottle.request.session.get('coutry', None)
        City = bottle.request.session.get('city', None)
        Capital = bottle.request.session.get('capital', None)
        header = Entreprise + street + street2 + '\nTel: ' + Phone + '\n' + City + Country + '\nNIF:' + NIF + '\nC.Social:' + Capital + '\n'
        report = self.tmpl_string.format(OpenDraw = OpenDraw, Now = Now, Today = Today, Line = Line, VatLine = VatLine, TanksLine = TanksLine, LineAdvance = LineAdvance, StartPrinter = StartPrinter, CutPaper = CutPaper, Entreprise = Entreprise, street = street, street2 = street2, Phone = Phone, NIF = NIF, Country = Country, City = City, Capital = Capital, header = header)
        #Ver como mandar o record para aqui de uma forma dinamica
        lpr.communicate(report.encode("utf-8"))
        return form_edit().show()

def make_function_name(string):
    """Esta função vai adaptar os nomes utilizados nos botões do workflow e os nomes das tabs para servirem para nomes de função:
    - espaços viram _
    - letras acentuadas perdem os acentos
    """
    #print('im in make_function_name {var1}'.format(var1=string))
    in_table = ' -éáàóãõâôç'
    out_table ='__eaaoaoaoc'
    translate_dict= str.maketrans(in_table, out_table)
    result = string.translate(translate_dict)
    #print( '{var1}'.format(var1=str(result)))
    return result

def get_select_fields(model, fields = []):
    """Devolve os campos que poderao ser utilizados no select"""
    #print('Im in get_select_fields')
    final_fields = []
    all_fields = []
    for field in get_model_fields(model):
        all_fields.append(field)
    if fields:
        for field in all_fields:
            if field[0] not in fields:
                all_fields.remove(field)
    #print( '{var1}'.format(var1=str(all_fields)))
    for field in all_fields:
        if field[1].__class__.__name__ not in ['function_field', 'many2many', 'list_field','separator','link','newline','label','hrline']:
            final_fields.append(field[0])
    #print('final_fields ', final_fields)
    return final_fields


def get_model_fields(model):
    """Devolve os atributos de um modelo que correspondem a 'fields'!!!"""
    #print ('in get_model_fields')
    #try:
    ordered_fields_dict = {}
    #print (str(model))
    #print (str(vars(model)))
    for var in vars(model):
        #print (str(vars(model)[var]))
        if 'orm.' in str(vars(model)[var]):
            field = eval('model.' + var)
            #print('este é um field', str(field))
            ordered_fields_dict[field.view_order] = (var, field)
        #print( str(ordered_fields_dict))
    for key in ordered_fields_dict.keys():
        #print(ordered_fields_dict[key])
        yield ordered_fields_dict[key]
    #print('fim de get_model_fields')
    #except:
    #    raise error_message(traceback.format_exc())

def get_model_record(model, key, force_db = False):
    """Função que valida se o registo está guardado e se não guarda, depois valida se este modelo corresponde ao formulario actual, se sim vai buscar os valores do request pois desta forma faz menos hits à base de dados e evita de o utilizador perder dados caso nao tenha gravado, se o modelo não for igual vai buscar na base de dados, significa que a ordem veio de outro modelo e a função foi chamada via código!
    Poderá tambem o modelo ter sido pedido a partir de uma lista e nesse caso tem que vir da BD!
    """
    #print('Estou no get_model_record {var1}, {var2}'.format(var1 = str(model), var2 = str(key)))
    # faltam os valores de id e dos campos hidden que eu necessito
    window_id = bottle.request.forms.get('window_id')
    ctx_dict = get_context(window_id)

    if key in [None, 'None']:
        from actions import model_action
        m_action = model_action(model)
        key = m_action.save(key=None, internal=True)
    if model.__model_name__ == ctx_dict.get('model_name') and not force_db:
        kargs = {}
        request_items = request_items_to_dict()
        #print( 'request_items {var1}'.format(var1=str(request_items)))
        for field in get_model_fields(model):
            if field[0] in request_items:
                kargs[field[0]] = request_items[field[0]]
        kargs['user'] = bottle.request.session.get('user')
        kargs['id'] = key
        #print( 'kargs do get_model_record {var1}'.format(var1=str(kargs)))
    else:
        #print('nao tinha no request por isso vou buscar na bd')
        kargs = model.get(key = key)[0]
        kargs['user'] = bottle.request.session.get('user')
    #print('out of get_model_record')
    return kargs

def format_number(s):
    """Formata os numeros num formato comercial mais user-friendle"""
    #print('im in format number')
    s = str(s)

    def split1000(s, sep='.'):
        return s if len(s) <= 3 else split1000(s[:-3], sep) + sep + s[-3:]

    s = s.replace('.', ',')
    s = s.split(',')
    d = ''
    if len(s) > 1:
        d = s[1]
    s = s[0]
    simbol = ''
    if len(s) > 2 and s[0] == '-':
        s = s[1:]
        simbol = '-'
    s = split1000(s)
    if d != '':
        d = ',' + d
    #print(simbol + s + d)
    return simbol + s + d


def convert_euro(v):
    v = to_decimal(v) / to_decimal('110.26')
    v = str(to_decimal(v)).replace('.', ',')
    return v


def to_decimal(number):
    if number not in [None, 'None', '']:
        number = Decimal('{number}'.format(number=str(number)))
        number = number.quantize(Decimal('0.1'))
    else:
        number = Decimal('0')
    return number


def get_terminal(terminal_name):
    #print('Im in get_terminal')#depois isto deve ser um metodo no objecto Terminal n~ao aqui
    from terminal import Terminal
    sql = """SELECT id from terminal Where name = '{name}';""".format(name=terminal_name)
    #print('{var1}'.format(var1=sql))
    terminal = run_sql(sql)
    if terminal:
        terminal_id = terminal[0]['id']
    else:
        terminal_id = Terminal(name = terminal_name, user = 1).put()
    return terminal_id


def get_many2many_name(table1, table2):
    #Gera o nome para a tabela intermédia no many2many ordenando os nomes das tuas tabelas por ordem alfabética
    tables = [table1, table2]
    tables.sort()
    name = tables[0] + '_' + tables[1]
    return name


def get_condition(condition, record):
    """Devolve a condição no caso dos list_field!"""
    #print('im in get_condition {var1}'.format(var1=str(condition)))
    condition_field = condition.split('{')[-1].split('}')[0]
    #print( '{var1} {var2}'.format(var1=condition_field, var2=str(record)))
    if record:
        condition_value = record[condition_field]
    else:
        condition_value = "0"
    if condition_value in ['None', None]:
        condition_value = "0"
    condition = condition.replace('{' + condition_field + '}', '{field}')
    condition = condition.format(field = condition_value)
    #print('{var1}'.format(var1=str(condition)))
    return condition


def set_base_context(window_id):
    """Cria os template_values por defeito que são partilhados por todos os objectos"""
    #print('oi do set_base_context')
    user = bottle.request.session.get('user', None)
    ctx_dict = {}
    if user:
        url = '/logout'
        url_linktext = 'Logout'
        user = user
        user_name = bottle.request.session.get('user_name', None)
    else:
        url = '/login'
        url_linktext = 'Login'
        user = ''
        user_name = ''
    ctx_dict['url'] = url
    ctx_dict['url_linktext'] = url_linktext
    ctx_dict['user'] = user
    ctx_dict['user_name'] = user_name

    if 'menu' not in bottle.SimpleTemplate.defaults:
        #bottle.request.session['menu'] = __get_menu__()
        ctx_dict['menu'] = __get_menu__()

    for variable in dir(erp_config):
        if '__' not in variable and 'db_' not in variable:
            ctx_dict[variable] = eval('erp_config.' + variable)
    set_context(window_id, ctx_dict)


def get_field_value(record, field, model):
    import objs
    """Devolve o valor e eventualmente as opções para os campos convertendo do que está na base de dados"""
    #print( 'estou no get_field_value', str(record), str(field), str(model))
    options = []
    if field[1].__class__.__name__ == 'function_field':
        if record:
            #print('im a function field', str(record['id']))
            value = eval("model.get_{field}(key = '{key}')".format(field = field[0], key = record['id']))
            #print( 'Im in get_field_value Im a function and my value is', str(value))
            record[field[0]] = value
            record['user'] = bottle.request.session['user']#tenho sempre que passar o user nos kargs quando quero fazer put
            #print( 'antes do put', str(model))
            model.kargs = record
            model.put()
            #print( 'depois do put')
        else:
            value = 0
        field_value = value
    else:
        if field[0] in record:
            field_value = record[field[0]]
            #print( 'o field[0] está no record {var1} e o field_name {var2}'.format(var1=str(record[field[0]]), var2=str(field_value)))
        else:
            #print( 'o field[0] não está no record')
            field_value = None
        if field[1].__class__.__name__ in ['combo_field', 'choice_field']:
            #print( 'its a combo or a choice my friend')
            if isinstance(field[1].options, list):
                options = field[1].options
            else:
                options = eval(field[1].options)
            #print( 'my combo options are {var1}'.format(var1 = str(options)))
            for option in options:
                #print( '{var1}'.format(var1 = str(option)))
                if str(field_value) in [str(option[0]), option[1]]:
                    field_value = (str(option[0]), option[1])
        elif field[1].__class__.__name__ == 'parent_field':
            #print( 'its a parent')
            options = eval('objs.{model_name}().get_options()'.format(model_name = field[1].model_name))
            #print( 'my parent options are {var1}'.format(var1 = str(options)))
            field_value = parent2HTML(value = field_value, options = options)
        elif field[1].__class__.__name__ == 'upload_field':
            if field_value:
                field_value = field_value
        if field_value in [None, 'None']:
            if field[1].__class__.__name__ in ['integer_field', 'float_field']:
                field_value = '0'
            else:
                field_value = ''
        if isinstance(field_value, Decimal):
            field_value = round(field_value, 2)
        if isinstance(field_value, float):
            field_value = round(field_value, 10)
    #print(str(field_value), str(options))
    return {'field_value':field_value, 'options':options}


def parent2HTML(value, options):
    """Formata o valor de uma parent_field como tuple"""
    for option in options:
        if str(value) == option[0]:
            if option[1] not in ['None', None]:
                value = (option[0], option[1])
            else:
                value = (option[0], '----')
    return value


def parent2DB(value, options):
    """transforma um tuple de um parent num valor para gravar na db"""
    for option in options:
        if value == option[1]:
            value = option[0]
    return value


def request_items_to_dict():
    """Transforma os items do request que é uma lista de tuples num dicionário"""
    #print('request_items_to_dict')
    result ={}
    for item in bottle.request.forms.items():
        result[item[0]] = bottle.request.forms.getunicode(item[0])
    #print('end of request_items_to_dict')
    return result


def run_onchange_function(values, model, field_name):
    """Aplica a função onchange do field e devolve os valores modificados pela função"""
    #print( 'estou no run_onchange_function e o field name e {var1} {var2}'.format(var1=field_name, var2=str(values)))
    for field in get_model_fields(model):
        if field[0] == field_name:
            function = field[1].onchange
            #print( function)
    values = eval('model.{function}({values})'.format(function = function, values = values))
    #print( 'estou no run_onchange_function e o meu values e: {var1}'.format(var1=str(values)))
    return values


def get_inputs(key, model, name, content_id, onchange=False):
    """Devolve os inputs que são utilizados nas listas em modo de edição inline
    O content_id serve para informar o id do elemento html que será preenchido com os id's'
    no caso do onchange alimenta-se do request em vez da base de dados"""
    import objs
    widgets = '/var/www/core/widgets/'
    window_id = bottle.request.forms.get('window_id')
    ctx_dict = get_context(window_id)
    print('estou no get_inputs')
    #print('content_id do get_inputs {var1}, {var2}, {var3}, {var4}'.format(var1=content_id, var2=str(model), var3=name, var4 = str(key)))
    #print( 'a porcaria do onchange e: {var1}'.format(var1=onchange))
    if onchange == False:
        print('onchange is false')
        if key in ['None', None]:
            values = None
        else:
            record_id = key
            values = model.get(key = record_id)[0]
            #print( record_id)
    else:
        #Significa que veio de um onchange e por isso os valores serão modificados pela função
        print( 'onchange is true')
        values = request_items_to_dict()
        #print( 'values e depois onchange {var1}, {var2}'.format(var1=str(values), var2=str(onchange)))
        if 'id' not in values:
            values['id'] = None
        values = run_onchange_function(values = values, model = model, field_name = onchange)
    #print( 'values are {var1}'.format(var1=str(values)))
    code = """
    <td></td>
    <td>
        <a href="#" class="button warning tiny" onclick="filter('{name}', '{content_id}', 'False');">
            <i class="fi-dislike"></i>
        </a>
    </td>""".format(name = name, content_id = content_id)
    first_field = True
    fields_order = 0
    fields_order_dict = {}
    for field in get_model_fields(model):
        fields_order_dict[fields_order] = field[0]
        fields_order += 1
    fields_order = 2
    for field in get_model_fields(model):
        kargs = {}
        #print( '{var1}'.format(var1=str(field)))
        if field[1].onlist == True:
            #print( 'sim é onlist {var1}'.format(var1=field[0]))
            if fields_order in fields_order_dict:
                focus_id = fields_order_dict[fields_order]
                fields_order += 1
            else:
                focus_id = 'save_button'
            if first_field == True:
                field[1].args += ' first_field'
            if values:
                kargs['value'] = get_field_value(values, field, model)['field_value']
                #if isinstance(kargs['value'], tuple):
                #   kargs['value'] = kargs['value'][1]
            elif field[1].default:
                if field[1].__class__.__name__ == 'parent_field':
                    options = eval('objs.{model_name}().get_options()'.format(model_name = field[1].model_name))
                    kargs['value'] = parent2HTML(value = field[1].default, options = options)
                else:
                    kargs['value'] = field[1].default
            #print( 'vou verificar se tenho o atributo onchange ', dir(field[1]))
            if hasattr(field[1], 'onchange') and field[1].onchange not in [False, 'False', None, 'None']:
                #print( 'tenho a opcao onchange ', field[1].onchange)
                if content_id == 'content':
                    target_id = 'form_list_onchange' + field[0]
                else:
                    target_id = 'list_field_onchange' + field[0]
                field[1].args = field[1].args + """ onChange="listEdit('{key}', '{name}', '{target_id}', '{focus_id}');" """.format(name = name, key = key, target_id = target_id, focus_id = focus_id );
            if field[1].__class__.__name__ in ['combo_field', 'choice_field']:
                if isinstance(field[1].options, list):
                    kargs['options'] = field[1].options
                else:
                    kargs['options'] = eval(field[1].options)
            for d_key in vars(field[1]):
                if d_key not in ['name', 'sum', 'source', 'nolabel', 'onlist', 'value', 'search', 'default', 'onchange', 'dynamic_atrs', 'options']:
                    kargs[d_key] = eval('field[1].' + d_key)
            kargs['name'] = field[0]
            kargs['nolabel'] = True
            #print( 'kargs {var1}'.format(var1=str(kargs)))
            if field[1].__class__.__name__ in ['integer_field', 'float_field', 'decimal_field', 'percent_field', 'currency_field', 'function_field']:
                text_align = 'right'
            else:
                text_align = 'left'
            kargs['source'] = 'list'
            kargs['cols'] = 12
            #print( field, kargs)
            #print('antes de widget', field[1].__class__.__name__ + '_inline', widgets)
            #print(bottle.SimpleTemplate(name = widgets + field[1].__class__.__name__ + '_inline').render(kargs))
            widget = bottle.SimpleTemplate(name = widgets + field[1].__class__.__name__ + '_inline').render(kargs)
            #print( 'widget', widget)
            #eval('widgets.{field_type}(**kargs).show()'.format(field_type=field[1].__class__.__name__))
            code += '<td style="text-align:{text_align};">{widget}</td>'.format(widget=widget, text_align=text_align)
    #se tiver main key actualizo a key senao o form e altero tambem no save para devolver a linha ou form consoante tenha mainkey ou nao
    #main_key = None
    #if 'main_key' in ctx_dict:
    #   main_key = ctx_dict.get('main_key')
    main_name = ctx_dict.get('name')
    if main_name != name:
        #print ('sim o name do get_inputs e diferente do name do ctx_dict')
        code += """<td width="15"></td>
        <td>
            <a href="#" class="button success tiny" onclick="save('{key}', '{name}', '{content_id}', 'Gravado com Sucesso!');$('#add_new').focus();" id="save_button">
                <i class="fi-save"></i>
            </a>
            <input name="key" value="{key}" type="hidden" id="key"></input>
        </td>""".format(key=key, name=name, content_id=content_id)
    else:
        #print ('nao o name do get_inputs nao e diferente do name do ctx_dict')
        code += """<td width="15"></td>
        <td>
            <a href="#" class="button success tiny" onclick="save('{key}', '{name}', '{content_id}', 'Gravado com Sucesso!');$('#add_new').focus();" id="save_button">
                <i class="fi-save"></i>
            </a>
            <input name="key" value="{key}" type="hidden" id="key"></input>
        </td>""".format(key=key, name=name, content_id='content')
    print ('fim do get_inputs')
    #print (code)
    return code

def generate_dates(start_date, end_date):
    """Utilizado para gerar uma lista de datas entre duas datas, util para por exemplo pesquisas entre datas"""
    start_date = format_date(start_date)
    end_date = format_date(end_date)
    return list(str(start_date + datetime.timedelta(days=d)) for d in range((end_date - start_date).days + 1))

def format_date(date):
    """Serve para formatar a data no formato ano-mes-dia"""
    if date not in ['None', '']:
        date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(str(date), '%Y-%m-%d')))
    else:
        date = None
    return date

def format_time(hour):
    """Serve para formatar a hora no formato hora:minuto:segundo"""
    if hour not in ['None', '']:
        hour = str(hour)
    else:
        hour = None
    return hour

def error_message(message):
    """Devolve a mensagem de erro formatada para o bottle com o código de status 500"""
    bottle.response.status = 500
    #return '<h4>Erro - Contacte o Administrador do Sistema</h4><br>' + message
    return '<h4>{msg}</h4>'.format(msg=message)

def correct_value(field, value, model_name):
    """Valores nas importações de CSV"""
    import objs
    model = eval('objs.{model_name}()'.format(model_name = model_name))
    if value not in ['None', '']:
        if field[1].__class__.__name__ in ['combo_field', 'parent_field', 'choice_field']:
            #caso seja parent ou combo poderá estar pelo seu valor de bd ou pelo valor humanamente agradavel, pode tambem ser um tuple com ambos
            if isinstance(value, tuple):
                value = value[0]
            else:
                #caso seja parent não esta na options do modelo
                if field[1].__class__.__name__ in ['combo_field', 'choice_field']:
                    if type(field[1].options) == "<class 'list'>":
                        options = field[1].options
                    else:
                        options = eval(field[1].options)
                elif field[1].__class__.__name__ == 'parent_field':
                    parent_model = eval('objs.{model_name}()'.format(model_name = model_name))
                    options = parent_model.get_options()
                for option in options:
                    if value in (option[0],option[1]):
                        value = option[0]
        elif field[1].__class__.__name__ == 'date_field':
            value = format_date(value)
        elif field[1].__class__.__name__ == 'time_field':
            value = format_time(value)
        elif field[1].__class__.__name__ == 'password_field':
            value = None
        elif field[1].__class__.__name__ == 'float_field':
            value = float(value)
        elif field[1].__class__.__name__ == 'integer_field':
            value = int(value)
        elif field[1].__class__.__name__ == 'boolean_field':
            if value == '' or value == 'False':
                value = False
            else:
                value = True
        elif field[1].__class__.__name__ in ['info_field', 'string_field', 'text_field']:
            if value == '':
                value = None
        return value


def data_to_csv(data, model, text=None, cols=[]):
    """Grava dados num ficheiro CSV, "text" é o texto que deve aparecer no botão para download, "cols" corresponde aos a lista dos campos a aparecer na listagem"""
    import base64
    fields = ''
    if text:
        if not cols:
            cols = data[0].keys()
        for field in cols:
            fields += field + ';'
        fields = fields[:-1]
        fields += '\n'
        for d in data:
            for field in cols:
                fields += str(d[field]) + ';'
            fields = fields[:-1]
            fields += '\n'
    else:
        for field in get_model_fields(model):
            if field[1].__class__.__name__ != 'list_field':
                fields += field[1].name + ';'
        fields = fields[:-1]
        fields += '\n'
        for d in data:
            for field in get_model_fields(model):
                if field[1].__class__.__name__ != 'list_field':
                    field_res = get_field_value(d, field, model)
                    field_value = field_res['field_value']
                    if isinstance(field_value, tuple):
                        field_value = '({value}, {description})'.format(value = field_res['field_value'][0], description = field_res['field_value'][1])
                    fields += str(field_value) + ';'
            fields = fields[:-1]
            fields += '\n'
    data = base64.encodestring(fields.encode('utf-8')).decode('utf8')
    if text:
        result = """<a href="data:text/csv;charset=utf-8;base64,{data}" class="button tiny radius success" download="ficheiro.csv" style="float:right;"><i class="fi-download"></i> {text}</a>""".format(data = data, text = text)
    else:
        result = """<a href="data:text/csv;charset=utf-8;base64,{data}" class="button tiny radius success" download="ficheiro.csv" style="float:right;"><i class="fi-download"></i></a>""".format(data = data)
    return result

def __compare__(string, paterns):
    from ldist import iterative_ldist
    result = False
    val = ''
    if not string:
        string = ''
    try:
        val = int(paterns)
    except:
        pass
    if isinstance(val,int):
        if paterns in string:
            result = True
    else:
        string = string.lower()
        string = string.replace('\xa0', ' ')
        paterns = paterns.lower()
        paterns = paterns.split(' ')
        words = string.split(' ')
        count_of_results = 0
        for word in words:
            for patern in paterns:
                if iterative_ldist(patern,word) < 2:
                    result = True
                else:
                    result = False
                if result == True:
                    count_of_results += 1
        if count_of_results == len(paterns):
            result = True
        else:
            result = False
    return result


def search(model, ctx_dict, list_name):
    """Função de Pesquisa que faz filtros nas listas, só vai buscar o que realmente necessito, ainda nao esta 100% completo tenho depois que melhorar o algoritmo de pesquisa e incluir alguma inteligencia inclusiver usando AND, OR e outros"""
    import objs
    #print('estou no search', list_name)
    #order_by = ctx_dict.get('order_by')#deve ir buscar pois o order_by do modelo pode n~ao ser o do modelo principal
    order_by = None
    if hasattr(model, '__order_by__'):
        if model.__order_by__:
            order_by = model.__order_by__
    #print ('1 do search')
    if ctx_dict.get('window_status') == 'popup':
        name = ctx_dict.get('popup_name')
    else:
        name = ctx_dict.get('name')
    join_expression = ''
    combo_expression = ''
    filter_expression = ctx_dict[list_name].get('filter_expression')
    if not filter_expression and ctx_dict[list_name].get('filter_expr_choice_restrict'):
        #print('não tenho filter expression mas tenho choise_restrict', list_name)
        filter_expression = ctx_dict[list_name].get('filter_expr_choice_restrict')
    if filter_expression:
        #print ('tenho filter_expression e estou no search ' , list_name, filter_expression)
        final_where = ''
        grouping_exp = None
        #quando utilizado nos list_field sabemos exactamente o que queremos, nao utilizamos o campo de pesquisa
        if '=' in filter_expression or '<' in filter_expression or '>' in filter_expression or ' in ' in filter_expression:
            #print('tenho comparações na minha expressão')
            final_where = filter_expression
        else:
            #print('não tenho comparações na minha expressão')
            filter_expression = filter_expression.replace('and', 'AND')
            filter_expression = filter_expression.replace('or', 'OR')
            # esta abordagem so permiter ter and ou or numa expressão e nunca os dois em simultaneo deve ser revista
            if 'AND' in filter_expression:
                filter_expression = filter_expression.split(' ')
                while 'AND' in filter_expression: filter_expression.remove('AND')
                grouping_exp = 'AND'
            elif 'OR' in filter_expression:
                filter_expression = filter_expression.split(' ')
                while 'OR' in filter_expression: filter_expression.remove('OR')
                grouping_exp = 'OR'
            else:
                if ' ' in filter_expression:
                    filter_expression = filter_expression.split(' ')
                    grouping_exp = 'AND'
                else:
                    filter_expression = [filter_expression]
                    grouping_exp = ''

            for expr in filter_expression:
                #print('a minha expressão é ', expr)
                if '-' in expr:  #depois precaver-me que a data é válida e o time tambem
                    #print('im a date')
                    filter_expression_type = 'date'
                elif ':' in expr:
                    #print('im a time')
                    filter_expression_type = 'time'
                else:
                    #print('im none of them')
                    try:
                        #print('im a number')
                        float(expr)
                        filter_expression_type = 'number'
                    except:
                        #print('im a text')
                        filter_expression_type = 'text'
                #print('filter_expression_type', filter_expression_type)
                fuzy_expression = ''
                normal_expression = ''
                for field in get_model_fields(model):
                    #print('field {var1}'.format(var1 = str(field)))
                    if field[1].__class__.__name__ in ['combo_field', 'choice_field']:
                        print('combo ou choice')
                        if hasattr (field[1], 'model') and field[1].model != None:
                            #print('tenho model {var1}, {var2}'.format(var1 = field[0], var2 = str(field[1].model)))
                            join_expression += 'LEFT JOIN {table_name} AS {alias_name} ON {alias_name}.id = {name}.{column_name} '.format(name = name, table_name = field[1].model, column_name = field[0], alias_name = field[0])
                            #print('{var1}'.format(var1 = join_expression))
                            column_names = field[1].column.split(' ')
                            #print('{var1}'.format(var1 = str(column_names)))
                            for column_name in column_names:
                                fuzy_expression += "coalesce({alias_name}.{column_name},'')||' '||".format(alias_name = field[0], column_name = column_name)
                            #print('{var1}'.format(var1 = fuzy_expression))
                        else:
                            #print('tenho options normais sem parent {var1}'.format(var1 = str(model)))
                            #E somente uma lista de opçoes e nao uma chamada a outra tabela por isso nao podemos fazer join
                            values = []
                            options = field[1].options
                            #print( 'options {var1}'.format(var1 = str(options)))
                            for option in options:
                                #print( '{var1}'.format(var1 = str(option)))
                                if __compare__(option[1], expr) or __compare__(option[0], expr):
                                    values.append(option[0])
                                #print( '{var1}'.format(var1 = str(values)))
                                if values:
                                    values = to_tuple(values)
                                    combo_expression += """{name}.{field} {values} """.format(name = name, field = field[0], values = values)
                        #print('out of combo')
                    elif field[1].__class__.__name__ == 'parent_field':
                        #print('parent')# se for um numero queremos que nos devolva apenas os que se parecem, agora devolve demais
                        join_expression += 'LEFT JOIN {table_name} ON {table_name}.id = {name}.{column_name} '.format(name = name, table_name = field[1].model_name.split('.')[0], column_name = field[0])
                        #print('{var1} {var2} {var3}'.format(var1 = join_expression, var2 = str(model), var3 = field[0]))
                        column_names = field[1].column.split(' ')
                        #print('{var1}'.format(var1 = str(column_names)))
                        for column_name in column_names:
                        #temos que rever a questao do join pois podera ter mais que uma coluna
                            fuzy_expression += "coalesce({table_name}.{column_name},'')||' '||".format(table_name = field[1].model_name.split('.')[0], column_name = column_name)
                        #print('{var1}'.format(var1 = fields_expression))
                        #print('out of parent')
                    elif field[1].__class__.__name__ in ['function_field', 'info_field']:
                        print('in search to fill the list, function or info fields', filter_expression_type, field[0])
                        if filter_expression_type in ['number']:
                            normal_expression += "{name}.{field} = '{filter_expression}' OR ".format(name = name, field = field[0], filter_expression = expr)
                        else:
                            #print('{var1} {var2}'.format(var1 = fuzy_expression, var2 = name))
                            #print(log(), "coalesce({name}.{field},'')||' '||".format(name = name, field = field[0]))
                            fuzy_expression += "coalesce({name}.{field},'')||' '||".format(name = name, field = field[0])
                        # como tratar os function??? este metodo presume que os valores estejam actualizados na BD
                    elif field[1].__class__.__name__ in ['date_field', 'time_field']:
                        if filter_expression_type in ['date', 'time']:
                            normal_expression += "{name}.{field} = '{filter_expression}' OR ".format(name = name, field = field[0], filter_expression = expr)
                    elif field[1].__class__.__name__ in ['percent_field', 'integer_field', 'currency_field', 'decimal_field', 'boolean_field']:
                        if filter_expression_type in ['number'] and field[0] != 'active':
                                normal_expression += "{name}.{field} = {filter_expression} OR ".format(name = name, field = field[0], filter_expression = expr)
                    elif field[1].__class__.__name__ in ['list_field', 'many2many', 'separator', 'new_line', 'link', 'label','hrline']:
                        pass

                    else:
                        fuzy_expression += "coalesce({name}.{field},'')||' '||".format(name = name, field = field[0])
                where = '('
                if fuzy_expression:
                    fuzy_expression = fuzy_expression[:-7]
                    where += """to_tsvector('portuguese', {fields}) @@ to_tsquery('portuguese', '{value}') """.format(fields = fuzy_expression, value = expr)
                #print('fuzy_expression ', fuzy_expression)
                if normal_expression:
                    if fuzy_expression:
                        normal_expression = 'OR ' + normal_expression[:-4]
                    else:
                        normal_expression = normal_expression[:-4]
                    where += normal_expression #"""OR """ +
                #print('normal_expression ', normal_expression)
                if join_expression:
                    model.kargs['join'] = join_expression
                if combo_expression:
                    where += 'OR ' + combo_expression
                where += ')'
                final_where += where + ' ' + grouping_exp
                #print('search where ', where)
                #print('final where ', final_where)
        if grouping_exp != '' and grouping_exp is not None:
            final_where = final_where[:-len(grouping_exp)]
        model.kargs['where'] = final_where
        #print('o meu where é ', final_where)
        if ctx_dict[list_name].get('filter_expr_choice_restrict'):
            #print('tenho filter_expr_choice_restrict')
            if 'id in' in model.kargs['where']:
                #print('tenho id in no meu where')
                id_in_expression = model.kargs['where'].split('id in')[1].replace('(', '[').replace(')', ']')
                #print('id_in_expression', id_in_expression)
                list_of_id_in_expression = eval(id_in_expression)
                #print('list_of_id_in_expression', list_of_id_in_expression)
                list_of_restrict = eval(ctx_dict[list_name].get('filter_expr_choice_restrict')[6:].replace('(', '[').replace(')', ']'))
                #print('list_of_restrict', list_of_restrict)
                final_id_list = []
                for my_id in list_of_id_in_expression:
                    if my_id in list_of_restrict:
                        final_id_list.append(my_id)
                model.kargs['where'] = 'id ' + to_tuple(final_id_list)
            else:
                model.kargs['where'] +=  ' AND ' + model.__name__  + '.' + ctx_dict[list_name].get('filter_expr_choice_restrict')
            #print('final model where ----------------', model.kargs['where'])
    # aqui depois temos que tratar expressoes,por enquanto vamos tratar apenas uma palavra
    #print('antes do get ao modelo')
    result_list = model.get(order_by = order_by, fields = ['id'])
    #print(result_list, order_by)
    result = []
    index = 0
    for record in result_list:
        result.append((index, record['id']))
        index += 1
    #print('{var1}'.format(var1 = str(result)))
    #print('end of search')
    return result


def prepare_list_data(model, ctx_dict, list_name):
    """
    Recebe os argumentos e devolve um dicionário com os dados necessários para montar a lista
    """
    #print('in_prepare_list_data', model, list_name, ctx_dict[list_name].get('list_field'))
    list_field = ctx_dict[list_name].get('list_field')
    list_edit_mode = ctx_dict[list_name].get('list_edit_mode')
    window_status = ctx_dict.get('window_status')
    #print('window_status---------------', window_status)
    #aqui se for um list_field tenho que ler o form type no field e nao no model e o form type declarado (vem nos atributos) tambem pode ser popup ai o list_edit_mode fica 'list_edit_mode' e o window_status vira popup
    #if list_edit_mode == 'popup':
        #window_status = 'popup'
        #list_edit_mode = 'edit'#isto fica temporario, com a possibilidade de abrir mapas ou gantt ou outro em popup isto tem que mudar
    #print('1')
    rights = ctx_dict.get('rights')#[list_name] depois posso ter rights ao nivel do list_field
    title = ctx_dict[list_name].get('title')
    page = ctx_dict[list_name].get('page')
    limit = ctx_dict[list_name].get('limit')
    #print('limit {var1}, page {var2},  list_name {var3}'.format(var1 = str(limit), var2 = str(page), var3 = list_name))
    offset = int(page) * int(limit)
    filter_expression = ctx_dict[list_name].get('filter_expression')
    #print ('prepare_list_data filter_expression ', filter_expression, list_name)
    if not filter_expression:
        filter_expression = ''#{}
        ctx_dict[list_name]['filter_expression'] = filter_expression
    order_by = None
    if hasattr(model, '__order_by__'):
        if model.__order_by__:
            order_by = model.__order_by__
    ctx_dict[list_name]['order_by'] = order_by
    show_search = ctx_dict[list_name].get('show_search')
    #print('show_search {var1}'.format(var1=str(show_search)))

    #caso tenha __records_view__ só aparecem os registos que respeitem a condição como por exemplo estado=active
    if hasattr(model, '__records_view__'):
        print('tenho records_view')
        for rv in model.__records_view__:
            print('o rv é --------------', rv, 'e o rights é ----', rights)
            for r in rights[1]:
                if r not in rv[2] and r != 'Administrator':
                    #adiciona as condições de __records_view__ a filtros
                    if isinstance(rv[1], tuple):
                        print('its a list')
                        ctx_dict[list_name]['filter_expression'] += ' {var1} {var2} {var3}'.format(var1=rv[0], var2=rv[3], var3=rv[1])
                        break
                    else:
                        print('its a function')
                        ctx_dict[list_name]['filter_expression'] += ' {var1} {var2} {var3}'.format(var1=rv[0], var2=[3], var3=eval('model.' + rv[1]))
                        #print(ctx_dict[list_name]['filter_expression'])
                        break
    print('out off __records_view__')
    #só necessito dos campos que sejam onlist pois serão os unicos que vão aparecer mas para efeitos de search necessito de todos que sejam search=True
    fields = []
    for field in get_model_fields(model):
        #print(field[0])
        if hasattr(field[1], 'onlist') and field[1].onlist == True:
            fields.append(field[0])
    fields = get_select_fields(model, fields)
    #print('fields = {var1}'.format(var1 = str(fields)))
    #vai buscar os id's que correspondem ao filtro da lista e grava na session
    selected_ids = ctx_dict[list_name].get('selected_ids')
    #print('before search {var1} {var2}'.format(var1 = str(model), var2 = filter_expression))
    #print('selected_ids are {var1}'.format(var1=str(selected_ids)))
    if not selected_ids:
        #print('I dont have selected ids')
        selected_ids = search(model=model, ctx_dict=ctx_dict, list_name=list_name)
        #list_ctx_dict[list_name]['selected_ids'] = selected_ids
    #print('selected_ids are {var1}'.format(var1 = str(selected_ids)))
    page_ids = []
    for rec_id in selected_ids:
        if rec_id[0] >= offset and rec_id[0] <= offset + (int(limit))-1:
            page_ids.append(rec_id[1])
    #print('page_ids are {var1}'.format(var1=str(page_ids)))
    where = model.__name__ + '.id ' + str(to_tuple(page_ids)) + ' '
    #print('prepare_list_data were is ', where)
    model.kargs['where'] = where
    data = model.get(order_by=order_by, fields=fields)
    #print('{var1}'.format(var1=str(data)))
    #print('after data')
    #print (len(selected_ids), offset, '------------------------------------------------------')
    if len(selected_ids) < offset:
        offset = 0
        page = 0
    rows_count = len(selected_ids)
    if window_status == 'popup':
        check_box = ''
    else:
        check_box = """
            <input type="checkbox" class="check" id="lines_controler" onchange="toggle_lines();">
            """
    columns = []
    #print(get_model_fields(model))
    for field in get_model_fields(model):
        #print('{var1}'.format(var1=str(field)))
        if hasattr(field[1], 'onlist') and field[1].onlist == True:
            if field[1].__class__.__name__ in ['integer_field', 'float_field', 'decimal_field', 'percent_field', 'currency_field', 'function_field']:
                columns.append((field[0], field[1].name, 'right'))
            else:
                columns.append((field[0], field[1].name, 'left'))
    #print('as colunas são: ', columns)
    #rights = ctx_dict.get('rights')
    add_ok = False
    add_rights = ['create', 'full_access']
    for add_right in add_rights:
        if add_right in rights[0]:
            add_ok = True
    delete_ok = False
    delete_rights = ['delete', 'full_access']
    for delete_right in delete_rights:
        if delete_right in rights[0]:
            delete_ok = True
    edit_ok = False
    edit_rights = ['write', 'full_access']
    for edit_right in edit_rights:
        if edit_right in rights[0]:
            edit_ok = True
    footer_vals = {}
    rows = []
    line_color = False
    #print('geting on the data')
    #print(data)
    for d in data:
        #print(d)
        fields = {}
        for field in get_model_fields(model):
            if hasattr(field[1], 'onlist') and field[1].onlist is True:
                #print(field[0])
                field_res = get_field_value(d, field, model)
                #print(field_res)
                field_value = field_res['field_value']
                #print('field_value type:', type(field_value), field_value)
                if isinstance(field_value, datetime.time):
                    # o ujson chateia-se com o datetime.time por isso tenho que converter antes de serializar
                    field_value = str(field_value)
                elif isinstance(field_value, tuple):
                    field_value = field_value[1]
                options = field_res['options']
                if hasattr(field[1], 'sum') and field[1].sum is True:
                    if field[0] in footer_vals:
                        # aqui validar que o campo pode ser somado
                        try:
                            footer_vals[field[0]] += to_decimal(field_value)
                        except:
                            pass
                    else:
                        try:
                            footer_vals[field[0]] = to_decimal(field_value)
                        except:
                            pass
                else:
                    footer_vals[field[0]] = ''
                #print('3')

                if isinstance(field_value, Decimal):
                    field_value = str(format_number(field_value))

                field_name = field[0]
                percent = ''
                if field[1].__class__.__name__ == 'percent_field':
                    percent = '%'
                if field[1].__class__.__name__ in ['integer_field', 'float_field', 'decimal_field', 'percent_field', 'currency_field', 'function_field']:
                    text_align = 'right'
                else:
                    text_align = 'left'
                #print('4')
                fields[field[0]] = (field_name, field_value, percent, text_align)
                #print(fields)
        text_color = 'black'
        text_weight = 'normal'
        #print('5')
        if hasattr(model, '__record_colors__'):
            #print('{var1}'.format(var1=model.__record_colors__))
            for rc in model.__record_colors__:
                for color in rc[1]:
                    if d[rc[0]] == color:
                        if rc[1][color] not in ['bold']:
                            text_color = rc[1][color]
                        else:
                            text_weight = rc[1][color]
        #print('6')
        row = [fields, (text_color, text_weight, d['id'])]
        rows.append(row)
    #print('{var1} {var2} {var3}'.format(var1 = str(rows), var2 = str(footer_vals), var3 = str(columns)))
    for key in footer_vals:
        footer_vals[key] = format_number(footer_vals[key])

    result = {
        'name': model.__name__,
        'check_box': check_box,
        'title': title,
        'columns': columns,
        'rows': rows,
        'add_ok': add_ok,
        'delete_ok': delete_ok,
        'edit_ok': edit_ok,
        'list_edit_mode': list_edit_mode,
        'footer_vals': footer_vals,
        'limit': limit,
        'offset': offset,
        'order_by': order_by,
        'page': page,
        'rows_count': rows_count,
        'window_status': window_status,
        'popup_option_fields': model.__get_options__,  # ver isto
        'popup_field_name': ctx_dict.get('popup_field_name'),  # ver isto
        'list_field': list_field,  # em vez de true ou false pode passar o nome do field
        'show_search': show_search,
        'selected_ids': selected_ids,
        'side_menu': ctx_dict.get('side_menu'),
        'breadcrumbs_navigation': ctx_dict.get('breadcrumbs_navigation')
    }
    #print('{var1}'.format(var1 = str(result)))
    #print('end of prepare_list_data', page)
    return result

def prepare_m2m_data(model, ctx_dict, fields, parent_ids):
    """
    Recebe os argumentos e devolve um dicionário com os dados necessários para montar a lista
    """
    #print('in_prepare_m2m_data')
    name = ctx_dict.get('name')
    record = ctx_dict.get('record')
    edit_ok = ctx_dict.get('edit_ok')
    popup = False
    if ctx_dict.get('window_status') == 'popup':
        popup = True
    title = ctx_dict.get('title')
    rights = ctx_dict.get('rights')
    columns = []
    #print('before get options')
    options = model.get_options()#final_filter
    #print( 'my options {var1}'.format(var1=str(options)))
    #isto pode ter que passar para o form o model claro
    data = model.get()
    #print( 'my data is {var1}'.format(var1=str(data)))
    disabled = ''
    if edit_ok == False:
        disabled = 'disabled'
    #cols=source
    #field_name=model.__title__, cols=cols, name=self.name, disabled=disabled)
    #for option in options:
    #   pass
        #value=option[0], description=option[1]
    #cols='4'
    footer_vals_ordered = []
    if fields: #estes fields e quando eu quero neste many2many ver apenas alguns campos ver depois se faz falta na lista
        for f in fields:
            for field in get_model_fields(model):
                if f == field[0]:
                    if field[1].onlist == True:
                        #name=field[1].name
                        footer_vals_ordered.append(field[0])
                        if field[1].__class__.__name__ in ['integer_field', 'float_field', 'decimal_field', 'percent_field', 'currency_field', 'function_field']:
                            columns.append((field[0], field[1].name, 'right'))
                        else:
                            columns.append((field[0], field[1].name, 'left'))
    else:
        for field in get_model_fields(model):
            if field[1].onlist == True:
                #name=field[1].name
                footer_vals_ordered.append(field[0])
                if field[1].__class__.__name__ in ['integer_field', 'float_field', 'decimal_field', 'percent_field', 'currency_field', 'function_field']:
                    columns.append((field[0], field[1].name, 'right'))
                else:
                    columns.append((field[0], field[1].name, 'left'))
    #name=self.name

    footer_vals = {}
    count_of_parent_ids = {}
    for parent_id in set(parent_ids):
        count_of_parent_ids[parent_id] = parent_ids.count(parent_id)
    #print( 'count_of_parent_ids {var1}'.format(var1=str(count_of_parent_ids)))
    line_color = False
    rows = []

    for d in data:
        if d['id'] in count_of_parent_ids:
            count_parent = count_of_parent_ids[d['id']]
        else:
            count_parent = 0
        #print( 'count_parent {var1}'.format(var1 = str(count_parent)))

        for count in range(0, count_parent):# o count parent ´e um truque que permite que se a opç~ao exisitr v´arias vezes aparece s´o uma depois deve ser melhorado
            text_color = 'black'
            text_weight = 'normal'
            #print('5')
            if hasattr(model, '__record_colors__'):
                #print('{var1}'.format(var1 = str(model.__record_colors__)))
                for rc in model.__record_colors__:
                    for color in rc[1]:
                        if d[rc[0]] == color:
                            if rc[1][color] not in ['bold']:
                                text_color = rc[1][color]
                            else:
                                text_weight = rc[1][color]
            fields = {}
            for field in get_model_fields(model):
                if hasattr(field[1], 'onlist') and field[1].onlist == True:
                    field_res = get_field_value(d, field, model)
                    field_value = field_res['field_value']
                    #print( 'field_value {var1}'.format(var1 = str(field_value)))
                    if isinstance(field_value, tuple):
                        if field[1].__class__.__name__ == 'parent_field':
                            field_value = '{a},{b}'.format(a=field_value[0], b=field_value[1])
                        else:
                            field_value = field_value[1]
                    #options = field_res['options']
                    #print( 'options {var1}'.format(var1 = str(options)))
                    #if hasattr(field[1], 'sum') and field[1].sum == True:
                    if hasattr(field[1], 'sum') and field[1].sum == True and field_value not in ['None', None,'']:
                        if field[0] in footer_vals:
                            footer_vals[field[0]] += float(field_value)
                        else:
                            footer_vals[field[0]] = float(field_value)
                    else:
                        footer_vals[field[0]] = ''
                    field_name = field[0]
                    percent = ''
                    if field[1].__class__.__name__ == 'percent_field':
                        percent = '%'
                    if field[1].__class__.__name__ in ['integer_field', 'float_field', 'decimal_field', 'percent_field', 'currency_field', 'function_field']:
                        text_align = 'right'
                    else:
                        text_align = 'left'
                    #print('novo field_value {var1}'.format(var1 = str(field_value)))

                    fields[field[0]] = (field_name, field_value, percent, text_align)

            row = [fields, (text_color, text_weight, d['id'])]
            #print( 'row {var1}, {var2}'.format(var1 = str(row), var2 = str(len(rows))))
            rows.append(row)
    #print( 'columns {var1}, {var2}'.format(var1=str(columns), var2=str(rows)))
    result = {'name':model.__name__,
                #'check_box':check_box,
                'field_name':title,
                'columns':columns,
                'rows':rows,
                #'add_ok':add_ok,
                #'delete_ok':delete_ok,
                'edit_ok':edit_ok,
                #'list_edit_mode':model.__list_edit_mode__,
                'footer_vals':footer_vals,
                #'limit':limit,
                #'offset':offset,
                #'page':page,
                #'rows_count':rows_count,
                'options':options
                #'fields':fields
            }
    #print( 'result {var1}'.format(var1 = str(result)))
    #result.update(ctx_dict)
    #print ('fim do prepare_m2m_data')
    return result

def simple_report(data, model, title):
    """Gera um relatório simples a partir de uma lista"""
    p = 40 # aqui falta salvaguardar a paginação... fica para depois
    labels = ''
    x = 4
    y = 12
    for field in get_model_fields(model):
        if field[1].__class__.__name__ not in ['list_field', 'parent_field','many2many']:
            labels += '<tspan x="{x}mm" y="{y}mm">{name}</tspan>'.format(x = str(x), y = str(y), name = field[1].name)
            if field[1].__class__.__name__ not in ['boolean_field']:
                x += int(field[1].size)
            else:
                x += 10
    values = ''
    x = 4
    y = 18
    for d in data:
        for field in get_model_fields(model):
            if field[1].__class__.__name__ not in ['list_field', 'parent_field', 'many2many']:
                field_res = get_field_value(d, field, model)
                field_value = field_res['field_value']
                if isinstance(field_value, tuple):
                    field_value = field_res['field_value'][1]
                values += '<tspan x="{x}mm" y="{y}mm">{value}</tspan>'.format(x = str(x), y = str(y), value = field_value)
                if field[1].__class__.__name__ not in ['boolean_field']:
                    x += int(field[1].size)
                else:
                    x += 10
        x = 4
        y += 5
    code ="""<?xml version="1.0" encoding="utf8" standalone="no"?>
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
            "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
            <svg xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
            width="212mm" height="297mm" >
                <rect x="2mm" y="2mm" width="206mm" height="293mm" fill="white" stroke="black"/>
                <text  x="4mm" y="3.5mm" fill="black" font-size="16" font-family="Helvetica">
                    {title}
                </text>
                <text fill="black" font-size="15" font-family="Helvetica">
                    {labels}
                </text>
                <line x1="4mm" y1="14mm" x2="200mm" y2="14mm" stroke="black" stroke-width="1"/>
                <text fill="black" font-size="13" font-family="helvetica">
                    {values}
                </text>
                <text  x="160mm" y="294mm" fill="black" font-size="9" font-family="Helvetica">
                    Produzido por computador ERP + v.2.0
                </text>
            </svg>
        """.format(title = title, labels = labels, values = values)
    return code

def __get_menu__(user = None):
    """Gera o menu a partir do ficheiro menu.list"""
    #print('get_menu')
    user = bottle.request.session.get('user', None)
    if not user:
        bottle.redirect('/login')
    sql = """SELECT nome FROM role
                join role_users ON
                role.id = role_users.role
                WHERE role_users.users = '{user}';""".format(user = user)
    #print( sql)
    user_roles = []
    db_user_roles = run_sql(sql)
    #print( str(db_user_roles))
    if db_user_roles:
        for user_role in db_user_roles:
            user_roles.append(user_role['nome'])
    code = """
            <ul class="left">
        """
    center_menu_code = """
            <ul class="center">
        """
    from erp_config import home_path
    #print(home_path)
    path = os.path.join(home_path, "menu.list")
    menu_file = open(path, encoding = 'utf-8')
    first_menu = True
    for line in menu_file.readlines():
        #depois fazer o .strip() por forma a permitir espaços no ficheiro menu.list, neste momento não é prioridade
        #print('linha')
        authorized = False
        line = line.strip()
        splited_line = line.split('[')
        menu = splited_line[0].split(',')
        authorized_roles = splited_line[1][:-1].split(',')
        authorized_roles.append('Administrator')
        if 'All' in authorized_roles:
            authorized = True
        else:
            for user_role in user_roles:
                if user_role in authorized_roles:
                    authorized = True
        if authorized == True:
            if menu[0] == '1':#significa que é um menu de 1º nivel
                if first_menu == False:
                    code += """</ul>
                        """
                code += """
            <li class="has-dropdown">
                <a href="#"><i class="{icon}"></i> {description}</a>
                    <ul class="dropdown">
                    """.format(icon = menu[1], description = menu[2])
                first_menu = False
            elif menu[0] == '2':#significa que é de segundo nivel depois repensar esta jonsa eventualmente usar xml
                code += """
                <li><a href="{url}"><i class="{icon}"></i> {description}</a></li>
                """.format(icon = menu[1], url = menu[3], description = menu[2])
            elif menu[0] == '3':#significa que é para alinhar ao centro e não tem submenus
                #print(' sou 3')
                center_menu_code += """
                <li><a href="{url}" style="color: #FFBF00"><i class="{icon}"></i> {description}</a></li>
                """.format(icon = menu[1], url = menu[3], description = menu[2])
    code += """
            </ul>
        </li>
    </ul>
    """
    code += center_menu_code
    code += """
    </ul>
    """

    #print(code)
    return code
