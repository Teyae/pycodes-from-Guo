import json
import pandas as pd
from sqlalchemy import create_engine

df = pd.DataFrame()
df = pd.read_csv('D:\\app\\test\\20181127T1700-yd.csv')

# 1. Dataframe写入到csv文件
df.to_csv('D:\\a.csv', sep=',', header=True, index=True)
# 第一个参数是说把dataframe写入到D盘下的a.csv文件中，参数sep表示字段之间用’,’分隔，header表示是否需要头部，index表示是否需要行号。
# 2. Dataframe写入到json文件

# 把dataframe转为json字符串
json.dumps(df.to_dict())

df.to_json('D:\\a.json')

# 把dataframe写入到D盘下的a.json文件中,文件的内容为

# {"0":{"0":1.049228614,"1":0.3485250629,"2":1.3073567907},"1":{"0":-0.7922606408,"1":-2.1176065444,"2":-0.7350348086},"2":{"0":0.0204180549,"1":1.4668228784,"2":0.2856083175},"3":{"0":-1.6649819404,"1":-0.9249205656,"2":-0.9053483976}}

# 3.Dataframe写入到html文件
df.to_html('D:\\a.html')

# 按条件提取行，提取symbol列为1的所有行
df1 = df[df.symbol == 1]

# 4.Dataframe写入到剪贴板中
# 这个是我认为最为贴心的功能, 一行代码可以将dataframe的内容导入到剪切板中，然后可以复制到任意地方
df.to_clipboard()

# 5.Dataframe写入到数据库中
engine = create_engine('postgresql://postgres:123456@localhost:5432/gis')
df.to_sql('tableName', con=engine, flavor='pgsql')


def sql2df(self):
    conn = psycopg2.connect(database="****", user="postgres", password="***", port="5432")
    with conn:
        cur = conn.cursor()
        cur.execute("select * from public.20160407_1")
        rows = cur.fetchall()
        t = pd.DataFrame(rows)
        print(t)


def df2sql(self):
    df = pd.read_csv(r'D:\app\test\20181127T1700-yd.csv')
    df.to_sql('tableName', con=dbcon, flavor='pgsql')

# 遍历DataFrame里面的每一行
def printAllRows(self, df):
    for r in df.values:
        print(r)


# 按条件选择数据
def fortianjian():
    res = df.loc[(df['symbol'] < '300000') | (df['symbol'] > '309999')].reset_index(drop=True)

# 提取列数据
def getColumns():
    #  如果是单列髁不不需要双层括号，且可以单独赋值
    return df[['column1', 'colum21', 'column3']]
