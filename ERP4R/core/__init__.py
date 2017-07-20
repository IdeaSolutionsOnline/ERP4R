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
sys.path.append('/var/www/core')

from auth import require_auth
from utils import set_base_context, get_context, set_context, get_window_id
from objs import *
from bottle import *
import uwsgi
import redis
import gevent.select
import uuid
import bottle

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

#from erp_config import *

#para implementação do CUBES
#from . import cubes
#MODEL_PATH = "/var/www/core/static/cubes/model.json"
#DB_URL = "sqlite:////var/www/core/static/cubes/data.sqlite"
#CUBE_NAME = "irbd_balance"
#workspace = None
#model = None

TEMPLATE_PATH.insert(0, '/var/www/core/views/')
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': '/tmp/',  # home_path +
    'session.timeout': 6000,
    'session.auto': True
}

#ser_url='''<a href=""></a>'''

#import subprocess
#child = subprocess.Popen("/usr/bin/python3 /var/www/core/check_pop3.py")
#child = subprocess.Popen("/usr/bin/python3 /var/www/core/check_pop3.py", shell=True)


class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''

    def __init__(self, a):
        self.a = a

    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

application = SessionMiddleware(app(), session_opts)
app = StripPathMiddleware(application)


@hook('before_request')
def setup_request():
    """Implements the request session"""
    request.session = request.environ['beaker.session']


@post('/get_new_window_id/<window>')
def get_new_window_id(window):
    """A funçao que atribui novos window_id a chamar de base.tpl"""
    #print(window)
    window = window.split('_')
    window_name = window[0]
    window_id = window[1]
    #print('im in the get_new_window_id called by base.tpl',
     #     window_name,
      #    window_id)
    return get_window_id(window_name=window_name, window_id=window_id)


@post('/popup_close/<window_id>')
def popup_close(window_id):
    """A funçao que permite retornar o window_status a edit quando o popup fecha"""
    #print ('oi estou no popup_close')
    from utils import get_context as gtx
    ctx_dict = gtx(window_id)
    ctx_dict['window_status'] = 'edit'
    set_context(window_id, ctx_dict)
    #print ('sai do popup_close')


@route('/.well-known/acme-challenge/rfW8CZPAII2ie8B7VgSMfVstGRME4_Iw1QZqcsuR9E0')
def letsencript_certificate_answer():
    """permite validar o certificado do lets encript e assim permitir gerar"""
    return 'rfW8CZPAII2ie8B7VgSMfVstGRME4_Iw1QZqcsuR9E0.9YUmNIp0ncX8uEaqjc55kjwkQY5dDPfh1asS-V8Ic6w'



@route('/')
@view('base')
#@require_auth
def main():
    """Funçao index"""
    #print('Init do main_route')
    window_id = str(get_window_id())
    #print(window_id)
    set_base_context(window_id)
    #print('oi')
    ctx_dict = get_context(window_id)
    #print(ctx_dict)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'index'
    ctx_dict['title'] = 'ERP +'
    ctx_dict['form'] = ''
    #print(ctx_dict)
    set_context(window_id, ctx_dict)
    return ctx_dict


#A ver mais tarde uma melhor soluçao (isto foi feito devido a alguns problemas no redirecionamento do nginx com o protal das compras publicas)
@route('/base')
@view('base')
#@require_auth
def main():
    """Funçao index"""
    #print('Init do main_route')
    window_id = str(get_window_id())
    #print(window_id)
    set_base_context(window_id)
    #print('oi')
    ctx_dict = get_context(window_id)
    #print(ctx_dict)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'index'
    ctx_dict['title'] = 'ERP +'
    ctx_dict['form'] = ''
    #print(ctx_dict)
    set_context(window_id, ctx_dict)
    return ctx_dict

# @route('/ws')
# def websocket():
#     print('im in ws')
#     env = request.environ
#     uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
#     while True:
#         msg = uwsgi.websocket_recv()
#         uwsgi.websocket_send(msg)


@route('/ws')
def websocket():
    #print('im in ws')
    env = request.environ
    uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    channel = r.pubsub()
    channel.subscribe('teste_ws')
    websocket_fd = uwsgi.connection_fd()
    redis_fd = channel.connection._sock.fileno()
    while True:
        #print("here in the loop")
        # wait max 4 seconds to allow ping to be sent
        ready = gevent.select.select([websocket_fd, redis_fd], [], [], 4.0)
        # send ping on timeout
        if not ready[0]:
            uwsgi.websocket_recv_nb()
        for fd in ready[0]:
            if fd == websocket_fd:
                msg = uwsgi.websocket_recv_nb()
                if msg:
                    r.publish('teste_ws', msg)
            elif fd == redis_fd:
                msg = channel.parse_response()
                # only interested in user messages
                if msg[0] == b'message':
                    uwsgi.websocket_send(msg[2])



@route('/webservice/<variavel>')
@view('simple')
#@require_auth
def webservice(variavel):
    """Funçao teste de webservice"""
    #print('Init do teste_webservice')
    return variavel


# def initialize_model():
#   ##print('got in initialize_model')
#   global workspace
#   global model
#   #print('before {var1} {var2}'.format(var1=str(workspace), var2=str(model)))
#   model = cubes.load_model(MODEL_PATH)
#   #print('model')
#   workspace = cubes.create_workspace("sql", model, url=DB_URL, fact_prefix="ft_")
#   #print('after {var1} {var2}'.format(var1=str(workspace), var2=str(model)))

# def get_browser():
#   ##print('oi in get_browser')
#   return workspace.browser(model.cube(CUBE_NAME))

# @route('/bi')
# @view('bi')
# def bi():
#   ##print('Inicio')
#   dim_name = 'item' # no original vem do url
#   initialize_model()
#   ##print('modelo iniciado')
#   global model
#   browser = get_browser()
#   ##print('browser iniciado')
#   # First we need to get the hierarchy to know the order of levels. Cubes
#   # supports multiple hierarchies internally.
#   dimension = model.dimension(dim_name)
#   hierarchy = dimension.hierarchy()
#   # Parse the`cut` request parameter and convert it to a list of
#   # actual cube cuts. Think of this as of multi-dimensional path, even that
#   # for this simple example, we are goint to use only one dimension for
#   # browsing.
#   cutstr = request.forms.get('cut')
#   #print('my cutstr e: {var1}'.format(var1=str(cutstr)))
#   cell = cubes.Cell(browser.cube, cubes.cuts_from_string(cutstr))
#   # Get the cut of actually browsed dimension, so we know "where we are" -
#   # the current dimension path
#   cut = cell.cut_for_dimension(dimension)
#   if cut:
#       path = cut.path
#   else:
#       path = []
#   # Do the work, do the aggregation.
#   result = browser.aggregate(cell, drilldown=[dim_name])
#   # If we have no path, then there is no cut for the dimension, # therefore
#   # there is no corresponding detail.
#   if path:
#       details = browser.cell_details(cell, dimension)[0]
#   else:
#       details = []
#   # Find what level we are on and what is going to be the drill-down level
#   # in the hierarchy
#   levels = hierarchy.levels_for_path(path)
#   if levels:
#       next_level = hierarchy.next_level(levels[-1])
#   else:
#       next_level = hierarchy.next_level(None)
#   # Are we at the very detailed level?
#   is_last = hierarchy.is_last(next_level)
#   # Finally, we render it
#   context = get_base_context()
#   context['name'] = 'bi'
#   context['title'] = 'ERP + Business Inteligence'
#   context['dimensions'] = model.dimensions
#   context['dimension'] = dimension
#   context['levels'] = levels
#   context['next_level'] = next_level
#   context['result'] = result
#   context['cell'] = cell
#   context['is_last'] = is_last
#   context['details'] = details

