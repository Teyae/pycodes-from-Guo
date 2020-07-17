import urllib
import urllib3

class Request():
    def __init__(self,url, values={}):
        self.values = values
        self.data = urllib.urlencode(self.values)

    def post(self):
        self.values = {"username":"1016903103@qq.com","password":"XXXX"}
        data = urllib.urlencode(self.values)
        url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
        request = urllib3.Request(url, data)
        response = urllib3.urlopen(request)
        print(response.read())
