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
import psycopg2
import psycopg2.extras
import psycopg2.pool
import datetime
from contextlib import contextmanager
from auth import verify_orm_rights
import uuid
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from decimal import Decimal#depois apagar isto quando tirar daqui o to_decimal
import traceback
import ujson

cache_opts = {
    'cache.type': 'memory',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))
erp_cache = cache.get_cache('erp_cache', type='memory', expire=10)
short_cache = cache.get_cache('short_cache', type='memory', expire=10)


def get_context(window_id):
    #print('Im on get_context', window_id)
    with open('../tmp/{window_id}ctx.json'.format(window_id=window_id), mode='r' , encoding='utf-8') as json_file:
        json_string = json_file.read()
        #print (json_string)
        ctx_dict = ujson.loads(json_string)
    return ctx_dict


def set_context(window_id, ctx_dict):
    #print('Im on set_context', window_id)
    #print (ctx_dict)
    with open('../tmp/{window_id}ctx.json'.format(window_id=window_id), mode='w' , encoding='utf-8') as json_file:
        #print (json_file)
        json_file.write(ujson.dumps(ctx_dict))
        #print ('sta scrito!!')
    #print ('out of set_context')


def to_decimal(number):
    if number not in [None, 'None', '']:
        number = Decimal('{number}'.format(number=str(number)))
        number = number.quantize(Decimal('0.1'))
    else:
        number = Decimal('0')
    return number


def get_model_fields(model):
    """Devolve os atributos de um modelo que correspondem a 'fields'!!!"""
    ordered_fields_dict = {}
    for var in vars(model):
        if 'widgets' in str(vars(model)[var]):
            field = eval('model.' + var)
            #print('{var1}'.format(var1=str(field)))
            ordered_fields_dict[field.view_order] = (var, field)
    #print('{var1}'.format(var1=str(ordered_fields_dict.keys())))
    for key in ordered_fields_dict.keys():
        yield ordered_fields_dict[key]


def connect():
    import erp_config
    global db
    db = psycopg2.pool.SimpleConnectionPool(1,10,"dbname={dbname} user={dbuser} host={dbhost} password={dbpass} sslmode='disable'".format(dbname=erp_config.db_name, dbuser=erp_config.db_user, dbhost=erp_config.db_host, dbpass=erp_config.db_password))


@contextmanager
def getcursor():
    try:
        db
    except:
        connect()
    con = db.getconn()
    try:
        yield con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    finally:
        con.commit()
        db.putconn(con)

        
def closedb():
    db.closeall()


