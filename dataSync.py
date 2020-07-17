# -*- coding: UTF-8 -*-

from cls.orm.mysql import Mysql
from datetime import datetime
import time


class UpdateDatabase():

    def __init__(self):
        self.maxId = 0
        self.db = Mysql()


    def getReaderCNN(self):
        return self.db.getCnn()

    def getWriterCNN(self):
        return self.db.getCnnW()

    def setMaxID(self, id):
        self.maxId = id
        return self.maxId

    def getMaxField(self, table, field):
        sql = "select max(" + field + ") from "+table
        value = self.db.execValue(sql)
        if value is None:
            return [field, 0]
        if isinstance(value, int):
            return [field, value]

        return [field, "'" + str(value) + "'"]

    def getResutes(self, table, columns, maxField):
        colStr = ','.join(columns)
        db = self.getReaderCNN()
        selectSql = "select " + colStr + " from " + table + " where " + maxField[0] + " > " + str(maxField[1])
        res = self.db.exec(selectSql)
        return res

    def updateTable(self, table, columns, res):
        self.db.insert(table, columns, res)

    def updateTransfer(self):
        self.getReaderCNN()
        self.db.exec('select')


obj = UpdateDatabase()
while True:
    tableOpt = 'se_operation_detail'
    optDetailColumns = ["OPT_ID", "EVENT_ID","USER_ID","OPT_USER_ID","OPERATOR_TYPE","OPT_TYPE","OPT_TIME","OPT_LNG","OPT_LAT","CREATE_TIME","UPDATE_TIME"]
    obj.getWriterCNN()
    maxField = obj.getMaxField(tableOpt, 'CREATE_TIME')
    obj.getReaderCNN()
    res = obj.getResutes(tableOpt, optDetailColumns, maxField)
    obj.getWriterCNN()
    obj.updateTable(tableOpt, optDetailColumns, res)

    tableUder = 'se_user'
    seUserColumns = ["USER_ID", "USER_NAME", "IDCARD_TYPE", "IDCARD_NO", "MOBILE", "CREATE_TIME", "UPDATE_TIME", "SOURCES", "IDENTITY_TYPE"]
    obj.getWriterCNN()
    maxField = obj.getMaxField(tableUder, 'user_id')
    obj.getReaderCNN()
    res = obj.getResutes(tableUder, seUserColumns, maxField)
    obj.getWriterCNN()
    obj.updateTable(tableUder, seUserColumns, res)

    deleteSQL = 'delete from lyr_transferredpeople WHERE id > 0'
    statSQL = "insert INTO lyr_transferredpeople(name,tel,ttype,ttime,city,county,town,village,responselevel,villagemname,villagemtel\
        ,relation,mname,mtel,count,midno,arealname,arealtel,villagelname,villageltel,placename,placemname,placemtel,dangertype,dangername,position,yjid) \
        SELECT ali.user_name AS name,ali.MObile AS tel,\
        case \
                when ali.opt_type = '1' then '报平安'\
                when ali.opt_type = '2' then '避灾安置所扫码'	\
                when ali.opt_type = '3' then '投亲靠友'  \
        \
        end as ttype,\
        ali.create_time AS ttime,z.city,z.county,z.town,z.village,z.level AS responselevel,z.villagemname,z.villagemtel,z.relation,z.mname,z.mtel,z.count,z.midno,\
        z.arealname,z.arealtel,z.villagelname,z.villageltel,z.placename,z.placemname,z.placemtel,z.dangertype,z.dangername,z.position,z.eveid AS yjid FROM \
        \
        (SELECT SE_USER.USER_name,\
            case \
                            when SE_OPERATION_DETAIL.OPERATOR_TYPE = '1' AND opt_type = '1'  then '1'  \
                            when SE_OPERATION_DETAIL.OPERATOR_TYPE = '2' AND opt_type = '2'  then '2'  \
                            when SE_OPERATION_DETAIL.OPERATOR_TYPE = '3' AND opt_type = '1'  then '3'  \
                                            end as OPT_TYPE,SE_USER.MOBILE,SE_OPERATION_DETAIL.CREATE_TIME FROM SE_OPERATION_DETAIL,SE_USER \
        WHERE SE_USER.USER_ID = SE_OPERATION_DETAIL.USER_ID AND SE_OPERATION_DETAIL.create_time > '2020-04-05 00:00:00' AND SE_USER.MOBILE IS NOT NULL \
        AND (SE_OPERATION_DETAIL.OPT_TYPE = '1' OR SE_OPERATION_DETAIL.OPT_TYPE = '2')) AS ALI, \
        \
        (SELECT tra.name,tra.tel,tra.village,tra.town,tra.county,tra.city,tra.villagemname,tra.villagemtel,tra.relation,tra.mname,tra.mtel,tra.count,tra.midno,tra.arealname,tra.arealtel,tra.villagelname,tra.villageltel\
        ,tra.placename,tra.placemname,tra.placemtel,tra.dangertype,tra.dangername,tra.position,ze.id AS eveid,ze.level FROM \
         (SELECT  id,SZZ,LEVEL from lyr_evento WHERE STATE = 1 AND SZZ IS not NULL) AS ze , lyr_transferpeople AS tra \
        WHERE ze.szz = tra.town AND level <= tra.responselevel AND tel IS NOT NULL) AS z \
        WHERE ali.USER_NAME = z.NAME GROUP BY z.NAME  order by ttime"
         # WHERE ali.mobile = z.tel GROUP BY z.tel"
    obj.db.sql(deleteSQL)
    obj.db.sql(statSQL)
    print('delete and stat')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(5)
