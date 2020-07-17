import pandas as pd
from config.database import Database
from sqlalchemy import create_engine

class PG(object):

    def __init__(self):
        db = Database()
        self.dbconfig = db.config
        self.cnn = db.getcnn()

    # 获取连接信息
    def getCnn(self):
        return self.cnn


    # 获取json（dict）的基本结构
    def getGeomJson(self, table, where=None):
        if where == None:
            whereClause = ''
        else:
            whereClause = ' where ' + where
        jsonSql = "SELECT json_build_object( \
            'type','FeatureCollection',\
            'name','区域范围',\
            'features', json_build_object(\
            'type', 'Feature',\
            'geometry', ST_AsGeoJSON(geom)::json)) FROM " + table + whereClause
        return self.exec(jsonSql)

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
        self.cnn.commit()
        cur.execute(sql)
        res = cur.fetchall()
        return pd.DataFrame(res)

        # 执行原生的SQL，没有实际数据，只执行命令，返回成功结果
    def ex(self, sql):
        cur = self.cnn.cursor()
        self.cnn.commit()
        cur.execute(sql)
        self.cnn.commit()
        return True

    # 执行sql获取返回一个值的内容
    def execValue(self, sql):
        res = self.exec(sql)
        if len(res) > 0:
            return res[0][0]
        else:
            return None

    # 获取engine,使用这个引擎
    def engine(self):
        engine = create_engine('postgresql://' + self.dbconfig['db_user'] + ':123456@' + self.dbconfig['db_host'] + ':' + str(self.dbconfig['db_port'])
                               + '/' + self.dbconfig['db_database'])
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

