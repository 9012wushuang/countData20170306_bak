#!/usr/local/bin/python3
# coding:utf-8

import sys

sys.path.append(r"/data/bifenghui/countData20170306")
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')
import read_write as rw
import db_util as db


def write_log_into_db():
    # todo 添加web、app日志文件路径
    log_web = rw.Read_write_log('/data/bifenghui/countData20170306/countIpUvPvVv_new.log', 'r').read_web()
    log_app = rw.Read_write_log('/data/bifenghui/countData20170306/countIpUvPvVv_new.log', 'r').read_web()

    pv_web = log_web.get('pv')
    pv_app = log_app.get('pv')
    pv_all = pv_web + pv_app

    uv_web = log_web.get('uv')
    uv_app = log_app.get('uv')
    uv_all = uv_web + uv_app

    rootPv_web = log_web.get('rootPv')
    rootUv_web = log_web.get('rootUv')
    rootPv_app = log_app.get('rootPv')
    rootUv_app = log_app.get('rootUv')

    subPv_web = log_web.get('subPv')
    subUv_web = log_web.get('subUv')
    subPv_app = log_web.get('subPv')
    subUv_app = log_web.get('subUv')

    rootModulePv_web = log_web.get('rootModulePv')
    rootModulePv_app = log_app.get('rootModulePv')

    subModulePv_web = log_web.get('subModulePv')
    subModulePv_app = log_app.get('subModulePv')

    dbClient = db.getConnectDb()
    '''
        get company
    '''
    date_time = time.strftime("%Y-%m-%d", time.localtime())
    cursor = dbClient.cursor()
    sql = 'select company_id from asset_basic_data where date =  %s'
    cursor.execute(sql, [date_time])
    data = cursor.fetchall()
    for sub in list(data):

        # 查询更新每一个公司 的 web端pv uv 模块浏览量  app端
        company_id = sub[0]

        asset_Vv = {}

        # web端uv
        uvWeb = 0
        if str(company_id) in subUv_web:
            uvWeb = len(subUv_web.get(str(company_id)))

        # app端uv
        uvApp = 0
        if str(company_id) in subUv_app:
            uvApp = len(subUv_app.get(str(company_id)))

        # web端pv
        pvWeb = 0
        if str(company_id) in subPv_web:
            pvWeb = subPv_web.get(str(company_id))

        # app端pv
        pvApp = 0
        if str(company_id) in subPv_app:
            pvApp = subPv_app.get(str(company_id))

        moduleWeb = {}
        if str(company_id) in subModulePv_web:
            moduleWeb = subModulePv_web.get(str(company_id))

        moduleApp = {}
        if str(company_id) in subModulePv_app:
            moduleApp = subModulePv_app.get(str(company_id))

        asset_Vv = {'uvWeb': uvWeb, 'uvApp': uvApp, 'pvWeb': pvWeb, 'pvApp': pvApp, 'moduleWeb': moduleWeb,
                    'moduleApp': moduleApp}

        sql = 'update asset_basic_data set asset_vv = %s where company_id = %s and date = %s'

        cursor.execute(sql, [str(asset_Vv), company_id, date_time])

        dbClient.commit()

    sqlRoot = 'select id from asset_company where status = 0 and data_status = 0 AND parent_company_id is null'

    '''
        get 子公司 uv pv  模块浏览量 总和
    '''
    cursor.execute(sqlRoot)
    dataRoot = cursor.fetchall()
    for root in list(dataRoot):
        rootCompany_id = root[0]
        asset_Vv = {}
        # web端uv
        uvWeb = 0
        if str(rootCompany_id) in rootUv_web:
            uvWeb = len(rootUv_web.get(str(rootCompany_id)))

        # app端uv
        uvApp = 0
        if str(rootCompany_id) in rootUv_app:
            uvApp = len(rootUv_app.get(str(rootCompany_id)))

        # web端pv
        pvWeb = 0
        if str(rootCompany_id) in rootPv_web:
            pvWeb = rootPv_web.get(str(rootCompany_id))

        # app端pv
        pvApp = 0
        if str(rootCompany_id) in rootPv_app:
            pvApp = rootPv_app.get(str(rootCompany_id))

        moduleWeb = {}
        if str(rootCompany_id) in rootModulePv_web:
            moduleWeb = rootModulePv_web.get(str(rootCompany_id))

        moduleApp = {}
        if str(rootCompany_id) in rootModulePv_app:
            moduleApp = rootModulePv_app.get(str(rootCompany_id))

        asset_Vv = {'uvWeb': uvWeb, 'uvApp': uvApp, 'pvWeb': pvWeb, 'pvApp': pvApp, 'moduleWeb': moduleWeb,
                    'moduleApp': moduleApp}

        sql = 'update asset_basic_data set asset_vv = %s where root_company_id = %s and date = %s and company_id is null'

        cursor.execute(sql, [str(asset_Vv), rootCompany_id, date_time])

        dbClient.commit()

    # 关闭数据库连接
    db.closeConnectDb(dbClient)

print(write_log_into_db())
