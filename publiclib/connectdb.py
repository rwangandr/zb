__author__ = 'carl'

import MySQLdb
import MySQLdb.cursors
import socket

'''
In this script, use the method directly, each publiclib sql query will call __init first to connect to database, then perform its own function.
'''


def create_database(**c):
    '''
    This method is used to create database
    :param c:   some para in connection string is pre-filled, while some not. you should assign value for the empty para first
                database field here stands for the database name that about to be created, if database is not defined, "DB_"+hostname will be used
    :return:    if creation succeeds, True will be returned, otherwise, False will be returned
    '''
    rt = False
    database = 'DB_' + socket.gethostname().replace('.', '')
    host = ''
    user = 'root'
    password = '111111'
    port = 3306
    if c.has_key('database'):
        database = c['database']
    if c.has_key('host'):
        host = c['host']
    if c.has_key('user'):
        user = c['user']
    if c.has_key('password'):
        password = c['password']
    if c.has_key('port'):
        port = int(c['port'])
    # print ("host="+host+",user="+user+",passwd="+password+",db="+database+",port="+str(port))
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password, port=port, connect_timeout=120)
        conn.autocommit(1)
        print "Connection had been setup."
        cmd = 'create database ' + database
        cur = conn.cursor()
        cur.execute(cmd)
        cur.close()
        conn.close()
        print "Connection had been closed."
        print "Database %s had been created." % database
        rt = True
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        # if cur:
        #     cur.close()
        # if conn:
        #     conn.close()
        #     print "Connection had been closed."
        return rt


def drop_database(**c):
    '''
    This method is used to drop database
    :param c:   some para in connection string is pre-filled, while some not. you should assign value for the empty para first
                database field here stands for the database name that about to be dropped, if database is not defined, "DB_"+hostname will be used
    :return:    if creation succeeds, True will be returned, otherwise, False will be returned
    '''
    rt = False
    database = 'DB_' + socket.gethostname().replace('.', '')
    host = ''
    user = 'root'
    password = '111111'
    port = 3306
    if c.has_key('database'):
        database = c['database']
    if c.has_key('host'):
        host = c['host']
    if c.has_key('user'):
        user = c['user']
    if c.has_key('password'):
        password = c['password']
    if c.has_key('port'):
        port = int(c['port'])
    # print ("host="+host+",user="+user+",passwd="+password+",db="+database+",port="+str(port))
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password, port=port, connect_timeout=120)
        conn.autocommit(1)
        print "Connection had been setup."
        cmd = 'drop database ' + database
        cur = conn.cursor()
        cur.execute(cmd)
        cur.close()
        conn.close()
        print "Connection had been closed."
        print "Database %s had been dropped." % database
        rt = True
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        # if cur:
        #     cur.close()
        # if conn:
        #     conn.close()
        #     print "Connection had been closed."
        return rt


def __init(**c):
    '''
    This method is for initializing the connection to mysql database
    :param c:   some para in connection string is pre-filled, while some not. you should assign value for the empty para first
    :return:    a connection handler will be returned
    '''
    conn = None
    host = ''
    user = 'root'
    password = '111111'
    database = 'DB_' + socket.gethostname().replace('.', '')
    port = 3306
    charsetkey = 'utf8'
    curmode = MySQLdb.cursors.DictCursor
    if c.has_key('host'):
        host = c['host']
    if c.has_key('database'):
        database = c['database']
    if c.has_key('user'):
        user = c['user']
    if c.has_key('password'):
        password = c['password']
    if c.has_key('port'):
        port = int(c['port'])
    if c.has_key('charset'):
        charsetkey = c['charset']
    if c.has_key('cursorclass'):
        curmode = c['cursorclass']

    # print ("host="+host+",user="+user+",passwd="+password+",db="+database+",port="+str(port))
    try:
        if c.has_key('cursorclass'):
            conn = MySQLdb.connect(host=host, user=user, passwd=password, db=database, port=port, charset=charsetkey,
                                   cursorclass=curmode, connect_timeout=120)
        else:
            conn = MySQLdb.connect(host=host, user=user, passwd=password, db=database, port=port, charset=charsetkey,
                                   connect_timeout=120)
        conn.autocommit(1)
        print "Connection had been setup."
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        return conn


def create_schema(schema_file, **c):
    '''
    This method will create schema in a database
    :param schema_file:  you should prepare a sql schema file first
    :param c:   This arg is for database connection, if any of config is not same with the default value, you should define is as key="value"
    :return:    return True or False
    '''
    result = False
    try:
        f = open(schema_file, 'r')
        sql = ''
        for l in f.readlines():
            # print l
            # sql+=l.strip()
            if not l.startswith("--"):
                sql += l.strip()
        # print sql
        conn = __init(**c)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        result = True
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        if conn:
            conn.close()
        return result


