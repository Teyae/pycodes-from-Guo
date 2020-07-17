import time
import datetime
from cls.orm.main import PG
from cls.finance.datas.tudata import TradeDatas

# 个股类,包括一个简单的交易系统，包括回测
class ShareItem(object):

    def __init__(self, code=None):
        self.code = code
        self.date = None
        self.dayDatas = None
        self.pre_close = None
        self.open = None
        self.low = None
        self.high = None
        self.close = None
        self.change = None
        self.pct_chg = None
        self.vol = None
        self.adj_factor = None
        self.db = PG()
        self.datas = TradeDatas()
        self.setCode(code)
        self.avgShort = 5
        self.avgLong = 20

    def getDatas(self, date, num):
        return self.getNumDatas(date, num)
        # if self.code != None:
        #     sql = 'select * from ' + self.table + ' where trade_date <= \'' + date + '\' order by trade_date desc limit ' + str(num)
        # return self.db.exec(sql)

    def setCode(self, code):
        if not code is None:
            self.code = code
            self.lcode = self.datas.toLongCode(code)
            self.table = 'gegu."' + self.lcode + '"'
        return self.code

    def getCode(self):
        return self.code

    #  设定日期后，即定义了当天的交易数据
    def setDate(self, date):
        # if date is self.date:
        #     return self.date
        self.date = date
        sql = 'select * from ' + self.table + ' where trade_date <= \'' + date + "' order by trade_date desc limit 1"
        self.dayDatas = self.db.exec(sql)
        if len(self.dayDatas) != 0 :
            self.dayDatas.columns = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg',
                       'vol', 'amount', 'adj_factor']
            self.pre_close = self.dayDatas.loc[0, 'pre_close']
            self.open = self.dayDatas.loc[0, 'open']
            self.low = self.dayDatas.loc[0, 'low']
            self.high = self.dayDatas.loc[0, 'high']
            self.close = self.dayDatas.loc[0, 'close']
            self.change = self.dayDatas.loc[0, 'change']
            self.pct_chg = self.dayDatas.loc[0, 'pct_chg']
            self.vol = self.dayDatas.loc[0, 'vol']
            self.adj_factor = self.dayDatas.loc[0, 'adj_factor']
        return self.date


    # 获取距离今天最近的交易日，
    def getTradeDate(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        return self.datas.tradeDate(today)

    # 设定比较的均线，包括两条：长均线与短均线
    def setAvgLine(self, short, long):
        self.avgShort = short
        self.avgLong = long
        return True

    # 获取均线值，未考虑除权
    def getAvg(self, date, num):
        sql = 'select avg(close) as price from (SELECT close FROM gegu."' + \
              self.code + '" where trade_date <= \'' + date + '\' order by trade_date desc limit ' + str(
            num) + ') as a;'
        return self.db.execValue(sql)

    # 比较短期均线与长期均线的大小
    def avgVS(self, date):
        valueShort = self.getAvg(date, self.avgShort)
        valueLong = self.getAvg(date, self.avgLong)
        if valueShort > valueLong:
            return True
        else:
            return False

    # 获取当前交易日的前一个交易日
    def lastTradeDate(self, date):
        tDate = self.datas.tradeDate(self.code, date)
        sql = 'select trade_date from gegu."' + self.code + '" where trade_date < \'' + tDate + '\' order by trade_date desc limit 1'
        return self.db.execValue(sql)

    # 获取交易日的收盘价
    def getDayClose(self, day):
        codeIn = self.datas.toLongCode(self.code)
        sql = 'select close from gegu."' + codeIn + '" where trade_date <= \'' + day + "' order by trade_date desc limit 1"
        return self.db.execValue(sql)

    # 获取交易日的最高价
    def getDayHigh(self, day):
        codeIn = self.datas.toLongCode(self.code)
        sql = 'select high from gegu."' + codeIn + '" where trade_date <= \'' + day + "' order by trade_date desc limit 1"
        return self.db.execValue(sql)

    # 获取交易日的最低价
    def getDayLow(self, day):
        codeIn = self.datas.toLongCode(self.code)
        sql = 'select low from gegu."' + codeIn + '" where trade_date <= \'' + day + "' order by trade_date desc limit 1"
        return self.db.execValue(sql)

    # 获取交易日的涨幅
    def getDayPctchg(self, day):
        codeIn = self.datas.toLongCode(self.code)
        sql = 'select pct_chg from gegu."' + codeIn + '" where trade_date <= \'' + day + "' order by trade_date desc limit 1"
        return self.db.execValue(sql)

    def getDayChange(self, day):
        codeIn = self.datas.toLongCode(self.code)
        sql = 'select change from gegu."' + codeIn + '" where trade_date <= \'' + day + "' order by trade_date desc limit 1"
        return self.db.execValue(sql)

    #  所有在市场上交易的股票完整列表
    @classmethod
    def getAllStockLists(cls):
        return cls.datas.allStockList()

    @classmethod
    def getAllStockCodes(cls):
        df = cls.getAllStockLists()
        return df[['symbol']].T.values[0]

    @classmethod
    #   复权处理，采用后复权，更为准确的计算
    def complexRights(cls, df, cdata):

        pass


    # 获取收盘价
    def getPrice(self, date):
        return self.getDayClose(date)

    # 是否涨停
    def isLimitUp(self):
        pass

    # 是否跌停
    def isLimitDown(self):
        pass

    # 当天5日与20日均线交易系统的策略
    def todayVS(self, code=None):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        return self.dayVS(today, code)

    # 某天5日与20日均线交易系统的策略
    def dayVS(self, date, code=None):
        if code != None:
            self.code = code
        return self.avgSellBuy(date)

    @staticmethod
    def today():
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        return today

    # 现价是否在均线上
    def isOnAvg(self, date, avg):
        price = self.getPrice(date)
        avgs = self.getAvg(date, avg)
        if(price > avgs):
            return True
        return False

    # 判断日期是否为交易所的交易日，包括对历史数据与当前年份的所有交易日进行判断
    def isTradeDay(self, date):
        day = datetime.datetime.strptime(date, '%Y%m%d')
        sql = "select is_open from public.calendar where cal_date = '" + date + "'"
        isopen = self.db.execValue(sql)
        if isopen == 1:
            return True
        return False

    # 判断当前时间是否为交易时间,未获取交易日历数据
    def isInTradeTime(self):
        if not self.isTradeDay():
            return False
        openTime = '09:20:00'
        closeTime = '15:00:01'
        now = time.strftime('%H:%M:%S', time.localtime(time.time()))
        if(openTime < now and now < closeTime):
            return True
        return False

    # 5日在20上时持有股票，5日在20下时持有现金，5日均线向上穿越20日均线买入，5日均线向下穿越20日均线卖出
    def avgSellBuy(self, date):
        lastTradeDay = self.lastTradeDate(date)
        lastAvgShort = self.getAvg(lastTradeDay, self.avgShort)
        lastAvgLong = self.getAvg(lastTradeDay, self.avgLong)
        currentShort = self.getAvg(date, self.avgShort)
        currentLong = self.getAvg(date, self.avgLong)
        if lastAvgShort > lastAvgLong:
            if currentShort > currentLong:
                return '持有股票'
            else:
                return '卖出'
        else:
            if currentShort > currentLong:
                return '买入'
            else:
                return '持有现金'

    # 系统回测
    def testSystem(self,startday, endday, code=None):
        baseRMB = 100000
        baseShares = 0
        if code != None:
            self.code = code
        sql = 'select trade_date from gegu."' + self.code + '" where trade_date >= \'' + startday + '\' and trade_date <= \'' \
              + endday + '\' order by trade_date asc'
        results = self.db.exec(sql)
        for res in results:
            day = res[0]
            dayClose = self.getDayClose(day)
            if self.dayVS(day) == '买入':
                baseShares = baseRMB // (dayClose * 100) * 100
                baseRMB = baseRMB - baseShares * dayClose
                print(day + '----买入金额：' + str(baseShares * dayClose))
            if self.dayVS(day) == '卖出':
                baseRMB = baseRMB + baseShares * dayClose * 0.9965
                print(day + '----卖出股票：' + str(baseShares * dayClose * 0.9965))
                baseShares = 0

        endClose = self.getDayClose(endday)
        endRMB = baseRMB + baseShares * endClose
        return endRMB

    # 获取最新交易日之前的第delta个交易日价格
    def getDeltaDatePrice(self, code, date, delta):
        # today = time.strftime('%Y%m%d', time.localtime(time.time()))
        itd = self.datas.itemTradeDate(code, date)
        lcode = self.datas.toLongCode(code)
        sql = 'select close from gegu."' + lcode + '" where trade_date <= \'' \
              + itd + '\' order by trade_date desc limit 1 offset ' + str(delta)
        datas = self.db.execValue(sql)
        return datas

    #  获取区间的最高价
    def getRangeHigh(self, code, dates, datee):
        lcode = self.datas.toLongCode(code)
        sql = "select max(high) from gegu.\"" + lcode + "\" where trade_date <= '" \
              + datee + "' and trade_date >= '" + dates + "'"
        return self.db.execValue(sql)

    # 获取最某交易日之前的第delta个交易日的范围内最高价
    def getDeltaHigh(self, code, date, delta):
        sdate = self.getDeltaDate(code, date, delta)
        return self.getRangeHigh(code, sdate, date)


    #  获取区间的最低价
    def getRangeLow(self, code, dates, datee):
        lcode = self.datas.toLongCode(code)
        sql = "select min(low) from gegu.\"" + lcode + "\" where trade_date <= '" \
              + datee + "' and trade_date >= '" + dates + "'"
        return self.db.execValue(sql)

    # 获取最某交易日之前的第delta个交易日的范围内最低价
    def getDeltaLow(self, code, date, delta):
        sdate = self.getDeltaDate(code, date, delta)
        return self.getRangeLow(code, sdate, date)

    # 获取相关delta日期的交易日数据,delta为正
    def getDeltaDate(self, code, date, delta):
        lcode = self.datas.toLongCode(code)
        sql = "select trade_date from gegu.\"" + lcode + "\" where trade_date < '" \
              + date + "' order by trade_date desc limit 1 offset " + str(delta - 1)
        return self.db.execValue(sql)

    # 从数据库中获取date日期前的num数量的交易数据，返回dataframe
    def getNumDatas(self, date, num):
        sql = 'select * from ' + self.table + "where trade_date <= '" + date + "' order by trade_date desc limit " + str(num)
        res = self.db.exec(sql)
        if len(res) is 0:
            return res
        res.columns = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg',
                       'vol', 'amount', 'adj_factor']
        return res

    def getDayTop(self, order=True):
        if order:
            return True
        pass

    #  获取涨停股票
    def getZT(self, date):
        all = self.datas.allStockList()
        tdate = self.datas.tradeDate(date)
        res = []
        for item in all.values:
            self.setCode(item[1])
            self.setDate(date)
            if len(self.dayDatas) == 0:
                continue
            ztp = self.calZT(tdate)
            if self.high >= ztp and self.close == self.high:
                res.append(item[1])
        self.code = None
        return res

    #  计算涨停价格
    # 计算涨停的价格与实际涨停的价格有差异是因为刚好当天除权，这种情况不少
    def calZT(self, date):
        # 前复权 = 当日收盘价 × 当日复权因子 / 最新复权因子
        # ddate = self.getDeltaDate(self.code, date, 1)
        #         # self.setDate(ddate)
        #         # pre_factor = self.adj_factor
        self.setDate(date)
        # adj_preclose = self.pre_close * (pre_factor / self.adj_factor)
        return round(self.pre_close * 1.10, 2)

        #  获取跌停股票
    def getDT(self):
        pass

    #  计算跌停价格
    def calDT(self, date):
        sql = 'select pre_close from ' + self.table + " where trade_date = '" + date + "'"
        pre_close = self.db.execValue(sql)
        if pre_close is None:
            return None
        return round(pre_close * 0.9, 2)

    # 合并所有个股表
    def allItems2one(self):
        sql = 'insert into gegu."all" select * from gegu."000007.SZ"'
        self.db.ex(sql)




#
#
# obj = ShareItem()
# res = obj.getZT('20190603')
# print(res)
# print(obj.getNumDatas('20190326', 10))
#
# obj.getDeltaHigh('000001', ShareItem.today(), 4)
# obj.getRangeHigh('603999', '20190011' , '20190319')