#   code = """
#       oi
#   """
#   context['form'] = code
#   return context


# @route('/upload', method='POST')
# def do_upload():
#     """
#     Este é o upload utilizado no WYSIWYG
#     """
#     user = request.session['user']
#     user_name = request.session['user_name']
#     data = request.files.upload
#     message = ''
#     url = ''
#     #print(request.query.keys())
#     #POST /upload?CKEditor=descricao&CKEditorFuncNum=1&langCode=pt
#     #dict_keys(['langCode', 'CKEditorFuncNum', 'CKEditor'])
#     funcNum = request.query.get('CKEditorFuncNum')
#     #Optional: instance name (might be used to load a specific configuration file or anything else).
#     CKEditor = request.query.get('CKEditor')
#     #Optional: might be used to provide localized messages.
#     langCode = request.query.get('langCode')

#     dir_path= request.forms.get('dir_path')
#     dir_name= request.forms.get('dir_name')
#     #print(dir_path, dir_name)
#     #name, ext = os.path.splitext(data.filename)
#     if dir_path == 'userfiles':
#         if dir_name == 'Pasta Pessoal':
#             save_path = "/var/www/core/static/userfiles/{user}".format(user=user)
#         else:
#             save_path = "/var/www/core/static/userfiles/{user}/{dir_name}".format(dir_name=dir_name, user=user)
#     else:
#         save_path = "/var/www/core/static/publicfiles/{dir_name}".format(dir_name=dir_name)

#     if not path.exists(save_path):
#         makedirs(save_path)

#     if data and data.file:
#         #raw = data.file.read() # This is dangerous for big files
#         filename = save_path + '/' + data.filename
#         with open(filename, 'wb') as open_file:
#             open_file.write(data.file.read())
#         url = save_path[13:] + '/' + data.filename
#         #print(url)
#         new_anexo = add_anexo(anexo_file=data.filename, user_name=user_name)
#     else:
#         message = 'Erro a carregar o ficheiro!'

#     return "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction({funcNum}, '{url}', '{message}');</script>".format(message=message, url=url, funcNum=funcNum)


@post('/mkdir')
def mkdir():
    """Cria novas directorias nas páginas de utilizador e projeto da área de anexos"""
    #print('estou em mkdir')
    new_dir = request.forms.get('new_dir')
    user = str(request.session['user'])
    path_newdir = "/var/www/core/static/files/Users/{user}/{new_dir}".format(user=user, new_dir=new_dir)
    #print(new_dir)
    if not os.path.exists(path_newdir):
        os.makedirs(path_newdir)


@post('/chdir/<new_path>')
def chdir(new_path=None):
    """Muda de  directoria nas páginas de utilizador e projeto da área de anexos"""
    #print('Im in chdir')
    funcNum = request.forms.get('funcNum')
    obj = request.forms.get('obj')
    obj_key = request.forms.get('obj_key')
    button_name = request.forms.get('button_name')
    window_id = request.forms.get('main_window_id')
    #print('obj', obj)
    #print('obj_key', obj_key)
    #print('window_id', window_id)
    wysiwyg = request.forms.get('wysiwyg')
    user = str(request.session['user'])
    #print('end of it')
    return browse(wysiwyg=wysiwyg, obj=obj, obj_key=obj_key, button_name=button_name, message='', path=new_path)


#@get('/browse/<window_id>/<obj>/<obj_key>/<button_name>/<wysiwyg>')
#@view('browser')
#def browse(wysiwyg=False, window_id=None, obj=None, obj_key=None, button_name=None, message='', path=''):

@post('/browse/<obj>/<obj_key>/<button_name>/<wysiwyg>')
#@view('browser')
def browse(wysiwyg=False, obj=None, obj_key=None, button_name=None, message='', path=''):
    print('in browse')
    #print(obj, obj_key)
    #print('button_name', button_name)
    forms = '/var/www/core/forms/'
    user = request.session['user']
    user_name = request.session['user_name']
    result_dict= {}
    funcNum = 1#request.query.get('CKEditorFuncNum')
    #print(window_id)
    #ctx_dict = get_context(window_id)
    if path == '':
        #print('sem path', path)
        save_path = '/var/www/core/static/files/Users/' + str(user)
        path = 'Users/' + str(user)
    else:
        #print('com path', path, type(path))
        path = path.replace('+', '/')
        save_path = '/var/www/core/static/files/' + path
    #print ('save_path', save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        #print('created')
    #print(save_path)
    dirs = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(save_path):
        dirs.append(dirnames)
        files.append(filenames)
    #print ({'dirs': dirs, 'files': files, 'user': user, 'funcNum': funcNum, 'wysiwyg':wysiwyg, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'window_id':window_id, 'button_name':button_name})
    #return {'dirs': dirs, 'files': files, 'user': user, 'funcNum': funcNum, 'wysiwyg':wysiwyg, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'window_id':window_id, 'button_name':button_name}
    result_dict={'dirs':dirs, 'files':files, 'wysiwyg': False, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'button_name':button_name, 'user': user, 'funcNum': funcNum}
    #print('result_dict', result_dict)
    return SimpleTemplate(name = forms + 'browser').render(result_dict)
    #return {'dirs': dirs, 'files': files, 'user': user, 'funcNum': funcNum, 'wysiwyg':wysiwyg, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'button_name':button_name}# 'window_id':window_id,


