# import sys
# sys.path.append('D:/pychon/pycodes')
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cls.orm.main import PG
from cls.finance.stock import ShareItem


# 依据股吧的操作，依据多日热度，保留每日数据进行验证，与大盘的连动
# 至少在20日线上
class GubaSelected(object):

    def __init__(self):
        self.table = 'gubahot'
        self.gubaUrl = 'http://guba.eastmoney.com/remenba.aspx'
        option = Options()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(options=option)
        self.driver.get(self.gubaUrl)
        time.sleep(0.5)  # sleep一下，否则有可能报错
        self.items = None

    def __del__(self):
        self.driver.close()

    def getHotestItem(self):
        return self.getTop30()

    # 获取最热门的30个股
    def getTop30(self):
        # if not self.items is None:
        #     return self.items
        lis = self.driver.find_elements_by_xpath('//div[@class="zhutibarlist"]//li/a')
        codes = []
        for i in lis:
            codes.append(i.get_attribute('href')[-11:-5])
        self.items = codes
        print('获取股吧热门股票成功')
        return codes

    #  获取个股的序号值
    def getItemSerial(self, code):
        url = 'http://guba.eastmoney.com/list,' + code + '.html'
        self.driver.get(url)
        em = self.driver.find_element_by_xpath('//span[@class="bar_rank"]/em')
        if em is None:
            return None
        return em.text


    # 获取当天的热门股票,或者查询历史数据
    def getDayItems(self, date):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        if date is today:
            return self.getTop30()
        stoObj = ShareItem()
        if stoObj.isTradeDay():
            resf = self.getForenoon(date)
            resa = self.getAfterNoon(date)
            if len(resa) > 0:
                return resf.append(resa, ignore_index=True)
            else:
                return resf
        else:
            return self.getAfterNoon(date)

    # 更新存储当天的热门股票,在任务中应该更新两次，一次是12：50，另一次是在23：50
    def updateNow(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        res = self.getTop30()
        line = {'code': res}
        df = pd.DataFrame(line)
        df['order'] = range(1, len(res) + 1)
        df['date'] = today
        df['time'] = today + time.strftime(' %H:%M:%S', time.localtime(time.time()))
        pg = PG()
        df.to_sql(self.table, pg.engine(), index=False, if_exists='append', schema='public')  #
        return True

    def schUpdate(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        stoObj = ShareItem()
        if not stoObj.isTradeDay(today):
            now = time.strftime('%H:%M:%S', time.localtime(time.time()))
            if now < '20:00:00':
                return None
        return self.updateNow()

    # 删除当天之前更新的数据，避免重复
    def delToday(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        sql = 'delete from ' + self.table + "where date = " + today
        pg = PG()
        if pg.isTableExist('public."' + self.table + '"'):
            self.pg.ex(sql)
        return True

    # 更新两次，12:50更新一次，23:40更新一次
    def save2sql(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        codes = self.getTop30()
        line = {'code': codes}
        df = pd.DataFrame(line)
        df['order'] = range(1, len(codes) + 1)
        df['date'] = today
        df['time'] = today + time.strftime(' %H:%M:%S', time.localtime(time.time()))
        pg = PG()
        df.to_sql(self.table, pg.engine(), index=False, if_exists='append', schema='public')  #
        return True

    def close(self):
        self.driver.close()

    # 对个股进行排序、排除，主要考虑流通股市值与之前的排序，前三日的涨跌幅，成交量
    def sort(self, items):
        for i in items:
            pass

    # 上午约12：50更新,先判断是
    def getForenoon(self, date):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        whereClause = "time > '" + (date + " 00:00:00'") + " and time < '" + date + " 15;00:00'"
        sql = 'select * from ' + self.table + ' where ' + whereClause
        res = PG().exec(sql)
        if len(res) > 0:
            return res
        if date == today:
            return self.getTop30()
        return None

    # 下午约23：50更新
    def getAfterNoon(self, date: str):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        whereClause = "time > '" + (date + " 15:00:00'") + " and time < '" + date + " 23:59:59'"
        sql = 'select * from ' + self.table + ' where ' + whereClause
        res = PG().exec(sql)
        if len(res) > 0:
            return res
        if date == today:
            return self.getTop30()
        return None

    # 依据n天的热门程度进行排序
    def hotDays(self,nday):
        pass


guba = GubaSelected()
guba.save2sql()
# guba.getItemSerial('000725')
