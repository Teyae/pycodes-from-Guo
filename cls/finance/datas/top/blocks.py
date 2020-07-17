
import time
# from lxml import etree
import pandas as pd
from cls.orm.main import PG
from cls.finance.datas.top.top import TopList

# 热门板块以一个季度为周期
# http://quote.eastmoney.com/centerv2/hsbk 可见页面
class HotBlocks(TopList):

    def __init__(self):

        TopList.__init__(self)
        self.token = '894050c76af8597a853f5b408b759f5d'
        self.setUrl()


    def setUrl(self):
        # 获取板块代码的URL
        self.url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?' \
                  'cb=&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=1&ps=40&_='
        return self.url

    # 获取板块的个股url
    def setiUrl(self, block , page=1):
        self.iUrl = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C.' + block + \
                    '&type=ct&st=(ChangePercent)&sr=-1&ps=50&js=var%20BrcBMwKx={pages:(pc),data:[(x)]}&p=' + str(page) +  \
                    '&sty=DCFFITA&rt=51806875&token=' + self.token
        return self.iUrl


    def getToken(self):
        return self.token

    # 获取上涨排名前20的热门股票
    def getHotBlocks(self):
        res = self.http.request("GET", self.url)
        itemArr = res.data.decode('utf-8')[3:-3].split('","')
        bcodesArr = []
        for strRes in itemArr:
            print(strRes)
            barr = strRes.split(',')
            bcodesArr.append(barr[1])
        return bcodesArr

    #  获取所有的概念板块
    # http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240060446341753880084_1555500084076&type
    # =CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=1&ps=20&_=1555500084268
    # http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112407748847854654342_1559615589555&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=2&ps=20&_=1559615591697
    def getAllConceptBlocks(self):
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery11240060446341753880084_1555500084076&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FPGBKI&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._BKGN&st=(ChangePercent)&sr=-1&p=1&ps=20&_=1555500084268'
        resArr = []
        for page in range(1, 11):
            url = url + str(page)
            res = self.http.request("GET", url).data.decode('utf-8')
            itemArr = res[res.find('[') + 2:res.find(']') - 1].split('","')
            for item in itemArr:
                arr = item.split(',', 10)
                numsArr = arr[6].split('|')
                blockarr = [arr[1], arr[2], arr[3], arr[5], numsArr[0], numsArr[2]]
                resArr.append(blockarr)
            df = pd.DataFrame(resArr)
            df.columns = ['bcode', 'name', 'pct_change', 'turnover', 'rise_num', 'fall_num']
        return df




    #  获取所有的行业板块
    def getIndustriesBlocks(self):
        pass

    # 获取版块中排在前面的个股
    def getTopItems(self, bItems):
        pass

    #  获取板块的所有个股
    def getBlockItems(self, block, concetp = False):
        pages = 1000
        page = 1
        bitems = []
        while page < pages + 1:
            self.setiUrl(block + '1', page)  # 板块代码都带有一个后缀1
            if concetp:
                self.setiUrl(block, page)  # 板块代码都带有一个后缀1
            res = self.http.request("GET", self.iUrl)
            time.sleep(0.05)
            itemsStr = res.data.decode('utf-8')
            if len(bitems) == 0:
                pages = int(itemsStr[20:itemsStr.find(',')])
            dataStr = itemsStr[itemsStr.find('['):itemsStr.find(']') + 1]
            dataArr = eval(dataStr)
            for item in dataArr:
                itemDateArr = item.split(',')
                bitems.append(itemDateArr[1])
            page += 1
        return bitems

    # 获取版块的指数,行业版块代码需要加1
    # http://quote.eastmoney.com/web/BK08301.html 可视页面地址，从页面中查找接口
    # rtntype=5&isCR=false&fsData1555500682606_69241144=fsData1555500682606_69241144
    def getBlockIndex(self, bkName):
        url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=' + bkName + \
              '&TYPE=K&js=fsData1555500682606_69241144((x))' \
              '&rtntype=5&isCR=false&fsData1555500682606_69241144=fsData1555500682606_69241144'
        res = self.http.request("GET", url).data.decode('utf-8')
        itemArr = eval(res[(res.find('({') + 1):-1].replace('false', '"false"'))
        dict = []
        yestodayIndex = 1000
        for dayStr in itemArr['data']:
            arr = dayStr.split(',')
            if len(arr) < 9:
                continue
            arr.append(round((float(arr[2]) - yestodayIndex)/yestodayIndex * 100, 2))
            dict.append(arr)
            yestodayIndex = float(arr[2])
        df = pd.DataFrame(dict)
        df.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'turnover', 'amplitude', 'turnrate', 'chg_pct']
        return df

    def getBlockHotestItems(self):
        res = []
        codeArr = self.getHotBlocks()
        for code in codeArr:
            items = self.getBlockItems(code)
            res = res + items
        return res

    # 获取两个板块的交集
    def inter(self, block1, block2):
        return list(set(block1).intersection(set(block2)))

    def saveBlockDatas(self):
        blocks_df = self.getAllConceptBlocks()
        for block in blocks_df['bcode'].T:
            dfIndex = self.getBlockIndex(block + '1')
            dfIndex['bcode'] = block
            table = 'block_index'
            dfIndex.to_sql(table, self.engine, index=False, if_exists='append', schema='index')  #
        return True





o = HotBlocks()
o.saveBlockDatas()
# res = o.getAllConceptBlocks()
# BK05961  融资融券
# BK08171 昨日触板
# res1 = o.getBlockItems('BK05961', True)
# res2 = o.getBlockItems('BK08171', True)
# res = o.inter(res1, res2)
# print(res)
# res = o.getBlockIndex('BK05961')
# print(res.tail(10).loc[569])
# print(res[['date', 'close', 'chg_pct']])
# l1 = len(res)
# l2 = len(res.loc[res['open'] > res['close']])
# print(l1)
# print(l2)
# print(1-l2/l1)

# print(o.getBlockItems('BK0830'))
# o.getBlockHotesItems()