
from cls.finance.avg import Average
from cls.finance.stock import ShareItem


# 指数分析，主要分析指数的趋势变化，
class IndexAnaly():

    def __init__(self):
        pass

    #
    def getIndex(self):
        item = ShareItem()
        # return item.datas.index('399006.SZ')
        return item.datas.getIndexDaily('000001.SH', '20130101', '20191231')
        # return item.datas.getIndexWeekly('000001.SH', '20090101', '20191231')

    # 统计指数，在时间段内依据均线进行统计，
    def statistic(self, dates, datee):
        ma = 20
        success = 0
        sd = 0
        succRatio = 0
        fail = 0
        fd = 0
        failRatio = 0
        dvalue = 0
        datas = self.getIndex()
        base = datas.values[len(datas) - 1][2]
        ma5 = base
        isOnline = True
        days = 0
        for index, row in datas.sort_values(by=['trade_date']).iterrows():
            ma5 = Average.getDatasAvg(datas, row['trade_date'], ma)
            days = days + 1
            if isOnline:
                if ma5 > row['close']:
                    delta = row['close'] - base
                    ratio = round(delta / base * 100, 2)
                    if delta > 0:
                        # print('off:' + row['trade_date'] + '   succ   ' + 'days:' + str(days) + '  ratio:' + str(ratio))
                        success = success + 1
                        sd = sd + days
                        succRatio = succRatio + abs(ratio)
                    else:
                        print('off:' + row['trade_date'] + '   fail   ' + 'days:' + str(days) + '  ratio:' + str(ratio))
                        fail = fail + 1
                        fd = fd + days
                        failRatio = failRatio + abs(ratio)
                    isOnline = False
                    base = row['close']
                    days = 0
            else:
                if ma5 < row['close']:
                    delta = row['close'] - base
                    ratio = round(delta / base * 100, 2)
                    if delta < 0:
                        # print('on :' + row['trade_date'] + '   succ   ' + 'days:' + str(days) + '  ratio:' + str(ratio))
                        success = success + 1
                        sd = sd + days
                        succRatio = succRatio + abs(ratio)
                    else:
                        print('on :' + row['trade_date'] + '   fail   ' + 'days:' + str(days) + '  ratio:' + str(ratio))
                        fail = fail + 1
                        fd = fd + days
                        failRatio = failRatio + abs(ratio)
                    isOnline = True
                    base = row['close']
                    days = 0
            # v1 = v2; v2 = v3; v3 = v4; v4 = row['close']
        print('统计数量' + str(len(datas)))
        print('成功次数：' + str(success) + '   失败次数：' + str(fail))
        print('成功天数：' + str(sd) + '   失败天数：' + str(fd))
        print('成功总比率：' + str(succRatio) + '   失败总比率：' + str(failRatio))
        return [success, fail , sd , fd]

o = IndexAnaly()
print(o.statistic('a', 'b'))
