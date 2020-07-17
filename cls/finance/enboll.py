from cls.finance.stock import Share

# 增强布林线
class EnBoll(Share):

    # MB =（N－1）日的MA
    # UP = MB + 2×MD
    # DN = MB－2×MD
    # 计算标准着，从数据库查询时就直接进行计算
    def getMD(self, num):
        sql = 'select stddev_samp(close) from (select close from gegu."' + self.code + '" order by trade_date limit '+str(num)+') as t'
        return self.db.execValue(sql)

    def getMB(self):
        newestTradeDate = self.tradeDate()
        # today = self.today()
        lastTradeDate = self.lastTradeDate(newestTradeDate)
        avg = self.getAvg(lastTradeDate, 20)
        return avg

    def getUP(self):
        up = self.getMB() + 2 * self.getMB()
        return up


    def getDOWN(self):
        down = self.getMB() - 2 * self.getMB()
        return down





