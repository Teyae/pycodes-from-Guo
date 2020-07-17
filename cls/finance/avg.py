# from cls.finance.stock import ShareItem
import pandas as pd

class Average(object):

    def __init__(self):
        self.share = None
        pass

    # 获取均线值，未考虑除权
    def getAvg(self, date, num):
        sql = 'select avg(close) as price from (SELECT close FROM gegu."' + \
              self.code + '" where trade_date <= \'' + date + '\' order by trade_date desc limit ' + str(
            num) + ') as a;'
        return self.db.execValue(sql)

    @classmethod
    def getDatasAvg(self, datas, date, num):
        index = eval(datas.loc[(datas['trade_date'] == date)].index[0])
        end = index + num
        if end > len(datas):
            end = len(datas)
        return datas[index:end].mean()['close']

    @classmethod
    def calMA(self, datas, date, num):
        dfs = pd.Dataframe()
        index = eval(datas.loc[(datas['trade_date'] == date)].index[0])
        end = index + num
        for index, row in datas.iterrows():
            rd = pd.DataFrame(row)
        if end > len(datas):
            end = len(datas)
        return datas[index:end].mean()['close']


    # 时间段内在num日均线上的天数
    def onAvgDays(self, dates, datee, num)->int:
        # res =
        # obj = ShareItem('000001')
        # print(obj.getNumDatas('20190326', 10))
        pass