def syncModel(model):
    import utils
    table = model.__name__
    fields = utils.get_model_fields(model)
    model_fields = ''
    model_fields_list = [('active','boolean'), ('id','varchar(50)'), ('date_create','date'), ('user_create','date'), ('date_change','date'), ('user_change','date')]
    db_types = {'active':'boolean', 'id':'varchar(50)', 'date_create':'date', 'user_create':'date', 'date_change':'date', 'user_change':'date'}
    import objs
    constrains = []
    for f in fields:
        #aqui depois colocar um if f not in [lista com nomes reservados]
        #print('{var1}'.format(var1=f[0]))
        if f[1].__class__.__name__ not in ['list_field', 'many2many','link','separator','label','newline','hrline']:
            field = eval(f[1].__class__.__name__ + '()')
            db_types[f[0]] = field.dbtype
            if f[1].__class__.__name__ == 'parent_field':
                #print('objs.{model_name}().__name__'.format(model_name=f[1].model_name))
                parent = eval('objs.{model_name}().__name__'.format(model_name=f[1].model_name))
                constrain = field.constrains%{'name':f[0],'parent':parent,'table':table}
                constrain_name = 'fk_%(table)s_%(parent)s'%{'parent':parent,'table':table}
                constrains.append((constrain, constrain_name))#aqui on caso das combo tambem deveria ter constrain se for parent=true
            dbtype = field.dbtype
            if f[1].__class__.__name__ == 'combo_field':
                if f[1].parent:
                    dbtype = 'VARCHAR(50)'
            model_fields += f[0] + ' ' + dbtype + ','
            model_fields_list.append((f[0], dbtype))
        elif f[1].__class__.__name__ == 'many2many':
            table1 = table
            #print('table1 {var1}'.format(var1=table1))
            #print('objs.{model_name}().__name__'.format(model_name=f[1].model_name))
            table2 = eval('objs.{model_name}().__name__'.format(model_name=f[1].model_name))
            #print('table2 {var1}'.format(var1=table2))
            new_table = utils.get_many2many_name(table1, table2)
            #print('new_table {var1}'.format(var1=new_table))
            sql = 'CREATE TABLE IF NOT EXISTS {table}(id VARCHAR(50) PRIMARY KEY, {field1} VARCHAR(50), {field2} VARCHAR(50));'.format(table=new_table, field1=table1, field2=table2)#aqui tambem teremos que introduzir as foreign keys

            with getcursor() as cursor:
                cursor.execute(sql)

    #print('1')
    # depois deveremos utilizar herança para estes campos base e outros que eventualmente o justifiquem, teremos que ter tambem estrat´egia de partiç~ao de tabelas
    model_fields += 'id VARCHAR(50) PRIMARY KEY, user_create VARCHAR(50), date_create DATE, user_change VARCHAR(50), date_change DATE, active BOOLEAN'
    sql = """CREATE TABLE IF NOT EXISTS %(table)s(%(cols)s);"""%{'table':table, 'cols':model_fields}
    #print(sql)    

    with getcursor() as cursor:
        cursor.execute(sql)

    #vou utilizar para ir buscar os nomes das colunas
    sql = """SELECT * FROM {table}""".format(table=table)
    #print(sql)
    with getcursor() as cursor:
        cursor.execute(sql)
    col_name_list = [desc[0] for desc in cursor.description]
    #print('{var1} {var2}'.format(var1=str(col_name_list), var2=str(model_fields_list)))
    if col_name_list:
        for f in model_fields_list:
            field_name = f[0]
            #print('{var1}'.format(var1=field_name))
            if field_name not in col_name_list:
                #print('{var1} {var2}'.format(var1=table, var2=str(db_types[f[0]])))
                sql = """ALTER TABLE {table} ADD COLUMN {column} {field_type}""".format(table=table, column=field_name, field_type=db_types[f[0]])
                #print(sql)

                with getcursor() as cursor:
                    cursor.execute(sql)

                if f[1].__class__.__name__ == 'parent_field':
                    sql = """ALTER TABLE {table} ADD CONSTRAINT fk_{name}_{parent} FOREIGN KEY ({name}) REFERENCES {parent}(id) ON DELETE RESTRICT;""".format(table=table, parent=f[1].parent, name=f[0])
                    #print(sql)
                    with getcursor() as cursor:
                        cursor.execute(sql)

    #print('contrains {var1}'.format(var1=str(constrains)))
    for constrain in constrains:
        constrain_name = constrain[1]
        constrain = constrain[0]
        sql = """
        ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {constrain_name};
        ALTER TABLE {table} ADD CONSTRAINT {constrain};""".format(table=table, constrain=constrain, constrain_name=constrain_name)
        #print(sql)

        with getcursor() as cursor:
            cursor.execute(sql)

#aqui deveria depois por o codigo para executar o codigo sql do on_create do modelo, claro que tenho que ter a certeza que a tabela acabou de ser criada, podera ser utilizada para criar users, por exemplo e tipos de documento e outros do genero