@route('/upload/<wysiwyg>', method='POST')
def upload(wysiwyg=False):
    """
    Este é o upload utilizado no browser
    """
    #print('Im in upload anexo')
    user = str(request.session['user'])
    user_name = request.session['user_name']
    obj = request.forms.get('obj')
    obj_key = request.forms.get('obj_key')
    button_name = request.forms.get('button_name')
    #print('obj', obj)
    #print('obj_key', obj_key)
    #print(1)
    data = request.files.get('upload')
    #print(2, data)
    path = request.forms.get('path')
    #print(path)
    #name, ext = os.path.splitext(data.filename)
    save_path = "/var/www/core/static/files/{path}".format(path=path)
    #print(3, save_path)
    #if not os.path.exists(save_path):
     #   os.makedirs(save_path)
    #print(4, type(data), dir(data))
    if data:
        filename = save_path + '/' + data.filename
        #print(5, filename)
        with open(filename, 'wb') as open_file:
            open_file.write(data.file.read())
        new_anexo = add_anexo(anexo_file=data.filename, user=user)
        #print(6, new_anexo)
        return browse(wysiwyg=wysiwyg, obj=obj, obj_key=obj_key, button_name=button_name, message=['success', 'ficheiro carregado com sucesso!'], path=path)#'<a href="/static/userfiles/' + user_name + '/' + data.filename + '">' + data.filename + '</a>\n'
    else:
        #print('no data')
        return browse(wysiwyg=wysiwyg, obj=obj, obj_key=obj_key, button_name=button_name, message=['alert', 'Erro ao carregar o ficheiro!'], path=path)


def add_anexo(anexo_file, user):
    """Este add_anexo refere-se a adicionar um anexo novo a função link_anexo é a que permite adicionar um anexo a uma tarefa ou projeto ou seja que objecto for"""
    #print('im in add_anexo')
    anexo = {}
    anexo_path = "/static/files/Users/{user}".format(user=str(user))
    anexo['id'] = str(uuid.uuid4())
    anexo['path'] = anexo_path
    anexo['nome'] = anexo_file
    #anexo_node, = db.create(anexo)
    #anexo_node.add_labels('Anexo')
    return anexo['id']


@get('/show_help/<obj>')
def show_help(obj):
    """Abre os ficheiro de ajuda da pasta help"""
    code = 'Sem Ficheiro de ajuda!'
    filename = '/var/www/core/help/' + obj + '.html'
    try:
        with open(filename, 'r') as open_file:
            code = open_file.read()
    except:
        pass
    return code


@route('/about')
@view('base')
def about():
    """Devolve a pagina about"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'about'
    ctx_dict['title'] = 'Sobre'
    code = """
        <div class="small-12 large-12 columns">
        <textarea rows="30" readonly>
    """
    code += """
    Sobre o ERP+

    Versão 1.0 de 2015

    O ERP + é uma plataforma de Gestão sobre a qual qualquer pessoa pode desenvolver
    objectos que suportem o seu negócio ou actividade.

    Bom trabalho

    Contactos:

    Dario Costa
    +238 983 04 90
    dariocostadaluz@gmail.com

    Eurides Costa
    +238 977 61 54 /993 60 49
    ecostadaluz@gmail.com

    """
    code += """
        </textarea>
        </div>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@route('/help')
@view('base')
def help():
    """Devolve a pagina de Ajuda"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'help'
    ctx_dict['title'] = 'Ajuda'


    code = """
        <textarea rows="30" class="small-12 large-12 columns">
    """
    code += """
    Ajuda

    Por Implementar...

    """
    code += """
        </textarea>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@route('/update')
@view('base')
def update():
    """Devolve a pagina de Actualizaçao da Implementacao Local"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'update'
    ctx_dict['title'] = 'Actualização'
    ctx_dict['hide_footer'] = 'teste hide'

    code = """
        <textarea rows="30" class="small-12 large-12 columns">
    """
    code += """
    Actualização

    Por Implementar...

    """
    code += """
        </textarea>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@route('/licence')
@view('base')
def licence():
    """Devolve a pagina da Licença"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'licence'
    ctx_dict['title'] = 'Licença'

    licence_file = open('/var/www/core/help/licence.txt', 'r', encoding='utf8')
    code = """
        <textarea rows="30" class="small-12 large-12 columns">
    """
    code += licence_file.read()
    code += """
        </textarea>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@get('/static/<filepath:path>')
def server_static(filepath):
    """Defina a Root para os ficheiros estaticos"""
    return static_file(filepath, root='/var/www/core/static')


@get('/login')
@view('login')
def login_form():
    """Implementa o Ecra de Login"""
    window_id = str(get_window_id())
    import erp_config as ec
    return dict(name='login', title='Autenticação do ERP+', url='url', favicon=ec.favicon, system_logo=ec.system_logo, logotipo=ec.logotipo, enterprise=ec.enterprise, form='', window_id=window_id)


@post('/login')
@view('login')
def login_submit():
    """Valida o Login"""
    #print('Im on login submit')
    window_id = request.forms.get('window_id')

    #este código elimina os dicionarios json que vão sendo criados para guardara informação contextual
    now = time.time()
    path = '/var/www/tmp/'
    for f in os.listdir(path):
        if os.stat(os.path.join(path,f)).st_mtime < now - 86400:
            os.remove(os.path.join(path, f))

    import base64
    #aqui ver se não seria melhor utilizar bcript por questões de segurança da password
    from users import Users
    user = request.forms.get('login')
    password = request.forms.get('password')
    #print('before db request')
    db_user = Users(where="login = '{user}'".format(user=user)).get()
    autenticated = False
    #print('1', user, db_user)
    if db_user:
        db_user = db_user[0]
        #print('password', base64.decodestring(db_user['password'].encode('utf-8')).decode('utf-8'))
        if base64.decodestring(db_user['password'].encode('utf-8')).decode('utf-8')[6:] == password:
            print('o utilizador {user} autenticou-se com sucesso!'.format(user=db_user['nome']))
            request.session['user'] = db_user['id']
            request.session['user_name'] = db_user['nome']
            request.session.save()
            autenticated = True
    #print('2')
    if not autenticated:
        return HTTPResponse(status=500, output='Autenticação Inválida!!!')
    else:
        #print('estou autenticado')
        if window_id:
            #print('tenho window_id')
            ctx_dict = get_context(window_id)
            if 'redirect_url' in ctx_dict:
                #print('tenho redirect'+str(ctx_dict['redirect_url']))
                return ctx_dict['redirect_url']
            else:
                return '/base'
        else:
            #print('nao tenho window_id')
            return '/base'
    #print('end')


