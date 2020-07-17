import json
import tushare as ts
import pandas as pd
import datetime
import time
import urllib3
from cls.orm.main import PG
# import configparser as cp


# 主要用来获取交易数据,个股更新，
class TradeDatas():

    def __init__(self, code=None):
        self.allstlist = None
        self.code = code
        self.pro = ts.pro_api('4552d85ac2d1492fc488a32646b501ed6faf1835820f65408790e59d')
        self.pg = PG()
        self.engine = self.pg.engine()

    # 单只股票最近一个交易日的日线数据
    def itemToday(self, code=None):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        try:
            df = self.pro.daily(ts_code=self.code, start_date=today, end_date=today);
            print('获取日线数据成功')
        except IOError:
            print("Error: 获取数据失败：" + self.code)
        else:  # 数据写入成功
            return df

    # 将股票代码转换为带.SZ与.SH后缀的代码
    # @ classmethod
    def toLongCode(self, code):
        codes = self.allStockList()
        df = codes[codes.symbol == code]
        if len(df) > 0:
            return df.values[0][0]
        else:
            print('股票代码错误')
            exit(1)

    # 代码转换为新浪请求参数
    def toSinaCode(self, code):
        lcode = self.toLongCode(code)
        scode = lcode[-2:].lower() + lcode[0:6]
        return scode


    # 读取与写入信息到配置文件当中
    def setConfig(self):
        pass
        # config = conpar.ConfigParser()
        # config.read("ini", encoding="utf-8")
        # config.remove_section("default")  # 整个section下的所有内容都将删除
        # config.write(open("ini", "w"))

    # 按日期返回总量的限制
    def item(self, plaincode, start, end):
        if start > end:
            return
        code = self.toLongCode(plaincode)
        try:
            df = self.pro.daily(ts_code=code, start_date=start, end_date=end)
            time.sleep(0.2)
            print('获取日线数据成功')
        except IOError:
            print("Error: 获取数据失败：" + code)
        else:  # 数据写入成功
            if len(df) == 0:
                print('获取数据为空:' + code)
                return
            try:
                df.to_sql(code, self.engine, index=False, if_exists='append', schema='gegu')  #
            except:
                print('Error:存在表:' + code)
            else:
                print('数据插入成功:' + code)

    # 从交易的第一天获取个股数据,分多次获取，每次获取3000左右数据,有点问题，应该从最后一个日期起算，而不是从第一个数据起算
    def plainItem(self, code, start='19910101'):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        day = datetime.datetime.strptime(start, '%Y%m%d')
        delta = datetime.timedelta(3999)
        nextDays = day + delta
        startStr = start
        endStr = nextDays.strftime('%Y%m%d')
        while endStr < today:
            self.item(code, startStr, endStr)
            delt = datetime.timedelta(1)
            nd = nextDays + delt
            startStr = nd.strftime('%Y%m%d')
            nextDays = nd + delta
            endStr = nextDays.strftime('%Y%m%d')
        self.item(code, startStr, today)

    def IndexDaily(self, code):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        key = 'getIndexDaily' + code + today
        jstr = self.pg.getValue(key)
        if jstr is None:
            dfs = pd.DataFrame()
            for year in range(1990, 2020, 10):
                startDate = str(year) + '0101'
                endDate = str(year + 10) + '1231'
                df = self.pro.index_weekly(ts_code=code, start_date=startDate, end_date=endDate,
                                   fields='ts_code,trade_date,open,high,low,close,vol,amount')
                if (len(dfs) > 0):
                    dfs = dfs.append(df, ignore_index=True)
                else:
                    dfs = df.copy(deep=False)
            self.pg.setValue(key, json.dumps(dfs.to_dict()))
            return dfs.sort_values(by=['trade_date'])
        else:
            return pd.DataFrame(json.loads(jstr))
        # dfs.to_sql(code, self.engine, index=False, if_exists='append', schema='gegu')


    def getIndexDaily(self, code, startDate, endDate):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        key = 'getIndexDaily' + code + startDate + endDate + today
        jstr = self.pg.getValue(key)
        if jstr is None:
            df = self.pro.index_daily(ts_code=code, start_date=startDate, end_date=endDate,
                                      fields='ts_code,trade_date,open,high,low,close,vol,amount')
            print('获取指数日线成功')
            self.pg.setValue(key, json.dumps(df.to_dict()))
        else:
            df = pd.DataFrame(json.loads(jstr)).sort_values('trade_date', ascending=False)
        return df

    def getIndexWeekly(self, code, startDate, endDate):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        key = 'getIndexWeekly' + code + startDate + endDate + today
        jstr = self.pg.getValue(key)
        if jstr is None:
            df = self.pro.index_weekly(ts_code=code, start_date=startDate, end_date=endDate,
                                       fields='ts_code,trade_date,open,high,low,close,vol,amount')
            print('获取指数周线成功')
            self.pg.setValue(key, json.dumps(df.to_dict()))
        else:
            df = pd.DataFrame(json.loads(jstr)).sort_values('trade_date', ascending=False)
        return df

    # 所有股票的完整列表，包括了上证指数以及深证指数以及创业板指数
    def allStockList(self):
        if self.allstlist is None:
            jstr = self.pg.getValue('allStockList')
            if jstr is None:
                data = self.pro.query('stock_basic', exchange='',
                                      list_status='L', fields='ts_code,name,symbol,list_date')
                print('获取股票列表成功')
                self.allstlist = data
                self.pg.setValue('allStockList', json.dumps(data.to_dict()))
            else:
                self.allstlist = pd.DataFrame(json.loads(jstr))
        return self.allstlist

    # 提取code全部复权因子
    def getAdjFactor(self, code):
        lcode = self.toLongCode(code)
        df = self.pro.adj_factor(ts_code=lcode, trade_date='')
        time.sleep(0.2)
        return df
        # 12.46

    # 更新所有表里面的复权因子
    def updateAllAdjFactor(self):
        data = self.allStockList()
        for row in data.values:
            code = row[1]
            self.updateAdjFactor(code)
        print('复权因子全部更新成功。。。。')

    # 更新单个股票的复权因子
    def updateAdjFactor(self, code):
        lcode = self.toLongCode(code)
        table = 'gegu."' + lcode + '"'
        if self.pg.isTableExist(table):
            columns = self.pg.getTableColumns(lcode)
            if 'adj_factor' not in columns:
                self.pg.addTableColumn(table, 'adj_factor')
            noneAdjDatas = self.getNoAdjFactorDatas(table)
            if len(noneAdjDatas) > 0:
                adjs = self.getAdjFactor(code)
            upSql = ''
            for one in noneAdjDatas.values:
                if len(adjs.loc[adjs['trade_date'] == one[0]]) is 0:
                    continue
                upSql = upSql + 'update ' + table + " set adj_factor = " + \
                        str(adjs.loc[adjs['trade_date'] == one[0]].values[0][2]) + \
                        ' where trade_date=\'' + one[0] + '\';'
            if upSql != '':
                self.pg.ex(upSql)
                print(table + '更新成功')

    # 获取没有复权因子的日期数据
    def getNoAdjFactorDatas(self, table):
        sql = 'select trade_date from ' + table + "where adj_factor is null order by trade_date desc"
        res = self.pg.exec(sql)
        if len(res) is 0:
            return res
        return res

    # 更新所有股票列表，最好每天更新一次
    def updateStockList(self):
        self.pg.delValue('allStockList')
        data = self.pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,name,symbol,list_date')
        print('获取股票列表成功')
        self.allstlist = data
        return self.pg.setValue('allStockList', json.dumps(data.to_dict()))

    # 从所有股票中挑选出创业板股票
    def getCYMarket(self):
        all = self.allStockList()
        res = all.loc[(all['symbol'] >= '300000') & (all['symbol'] <= '300999')].reset_index(drop=True)
        return res

    # 排除创业板股票
    def notCYMarket(self, df):
        res = df.loc[(df['symbol'] < '300000') | (df['symbol'] > '309999')].reset_index(drop=True)
        return res

    # 从所有股票中挑选出次新股,上市后1年内的新股
    def getSubnewMarket(self):
        res = self.ddaysShare(-250)
        return res

    #  排除次新股
    def notSubnewMarket(self, df):
        end = self.ddays(-250)
        # df = self.allStockList()
        return df[df.list_date < end].reset_index(drop=True)

    # 距离当前日期ddays天内，上市交易的股票列表
    def ddaysShare(self, ddays):
        start = self.ddays(ddays)
        df = self.allStockList()
        return df[df.list_date > start].reset_index(drop=True)

    # 返回距离当前日期ds天的日期，可以为正，也可以为负
    def ddays(self, ds):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        day = datetime.datetime.strptime(today, '%Y%m%d')
        delta = datetime.timedelta(days=ds)
        dd = day + delta
        strfDay = dd.strftime('%Y%m%d')
        return strfDay

    # 每日的交易数据入库
    def allDaily2sql(self):
        data = self.allStockList()
        for row in data.values:
            lcode = self.toLongCode(row[1])
            # 如果表不存在，则通过接口获取新数据
            if not self.pg.isTableExist('gegu."' + lcode + '"'):
                self.plainItem(row[1])
        print('获取数据成功')

    # 获取每日技术指标数据并入库
    def dailyTechTarget(self):
        df = self.pro.daily_basic(ts_code='', trade_date='20140227', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
        startDate = ''
        today = time.strftime('%Y%m%d', time.localtime(time.time()))   # 格式为20190221
        data = self.allStockList()
        for row in data.values:
            try:
                # pro.daily_basic(ts_code='', trade_date='20180726',fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
                df = self.pro.daily(ts_code=row[0], start_date=startDate, end_date=today);
            except IOError:
                print("Error: 获取数据失败：" + row[1])
            else:  # 数据写入成功
                print('获取数据成功:' + row[1])
                try:
                    df.to_sql(row[1], self.engine, index=False, if_exists='fail', schema='index')  #
                except:
                    print('Error:存在表:' + row[1])
                else:
                    print('数据插入成功:' + row[1])
        return 0

    # 股票实时行情数据，采用新浪的接口
    # 上证：
    # http://hq.sinajs.cn/list=sh600115
    # 深证：
    # http://hq.sinajs.cn/list=sz002681
    def realTimePrice(self, codeArr):
        http = urllib3.PoolManager()
        for i in range(0, len(codeArr)):
            codeArr[i] = self.toSinaCode(codeArr[i])
        scodeStr = ",".join(codeArr)
        res = http.request("GET", "http://hq.sinajs.cn/list=" + scodeStr)
        strRes = res.data.decode('gb2312')
        itemArr = strRes.split(';\n')
        itemArr.pop()
        dfs = pd.DataFrame()
        for strRes in itemArr:
            spStr = strRes.split('"', 1)
            arr = spStr[1].split(',', 14)
            lcode = self.toLongCode(spStr[0][13:19])
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            dic1 = {'ts_code': [lcode], 'trade_date': [today],
                    'open': [arr[1]],'high':[arr[4]],'low':[arr[5]],'close':[arr[3]],
                    'pre_close':[arr[2]],'change':[float(arr[3])-float(arr[2])],
                    'pct_chg':round((float(arr[3])-float(arr[2]))/float(arr[2]),4),  # 单位为手
                    'vol':round(float(arr[8])/100),'amount':float(arr[9])/10000}  # 单位为万
            df = pd.DataFrame(dic1)
            if(len(dfs) > 0):
                dfs = dfs.append(df, ignore_index=True)
            else:
                dfs = df.copy(deep=False)
        return dfs

    # 获取个股中离输入日期最近的交易日
    def itemTradeDate(self, code, date):
        self.code = self.toLongCode(code)
        sql = 'select trade_date from gegu."' + self.code + '" where trade_date <= \'' + date + '\' order by trade_date desc limit 1'
        value = self.pg.exec(sql)
        return value[0][0]

    # 获取交易所中离输入日期最近的交易日
    def tradeDate(self, date):
        # self.code = self.toLongCode(code)
        sql = "select cal_date from calendar where cal_date <= '" + date + "' and is_open = 1 order by cal_date desc limit 1 "
        return self.pg.execValue(sql)

    # 判断日期是否为交易所的交易日，包括对历史数据与当前年份的所有交易日进行判断
    def isTradeDay(self, date):
        day = datetime.datetime.strptime(date, '%Y%m%d')
        sql = "select is_open from public.calendar where cal_date = '" + date + "'"
        isopen = self.pg.execValue(sql)
        if isopen == 1:
            return True
        return False

    # 返回日期范围内的交易日历信息
    def updateTradeCalendar(self):
        # 由于每次获取的条数有限制，所以分两次操作
        self.pg.clearTable('public.calendar')
        cal = self.pro.trade_cal(exchange='', start_date='19910101', end_date='20111231')
        cal.to_sql('calendar', self.pg.engine(), index=False, if_exists='append', schema='public')
        cal2 = self.pro.trade_cal(exchange='', start_date='20120101', end_date='20221231')
        cal2.to_sql('calendar', self.pg.engine(), index=False, if_exists='append', schema='public')
        print('获取交易日历成功')
        return True

    # 单只股票更新到最新的日线交易数据
    def updateStock(self, code=None):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        lcode = self.toLongCode(code)
        # 如果表存在，找到最后更新的日期，从下一个日期开始更新数据,直接从头开始下载数据并入库
        if self.pg.isTableExist('gegu."' + lcode + '"'):
            date = self.itemTradeDate(code, today)
            day = datetime.datetime.strptime(date, '%Y%m%d')
            delta = datetime.timedelta(days=1)
            nextDay = day + delta
            self.item(code, nextDay.strftime('%Y%m%d',), today)
        else:
            self.plainItem(code)

    #  每日数据更新，包括股票列表、股票音交易日历、以及日线行情数据
    def dailyUpdate(self):
        self.updateStockList()
        self.updateTradeCalendar()
        self.updateAll()
        self.updateAllAdjFactor()

    # 更新所有A股市场的数据
    def updateAll(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        if self.isTradeDay(today):
            data = self.allStockList()
            for row in data.values:
                self.updateStock(row[1])
        else:
            print("非交易日，请在交易日进行数据更新")
            return False
        print('数据更新成功')
        return True

# obj = TradeDatas()
# obj.updateAllAdjFactor()
# obj.allStockList()
# obj.updateAll()
# print(obj.notCYMarket())
# obj.updateStock('002032')
# obj.updateTradeCalendar()
# dfs = obj.realTimePrice(['000001','600115'])
