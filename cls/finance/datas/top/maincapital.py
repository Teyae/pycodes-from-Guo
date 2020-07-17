import time
import pandas as pd
from .....cls.finance.datas.top.top import TopList


# 主力净流入排名
# 主要是：超大单加大单买入成交额之和
# 一种买占，长上影线，说明主力买入，而散户没意识到，这是一个比较确定的买点


class CapitalMain(TopList):

    def __init__(self):

        TopList.__init__(self)
        self.baseUrl = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(BalFlowNetRate)&p=1&js=var%20WzKgjeXl={pages:(pc),data:[(x)]}&cmd=C._AB&sty=DCFFITAM&rt=51740674'

        # 按当日主力净占比排序
        # 获取列表后，自己来判断创业，主板等
        # self.baseUrl = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(BalFlowNetRate)&sr=-1&' \
        #                'p=1&ps=50&js=var%20uAnaNxqa={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51737137'
        #
        # # 5日流入排行
        # self.baseUrl = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(FFRank5)&sr=1&p=1&ps=50&' \
        #                'js=var%20MtgWvIuf={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51737867'
        self.dkey = 'capitalupdatedate'

    # 先从基本页面获取token
    def getWebToken(self):
        token = '894050c76af8597a853f5b408b759f5d'
        return token

    def parse(self, res):
        resStr = TopList.parse(self, res)
        pstart = resStr.find('["') + 2
        pend = resStr.find('"]')
        itemArr = resStr[pstart:pend].split('","')
        lstRes = []
        for item in itemArr:
            arrs = item.split(',')
            lstRes.append(arrs)
        lstRes = pd.to_numeric(lstRes, errors='ignore')
            # "1,601865,福莱特,10.93,99.65,1,9.96,75.69,1,60.97,75.01,1,159.00,玻璃陶瓷,BK05461,2019-03-07 15:00:00",
        df = pd.DataFrame(lstRes, columns=['type', 'code', 'name', 'cprice','ratio', 'ranking', 'iratio',
                                           'ratio5', 'ranking5', 'iratio5', 'ratio10', 'ranking10','iratio10', 'block', 'bcode', 'time'])
        # df = pd.to_numeric(df.values, errors='ignore')
        return df


    def urlSet(self):
        token = self.getWebToken()
        # url = TopList.urlSet(self)
        url = self.baseUrl
        url += '&token=' + token
        url += '&sr=' + self.order
        url += '&ps=' + str(self.itemNum)
        return url

    def getLists(self):
        url = self.urlSet()
        res = self.http.request('GET', url)
        df = self.parse(res)
        df[['cprice','ratio', 'iratio','ratio5', 'iratio5', 'ratio10','iratio10']] = \
            df[['cprice', 'ratio', 'iratio', 'ratio5', 'iratio5', 'ratio10', 'iratio10']]\
                .replace('-', -100).astype(float)
        # df['tradedate'] = time.strftime('%Y%m%d ', time.localtime(time.time()))
        return df

        # lst = json.loads(resStr)
        # df = json_normalize(lst)


# obj = CapitalMain()
# pg = obj.save2sql('capital')



