from cls.finance.stock import Share
from cls.finance.datas.tudata import TradeDatas

class Chan(Share):

    def __init__(self, code=None):
        self.__init__(code)
        self.td = TradeDatas()

    def dingSimple(self, date):
        datas = self.td.item(self.code)

    def diSimple(self):
        pass