class Model(object):

    def __init__(self, **kargs):
        #print('im in model do orm', str(self))
        #Define o tipo de formulário, pode ser 'inline', 'edit' ou 'popup' no futuro podera haver outros, se vem de um field as mesmas opçoes devem ficar no field
        self.__list_edit_mode__ = 'edit'  # do ponto de vista de flaxiblidade isto tem que ser repensado, corresponde a como numa lista editamos um registo a lista pode ser um field ou um form, e pode o mesmo modelo ser chamado num form como edit mas noutro como inline por isso a accao deveria estar na parameterizaçao do campo se for field e a do modelo so e utilizado se for form.
        #Sempre que for necessário correr um determinado sql após a criação da tabela
        self.__on_create_sql__ = ''
        #Define a ordem pela qual os registos são apresentados nas listas, podem ser varios campos separados por virgulas, e ter qualquer espress~ao usada em SQL ex: 'int8(tabela.coluna) DESC', sempre deve ter a tabela para evitar conflitos no SQL e pode usar qualquer tabela que esteja relacionada a montante (parent,combo, choice)
        self.__order_by__ = ''
        #Define o Workflow
        self.__workflow__ = ()
        #Gestão de Permissões para o workflow. Só aparecem os botões se o utilizador tiver autorização para efectuar a tarefa
        self.__workflow_auth__ = {}
        #Utilizado para inibir botões no workflow se determinada condição não for cumprida
        self.__workflow_context__ = {}
        #Utilizado para mostrar ou inibir a visualização de registos mediante determinada condição, Inibe todos os registos cujo campo (1º valor da lista), for igual a um dos valores do tuple ou em alternativa um dos valores do tuple devolvido pela função (2º valor da lista), desde que não tenham uma das funções (perfis) da lista(3º valor da lista) (auth) . o 4º valor da lista pode ser 'in' ou 'not in' dependendo se é para mostrar os registos com campo=valor do tuple ou o oposto
        self.__records_view__ = []
        #Permite organizar os campos em tabs sempre que o formulário for do tipo edit
        self.__tabs__ = []
        #Não permite editar quando um determinado campo tiver os valores da lista
        self.__no_edit__ = []
        #Esta opção permite definir o campo ou os campos que servirão para enviar para as combobox
        self.__get_options__ = []
        #Esta opção serve para definir que colunas deveremos considerar em caso de JOIN depois melhorar isto
        self.__join_columns__  = {}
        #Esta opção serve para colorir os registos conçoante o valor de um determinado campo ou campos
        self.__record_colors__ = []
        #[('estado',{'Novo':'Black', 'Enviado':'Red'})]
        self.__force_db__ = False
        #No caso de eu fazer algo a partir da lista utilizando o sidebar tenho que definir o __force_db__ para true para que vá buscar o record na Base de Dados e não no request, dado que se estou na lista e não no edit não terei os valores que necessito no request.
        self.__db_mode__ = 'Table'
        #pode ser 'Table', 'View' ou 'None' e serve para definir o comportamento em relação à base de dados, se for 'Table' tem o comportamento normal, se for 'View' tenho que definir o __on_create_sql__ com o query para criar a view e se for 'None' não influencia nada na base de dados e não aparecem os botões de gravar,etc pois será utilizado em wizards ou formulários para recolha de dados que serão utilizados para uma qualquer função tipo imprimir um relatório.

        #Gestão de Permissões
        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['All'],
            'full_access':['all']
        }#não necessita de pôr "Administrator" pois por defeito tem acesso total!!! podemos utilizar a keyword "All" que significa que todos tem aquele tipo de acesso! quem for colocado em full_access não necessita de ser colocado nas restantes categorias!

        self.__side_menu__ = []
        #define um menu lateral que facilita a navegação no objecto quando em modo lista, principalmente quando tem hierarquias
        self.__breadcrumbs_navigation__ = False
        #permite a navegação "migalhas de pão" ou seja uma barra superior que apresenta o caminho em que navegamos num objecto que tem hierarquia



        #   def estado_dyn_attrs(self, value):
        #       # permite devolver atributos dinamicos ou seja atributos html que mudam consoante por exemplo   valores de certos campos
        #       result = {}
        #       #if value == 'Rascunho':
        #       #   result = {'total':'hidden', 'data':'hidden'}
        #       #elif value in ['Confirmado','Facturado']:
        #       #   result = {'total':'disabled', 'data':'disabled'}
        #       return result
        #   def get_options(self, cliente=None):
        #       #no get_options se eu acrescentar argumentos além do habitual "self" tenho que os ter em conta, no caso dos many2many pode ser utilizado para definir field_filters que limitam o que pode ser acrescentado na lista,
        #       options = []
        #       opts = self.get()
        #       for f in self.__fields__:
        #           if f[0] == 'cliente':
        #               field=f
        #       for option in opts:
        #           if cliente:
        #               if str(option['cliente']) == str(cliente):
        #                   nome_cliente = get_field_value(record=option, field=field, model=self)  ['field_value'][1]
        #                   options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), cliente=nome_cliente,total=self.get_total(option['id']))))
        #           else:
        #               nome_cliente = get_field_value(record=option, field=field, model=self)['field_value']
        #               options.append((str(option['id']), '{numero}'.format(data=str(option['data']), numero=str(option['numero']), cliente=nome_cliente,total=self.get_total(option['id']))))
        #       return options
        self.kargs = kargs
        #print('os kargs no orm, modelo sao {var1}'.format(var1=self.kargs))

    def get_options(self):
        """a variavel __get_options__ diz-nos o que mandar para as combobox, esta função pode ser substituída claro, caso não queiramos mandar o id como valor, o que é por defeito, não esquecer que nesse caso poderemos ter que por o parent como false para que não crie o campo na base de dados como VARCHAR(50) mas sim como string"""
        def get_results():
            #print('estou no get_options em ORM {var1}'.format(var1=self.__name__))
            options = []
            fields = []
            if isinstance(self.__get_options__, list):
                fields = self.__get_options__
            else:
                fields.append(self.__get_options__)
            #print('self.kargs {var1}'.format(var1=str(self.kargs)))
            if 'where' in self.kargs:
                del self.kargs['where']
            #print('self.kargs {var1} {var2} {var3}'.format(var1=str(self.kargs), var2=str(self.__order_by__), var3=str(fields)))
            opts = self.get(order_by = self.__order_by__, fields = fields)
            #print('opts do get_options {var1}'.format(var1=str(opts)))
            for record in opts:
                #print('{var1}'.format(var1=str(record)))
                if isinstance(self.__get_options__, list):
                    model_options = ''
                    for option in self.__get_options__:
                        model_options += str(record[option]) + ' - '
                    model_options = model_options [:-3]
                else:
                    model_options = record[self.__get_options__]
                options.append((str(record['id']), model_options))
            return options
        return erp_cache.get(key=self.__model_name__ + '_options', createfunc=get_results)

    def put_many(self):
        values_list = self.kargs['records']
        created_ids = []
        records = []
        fields = ''
        values = ''
        for f in values_list[0]:
            if f not in ('id', 'user'):
                fields += f + ','
                values += "%({field})s,".format(field=f)
        fields = fields[:-1]
        values = values[:-1]
        fields += ",user_create,date_create,id,active"
        values += ",%(user_create)s,%(date_create)s,%(id)s,True"
        for record in values_list:
            record['user_create'] = str(record['user'])
            record['date_create'] = str(datetime.datetime.today())
            if 'id' not in record:
                record['id'] = get_identity(table=self.__name__, user=record['user'])
            records.append(record)
            created_ids.append(record['id'])
        records = tuple(records)
        sql = "INSERT INTO {table} ({fields}) VALUES ({values});\n".format(table=self.__name__, fields=fields, values=values)
        #print(sql)
        with getcursor() as cursor:
            cursor.executemany(sql, records)

        return created_ids

    @verify_orm_rights
    def put(self, synchronize=True):
        print('im in put de ORM')
        erp_cache.remove_value(key=self.__model_name__)
        row_id = None
        if self.__db_mode__ not in ['None', 'View']:
            #print('not in none view')
            if self.kargs:
                #print('kargs {var1}'.format(var1=str(self.kargs)))
                fields_dict = self.kargs
            else:
                #print('not kargs')
                fields_dict = {}
                for f in get_model_fields(self):
                    #print('type(f) {var1}'.format(var1=str(type(f))))
                    if hasattr(self, f[0]):
                        fields_dict[f[0]] = eval('self.' + f[0])
            fields = ''
            values = ''
            fields_values = ''
            for f in fields_dict:
                if f not in ('id', 'user', 'user_change', 'date_change', 'active'):
                    if fields_dict[f] not in ['None', '', None]:
                        fields += f + ','
                        if fields_dict[f] == 'Null':
                            values += "{field_value},".format(field_value=fields_dict[f])
                            fields_values += "{field} = {field_value},".format(field=f, field_value=fields_dict[f])
                        else:
                            field_value=fields_dict[f]
                            if isinstance(field_value, str):
                                field_value=field_value.replace("'", "''")
                            values += "'{field_value}',".format(field_value=field_value)
                            fields_values += "{field} = '{field_value}',".format(field=f, field_value=field_value)
            fields = fields[:-1]
            values = values[:-1]
            fields_values = fields_values[:-1]
            #print(' o fields_dict passado ao put é: ', fields_dict)
            try:
                if 'id' in fields_dict and fields_dict['id'] not in ['', '0', 0, 'None', None]:
                    if fields_values:
                        fields_values += ','
                    fields_values += "user_change='{user}',date_change='{date}'".format(user=str(self.kargs['user']), date=str(datetime.datetime.today()))
                    sql = "UPDATE {table} SET {values} where id='{key}'".format(table=self.__name__, values=fields_values, key=self.kargs['id'])
                    row_id = fields_dict['id']

                    with getcursor() as cursor:
                        cursor.execute(sql)
                    rowcount = cursor.rowcount;

                    print('im in put do orm making one update and the result is', rowcount)
                    if rowcount == 0:
                        row_id = 'Erro: A gravação do Registo Falhou: ' + sql
                else:
                    #print('fields {var1}'.format(var1=str(fields)))
                    if fields:
                        fields += ','
                        values += ','
                    #print('self.kargs {var1} {var2}'.format(var1=str(self.kargs), var2=str(fields_dict)))
                    fields += "user_create,date_create,id,active"
                    values += "'{user}','{date}','{new_id}',True".format(user=str(fields_dict['user']), date=str(datetime.datetime.today()),new_id=get_identity(table=self.__name__, user=str(fields_dict['user'])))
                    sql = "INSERT INTO {table} ({fields}) VALUES ({values}) RETURNING id".format(table=self.__name__, fields=fields, values=values)
                    with getcursor() as cursor:
                        cursor.execute(sql)
                        row_id = cursor.fetchone()['id']
                        #print('{var1}'.format(var1=str(row_id)))

            except Exception as err:
                print('estou numa excepção do put')
                print('o erro é', err)
                row_id = 'Erro: ' + str(err)

        return row_id

    @verify_orm_rights
    def get(self, order_by=None, key=None, limit=None, offset=None, fields=[]):
        """vai buscar dados na bd deste modelo, o fields serve para só ir buscar alguns campos e assim melhorar a performance"""
        print('im in get do ORM')
        result = []
        if self.__db_mode__ != 'None':
            table = self.__name__
            #print('table {var1}'.format(var1=table))
            if 'where' in self.kargs:# and self.kargs['where'] != ''
                where = 'WHERE ({table}.active=True OR {table}.active is NULL) AND '.format(table=self.__name__) + self.kargs['where'].replace('None', '0')
            elif hasattr(self, 'where'):
                where = 'WHERE ({table}.active=True OR {table}.active is NULL) AND '.format(table=self.__name__) + self.where.replace('None', '0')
            else:
                where = 'WHERE ({table}.active=True OR {table}.active is NULL) '.format(table=self.__name__)
            #print('where {var1}'.format(var1=where))
            if 'join' in self.kargs:
                join = self.kargs['join']
            else:
                join = ''
            if limit:
                limit = 'LIMIT ' + str(limit)
            else:
                limit = ''
            if offset:
                offset = 'OFFSET ' + str(offset)
            else:
                offset = ''
            if order_by:
                order_by = 'ORDER BY ' + str(order_by)
            else:
                order_by = ''
            if key or key==[]:
                if where:
                    where += ' AND '
                else:
                    where = 'WHERE ({table}.active=True OR {table}.active is NULL) AND '.format(table=self.__name__)
                #print(where)
                if key not in ['None', None]:
                    if isinstance(key,list):
                        if len(key) > 1:
                            where += """{table}.id in {ids}""".format(ids=tuple(key), table=table)
                        elif len(key) == 0:
                            where += """{table}.id = '0' """
                        else:
                            where += """{table}.id = '{ids}'""".format(ids=key[0], table=table)
                    else:
                        where += """{table}.id = '{ids}'""".format(ids=key, table=table)
                else:
                    where += """{table}.id = '0' """.format(table=table)
            return_fields = '{table}.id'.format(table=table)
            #print(return_fields, 'cheguei em baixo')
            if fields:
                for field in fields:
                    if field != 'id':
                        return_fields += ', ' + table + '.' + field
            else:
                return_fields = '*'

            #Executar o código
            sql = """SELECT {fields} FROM {table} {join} {where} {order_by} {limit} {offset}""".format(table=table, join=join, where=where, order_by=order_by,limit=limit, offset=offset, fields=return_fields)
            #print(sql)
            try:
                with getcursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
            except Exception as err:
                if 'relation "users" does not exist' in str(err) or 'relation "role" does not exist' in str(err) or 'relation "sequence" does not exist' in str(err) or 'relation "identity" does not exist' in str(err):
                    create_base_tables()
                    #self.get(limit=limit, offset=offset, key=key)
                elif 'does not exist' in str(err):
                    #print ('{var1}'.format(var1=err))
                    syncModel(self)
                    #self.get(limit=limit, offset=offset, key=key)
                else:
                    etype = sys.exc_info()[0]
                    try:
                        ename = etype.__name__
                    except AttributeError:
                        ename = etype
                    result = str(ename) + ":", sys.exc_info()[1]
        return result

    @verify_orm_rights
    def delete(self):
        #print('in delete de orm')
        if 'where' in self.kargs:
            where = 'WHERE {where}'.format(where=self.kargs['where'])
        elif hasattr(self, 'where'):
            where = 'WHERE {where}'.format(where=self.where)
        else:
            where = 'WHERE id=None'
        #print('{var1}'.format(var1=where))
        #print('user {var1}'.format(var1=str(self.kargs['user'])))
        sql = "UPDATE {table} SET active=False, user_change='{user}', date_change='{date}' {where}".format(table=self.__name__, where=where, user=str(self.kargs['user']), date=str(datetime.datetime.today()))
        #print(sql)

        try:
            with getcursor() as cursor:
                cursor.execute(sql)
                row_count = cursor.rowcount
                result = row_count
        except Exception as err:
            etype = sys.exc_info()[0]
            try:
                ename = etype.__name__
            except AttributeError:
                ename = etype
            return str(ename) + ":", sys.exc_info()[1]
        return result

    def get_m2m_ids(self, field_name, record):
        """Processa os many2many e devolve uma lista com os ids da tabela ascendente"""
        #print('estou no orm em get_m2m_ids')
        import objs
        from utils import get_many2many_name, get_condition, get_model_fields
        for f in get_model_fields(self):
            if f[0] == field_name:
                field = f[1]
        parent_model = eval('objs.' + field.model_name + '()')
        table = get_many2many_name(self.__name__, parent_model.__name__)
        where = get_condition(field.condition, record=record)
        #print('o meu where é', where)
        sql = "SELECT * FROM {table} WHERE {where}".format(table=table, where=where)
        #print(sql)
        result = []
        try:
            with getcursor() as cursor:
                cursor.execute(sql)
                res = cursor.fetchall()
            for r in res:
                result.append(r[parent_model.__name__])
        except Exception as err:
            if 'does not exist' in str(err):
                syncModel(self)
            else:
                etype = sys.exc_info()[0]
                try:
                    ename = etype.__name__
                except AttributeError:
                    ename = etype
                return str(ename) + ":", sys.exc_info()[1]
        #print('o resultado do m2m é ', result)
        return result

    def put_m2m(self):
        """Grava a relação entre duas tabelas na relação many2many """
        import objs
        from utils import get_many2many_name, get_model_fields
        #print('orm put_m2m kargs {var1} {var2}'.format(var1=str(self.kargs), var2=str(dir(self))))
        for f in get_model_fields(self):
            if hasattr(f[1],'model_name') and f[1].model_name.split('.')[0] == self.kargs['parent_name']:
                field = f[1]
        parent_model = eval('objs.' + field.model_name + '()')
        table = get_many2many_name(self.__name__, parent_model.__name__)
        #print('table to write to! {var1}'.format(var1=table))
        fields = """{field1},{field2},id""".format(field1=self.__name__, field2=parent_model.__name__)
        values = """'{value1}', '{value2}','{new_id}'""".format(value1=self.kargs[self.__name__], value2=self.kargs[parent_model.__name__],new_id=get_identity(table=table, user=str(self.kargs['user'])))
        sql = "INSERT INTO {table} ({fields}) VALUES ({values})".format(table=table, fields=fields, values=values)
        #print(sql)


        with getcursor() as cursor:
            cursor.execute(sql)
        return 'ok'# aqui talvez um rowid qualquer relativo á relação ou algo assim... dificil no entanto não me parece grave dado que a maioria das vezes a relação terá apenas uma ocorrencia

    def remove_m2m(self):
        """Elimina a relação entre as duas tabelas e no caso de ter varias relações entre as mesmas tabelas, elimina apenas uma"""
        import objs
        from utils import get_many2many_name, get_model_fields
        #print('{var1}'.format(var1=str(self.kargs)))
        for f in get_model_fields(self):
            #print('{var1}'.format(var1=str(f)))
            if f[0] == self.kargs['parent_name']:
                field = f[1]
        try:
            parent_model = eval('objs.' + field.model_name + '()')
        except:
            return 'Verifique o model_name na definição do campo M2M!'
        table = get_many2many_name(self.__name__, parent_model.__name__)
        where = """WHERE {field1}='{value1}' AND {field2}='{value2}'""".format(field1=self.__name__, field2=parent_model.__name__, value1=self.kargs[self.__name__], value2=self.kargs[parent_model.__name__])
        sql = "SELECT id from {table} {where}".format(table=table, where=where)
        #print(sql)
        with getcursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()['id']
        sql = "DELETE FROM {table} WHERE id='{result}'".format(table=table, result=result)
        #print(sql)

        with getcursor() as cursor:
            cursor.execute(sql)
        return 'ok'