@post('/change_pass')
@view('login')
def change_pass_submit():
    """Valida a mudança de Password"""
    #print('im in change_pass')
    import base64
    from users import Users
    user = request.forms.get('login')
    password = request.forms.get('password')
    new_password = request.forms.get('new_password')
    confirm_password = request.forms.get('confirm_password')
    #print('before db request')
    db_user = Users(where = "login='{user}'".format(user=user)).get()
    autenticated = False
    if db_user:
        db_user = db_user[0]
        if base64.decodestring(db_user['password'].encode('utf-8')).decode('utf-8')[6:] == password:
            if request.forms.get('new_password') != request.forms.get('confirm_password'):
                return HTTPResponse(status=500, output='A nova password e a password de confirmação tem que ser iguais!!!')
            if len(request.forms.get('new_password')) > 3:
                import base64
                pass_string = 'noops!' + request.forms.get('new_password')
                db_user['password'] = base64.encodestring(pass_string.encode('utf-8')).decode('utf-8')
                db_user['user'] = db_user['id']
                Users(**db_user).put()
            else:
                return HTTPResponse(status=500, output='A nova password deve ter mais de 3 caracteres!!!')
            print('o utilizador {user} mudou a password com sucesso!'.format(user=db_user['nome']))
            request.session['user'] = db_user['id']
            request.session['user_name'] = db_user['nome']
            request.session.save()
            autenticated = True
    #print('end')
    if not autenticated:
        return HTTPResponse(status=500, output='Autenticação Inválida!!!')
    else:
        return 'Password modificada com sucesso!'


@route('/logout')
def logout():
    """Implementa o Logout"""
    for key in request.session:
        del request.session[key]
    redirect('/login')


@post('/calc')
def calc():
    """Implementa a funçao da calculadora"""
    #print('{var1}'.format(var1=str(request.forms.get('calc'))))
    try:
        value = eval(request.forms.get('calc'))
    except:
        value = 'Error'
    return str(value)


@post('/chamar')
@view('base')
def gap_chamar():
    user_estado = request.forms.get('user_estado')
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    res = GAPSequencia().chamar_senha(user_estado=user_estado, loja=ec.terminal_name)
    #Se for igual a none retorna uma mensagem de erro
    if res == None:
        #E necessario ver ainda o porque do javascript nao estar a captar o output de erro
        return HTTPResponse(status=500, output='Actualmente nao temos nenhuma senha em espera')
    #Se nao for none retorna o numero da senha solicitada
    else:
        return str(res)

@post('/chamar_por_senha/<senha>')
@view('base')
def gap_chamar_por_senha(senha):
    user_estado = request.forms.get('user_estado')
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    res = GAPSequencia().chamar_por_senha(senha=senha,user_estado=user_estado, loja=ec.terminal_name)
    #Se for igual a none retorna uma mensagem de erro
    if res == None:
        #E necessario ver ainda o porque do javascript nao estar a captar a mensagem de erro
        return HTTPResponse(status=500, output='Senha Invalida')
    #Se nao for none retorna o numero da senha solicitada
    else:
        return str(res)

@post('/chamar_senhaEspera/<senha>')
@view('base')
def gap_chamar_senhaEspera(senha):
    user_estado = request.forms.get('user_estado')
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    res = GAPSequencia().chamar_senhaEspera(senha_id=senha,user_estado=user_estado, loja=ec.terminal_name)
    #Se for igual a none retorna uma mensagem de erro
    if res == None:
        #E necessario ver ainda o porque do javascript nao estar a captar a mensagem de erro
        return HTTPResponse(status=500, output='Senha Invalida')
    #Se nao for none retorna o numero da senha solicitada
    else:
        return str(res)


@post('/transferir/<senha>/<keyservico>/<servico>')
@view('base')
def gap_transferir(senha,keyservico,servico):
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    return str(GAPSequencia().transferir_senha(senha=senha, keyservico=keyservico, newservico=servico, loja=ec.terminal_name))

@post('/terminar/<senha>/<tempo_atendimento>')
@view('base')
def gap_terminar(senha, tempo_atendimento):
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    return str(GAPSequencia().terminar_senha(senha=senha,tempo_atendimento=tempo_atendimento, loja=ec.terminal_name))

@post('/esperar/<senha>/<tempo_atendimento>/<comentario>')
@view('base')
def gap_esperar(senha, tempo_atendimento,comentario):
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    return str(GAPSequencia().espera_atendedor(senha=senha,tempo_atendimento=tempo_atendimento,comentario=comentario, loja=ec.terminal_name))

@post('/desistir/<senha>/<tempo_atendimento>')
@view('base')
def gap_desistir(senha, tempo_atendimento):
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    return str(GAPSequencia().desistir_senha(senha=senha,tempo_atendimento=tempo_atendimento, loja=ec.terminal_name))

@post('/fazer_intervalo')
@view('base')
def gap_intervalo():
    from my_users import Users
    return str(Users().Intervalo())

@post('/terminar_atendimento')
@view('base')
def gap_terminar_atendimento():
    from my_users import Users
    return str(Users().Terminado())

@post('/saveTime/<senha>/<tempo_atendimento>')
@view('base')
def  guardarTempo(senha, tempo_atendimento):
    from gap_sequencia import GAPSequencia
    import erp_config as ec #Para sabermos em que loja estamos no momento
    return str(GAPSequencia().saveTime(senha_id=senha, tempo_atendimento=tempo_atendimento, loja=ec.terminal_name))


#Faz o get do serviço actualmente em atendimento retornando os respectivos manuais, legislaçoes entre outros
@post('/servico_em_atendimento')
@view('base')
def  get_servico_em_atendimento():
    from gap_timeAtendimento import  GAPTimeAtendimento
    from gap_documento import GAPDocumento
    from gap_servico import GAPServico
    import erp_config as ec #Para sabermos em que loja estamos no momento
    servico_em_Atendimento = GAPTimeAtendimento().getServicoAtendimento(loja=ec.terminal_name)
    result = GAPServico().get_servico_Subid(nome=servico_em_Atendimento)
    result = str(result).split(";")
    servico = result[0]
    subservico = result[1]
    legislacao = None
    manual = None
    outros = None
    if (subservico!='None'):
        legislacao = GAPDocumento().get_legislacao(servicoId=servico,ascendenteId=subservico)
        manual = GAPDocumento().get_manual(servicoId=servico,ascendenteId=subservico)
        outros =  GAPDocumento().get_outros(servicoId=servico,ascendenteId=subservico)
    else:
        legislacao = GAPDocumento().get_legislacao(servicoId=servico)
        manual = GAPDocumento().get_manual(servicoId=servico)
        outros =  GAPDocumento().get_outros(servicoId=servico)
    legislacao = ''.join(legislacao)
    manual = ''.join(manual)
    outros = ''.join(outros)
    alldocs = legislacao+"#"+manual+"#"+outros
    return str(alldocs)


#Faz o reset dos numeros de senha numa loja xpto
@post('/resetTicket')
@view('base')
def  resetTicket():
    from gap_sequencia import GAPSequencia
    from gap_timeAtendimento import GAPTimeAtendimento
    from gap_senha import GAPSenha
    import erp_config as ec
    GAPSequencia().reset_numero(loja=ec.terminal_name)
    #faz o controlo do atendimento caso o atendedor nao tenha completado o atendimento anterior corretamente logo e mudado para desistido
    GAPTimeAtendimento().checkTimeAtendimento(loja=ec.terminal_name)
    #faz o controlo do atendimento caso o atendedor nao tenha completado atendimento em dia/ dias anteriores logo e alterado para desistir
    GAPSenha().descartar_senha(loja=ec.terminal_name)
    return 'Done'

