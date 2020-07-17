from cls.finance.datas.top.top import TopList

# 个股资金流排序
class CapitalItem(TopList):


    def __init__(self):
        self.__init__()


        # 依据净买入资金量
        self.baseUrl = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,' \
                       'sortType=JmMoney,startDate=2019-03-08,endDate=2019-03-08,gpfw=0,js=var%20data_tab_1.html?rt=25868523'
        # 依据涨幅排序
        self.baseUrl = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page=1,sortRule=-1,' \
                       'sortType=Chgradio,startDate=2019-03-06,endDate=2019-03-07,gpfw=0,js=var%20data_tab_2.html?rt=25868536'

        # 依据总成交额
        self.baseUrl = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page=1,sortRule=-1,' \
                       'sortType=ZeMoney,startDate=2019-03-06,endDate=2019-03-07,gpfw=0,js=var%20data_tab_2.html?rt=25868537'

        # 依据净买额成交占比
        self.baseUrl = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page=1,sortRule=-1,' \
                       'sortType=JmRate,startDate=2019-03-06,endDate=2019-03-07,gpfw=0,js=var%20data_tab_2.html?rt=25868539'