class dummy_model(Model):
    pass

def create_base_tables():    
    """Cria as tabelas base e prenche os valores iniciais!"""
    import objs
    from base_models import Sequence
    model = Sequence()
    syncModel(model)

    #print('users')
    from users import Users
    model = Users()
    syncModel(model)

    #print('role')
    from role import Role
    model = Role()
    syncModel(model)

    result = Users().get()
    if len(result) == 0:
        import base64
        password = base64.encodestring('noops!admin'.encode('utf-8')).decode('utf-8')
        new_user_id = get_identity(table='users', user=None)
        sql = "INSERT INTO users (nome, login, password, email, estado, id, user_create, date_create, active) VALUES ('admin', 'admin', '{var1}', 'admin@localhost', 'active','{var2}','{var3}','{var4}', True);".format(var1=password,var2= new_user_id, var3=new_user_id, var4=str(datetime.datetime.today()))
        #print(sql)
        with getcursor() as cursor:
            cursor.execute(sql)

    result = Role().get()
    if len(result) == 0:
        new_role_id = get_identity(table='role', user=new_user_id)
        sql = "INSERT INTO role (nome, id, user_create, date_create, active) VALUES ('Administrator', '{var1}','{var2}','{var3}', True);".format(var1=new_role_id, var2=new_role_id, var3=str(datetime.datetime.today()))
        #print(sql)

        with getcursor() as cursor:
            cursor.execute(sql)

        #sql = 'CREATE TABLE IF NOT EXISTS role_users (id VARCHAR(50) PRIMARY KEY, role INTEGER, user_id INTEGER);'
        #with getcursor() as cursor:
        #   cursor.execute(sql)
        new_id = get_identity(table='role_users', user=new_user_id)
        sql = "INSERT INTO role_users (role, users, id) VALUES ('{var1}','{var2}','{var3}');".format(var1=new_role_id, var2=new_user_id, var3=new_id)
        #print(sql)

        with getcursor() as cursor:
            cursor.execute(sql)

