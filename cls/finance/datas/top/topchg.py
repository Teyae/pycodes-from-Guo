
import time
import json
import urllib3
import pandas as pd
from cls.finance.datas.top.top import TopList

class TopChange(TopList):

    def __init__(self):
        self.riseNum = 200
        self.fallNum = 20
        self.url = None
        # self.http = urllib3.PoolManager() 父类中有了

    def setUrl(self, num, rise):
        baseUrl = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?' \
                   'page=1&sort=changepercent&node=hs_a&symbol=&_s_r_a=sort'
        if rise:
            addStr = '&asc=0&num=' + str(num)
        else:
            addStr = '&asc=1&num=' + str(num)
        self.url = baseUrl + addStr
        return self.url

    #  获取新浪接口排序数据
    def getSortList(self, num, rise=True):
        self.setUrl(num, rise)
        res = self.http.request("GET", self.url)
        itemArr = res.data.decode('gb2312')[2:][:-2].split('},{')
        dfs = pd.DataFrame()
        for strRes in itemArr:
            tpos = strRes.find('ticktime')
            tStr = strRes[tpos+10:tpos+18]  # 时间字符串单独处理
            dictStr = '{"' + strRes.replace(tStr, '').replace(':', '":[').replace(',', '],"') + ']}'
            df = pd.DataFrame(json.loads(dictStr))
            df['ticktime'] = tStr
            dfs = dfs.append(df, ignore_index=True)
        subdf = dfs[['code', 'open', 'high', 'low','trade',  'pricechange', 'changepercent','volume', 'amount']]
        subdf.columns = ['ts_code',  'open', 'high', 'low', 'close',  'change', 'pct_chg', 'vol', 'amount']
        # 'trade_date','pre_close',
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        subdf[['trade_date']] = today
        subdf[['pre_close']] = 0
        return subdf


    def getTopRise(self):
        return self.getSortList(self.riseNum)

    def getTopFall(self):
        return self.getSortList(self.fallNum, False)

    def getLists(self):
        rise = self.getTopRise()
        fall = self.getTopFall()
        return rise.append(fall, ignore_index=True)


o = TopChange()
print(o.getTopFall()[0])

# res.columns = ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount']
#              ['code', 'open', 'high', 'low','trade',  'pricechange', 'changepercent','volume', 'amount']
# ['symbol', 'code', 'name', 'trade', 'pricechange', 'changepercent', 'buy', 'sell', 'settlement', 'open', 'high', 'low', 'volume', 'amount','ticktime', 'per', 'pb', 'mktcap', 'nmc', 'turnoverratio']