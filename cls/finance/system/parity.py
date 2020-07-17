

# 比价系统，主要对比与在各个阶段的相对涨跌幅度。
# 选择在某个阶段涨幅较小的个股进行潜伏，拉升后立马出来，然后潜伏到另外的板块或者个股。
# 个股选择时考虑基本面
class ParitySystem(object):

    def __init__(self):
        tradeDate = None
        self.startDate = None
        self.endDate = tradeDate
        pass

    # 当天与大盘的比较，涨跌幅
    def index(self, code):
        pass

    # 时间段内与大盘的比较
    def periodIndex(self, dates, datee):
        pass

    # 时间段内与个股的比较
    def periodItem(self, code, dates, datee):
        pass


