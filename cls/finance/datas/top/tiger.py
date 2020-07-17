import time
import datetime
import pandas as pd
from cls.finance.datas.top.top import TopList

# http://data.eastmoney.com/stock/tradedetail.html
class TigerData(TopList):

    def __init__(self):
        TopList.__init__(self)
        self.unixMinute = None
        # 龙虎榜龙虎榜净买额=龙虎榜买入额-龙虎榜卖出额；代表龙虎榜资金的净流入情况。
        # self.url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=3,page=1,sortRule=-1,' \
        #            'sortType=JmMoney,startDate=2019-03-08,endDate=2019-03-08,gpfw=0,js=var%20data_tab_1.html?rt=25868677'
    #     #   龙虎榜成交额占总成交比率，可能是买与卖之和
        self.baseUrl = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,' \
                       'sortType=ZeRate,startDate=2019-03-08,endDate=2019-03-08,gpfw=0,js=var%20data_tab_1.html'
    #     #  净买额占总成交比率
    #     self.url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,' \
    #                'sortType=JmRate,startDate=2019-03-08,endDate=2019-03-08,gpfw=0,js=var%20data_tab_1.html?rt=25868684'
    # #     近5日上榜排序
    #     self.url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page=1,sortRule=-1,' \
    #                'sortType=,startDate=2019-03-04,endDate=2019-03-08,gpfw=0,js=var%20data_tab_2.html?rt=25868687'


    # 其中参数rt的值为linux毫秒时间戳/60000
    def getUnixMinute(self):
        millis = int(round(time.time() / 60))
        return str(millis)

    # 解析字符串结果，返回dataframe
    def parse(self, res):
        string = res.data
        str = string.decode('gb2312').split('=')[1]
        pstart = str.find('[{') + 2
        pend = str.find('}]')
        itemsArr = str[pstart:pend].split('},{')
        arrKeys = []
        arrRes = []
        tag = True
        for item in itemsArr:
            keyValues = item.split(',')
            arrValues = []
            for kv in keyValues:
                if tag:
                    arrKeys.append(kv.split(':')[0].replace('"', ''))
                arrValues.append(kv.split(':')[1].replace('"', ''))
            tag = False
            arrRes.append(arrValues)
        index = arrKeys.index('SCode')
        arrKeys[index] = 'code'
        df = pd.DataFrame(arrRes, columns=arrKeys)
        return df

    def urlSet(self):
        # 这一行要放最后
        self.baseUrl += '?rt=' + self.getUnixMinute()
        return self.baseUrl

    # "SCode": "000530", "SName": "大冷股份", "ClosePrice": "4.84", "Chgradio": "10", "Dchratio": "5.4",
    def getLists(self):
        self.urlSet()
        res = self.http.request('GET', self.baseUrl)
        df = self.parse(res)
        df['tradedate'] = time.strftime('%Y%m%d ', time.localtime(time.time()))
        return df

    #  一定时间段内，统计个股上榜次数排序
    def getStatisticLists(self):
        # 近六个月内，上榜排序前100支
        url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/StockStatistic/pagesize=100,page=1,sortRule=-1,' \
              'sortType=,startDate=2018-09-24,endDate=2019-03-24,gpfw=0,js=var%20data_tab_3.html?rt=25890313'
        res = self.http.request('GET', url)
        return self.parse(res)

    # def statUrlSet(self, preUrl, startDate, endDate):
    #     url = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=100,page=1,sortRule=-1,' \
    #           'sortType=Chgradio,startDate=2019-02-11,endDate=2019-03-11,gpfw=0,js=var%20data_tab_1.html?rt=25871805'
    #     day = datetime.datetime.strptime(date, '%Y%m%d')
    #     delta = datetime.timedelta(days=1)
    #     nextDay = day + delta
    #     pass




    def saveStat2sql(self, table):
        df = self.getStatisticLists()
        pg = self.getPG()
        tableName = 'public."' + table + '"'
        if pg.isTableExist(tableName):
            pg.clearTable(tableName)
        df.to_sql(table, pg.engine(), index=False, if_exists='append', schema='public')  #
        # self.deleteRepeat(table)
        return True

