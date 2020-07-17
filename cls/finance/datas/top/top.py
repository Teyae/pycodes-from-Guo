
import urllib3
import pandas as pd
from cls.orm.main import PG

class TopList(object):

    def __init__(self):
        # 主力排名
        self.baseUrl = None
        self.pg = PG()
        self.engine = self.pg.engine()
        self.itemNum = 100
        self.order = '-1'   #   1为正序，-1为反序 &sr=1
        self.dataColumns = []
        self.http = self.initLib()

    def initLib(self):
        return urllib3.PoolManager()

    def urlSet(self):
        return self.baseUrl

    def getToken(self):
        pass

    def getLists(self):
        pass

    def parse(self, res)->str:
        string = res.data
        return string.decode('utf-8').split('=')[1]

    def getPG(self):
        if self.pg is None:
            self.pg = PG()
        return self.pg

    def save2sql(self, table):
        df = self.getLists()
        pg = self.getPG()
        tableName = 'public."' + table + '"'
        if pg.isTableExist(tableName):
            pg.clearTable(tableName)
        df.to_sql(table, pg.engine(), index=False, if_exists='append', schema='public')  #
        self.deleteRepeat(table)
        return True

    def deleteRepeat(self, table):
        return None
        tableName = 'public."' + table + '"'
        sql = 'delete from ' + tableName + ' where ctid not in (select min(ctid) from ' \
              + tableName + ' emp group by code) and  '
        pg = self.getPG()
        return pg.ex(sql)

