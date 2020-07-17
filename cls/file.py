#  实现自动获取IP地址写入配置文件，当服务器IP地址不断发生变化时，其它相应的IP配置信息自动发生变化。
import os
import time
import socket
import re
import json
# import pdfkit
import requests

class MFile(object):
    def __init__(self , path):
        self.path = path

    def getIP(ipReg):
        # 查看当前主机名
        # print('当前主机名称为 : ' + socket.gethostname())
        # 根据主机名称获取当前IP
        # print('当前主机的IP为: ' + socket.gethostbyname(socket.gethostname()))
        # 下方代码为获取当前主机IPV4 和IPV6的所有IP地址(所有系统均通用)
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in addrs:
            str = item[4][0]
            if str[0:5] == ipReg:
                return str

    def alter(file,new_str):
    # 将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字

        with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
            for line in f1:
                line2 = re.sub(re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", re.S), new_str, line)
                f2.write(line2)
        os.remove(file)
        os.rename("%s.bak" % file, file)


        # """
        # 将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
        # :param file: 文件路径
        # :param old_str: 需要替换的字符串
        # :param new_str: 替换的字符串
        # :return: None
        # """
        # with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        #     for line in f1:
        #         line2 = re.sub(re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", re.S), new_str, line)
        #         f2.write(line2)
        # os.remove(file)
        # os.rename("%s.bak" % file, file)

    def toJS(dir):
        rootdir = dir
        listFiles = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for fileName in listFiles:
            filePart = fileName.split('.')
            file = rootdir + fileName
            if os.path.isfile(file):
                with open(file, "r", encoding="gbk") as f1:
                    contents = 'var dk' + ' = ' + f1.read()
                    f1.close()
                    with open('js/dk_' + filePart[0] + '.js', 'w', encoding="utf-8") as fw:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                        fw.write(contents)
                        fw.close()

    #
    def readLines(self):
        with open("d:/geometry_1.json") as files:
            content = files.read()
            jsonDic = eval(content)
            jsonStr = json.dumps(jsonDic, indent=4)
            with open('ab.json', 'w', encoding="utf-8") as fw:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                fw.write(jsonStr)
                fw.close()

    # 最快的读取文本数据的方法，每次读取100000行
    def rapidReadLines(filePath):
        with open(filePath) as file:
            while 1:
                lines = file.readlines(100000)
                if not lines:
                    break
                for line in lines:
                    print(line)    # do something
    # ip = getIP(ipREG)
    # alter("d:/test/a.txt", ip)
    # readLines()
    # toJS('dk/')
    # stringTest = "hello this is my ip: 4444.10.0100.12.254.88899, hahaha"
    # print(re.sub(re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", re.S), "50000000000000005", stringTest))


    #  需要安装exe文件并写入PATH环境变量
    # def html2pdf():
    #     pass
        # pdfkit.from_url(url,'.');

    # 这个直接保存成html了，但是图片显示不出来 ，都变成了base64的编码内容
    def url2html(url , file):
            r = requests.get(url)
    with open(file, 'wb') as fh:
        fh.write(r.content)
        fh.close()

    def now(self):
        now = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
        return now