#ecran de Espera TV
@route('/tv')
@view('ecranEspera')
def get_ecranEspera():
    window_id = str(get_window_id())
    from gap_multimedia import GAPMultimedia
    from gap_servico import GAPServico
    import erp_config as ec
    #Descarta a lista multimedia cuja a data final encontra-se ultrapassada na loja especifica
    GAPMultimedia().descartar_multimedia(loja=ec.terminal_name)
    #faz o get do playlist da loja xpto
    playlist = GAPMultimedia().get_playlist_loja(loja=ec.terminal_name)
    playlistsize = len(playlist) #para ajudar no controlo do playlist
    playlist = ''.join(playlist)
    return dict(title='Ecran Espera', favicon=ec.favicon, window_id=window_id,playlist=playlist, playlistsize=playlistsize)


#addicionar nova opiniao
@post('/sendOpiniao/<nome>/<comentario>/<contacto>')
def addOpiniao(nome,comentario,contacto):
    try:
        import base64
        from users import Users
        #nao estou a utilizar o request.forms get em alguns casos devido a problemas com o encoding...
        #user = request.forms.get('user')
        #nome = request.forms.get('name')
        #contacto = request.forms.get('contact')
        comentario = str(comentario).replace("+", " ")
        if(nome == 'null'):
             nome = ""
        if(comentario == 'null'):
             comentario = ""
        if(contacto == 'null'):
             contacto = ""

        classificacao = request.forms.get('classify')
        atendedor = request.forms.get('atendedor')
        db_user = Users(where = "login='{user}'".format(user=atendedor)).get()
        if db_user:
            from gap_opiniao import GAPOpiniao
            db_user = db_user[0]
            import erp_config as ec
            res = GAPOpiniao().addOpiniao(user=db_user['id'],nome=nome,contacto=contacto,comentario=comentario,classificacao=classificacao, loja=ec.terminal_name, nome_atendedor=atendedor)
            if(res == True):
                return dict(reponse='ok')
            else:
                return dict(reponse='error')
    except:
        return dict(reponse='error')


#get o ecran do quiosque
@route('/quiosque')
@view('ecranQuiosque')
def get_ecranSenha():
    window_id = str(get_window_id())
    import erp_config as ec
    from gap_servico import GAPServico
    servicos = GAPServico().get_servico()
    return dict(title='Ecran Quiosque', favicon=ec.favicon, logotipo=ec.logotipo, servicos=servicos, window_id=window_id)


#imprimir senha
@post('/printSenha/<servico>/<letra>')
def  imprimirSenha(servico,letra):
    try:
        import base64
        from users import Users
        db_user = Users(where = "login='{user}'".format(user='admin')).get()
        if db_user:
             db_user = db_user[0]
             #window_id = str(get_window_id())
             from gap_senha import  GAPSenha
             import erp_config as ec
             res = GAPSenha().get_SenhaCliente(user=db_user['id'], servico=servico, letra=letra, loja=ec.terminal_name)
             return res
    except:
        return None


#faz o get voz da tv fururamente por melhorar
@post('/getvoicetv/<senha_content>/<numero_balcao>')
def  get_voicetv(senha_content,numero_balcao):
    from gap_multimedia import  GAPMultimedia
    import erp_config as ec
    #sound tv path
    path = "/var/www/core/static/audio"
    warning=GAPMultimedia().find(name='aviso.wav', path=path)
    servico=GAPMultimedia().find(name='serviço.wav', path=path)
    senha=GAPMultimedia().find(name='senha.wav', path=path)
    balcao=GAPMultimedia().find(name='balcão.wav', path=path)
    numero_senha=senha_content[1:]
    letra_senha=senha_content[:1]
    letra_senha=GAPMultimedia().find(name=str(letra_senha).lower()+'.wav', path=path)
    numero_senha=GAPMultimedia().find(name=str(numero_senha)+'.wav', path=path)
    numero_balcao=GAPMultimedia().find(name=str(numero_balcao)+'.wav', path=path)
    #Por enquanto estamos a seguir a seguinte sequencia (futuramente aprimorar de forma a tornar isso dinamico)
    return str(warning)+";"+str(servico)+";"+str(letra_senha)+";"+str(senha)+";"+str(numero_senha)+";"+str(balcao)+";"+str(numero_balcao)



#Compras Publicas ainda essas funçoes precisam de toque

@route('/cms')
@view('cms')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    print('1')
    #set_base_context(window_id)
    print('2')
    #ctx_dict = get_context(window_id)
    #ctx_dict = {'titulo':'Portal de Compras Públicas'}
    #ctx_dict['window_id'] = window_id
    ctx_dict = {}
    ctx_dict['name'] = 'index'
    ctx_dict['title'] = 'Portal de Compras Públicas'
    from cp_banner import Banner
    resImgBanner = Banner().get_imgBanner()
    ctx_dict['dadosImgBanner'] = resImgBanner
    from cp_planoaquisanual import Planoaquisanual
    res = Planoaquisanual().get_Planoaquisanual()
    ctx_dict['dadosPlanoAA'] = res
    respaaa = Planoaquisanual().get_PlanoaquisanualAgrup()
    ctx_dict['dadosPlanoAAAgru'] = respaaa

    from cp_procedimento import Procedimento
    resconcAbert = Procedimento().getConcursoAberto()
    ctx_dict['dadosconcursAbert'] = resconcAbert
    ctx_dict['pagecountAberto'] = Procedimento().get_pagecountAberto()

    resconcEmAndament = Procedimento().getConcursoEmAndamento()
    ctx_dict['dadosconcursEmAndament'] = resconcEmAndament
    ctx_dict['pagecountEmAndament'] = Procedimento().get_pagecountEmAndament()

    resconcConcluid = Procedimento().getConcursoConcluido()
    ctx_dict['dadosconcursConcluid'] = resconcConcluid
    ctx_dict['pagecountConcluido'] = Procedimento().get_pagecountConcluido()

    print("erro -------->>>> Aqui  ")
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    print('fim do main_route')
    return ctx_dict

