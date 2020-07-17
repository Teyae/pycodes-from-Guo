import time
from cls.finance.stock import ShareItem
from cls.finance.system.system import TradeSystem

# 核心思想在于人对于时间周期的敏感，以及现有时间的特点，一般以5日左右为一个调整或者下跌周期，控制亏损，让利润奔腾
# 仓位控制是一方面，还有一方面是对于止损策略的调整，来实现现有系统的
# 止损：1 超出前高，日线破5日线止损 2 连续8个交易日未超出前高，则择机或者直接退出，收盘价破4日调整最低则退出
# 目前还只考虑了价格的关系，未考虑成交量
# 选择缓步上涨型，拉升后暂停型，量能放大型，属于比较典型的牛市类型策略
# 关键还是对进行股票进行分类，对于大盘的同步性，牛市、熊市、震荡市的不同特点
# 对于明显顶部的调整，不如不买
# 设定多个因子，比较量能因子，均线因子，整体市场因子、图形因子
# 这里面赚的钱是属于贪婪的钱，个股被人注意到了后，参与的资金与人气越来越高，一波调整后，继续有下一波上冲，所以控制亏损，让利润奔腾
# 绝大部分情况，在4日调整的情况下，已经达到一个最低价
# 其中一个因子前面20个交易日是需要强于大盘
# 对于4日调整时有大跌或者大涨时，处于在排序的后面
# 如果买入后5个交易日未创新高，则卖出
# 20日线下的股票不考虑
# 需要考虑强于大盘的股票
# 优先：1 股吧排名名显上升的排序优先 2 大盘下跌时强于大盘股票优先

class WaveSystem(TradeSystem):

    def __init__(self):
        self.testdate = '20190517'   # 测试日期
        self.listNun = 50  # 获取满足条件的个股数据限制
        self.share = ShareItem()

    # 获取股票代码，对于特定的板块，且排除一些次新股等，或者选择创业板
    def getList(self):
        allItems = self.share.datas.allStockList()
        # allItems = self.share.datas.getCYMarket()
        cyItems = self.share.datas.notSubnewMarket(allItems)
        itemsArr = cyItems[['symbol']].T.values[0]
        res = []
        for code in itemsArr:
            # if code == '300762':
            #     break
            if self.isOnline(code):
                res.append(code)
            if len(res) == self.listNun:
                # print(code)
                break
        return res


    # 是否满足最主要的技术条件，创新高后连续4日调整，即出现买点
    def isOnline(self, code):
        shortDay = 4
        longDay = 21
        self.share.code = code
        tdate = self.share.datas.itemTradeDate(code, self.testdate)
        ddate = self.share.getDeltaDate(code, tdate, shortDay)
        d5high = self.share.getDayHigh(ddate)  # 前4天的最高价
        hv10 = self.share.getDeltaHigh(code, tdate, longDay)  # 前一个月的最高价
    #     判断逻辑：前21天的最高价与前4日是最高价相同时，即为上涨后调整了5日
        if d5high == hv10:
            return True
        return False

    #  过滤系统，对挑选出来的个股，做一些条件限制，排除不能操作的个股,主要侧重于技术指标
    #  过滤掉ST，以及最大成交量大阴线下跌，即主力出逃股
    #  不考虑次新股
    #
    def filter(self, res):
        pass

    # 去除停牌股票，去除高风险股票
    def exceptItems(self):
        pass

    # 对符合条件的个股进行优先度排序，最后按照优先顺序进行买卖
    # 前期连续小阳线，5日或者10日线上缓步上涨股最优先
    # 不考虑基本面
    # 考虑布林线
    def sort(self, res):
        pass

    #  核心逻辑
    def start(self):
        res = self.getList()
        exceptRes = self.exceptItems(res)
        fRes = self.filter(exceptRes)
        sRes = self.sort(fRes)
        return sRes


    # 连续小涨的股票（前15天连续红盘的概率在0.75以上），第一次调整后为买点
    def getSeriesRed(self, timeperiods = 20, date=None ):
        if date is None:
            td = time.strftime('%Y%m%d', time.localtime(time.time()))
        else:
            td = date
        allItems = self.share.datas.allStockList()
        itemsArr = allItems[['symbol']].T.values[0]
        res = []
        for code in itemsArr:
            print('开始测试，股票代码' + code)
            if self.isSeriesRed(code, td, timeperiods - 4):
                res.append(code)
            if len(res) == self.listNun:
                # print(code)
                break
        return res


    # 判断个股在某个时间前是否为连续红盘,平均红盘变动小于3%
    def isSeriesRed(self, code, date, periods):
        self.share.setCode(code)
        sdatas = self.share.getNumDatas(date, periods)
        if len(sdatas) < periods:   # 排除新股等
            return False
        sdatas['red_pct'] = (sdatas['close'] - sdatas['open']) / sdatas['pre_close']
        if sdatas['pct_chg'].mean() > 2:  # 排除平均涨幅大的，比如刚上市的股票
            return False
        if len(sdatas.loc[(sdatas['red_pct'] > 0) | (sdatas['pct_chg'] > 0)]) / len(sdatas) > 0.85:
            return True
        return False
        # exit(2)
        # if len(sdatas.loc[sdatas['red_pct'] > 0 | )) / len(sdatas) > 0.8:
        #     return True
        # return False

    #  获取均线数据
    def getDatasAvg(self, datas, date, num):
        index = eval(datas.loc[(datas['trade_date'] == date)].index[0])
        end = index + num
        if end > len(datas):
            end = len(datas)
        return datas[index:end].mean()['pct_chg']

    #  成交量分析
    def volumePriceAnalysis(self):
        pass







# o = WaveSystem()
# res = o.getList()
# print(res)

# res = o.isSeriesRed('000501', '20190414', 16)
# print(res)