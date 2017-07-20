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

import os, sys
sys.path.append(os.getcwd())
import bottle

def get_model_fields(model):
    """Devolve os atributos de um modelo que correspondem a 'fields'!!!"""
    ordered_fields_dict = {}
    for var in vars(model):
        if 'widgets' in str(vars(model)[var]):
            field = eval('model.' + var)
            #print (field)
            ordered_fields_dict[field.view_order] = (var, field)
    #print (ordered_fields_dict.keys())
    for key in ordered_fields_dict.keys():
        yield ordered_fields_dict[key]

def require_auth(target):
    #Method decorator to ensure login
    def secure(*args, **kargs):
        #print ('inicio do secure de require_auth')
        #print (args)
        #print (kargs)
        if 'user' in bottle.request.session:
            #print ('fim do secure vou retornar o objecto')
            return target(*args, **kargs)
        else:
            #bottle.request.session['redirect_url'] = bottle.request.url
            #bottle.request.session.save()
            bottle.redirect('/login')
    return secure

#def require_auth(target):
#   session = bottle.request.environ.get('beaker.session')
#   def wrapper(*a, **ka):
#       user, password = bottle.request.auth or (None, None)
#       if session and user not in session:
#           bottle.response.headers['WWW-Authenticate'] = 'Basic realm="private"'
#           return bottle.HTTPError(401, text)
#       return target(*a, **ka)
#   return wrapper

def verify_orm_rights(target):
    """Method decorator to verify if the user have the right to do what is requiring
    Esta abordagem só serve no ORM"""
    #print('im in verify_orm_rights')
    def secure(self, *args, **kargs):
        #session = bottle.request.environ.get('beaker.session')
        result = verify_rights(model=self, action=target.__name__)
        if result == True:
            return target(self, *args, **kargs)
        else:
            return result
    return secure

def verify_form_rights(target):
    """Method decorator to verify if the user have the right to do what is requiring
    Esta abordagem só serve no formulário"""
    def secure(*args, **kargs):
        #print ('inicio do secure do verify_form_rights')
        from utils import get_context, set_context
        import objs
        window_id = kargs.get('window_id')
        #print (window_id)
        ctx_dict = get_context(window_id)
        #print ('ctx_dict no verify_form_rights', ctx_dict)
        model_name = ctx_dict.get('model_name')
        model = eval("""objs.{model_name}()""".format(model_name=model_name))
        result = verify_rights(model=model, action=target.__name__)
        #print ('2')
        if result == True:
            return target(*args, **kargs)
        elif isinstance(result, list):
            ctx_dict['rights'] = result
            set_context(window_id, ctx_dict)
            #print ('fim do secure de form, vou carregar o objecto')
            return target(*args, **kargs)
        else:
            return result
    return secure

def verify_rights(model, action):
    #Função que verifica os direitos e devolve True ou False
    #Não esquecer os especiais 'All' e 'Administrator'
    #print('verify_rights')
    from orm import run_sql, put, get_identity
    #from utils import bottle
    #from utils import ustring
    #session = bottle.request.environ.get('beaker.session')
    #print ('verify_rights')
    user = bottle.request.session.get('user', None)
    return_type = 'binary'
    if not user:
        return True
    sql = """SELECT nome FROM role 
join role_users ON
role.id = role_users.role
WHERE role_users.users='{user}'""".format(user=user)
    user_roles = []
    #print('before my_roles')
    my_roles = run_sql(sql)
    #print(my_roles)
    for user_role in my_roles:
        user_roles.append(user_role['nome'])
    if hasattr(model, '__auth__') and model.__auth__ != {}:
        auth_rules = model.__auth__
        rules = []
        rules_in_db_list = []
        for auth_rule in auth_rules:
            for rule in auth_rules[auth_rule]:
                if rule not in rules:
                    rules.append(rule)
        rules_list = rules
        if str(tuple(rules))[-2:] == ',)':
            rules = str(tuple(rules))[:-2] + ')'
        else:
            rules = tuple(rules)
        sql = """SELECT nome FROM role WHERE nome in {rules}""".format(rules=rules)
        #print(1)
        rules_in_db = run_sql(sql)
        #print(2)
        for rule_in_db in rules_in_db:
            if rule_in_db not in rules_in_db_list:
                rules_in_db_list.append(rule_in_db['nome'])
        #print(3)
        #print(rules_list)
        #print(rules_in_db_list)
        for rule in rules_list:
            #print(rule)
            if rule not in rules_in_db_list and rule not in ['All']:
                kargs = {'nome':rule, 'user':user}
                #print(kargs)
                resp = put('role', **kargs)
                #print(resp)
        #print(4)
    else:
        return True
    #print(4)
    if action == 'get':
        #print('i m get')
        authorized_roles = auth_rules['read'] + auth_rules['full_access']
        false_result = [0,[]]
    elif action == 'put':
        #print ('im in auth', model.kargs)
        if model.kargs:
            fields_dict = model.kargs
        else:
            fields_dict = {}
            for f in get_model_fields(model):#aqui rever depois esta coisa tenho 3 funcoes a fazer o mesmo uma no orm outra em utils e outra no auth e muito provavelmente pelo menos aqui podera ser excluido
                if hasattr(model, f[0]):
                    fields_dict[f[0]] = eval('model.' + f[0])
        if 'id' in fields_dict:
            authorized_roles = auth_rules['write'] + auth_rules['full_access']
            false_result = None
        else:
            authorized_roles = auth_rules['create'] + auth_rules['full_access']
            false_result = None
    elif action == 'delete':
        authorized_roles = auth_rules['delete'] + auth_rules['full_access']
        false_result = 0
    else:
        return_type = 'verbose'
        authorized_roles = auth_rules['read'] + auth_rules['full_access']
        false_result = """<div style="color:red;">Não tem direito de utilizar este recurso, fale com o Administrador !!!</div>"""
    authorized = False
    authorized_roles.append('Administrator')
    form_rights = []
    #print('before authorized_roles')
    if 'All' in authorized_roles:
        authorized = True
    for user_role in user_roles:
        if user_role in authorized_roles or 'All' in authorized_roles:
            authorized = True
            if return_type == 'verbose':
                for rule in auth_rules:
                    if user_role in auth_rules[rule]:
                        form_rights.append(rule)
                    elif user_role == 'Administrator':
                        form_rights.append('full_access')
    #print('fim de verify_rights')
    if authorized:
        if return_type == 'verbose':
            return [form_rights, user_roles]
        else:
            return True
    else:
        return false_result

