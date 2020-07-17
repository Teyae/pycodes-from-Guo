
# 贪婪模型，选择人气最高，资金参与量最多的，最热门的股票进行操作，龙虎榜上榜数据，成交量放大数据，做趋势模型，采用突破方法，
# 建立人气指数等
# 不管以何种方式，只有有曝光度，将曝光度进行排序，选择排序前列的股票，然后再依据其它的技术指标，配合买卖点
# 需要控制的是止损，一般一波上冲之后，还会有第二波，第一次回撤后，基本上90的概率上破前高
class GreedySystem(object):

    def __init__(self):
        pass

    def getItems(self):
        pass

    def orderItems(self, items):
        pass

    def filter(self, items):
        pass

    # 主要用于排除ST，特大盘，新股
    def typeFilter(self):
        pass

    #
    def priceFilter(self):
        pass

    def volFilter(self):
        pass