def run_sql(sql):
    #print(sql)
    with getcursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
    return result


def get(sql):
    """vai buscar dados na base de dados"""
    #print('im in outer get')
    #print(sql)
    with getcursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result

def put(table, **kargs):
    """Serve para inserir valores na Base de Dados"""
    #from utils import ustring
    print('im in outer put')
    row_id = None
    fields = ''
    values = ''
    fields_values = ''
    for f in kargs:
        if f not in ('id', 'user', 'user_change', 'date_change', 'active'):
            if kargs[f] not in ['None', '', None]:
                fields += f + ','
                values += "'{field_value}',".format(field_value=kargs[f])
                fields_values += "{field} = '{field_value}',".format(field=f, field_value=kargs[f])
    fields = fields[:-1]
    values = values[:-1]
    fields_values = fields_values[:-1]
    #print(1)
    if 'id' in kargs:
        fields_values += ",user_change='{user}',date_change='{date}'".format(user=str(kargs['user']), date=str(datetime.datetime.today()))
        sql = "UPDATE {table} SET {values} where id='{key}'".format(table=table, values=fields_values, key=kargs['id'])
        row_id = kargs['id']
    else:
        fields += ",user_create,date_create,id,active"
        row_id = get_identity(table=table, user=str(kargs['user']))
        values += ",'{user}','{date}','{new_id}', True".format(user=str(kargs['user']), date=str(datetime.datetime.today()),new_id=row_id)
        sql = "INSERT INTO {table} ({fields}) VALUES ({values})".format(table=table, fields=fields, values=values)
    #print(sql)
    with getcursor() as cursor:
        cursor.execute(sql)
    #print('fim de put')
    return row_id