@route('/View_concursos/<viewid>')
@view('concursosview')
#@require_auth
def main(viewid):
    """Funçao index"""
    print('Init do main_route')
    print('->>>>>>>>>>>>>>>>>>'+viewid)
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_procedimento import Procedimento
    resconcursView = Procedimento().getConcursoView(viewid)
    ctx_dict['dadosconcursView'] = resconcursView
    from cp_esclarecimento import Esclarecimento
    respEsclare = Esclarecimento().getProcedEsclare(viewid)
    ctx_dict['dadosrespEsclare'] = respEsclare
    from cp_documentoprocedimento import Documentoprocedimento
    respDocProced = Documentoprocedimento().getProcedDoc(viewid)
    ctx_dict['dadosrespDocProced'] = respDocProced
    from cp_financiadorprocedimento import Financiadorprocedimento
    respFinaciadProced = Financiadorprocedimento().getFinaciadProced(viewid)
    ctx_dict['dadosrespFinaciadProced'] = respFinaciadProced
    from cp_observacaoprocedimento import Observacaoprocedimento
    respObservaProced = Observacaoprocedimento().getObservaProced(viewid)
    ctx_dict['dadosrespObservaProced'] = respObservaProced
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    print('fim do main_route')
    return ctx_dict

@route('/Concursos')
@view('concursos')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict


@route('/view_new')
@view('newview')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Contratos')
@view('contratos')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_contrato import Contrato
    respContrato = Contrato().getContrato()
    ctx_dict['dadosrespContrato'] = respContrato
    ctx_dict['pagecount'] = Contrato().get_pagecount()
    print(ctx_dict['dadosrespContrato'])
    print(ctx_dict['pagecount'])
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Entidade_publica')
@view('entidade_publica')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_adjudicante import Adjudicante
    resQueryEntidadeAdjucante = Adjudicante().getEntidadeAdjucante()
    ctx_dict['dadosEntidadeAdjucante'] = resQueryEntidadeAdjucante
    ctx_dict['pagecount'] = Adjudicante().get_pagecount()
    print(ctx_dict['pagecount'])
    #from cp_adjudicante import Adjudicante
    #resadjud = Adjudicante().get_adjudicante()
    #ctx_dict['dadosadjudic'] = resadjud
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Faq')
@view('faq')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_faqs import Faqs
    respFaqs = Faqs().get_faqs()
    ctx_dict['dadosRespFaqs'] = respFaqs
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Legislacao')
@view('legislacao')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDocLeis = Documento().getDocLeis()
    ctx_dict['dadosDocLeis'] = resQueryDocLeis
    print(str(resQueryDocLeis))
    resQueryDocDecretos = Documento().getDocDecretos()
    ctx_dict['dadosDocDecretos'] = resQueryDocDecretos
    resQueryDocResolucoesPortarias = Documento().getDocResolucoesPortarias()
    ctx_dict['dadosDocResolucoesPortarias'] = resQueryDocResolucoesPortarias
    resQueryDocRegulamentos = Documento().getDocRegulamentos()
    ctx_dict['dadosDocRegulamentos'] = resQueryDocRegulamentos
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Directiva')
@view('directiva')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDirectiva = Documento().getDocDirectiva()
    ctx_dict['dadosDocDirectiva'] = resQueryDirectiva
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/DeclaracoesFornecedores')
@view('declaracoes_fornecedores')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDeclaracoesFornecedores = Documento().getDocDeclaracoesFornecedores()
    ctx_dict['dadosDeclaracoesFornecedores'] = resQueryDeclaracoesFornecedores
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/DocEstandarizados')
@view('doc_estandarizados')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDocEstandarizadosProgramas = Documento().getDocEstandarizadosProgramas()
    ctx_dict['dadosDocEstandarizadosProgramas'] = resQueryDocEstandarizadosProgramas
    resQueryDocEstandarizadosCadernos = Documento().getDocEstandarizadosCadernos()
    ctx_dict['dadosDocEstandarizadosCadernos'] = resQueryDocEstandarizadosCadernos
    resQueryDocEstandarizadosConvites = Documento().getDocEstandarizadosConvites()
    ctx_dict['dadosDocEstandarizadosConvites'] = resQueryDocEstandarizadosConvites
    resQueryDocEstandarizadosTermos = Documento().getDocEstandarizadosTermos()
    ctx_dict['dadosDocEstandarizadosTermos'] = resQueryDocEstandarizadosTermos
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Mapa_do_site')
@view('mapa_site')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDocResolucoesPortarias = Documento().getDocResolucoesPortarias()
    ctx_dict['dadosDocResolucoesPortarias'] = resQueryDocResolucoesPortarias
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

@route('/Manual')
@view('manual')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDocManual = Documento().getDocManual()
    ctx_dict['dadosDocManual'] = resQueryDocManual
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict

"""
@route('/Regulamentos')
@view('regulamento')
#@require_auth
def main():
    #Funçao index
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_documento import Documento
    resQueryDocRegulamentos = Documento().getDocRegulamentos()
    ctx_dict['dadosDocRegulamentos'] = resQueryDocRegulamentos
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    #print('fim do main_route')
    return ctx_dict
"""

@route('/Fornecedores')
@view('fornecedores')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    #print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Portal de Compras Públicas'}
    from cp_fornecedor import Fornecedor
    res = Fornecedor().get_fornecedor()
    ctx_dict['dados'] = res
    ctx_dict['pagecount'] = Fornecedor().get_pagecount()
    print(ctx_dict['pagecount'])
    #ctx_dict['window_id'] = window_id
    #ctx_dict['name'] = 'index'
    #ctx_dict['title'] = 'ERP +'
    #ctx_dict['form'] = ''
    #set_context(window_id, ctx_dict)
    print('fim do main_route')
    return ctx_dict

@get('/get_page/<page>/<pagelimit>')
def get_page(page, pagelimit):
    from cp_fornecedor import Fornecedor
    res = Fornecedor().get_html_page(page=page, pagelimit=pagelimit)
    return str(res)

@get('/get_pageEntidadePublica/<page>/<pagelimit>')
def get_page(page, pagelimit):
    from cp_adjudicante import Adjudicante
    res = Adjudicante().get_html_page(page=page, pagelimit=pagelimit)
    return str(res)

@get('/get_pageContrato/<page>/<pagelimit>')
def get_page(page, pagelimit):
    from cp_contrato import Contrato
    res = Contrato().get_html_page(page=page, pagelimit=pagelimit)
    return str(res)

@get('/get_pageProcedAbert/<page>/<pagelimit>')
def get_page(page, pagelimit):
    from cp_procedimento import Procedimento
    res = Procedimento().get_html_pageAbert(page=page, pagelimit=pagelimit)
    return str(res)

@get('/get_pageProcedEmAndament/<page>/<pagelimit>')
def get_page(page, pagelimit):
    from cp_procedimento import Procedimento
    res = Procedimento().get_html_pageEmAndament(page=page, pagelimit=pagelimit)
    return str(res)

@get('/get_pageProcedConcluido/<page>/<pagelimit>')
def get_page(page, pagelimit):
    from cp_procedimento import Procedimento
    res = Procedimento().get_html_pageConcluido(page=page, pagelimit=pagelimit)
    return str(res)

