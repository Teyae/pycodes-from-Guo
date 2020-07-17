# json与其它python格式的互相转换

import json


class Myjson(object):

    def __init__(self, datas):
        self.data = datas

    # dict字典转成json数据
    def dict2json(dict):
        # dict = {}
        # dict['name'] = 'many'
        # dict['age'] = 10
        # dict['sex'] = 'male'
        # print(dict)  # 输出：{'name': 'many', 'age': 10, 'sex': 'male'}
        j = json.dumps(dict)
        return j
        # print(j)  # 输出：{"name": "many", "age": 10, "sex": "male"}

    # 对象转json数据
    def obj2json():
        stu = Student('007', '007', 28, 'male', '13000000000', '123@qq.com')
        print(type(stu))  # <class 'json_test.student.Student'>
        stu = stu.__dict__  # 将对象转成dict字典
        print(type(stu))  # <class 'dict'>
        print(stu)  # {'id': '007', 'name': '007', 'age': 28, 'sex': 'male', 'phone': '13000000000', 'email': '123@qq.com'}
        j = json.dumps(obj=stu)
        print(j)  # {"id": "007", "name": "007", "age": 28, "sex": "male", "phone": "13000000000", "email": "123@qq.com"}

    # json数据转成dict字典
    def json2dict(j):
        # j = '{"id": "007", "name": "007", "age": 28, "sex": "male", "phone": "13000000000", "email": "123@qq.com"}'
        dict = json.loads(s=j)
        return dict
        # print(dict)  # {'id': '007', 'name': '007', 'age': 28, 'sex': 'male', 'phone': '13000000000', 'email': '123@qq.com'}

    # json数据转成对象
    def json2obj():
        j = '{"id": "007", "name": "007", "age": 28, "sex": "male", "phone": "13000000000", "email": "123@qq.com"}'
        dict = json.loads(s=j)
        stu = Student()
        stu.__dict__ = dict
        print('id: ' + stu.id + ' name: ' + stu.name + ' age: ' + str(stu.age) + ' sex: ' + str(
            stu.sex) + ' phone: ' + stu.phone + ' email: ' + stu.email)  # id: 007 name: 007 age: 28 sex: male phone: 13000000000 email: 123@qq.com


    # json的load()与dump()方法的使用
    # load()
    def dict2json_write_file():
        dict = {}
        dict['name'] = 'many'
        dict['age'] = 10
        dict['sex'] = 'male'
        print(dict)  # {'name': 'many', 'age': 10, 'sex': 'male'}
        with open('1.json', 'w') as f:
            json.dump(dict, f)  # 会在目录下生成一个1.json的文件，文件内容是dict数据转成的json数据

    # dump()
    def json_file2dict(files):
        with open(files, 'r') as f:
            dict = json.load(fp=f)
            return dict
            # print(dict)  # {'name': 'many', 'age': 10, 'sex': 'male'}

    #  格式化输出json数据
    def dumpjson(self):
        json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': '))

    def jsonfy(s: str) -> object:
        # 此函数将不带双引号的json的key标准化
        obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
        return obj