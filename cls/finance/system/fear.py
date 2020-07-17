import time
from cls.finance.stock import ShareItem
from cls.finance.system.system import TradeSystem
from cls.finance.datas.top.blocks import HotBlocks


# 设立恐惧模型，主要为超跌，一些特殊事件的影响，对于板块，对于个股等。
# 也可以理解为上涨途中的恐惧，如中途突然大跌或者跌停，次日又大涨时得到确认，进入时还是应该在大跌是进入
# 可能出现在大热的板块，在大幅上涨后的，突然调整，后续又继续上涨
# 空中加油


class FearSystem(object):

    def __init__(self):
        self.stock = ShareItem()
        self.date = self.stock.today()

    def setDate(self, date):
        self.date = date

    def getAll(self, date):
        all = self.stock.datas.allStockList()
        tdate = self.stock.datas.tradeDate(date)
        res = []
        for item in all.values:
            self.stock.setCode(item[1])
            self.stock.setDate(tdate)
            if len(self.stock.dayDatas) == 0:
                continue
            close = self.stock.pre_close
            highMax = round(close * 1.07, 2)
            if self.stock.high >= highMax and self.stock.close <= self.stock.high - 0.02 * close:
                res.append(item[1])
        return res



obj = FearSystem()
block = HotBlocks()
rzrq = block.getBlockItems('BK05961', True)
res = obj.getAll('20190603')
interRes = block.inter(res, rzrq)
print(interRes)