#addicionar novo FORNECEDOR
@post('/registFornecd')
def addFornecedor():
    try:
        import base64
        from users import Users

        nomeForn = request.forms.get('fornecName')
        nifForn = request.forms.get('fornecNif')
        tipoEmpForn = request.forms.get('tipo_empresa')
        paisForn = request.forms.get('pais_empresa')
        areaForn = request.forms.get('area_servico')
        localizacaoForn = request.forms.get('fornecLocalizacao')
        emailForn = request.forms.get('fornecEmail')
        senhaForn = request.forms.get('fornecSenha')
        obsForn = request.forms.get('fornecObs')

        db_user = Users(where = "login='{user}'".format(user='admin')).get()
        if db_user:
            from cp_fornecedor import Fornecedor
            db_user = db_user[0]
            import erp_config as ec
            res = Fornecedor().addFornecedor(user=db_user['id'], nomeForn=nomeForn, nifForn=nifForn, tipoEmpForn=tipoEmpForn, paisForn=paisForn, areaForn=areaForn, localizacaoForn=localizacaoForn,  emailForn=emailForn, senhaForn=senhaForn, obsForn=obsForn)

            if(res == True):
                return 'ok'
            else:
                return 'error'
    except:
        return 'error'

#addicionar novo FORNECEDOR
@get('/getdadosFornecd/<nifForn>')
def get_dad_contribuinte(nifForn):
    from cp_contribuinte import Contribuinte
    resContrib = Contribuinte().get_dad_contribuinte(nifForn=nifForn)
    return resContrib

#addicionar novo Esclarecimento
@get('/registEsclareciment/<nomeForn>/<nifForn>/<contatolForn>/<assuntEsclrt>/<textEsclrt>/<estadoEsclrt>/<refProcedt>')
def addEsclarecimento(nomeForn, nifForn, contatolForn, assuntEsclrt, textEsclrt, estadoEsclrt, refProcedt):
    try:
        import base64
        from users import Users
        """
        nomeForn = request.forms.get('nomeFornec')
        nifForn = request.forms.get('nifFornec')
        contatolForn = request.forms.get('contatFornec')
        assuntEsclrt = request.forms.get('esclrassunto')
        textEsclrt = request.forms.get('esclrtest')
        estadoEsclrt = request.forms.get('esclrestado')
        refProcedt = request.forms.get('referencprocedimet')
        """
        db_user = Users(where = "login='{user}'".format(user='admin')).get()
        if db_user:

            from cp_esclarecimento import Esclarecimento
            db_user = db_user[0]
            import erp_config as ec
            res = Esclarecimento().addEsclarecimento(user=db_user['id'],nomeForn=nomeForn,nifForn=nifForn,contatolForn=contatolForn,assuntEsclrt=assuntEsclrt, textEsclrt=textEsclrt, estadoEsclrt=estadoEsclrt, refProcedt=refProcedt)

            if(res == True):
                return 'ok'
            else:
                return 'error'

    except:
        return 'error'

#addicionar novo Help
@post('/registoHelp')
def addHelp():
    try:
        import base64
        from users import Users
        emailHelp = request.forms.get('emailHelp')
        assuntEsclrt = request.forms.get('assuntoHelp')
        textEsclrt = request.forms.get('textHelp')
        tipoEsclrt = request.forms.get('tipohelp')
        estadoEsclrt = request.forms.get('estadoHelp')

        db_user = Users(where = "login='{user}'".format(user='admin')).get()
        if db_user:

            from cp_helpdesk import Helpdesk
            db_user = db_user[0]
            import erp_config as ec
            res = Helpdesk().addHelp(user=db_user['id'],emailHelp=emailHelp,assuntEsclrt=assuntEsclrt,textEsclrt=textEsclrt,tipoEsclrt=tipoEsclrt,estadoEsclrt=estadoEsclrt)

            if(res == True):
                return 'ok'
            else:
                return 'error'

    except:
        return 'error'

#addicionar novo Newsletter
@post('/registoNewsletter')
def addNewsletter():
    try:
        import base64
        from users import Users
        emailHelp = request.forms.get('emaiNewsl')
        estadoEsclrt = request.forms.get('estadoNewsl')

        db_user = Users(where = "login='{user}'".format(user='admin')).get()
        if db_user:

            from cp_newsletter import Newsletter
            db_user = db_user[0]
            import erp_config as ec
            res = Newsletter().addNewsletter(user=db_user['id'],emailHelp=emailHelp,estadoEsclrt=estadoEsclrt)

            if(res == True):
                return 'ok'
            else:
                return 'error'

    except:
        return 'error'

#Compras Publicas ainda essas funçoes precisam de toque

@route('/formcasatodos')
@view('formcasatodos')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    #window_id = str(get_window_id())
    print('1')
    #set_base_context(window_id)
    #print('2')
    #ctx_dict = get_context(window_id)
    ctx_dict = {'titulo':'Casa para todos'}
    #ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'index'
    ctx_dict['title'] = 'ERP +'
    from formulario import Formulario
    res = Formulario().get_formulario()
    ctx_dict['dadosformulario'] = res
    #ctx_dict['pagecount'] = Formulario().get_pagecount()
    #print("inserção>>>>>>>>>>")
    #set_context(window_id, ctx_dict)
    print('fim do main_route')
    return ctx_dict


#função que permite cadastro funcionario

@post('/cadastrofunc')
def addForm():

    try:
        import base64
        from users import Users
        nomefun = request.forms.get('nomecompleto')
        emailfun = request.forms.get('email')

        db_user = Users(where = "login='{user}'".format(user='admin')).get()
        if db_user:

            from formulario import Formulario
            db_user = db_user[0]
            import erp_config as ec
            res = Formulario().addForm(user=db_user['id'], nomefun=nomefun, emailfun=emailfun)

            if(res == True):
                return 'Ok'
            else:
                return 'error'

    except:
        return 'Error'

""" esta funcao retorna context com o header o footer e o banner lateral do upppp,
 permitindo assim as suas alteraçoes por um unico objecto, o upppp_layout """
def get_upppp_default_context(title=""):
    window_id = str(get_window_id())
    from upppp_layout import UPPPPLayout
    header = UPPPPLayout().get_html_header(title=title)
    footer = UPPPPLayout().get_html_footer()
    banner_lateral = UPPPPLayout().get_html_banner_lateral()
    return dict(banner_lateral=banner_lateral, footer=footer, header=header, window_id=window_id)