def remove(table, where):
    """Serve para remover valores na Base de Dados mas na verdade apenas desactiva"""
    #print ('Im on remove')
    #try:
    if where:
        where = 'WHERE {where}'.format(where=where)
    else:
        where = ''
    sql = "UPDATE {table} SET active=False {where}".format(table=table, where=where)
    #print(sql)
    with getcursor() as cursor:
        #print('{var1}'.format(var1=sql))
        cursor.execute(sql)
    return True


def remove_pos(table, where):
    """Serve para remover valores na Base de Dados e remove mesmo"""
    #print ('Im on remove pos')
    #try:
    if where:
        where = 'WHERE {where}'.format(where=where)
    else:
        where = ''
    sql = "DELETE FROM {table} {where}".format(table=table, where=where)
    #print(sql)
    with getcursor() as cursor:
        #print('{var1}'.format(var1=sql))
        cursor.execute(sql)
    return True


class field(object):
    """Classe base para todos os objectos do tipo field"""
    def __init__(self,
        hidden_class=False,
        delete_ok=True,
        noline=False,
        legend='',
        description='',
        url='',
        unique = False,
        size = 0,
        view_order = 0,
        name = '',
        value = '',
        args = '',
        edit_ok = True,
        options = [],
        parent = None,
        source = '',
        nolabel = False,
        onlist = True,
        search = True,
        default = '',
        onchange = False,
        dynamic_atrs = False,
        field_name = '',
        model = None,
        model_name = '',
        condition = '',
        fields = [],
        show_footer = True,
        sum = False,
        hidden = False,
        column = None,
        list_edit_mode = None,
        simple = False):
        self.delete_ok=delete_ok
        self.noline=noline
        self.legend=legend
        self.description = description
        self.url = url
        self.unique = unique# falta implementar isto nos campos para sempre que não queira-mos valores duplicados!
        self.size = size
        self.view_order = view_order
        self.name = name
        self.value = value
        self.args = args
        self.edit_ok = edit_ok
        self.options = options
        self.parent = parent
        self.source = source
        self.nolabel = nolabel
        self.onlist = onlist
        self.search = search
        self.default = default
        self.onchange = onchange
        self.dynamic_atrs = dynamic_atrs
        self.field_name = field_name
        self.model = model
        self.model_name = model_name
        self.condition = condition
        self.fields = fields
        self.show_footer = show_footer
        self.sum = sum
        self.hidden = hidden
        self.column = column
        self.list_edit_mode = list_edit_mode #representa a forma como o edit da lista deve abrir o registo e pode ser inline, edit, popup, newwin, etc
        self.simple = simple
        #aqui penso que basta por hidden pois a plataforma ira converter para o que for adequado para cada widget e o nolabel
        #tambem não é necessário, só o onlist pois mesmo estando escondido no form eu posso querer ver na lista