def drop_schema(table_list, **c):
    '''
    This method will drop all the tables in a database, instead of dropping the whole database
    :param table_list:  you should provide a list of which tables you want to drop
    :param c:   This arg is for database connection, if any of config is not same with the default value, you should define is as key="value"
    :return:    return True or False
    '''
    result = False
    try:
        conn = __init(**c)
        cur = conn.cursor()
        for table in table_list:
            cmd = "DROP TABLE IF EXISTS " + table + ";"
            # print cmd
            cur.execute(cmd)
        cur.close()
        result = True
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    finally:
        if conn:
            conn.close()
        return result


def query_one_line(cmd, **c):
    '''
    :param cmd:
    :param c:   This arg is for database connection, if any of config is not same with the default value, you should define is as key="value"
    :return:    This method is using "fetch one", which will only return the first result of the query, in tuple type
    '''
    print cmd
    conn = None
    result = ''
    try:
        conn = __init(**c)
        cur = conn.cursor()
        # count=cur.execute(cmd)
        # print 'There are %s rows record' % count
        cur.execute(cmd)
        result = cur.fetchone()
        if result == None:
            print "Cannot fetch any result."
        else:
            print "Fetch latest result."
        cur.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        result = e.message
    finally:
        if conn:
            conn.close()
        return result


def query_multi_lines(cmd, **c):
    '''
    :param cmd:
    :param c:   This arg is for database connection, if any of config is not same with the default value, you should define is as key="value"
    :return:    This method is using "fetch all", which will return all the result of the query, in tuple type
    '''
    print cmd
    conn = None
    result = ''
    try:
        conn = __init(**c)
        cur = conn.cursor()
        # count=cur.execute(cmd)
        # print 'There are %s rows record' % count
        cur.execute(cmd)
        result = cur.fetchall()
        if result == None:
            print "Cannot fetch any result."
        else:
            print "Fetch all the results."
        cur.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        result = e.message
    finally:
        if conn:
            conn.close()
        return result


def query_update(cmd, **c):
    '''
    :param cmd:
    :param c:   This arg is for database connection, if any of config is not same with the default value, you should define is as key="value"
    :return:    This method is only using "execute", which will return the count of affected rows
    '''
    print cmd
    conn = None
    result = ''
    try:
        conn = __init(**c)
        cur = conn.cursor()
        result = cur.execute(cmd)
        print 'There are %s row(s) affected.' % result
        cur.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        result = e.message
    finally:
        if conn:
            conn.close()
        return result


def query_specific_field(select_field, db_table, where_field, where_value, **c):
    cmd = "select * from %s where %s=\'%s\'" % (db_table, where_field, where_value)
    print cmd
    rt = query_one_line(cmd, **c)
    print rt
    if rt:
        return str(rt[select_field])
    else:
        return ''


def query_random_entry(db_table, where_field='na', where_value='na', **c):
    if where_field == 'na':
        cmd = 'select * from %s order by rand() limit 1;' % db_table
    else:
        cmd = 'select * from %s where %s=\'%s\' order by rand() limit 1;' % (db_table, where_field, str(where_value))
    print cmd
    return query_one_line(cmd, **c)


def query_random_para(select_field, db_table, where_field='na', where_value='na', **c):
    rt = {select_field: None}
    rand_entry = query_random_entry(db_table, where_field, where_value, **c)
    if rand_entry.has_key(select_field):
        rt[select_field] = rand_entry[select_field]
    return rt


def query_entry_count(db_table, where_field='na', where_value='na', **c):
    if where_field == 'na':
        cmd = 'select count(*) from %s' % db_table
    else:
        cmd = 'select count(*) from %s where %s=\'%s\'' % (db_table, where_field, str(where_value))
    print cmd
    rt = query_one_line(cmd, **c)
    if rt and rt.has_key('count(*)'):
        return int(rt['count(*)'])
    else:
        return 0

# conn = {'host': '172.16.50.201', 'database': 'AutoTest', 'password': '111111',
#         'cursorclass': MySQLdb.cursors.DictCursor}
# print query_specific_field('id', 'TestServers', 'component', 'sag', **conn)
# print query_specific_field('component', 'TestServers', 'server', '172.16.50.206', **conn)
# print query_random_entry('DetailedResults', 'casePriority', 'p2', **conn)
# print query_random_entry('DetailedResults', **conn)
# print query_random_para('result', 'DetailedResults', **conn)
