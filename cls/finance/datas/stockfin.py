
# import json
import tushare as ts
# import pandas as pd
# import datetime
# import time
# import urllib3
from cls.orm.main import PG

# 主要财务数据：每股收益，PE，净资产，市净率，收入与增长率，利润与增长率，毛利率，净利率，ROE（每股收益）、负债率
# 总股本，总值，流通股，流值。
class StockFinance(object):

    def __init__(self, code):
        self.allstlist = None
        self.code = code
        self.pro = ts.pro_api('4552d85ac2d1492fc488a32646b501ed6faf1835820f65408790e59d')
        # self.pg = PG()
        # self.engine = self.pg.engine()

    # 设置数据库
    def setPG(self):
        self.pg = PG()
        self.engine = self.pg.engine()
        return

    # pe<30, ROE>10%, 负债率<60%，年度收入增长8%
    def getDatas(self):
        df = self.pro.fina_indicator(ts_code='600000.SH')
        print(len(df.index))
        print(df)


obj = StockFinance('600000.SH')
obj.getDatas()