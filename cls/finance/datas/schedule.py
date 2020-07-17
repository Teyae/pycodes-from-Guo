import sys
import time
from cls.finance.datas.tudata import TradeDatas
from cls.finance.datas.top.tiger import TigerData
from cls.finance.datas.top.guba import GubaSelected
from apscheduler.schedulers.background import BackgroundScheduler

class DataSchedule():

    def __init__(self):
        self.tudata = None
        self.guba = None
        self.tiger = None
        self.sch = BackgroundScheduler()

    def preStart(self):
        self.tudata = TradeDatas()
        self.guba = GubaSelected()
        self.tiger = TigerData()




    def updateDatas(self):
        # self.guba.save2sql()
        # self.tiger.save2sql('tiger')
        # self.tudata.updateAll()

        # 这里的调度任务是独立的一个线程
        self.sch.start()
        try:
            pass
            # 其他任务是独立的线程执行
            while True:
                time.sleep(2)
                print('sleep!')
        except (KeyboardInterrupt, SystemExit):
            self.sch.shutdown()
            print('Exit The Job!')

    def updateGuba(self):
        self.guba = GubaSelected()
        # today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # now = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        # self.sch.add_job(self.guba.updateToday, 'cron', hour='12', minute='50', second='01')
        # self.sch.add_job(self.guba.schUpdate, 'cron', hour='12', minute='50', second='01')
        self.guba.schUpdate()
        self.sch.add_job(self.guba.schUpdate, 'cron', hour='23', minute='50', second='01')
        # self.sch.add_job(self.guba.updateToday, 'cron', hour='23', minute='50', second='01')
        self.sch.start()
        try:
            while True:
                com = input('请输入命令(c退出)：')
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                if com is 'c':
                    self.sch.shutdown()
                    print('Exit The Job!')
                    exit(0)
                else:
                    pass

        except(KeyboardInterrupt, SystemExit):
            self.sch.shutdown()
            print('Exit The Job!')

    def demo(self):
        # time2 = today + ' 23:50:00'
        # 就在某时间点执行一次
        # self.sch.add_job(self.s2, 'date', run_date=time2)
        # 每天固定时间执行
        # self.sch.add_job(self.s2, 'cron', hour='23', minute='54', second='03')
        # 间隔3秒钟执行一次
        # self.sch.add_job(self.guba.updateToday, 'interval', seconds=3)
        # 带的参数可以单独放在最后
        # self.sch.add_job(self.s1, 'cron', hour='00', minute='15', second='53', args=['this is a dog'])
        self.sch.start()
        try:
            while True:
                com = input('请输入命令(c退出)：')
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                if com is 'c':
                    self.sch.shutdown()
                    print('Exit The Job!')
                    exit(0)
        except(KeyboardInterrupt, SystemExit):
            self.sch.shutdown()
            print('Exit The Job!')

    def s1(self, string):
        print(string)
        return True

    def s2(self, string):
        print(string)
        return True