class hrline(field):
    pass

class label(field):
    pass

class separator(field):
    pass

class newline(field):
    pass

class link(field):
    pass

class many2many(field):
    pass

class list_field(field):
    pass

class function_field(field):
    dbtype='varchar'

class string_field(field):
    dbtype='varchar'


class email_field(field):
    dbtype='varchar'


class image_field(field):
    dbtype='varchar'


class upload_field(field):
    dbtype='varchar'


class password_field(field):
    dbtype='varchar'


class combo_field(field):
    dbtype='varchar'
    #apesar de por defeito ser varchar no caso de parent ser igual a true passa a ser VARCHAR(50) pois significa que é uma relaçao com outra tabela
    constrains = 'fk_%(table)s_%(parent)s FOREIGN KEY (%(name)s) REFERENCES %(parent)s(id) ON DELETE RESTRICT'


class choice_field(field):
    dbtype='VARCHAR(50)'
    constrains = 'fk_%(table)s_%(parent)s FOREIGN KEY (%(name)s) REFERENCES %(parent)s(id) ON DELETE RESTRICT'


class parent_field(field):
    dbtype = 'VARCHAR(50)'
    constrains = 'fk_%(table)s_%(parent)s FOREIGN KEY (%(name)s) REFERENCES %(parent)s(id) ON DELETE RESTRICT'


class boolean_field(field):
    dbtype='boolean'


class integer_field(field):
    dbtype='integer'


class float_field(field):
    dbtype='float'


class currency_field(field):
    #dbtype='decimal(10,2)'
    dbtype='bigint'


class percent_field(field):
    dbtype='decimal(4,2)'


class decimal_field(field):
    dbtype='decimal(10,2)'


class date_field(field):
    dbtype='date'


class time_field(field):
    dbtype='time'


class text_field(field):
    dbtype='text'


class message_field(field):
    dbtype='text'


class info_field(field):
    dbtype='varchar'


def get_identity(table, user):
    """
    Aqui o table e user já não faz falta deveria substituir a chamada a esta função directamente pelo comando do uuid
    """
    return str(uuid.uuid4())