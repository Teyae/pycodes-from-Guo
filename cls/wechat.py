#  wxpy 通过参考这个文档可以解决几乎所有问题：https://wxpy.readthedocs.io/zh/latest/chats.html
#  这里还包括了类的定义内容

import time
from wxpy import *


class Chat(object):

    def __init__(self):
        self.bot = Bot()

    def sendmessage(self, user, text):
        my_friend = self.bot.friends().search(user)[0]
        my_friend.send(text)
        return 'send success:' + text

    def test(self):
        strshaha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return strshaha + ':这是一条测试信息'

    def getgroups(self):
        print('hello groups')



