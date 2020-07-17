import requests
from config.database import Database
import time


# def get_admin_region(grade, location):          # 查询的区划等级，经纬度string
#     items = {'locatoin': location, 'key': 'TIGBZ-ZOM36-COSSO-E2D5M-7MIGS-HTFFI'}
#     res = requests.get('https://apis.map.qq.com/ws/geocoder/v1/', params=items)
#     info = res.json()
#     if grade == 'province':
#         return info['result']['address_component']['province']
#     elif grade == 'city':
#         return info['result']['address_component']['city']
#     elif grade == 'region':
#         return info['result']['address_component']['district']         # region
#     else:
#         return info['result']['address_reference']['town']['title']    # town


def get_admin_region_tx(lat, lon):          # 经纬度获取行政区划信息
    location = lat + ',' + lon
    items = {'location': location, 'key': 'TIGBZ-ZOM36-COSSO-E2D5M-7MIGS-HTFFI'}
    res = requests.get('https://apis.map.qq.com/ws/geocoder/v1/', params=items)
    info = res.json()
    return info


def get_admin_region_gov(lat, lon):
    items = {'lon': lon, 'lat': lat, 'zoom': 4}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                             '537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}    # a User-Agent required
    res = requests.get('http://ditu.zjzwfw.gov.cn/ime-server/rest/xzqh_zj/division/rgeo', params=items, headers=headers)
    info = res.json()
    return info


db = Database()
db2 = Database()
conn = db.getMysqlCnn()
conn2 = db2.getMysqlCnn()
cur = conn.cursor()
cur2 = conn2.cursor()
# sql = 'select * from lyr_user where lon is not null and town*region is null'
sql = 'select AdcdId,Lat,Lng from adcdinfo where city is null'
cur.execute(sql)
while True:
    start = time.time()
    row = cur.fetchone()
    if not row:
        break
    # admin_info = get_admin_region_tx(row[24], row[23])
    # admin_info = get_admin_region_gov(row[24], row[23])
    admin_info = get_admin_region_gov(row[1], row[2])
    print(row[1], row[2])
    print(admin_info)
    # region = admin_info['result']['address_component']['district'] if row[20] is None else row[20]
    try:
        # region = admin_info['result']['COUNTY']['NAME'] if row[20] is None else row[20]
        region = admin_info['result']['COUNTY']['NAME']
        print(region)
    except KeyError:
        continue
    try:
        # town = admin_info['result']['address_reference']['town']['title'] if row[21] is None else row[21]
        # town = admin_info['result']['NAME'] if row[21] is None else row[21]
        town = admin_info['result']['NAME']
    except KeyError:
        continue
    try:
        city = admin_info['result']['CITY']['NAME']
    except KeyError:
        continue
    print(town)
    print(city)
    print(row[0])
    # sql_row = "update lyr_user set region = '%s',town = '%s' where ID = '%s'" % (region, town, row[0])
    sql_row = "update adcdinfo set county = '%s',town = '%s', city = '%s' where AdcdId = '%s'" \
              % (region, town, city, row[0])
    cur2.execute(sql_row)
    conn2.commit()
    end = time.time()
    print(end-start)
    # time.sleep(0.2)               # key每秒请求有限制


cur.close()
conn.close()
cur2.close()
conn2.close()

















