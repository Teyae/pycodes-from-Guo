import psycopg2
import mysql.connector
import pymysql


class Database(object):
    def __init__(self):
        self.configs2 = {
                'db_type': 'mysql_sql',
                'db_host': '120.79.50.98',
                'db_user': 'wdkj@dev',
                'db_passwd': 'wdkj@devpwd',
                'db_database': 'yjgl',  # stock
                'db_port': 3306  # 5433
        }

        # self.mysqlConfigs = {
        #         'db_type': 'mysql_sql',
        #         'db_host': '120.79.50.98',
        #         'db_user': 'wdkj@dev',
        #         'db_passwd': 'wdkj@devpwd',
        #         'db_database': 'yjgl',  # stock
        #         'db_port': 3306  # 5433
        # }

        self.mysqlConfigs = {                    # local
                'db_type': 'mysql_sql',
                'db_host': 'localhost',
                'db_user': 'root',
                'db_passwd': '123456',
                'db_database': 'yjgl',  # stock
                'db_port': 3306  # 5433
        }

        self.configs = {
                'db_type': 'pg_sql',
                'db_host': '127.0.0.1',
                'db_user': 'postgres',
                'db_passwd': '123456',
                'db_database': 'stock',
                'db_port': 5432
        }


    def getMysqlCnn(self):
        mydb = mysql.connector.connect(
            host=self.mysqlConfigs['db_host'],
            user=self.mysqlConfigs['db_user'],
            passwd=self.mysqlConfigs['db_passwd'],
            database=self.mysqlConfigs['db_database']
        )
        return mydb

    def getMysqlCnnW(self):
        mydb = mysql.connector.connect(
            host=self.configs2['db_host'],
            user=self.configs2['db_user'],
            passwd=self.configs2['db_passwd'],
            database=self.configs2['db_database']
        )
        return mydb

    # 获取数据库连接对象
    def getcnn(self):
        configs = self.config
        return psycopg2.connect(host=configs['db_host'], user=configs['db_user'],
                                port=configs['db_port'], password=configs['db_passwd'], database=configs['db_database'])