@route('/index_u4p')
@view('index_u4p')
#@require_auth
def get_index():
    ctx_dict = get_upppp_default_context(title='UPPPP Cabo Verde')
    from upppp_home import UPPPPHome
    ctx_dict['home_info'] = UPPPPHome().get_self()

    from upppp_slide_image import UPPPPSlideImage
    ctx_dict['slides'] = UPPPPSlideImage().get()

    from upppp_evento import UPPPPEvento
    ctx_dict['eventos'] = UPPPPEvento().get_all()    
    ctx_dict['pagecount'] = UPPPPEvento().get_pagecount() 

    from upppp_projeto import UPPPPProjeto
    ctx_dict['projetos'] = UPPPPProjeto().get(order_by="int8(posicao)")
    ctx_dict['pagecountProj'] = UPPPPProjeto().get_pagecount() 

    from upppp_artigo import UPPPPArtigo
    ctx_dict['artigos'] = UPPPPArtigo().get(order_by="int8(posicao)")
    ctx_dict['pagecountArt'] = UPPPPArtigo().get_pagecount()
    return ctx_dict

@route('/quem_somos_u4p')
@view('quem_somos_u4p')
#@require_auth
def get_quem_somos():
    ctx_dict = get_upppp_default_context(title='UPPPP CV - Quem Somos')
    ctx_dict['name'] = 'quem_somos'
    from upppp_identificacao import UPPPPIdentificacao
    ctx_dict['infos'] = UPPPPIdentificacao().get_info()
    from upppp_slide_image import UPPPPSlideImage
    ctx_dict['slides'] = UPPPPSlideImage().get() 
    from upppp_evento import UPPPPEvento
    ctx_dict['eventos'] = UPPPPEvento().get_all() 
    ctx_dict['pagecount'] = UPPPPEvento().get_pagecount()
    from upppp_projeto import UPPPPProjeto
    ctx_dict['projetos'] = UPPPPProjeto().get(order_by="int8(posicao)")
    ctx_dict['pagecountProj'] = UPPPPProjeto().get_pagecount()
    from upppp_artigo import UPPPPArtigo
    ctx_dict['artigos'] = UPPPPArtigo().get()     
    return ctx_dict

@route('/missao_u4p')
@view('missao_u4p')
#@require_auth
def get_missao():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Missão") 
    from upppp_identificacao import UPPPPIdentificacao
    ctx_dict['infos'] = UPPPPIdentificacao().get_info()

    from upppp_slide_image import UPPPPSlideImage
    ctx_dict['slides'] = UPPPPSlideImage().get() 
    from upppp_evento import UPPPPEvento
    ctx_dict['eventos'] = UPPPPEvento().get_all() 
    ctx_dict['pagecount'] = UPPPPEvento().get_pagecount()
    from upppp_projeto import UPPPPProjeto
    ctx_dict['projetos'] = UPPPPProjeto().get(order_by="int8(posicao)")
    ctx_dict['pagecountProj'] = UPPPPProjeto().get_pagecount()
    from upppp_artigo import UPPPPArtigo
    ctx_dict['artigos'] = UPPPPArtigo().get()     
    return ctx_dict

@route('/organica_u4p')
@view('organica_u4p')
#@require_auth
def get_organica():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Orgãnica")    
    return ctx_dict


@route('/estrategia_u4p')
@view('estrategia_u4p')
def get_estrategia():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Estratégia")    
    return ctx_dict

@route('/legislacao_u4p')
@view('legislacao_u4p')
def get_legislacao_ppp():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Legislação de Privatização")  
    from upppp_legislacao_ppp import UPPPPLegislacaoPPP
    ctx_dict['legislacao'] = UPPPPLegislacaoPPP().get_self()    
    return ctx_dict

@route('/legislacao_privatizacoes_u4p')
@view('legislacao_privatizacoes_u4p')
def get_legislacao_privatizacoes():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Legislação de Privatização")  
    from upppp_legislacao_privatizacoes import UPPPPLegislacaoPrivatizacoes
    ctx_dict['legislacao'] = UPPPPLegislacaoPrivatizacoes().get_self()    
    return ctx_dict

@route('/conceito_privatizacao_u4p')
@view('conceito_privatizacao_u4p')
def get_dossiers():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Conceito de Privatização")      
    return ctx_dict

@route('/conceito_u4p')
@view('conceito_u4p')
def get_dossiers():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Conceito de PPP")      
    return ctx_dict

@route('/conceito_concessao_u4p')
@view('conceito_concessao_u4p')
def get_dossiers():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Conceito de Concessão")      
    return ctx_dict

@route('/dossiers_u4p')
@view('dossiers_u4p')
def get_dossiers():    
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Dossiers") 
    from upppp_dossiers import UPPPPDossiers
    ctx_dict['dossiers'] = UPPPPDossiers().get_all()
    return ctx_dict

@route('/concursos_u4p')
@view('concursos_u4p')
def get_concursos_ppp():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Concursos")
    from upppp_concurso import UPPPPConcurso
    ctx_dict['concursos'] = UPPPPConcurso().get_all()    
    return ctx_dict

@route('/estudos_u4p')
@view('estudos_u4p')
def get_estudos_ppp():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Estudos")
    from upppp_estudo import UPPPPEstudo
    ctx_dict['estudos'] = UPPPPEstudo().get_all()    
    return ctx_dict

@route('/parcerias_u4p')
@view('parcerias_u4p')
def get_concursos_ppp():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - Parcerias")      
    return ctx_dict

@route('/faq_u4p')
@view('faqs_u4p')
def get_cfaq_ppp():
    ctx_dict = get_upppp_default_context(title="UPPPP CV - FAQ´s")
    from upppp_faqs import UPPPPFaqs
    ctx_dict['dados_faqs']=UPPPPFaqs().get()     
    return ctx_dict

@get('/get_pageUPPPPDossiers/<page>/<numForPage>')
def get_page_dossiers(page, numForPage):      
    from upppp_dossiers import UPPPPDossiers     
    return UPPPPDossiers().get_html_page(page=page, numForPage=numForPage)

@get('/get_pageUPPPPConcurso/<page>/<numForPage>')
def get_page_concurso(page, numForPage):      
    from upppp_concurso import UPPPPConcurso     
    return UPPPPConcurso().get_html_page(page=page, numForPage=numForPage)

@get('/get_pageUPPPPEstudo/<page>/<numForPage>')
def get_page_estudo(page, numForPage):      
    from upppp_estudo import UPPPPEstudo     
    return UPPPPEstudo().get_html_page(page=page, numForPage=numForPage)

@get('/get_pageUPPPPFaqs/<page>/<numForPage>')
def get_page_estudo(page, numForPage):      
    from upppp_faqs import UPPPPFaqs     
    return UPPPPFaqs().get_html_page(page=page, numForPage=numForPage)


@post('/registarPergunta/<pergunta>')
def addPergunta(pergunta):
    try:
        from upppp_faqs import UPPPPFaqs
        if (pergunta !='') & (UPPPPFaqs().savePergunta(pergunta=pergunta)):        
            return 'ok'       
        else:
            return 'error'
    except:
        return 'error'
