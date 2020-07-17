import pandas as pd
from config.database import Database
from sqlalchemy import create_engine
# import request
# import flask



class Mysql(object):

    def __init__(self, write=None):
        self.db = Database()
        if(write):
            self.cnn = self.db.getMysqlCnnW()
            return
        self.cnn = self.db.getMysqlCnn()

    # 获取连接信息
    def getCnn(self):
        self.cnn = self.db.getMysqlCnn()
        return self.cnn

    def getCnnW(self):
        self.cnn = self.db.getMysqlCnnW()
        return self.cnn


    # 获取json（dict）的基本结构
    def getGeomJson(self, table, where=None):
        pass

    # 获取表的所有字段名称,注意表名是不带模式的
    def getTableColumns(self, tablename):
        sql = "SELECT a.attname as field FROM pg_class as c,pg_attribute as a inner " \
              "join pg_type on pg_type.oid = a.atttypid where c.relname = '" \
              + tablename + "' and a.attrelid = c.oid and a.attnum>0"
        dbRows = self.exec(sql)
        return dbRows.T.values[0]

    # 给表增加字段
    def addTableColumn(self, table, column):
        sql = 'ALTER TABLE ' + table + ' ADD ' + column + ' double precision '
        return self.ex(sql)

    # 获取所有队了geom字段的值，转为json（dict）
    def getProperties(self, table, where=None):
        if where == None:
            whereClause = ''
        else:
            whereClause = ' where ' + where
        columns = self.getTableColumns(table)
        columns.pop()
        colexcept = ",".join(columns)
        sql = 'select row_to_json(t) from (select ' + colexcept + ' from ' + table + whereClause + ') as t'
        return self.exec(sql)

    # 执行原生的SQL并返回dataframe结果
    def exec(self, sql):
        cur = self.cnn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        return res
        # return pd.DataFrame(res)

        # def exec(self, sql):
        #     cur = self.cnn.cursor()
        #     self.cnn.commit()
        #     cur.execute(sql)
        #     res = cur.fetchall()
        #     return pd.DataFrame(res)

    # 数据表内容有更新，必须使用到该语句
    def insert(self, table, columns, values):
        tableStr = table + '(' + ','.join(columns) + ')'
        valStr = []
        for col in columns:
            valStr.append('%s')
        sql = "INSERT INTO " + tableStr+" VALUES (" + ','.join(valStr) + ")"
        cur = self.cnn.cursor()
        cur.executemany(sql, values)
        self.cnn.commit()

    def sql(self, sql):
        cur = self.cnn.cursor()
        cur.execute(sql)
        self.cnn.commit()
        return True

    # 执行原生的SQL，没有实际数据，只执行命令，返回成功结果
    def ex(self, sql):
        return self.sql(sql)

    # 执行sql获取返回一个值的内容
    def execValue(self, sql):
        res = self.exec(sql)
        if len(res) > 0:
            return res[0][0]
        else:
            return None

    # 获取engine,使用这个引擎
    def engine(self):
        # engine = create_engine('postgresql://' + self.dbconfig['db_user'] + ':123456@' + self.dbconfig['db_host'] + ':' + str(self.dbconfig['db_port'])
        #                        + '/' + self.dbconfig['db_database'])
        engine = create_engine("mysql://cekeyuan:Cekeyuan@0430@101.37.250.228:3306/securitycode",
                               max_overflow=5)
        # create_engine("mysql+pymysql://user:passwd@host:port/db?charset=utf8")
        # engine = create_engine('mysql://user:password@localhost:3306/test?charset=utf8mb4')
        return engine

    def myEngine(self):
        engine = create_engine("mysql://wdkj@dev:wdkj@devpwd@120.79.50.98:3306/yjgl",
                               max_overflow=5)
        return engine

    def isTableExist(self, table):
        sql = "select to_regclass('" + table + "')"
        table_name = self.execValue(sql)
        if table_name is None:
            return False
        else:
            return True

    def clearTable(self, table):
        sql = 'TRUNCATE ' + table
        return self.ex(sql)

    def dropTable(self, tableArr:list):
        for table in tableArr:
            if self.isTableExist('gegu."' + table + '"'):
                sql = 'drop table gegu."' + table + '"'
                self.ex(sql)
                print('删除表成功：' + table)
        print()
        return True

    def getValue(self, key):
        sql = 'select value from kv ' + "where key = '" + key + "'"
        return self.execValue(sql)

    def setValue(self, key, value):
        sql = 'select key from kv ' + "where key = '" + key + "'"
        skey = self.execValue(sql)
        exSql = ''
        if skey is None:
            exSql = "insert into kv(key,value) values('"+ key +"','" + value + "')"
        else:
            exSql = "update kv set value = '" + value + "' " + " where key='" + key + "'"
        self.ex(exSql)
        return True

    def delValue(self, key):
        sql = 'delete from kv ' + "where key = '" + key + "'"
        return self.ex(sql)

    def deleteSQL(self, sql):
        pass
