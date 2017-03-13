#!/usr/local/bin/python3
# coding:utf-8

import sys
import time
import do_excel_csv as decsv

sys.path.append(r"/data/bifenghui/countData20170306")
import db_util as db
import db_write as dw
import send_mail as sm
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')


def query_asset_basic_data():
    pass
    csv_list = []
    date_time = time.strftime("%Y-%m-%d", time.localtime())
    show_data_list = []
    dbClient = db.getConnectDb()
    cursor = dbClient.cursor()
    sql = 'select id,name from asset_company where parent_company_id is null and data_status  = 0 '
    cursor.execute(sql)
    data = cursor.fetchall()
    for root in list(data):
        rootCompnay_id = root[0]

        # 拿到总数行
        sql = 'select asset_vv,asset_status,asset_source,asset_other,company_overview ,asset_change,company_change from asset_basic_data where root_company_id = %s and company_id is null and date =%s'
        cursor.execute(sql, [rootCompnay_id, date_time])
        result = cursor.fetchone()
        print(result)
        if result == None:
            pass
        else:
            resultList = list(result)
            assetVv = eval(resultList[0])
            assetSatus = eval(resultList[1])
            assetSource = eval(resultList[2])
            assetOther = eval(resultList[3])
            companyOverview = eval(resultList[4])
            assetChange = eval(resultList[5])
            companyChange = eval(resultList[6])
            list_title = []
            list_title.append('总数')
            list_title.append(str(assetVv.get('uvWeb')) + "/" + str(assetVv.get('uvApp')))
            list_title.append(str(assetVv.get('pvWeb')) + "/" + str(assetVv.get('pvWeb')))
            list_title.append(
                str(0 if assetVv.get('moduleWeb').get('ASSET_MANAGER') == None else assetVv.get('moduleWeb').get(
                    'ASSET_MANAGER')) + "/" + str(
                    0 if assetVv.get('moduleApp').get('ASSET_MANAGER') == None else assetVv.get('moduleApp').get(
                        'ASSET_MANAGER')))
            list_title.append(
                str(0 if assetVv.get('moduleWeb').get('DATA_REPORT') == None else assetVv.get('moduleWeb').get(
                    'DATA_REPORT')) + "/" + str(
                    0 if assetVv.get('moduleApp').get('DATA_REPORT') == None else assetVv.get('moduleApp').get(
                        'DATA_REPORT')))
            list_title.append(str(
                0 if assetVv.get('moduleWeb').get('INVENTORY_MANAGER') == None else assetVv.get('moduleWeb').get(
                    'INVENTORY_MANAGER')) + "/" + str(
                0 if assetVv.get('moduleApp').get('INVENTORY_MANAGER') == None else assetVv.get('moduleApp').get(
                    'INVENTORY_MANAGER')))
            list_title.append(
                str(0 if assetVv.get('moduleWeb').get('ADMIN_MANAGER') == None else assetVv.get('moduleWeb').get(
                    'ADMIN_MANAGER')) + "/" + str(
                    0 if assetVv.get('moduleApp').get('ADMIN_MANAGER') == None else assetVv.get('moduleApp').get(
                        'ADMIN_MANAGER')))
            list_title.append(
                str(0 if assetVv.get('moduleWeb').get('NOT_KNOW_MODULE') == None else assetVv.get('moduleWeb').get(
                    'NOT_KNOW_MODULE')) + "/" + str(
                    0 if assetVv.get('moduleApp').get('NOT_KNOW_MODULE') == None else assetVv.get('moduleApp').get(
                        'NOT_KNOW_MODULE')))
            for i in range(5):
                list_title.append('')
            list_title.append(str(assetOther.get('all').get('count'))+'('+str(assetChange.get('all'))+')')
            list_title.append(str(assetSatus.get('receive').get('count'))+'('+str(assetChange.get('receive'))+')')
            list_title.append(str(assetSatus.get('borrow').get('count'))+'('+str(assetChange.get('borrow'))+')')
            list_title.append(str(assetSatus.get('free').get('count'))+'('+str(assetChange.get('free'))+')')
            list_title.append(str(assetSatus.get('delFromDepotHistory').get('count'))+'('+str(assetChange.get('delFromDepotHistory'))+')')
            list_title.append(str(companyOverview.get('subCompanyCount'))+'('+str(companyChange.get('subCompanyCount'))+')')
            list_title.append(str(companyOverview.get('departmentCount'))+'('+str(companyChange.get('departmentCount'))+')')
            list_title.append(str(companyOverview.get('memberCount'))+'('+str(companyChange.get('memberCount'))+')')

            csv_list.append(list_title)
            sql_sub = 'select id from asset_company where parent_company_id = %s or id = %s'
            cursor.execute(sql_sub, [rootCompnay_id, rootCompnay_id])
            data_sub = cursor.fetchall()
            if len(list(data_sub)) == 0:
                csv_list.append('')
            flag = 0
            for sub in list(data_sub):
                flag += 1
                company_id = sub[0]

                sql_sub = 'select asset_vv,asset_status,asset_source,asset_other,company_overview ,asset_change,company_change,asset_change,company_change  from asset_basic_data where root_company_id is not null and company_id =%s and date =%s'
                cursor.execute(sql_sub, [company_id, date_time])
                result = cursor.fetchone()
                resultList = list(result)
                assetVv = eval(resultList[0])
                assetSatus = eval(resultList[1])
                assetSource = eval(resultList[2])
                assetOther = eval(resultList[3])
                companyOverview = eval(resultList[4])
                assetChange = eval(resultList[5])
                companyChange = eval(resultList[6])
                list_sub = []
                list_sub.append(getCompanyName(company_id))
                list_sub.append(str(assetVv.get('uvWeb')) + "/" + str(assetVv.get('uvApp')))
                list_sub.append(str(assetVv.get('pvWeb')) + "/" + str(assetVv.get('pvWeb')))
                list_sub.append(
                    str(0 if assetVv.get('moduleWeb').get('ASSET_MANAGER') == None else assetVv.get('moduleWeb').get(
                        'ASSET_MANAGER')) + "/" + str(
                        0 if assetVv.get('moduleApp').get('ASSET_MANAGER') == None else assetVv.get('moduleApp').get(
                            'ASSET_MANAGER')))
                list_sub.append(
                    str(0 if assetVv.get('moduleWeb').get('DATA_REPORT') == None else assetVv.get('moduleWeb').get(
                        'DATA_REPORT')) + "/" + str(
                        0 if assetVv.get('moduleApp').get('DATA_REPORT') == None else assetVv.get('moduleApp').get(
                            'DATA_REPORT')))
                list_sub.append(str(
                    0 if assetVv.get('moduleWeb').get('INVENTORY_MANAGER') == None else assetVv.get('moduleWeb').get(
                        'INVENTORY_MANAGER')) + "/" + str(
                    0 if assetVv.get('moduleApp').get('INVENTORY_MANAGER') == None else assetVv.get('moduleApp').get(
                        'INVENTORY_MANAGER')))
                list_sub.append(
                    str(0 if assetVv.get('moduleWeb').get('ADMIN_MANAGER') == None else assetVv.get('moduleWeb').get(
                        'ADMIN_MANAGER')) + "/" + str(
                        0 if assetVv.get('moduleApp').get('ADMIN_MANAGER') == None else assetVv.get('moduleApp').get(
                            'ADMIN_MANAGER')))
                list_sub.append(
                    str(0 if assetVv.get('moduleWeb').get('NOT_KNOW_MODULE') == None else assetVv.get('moduleWeb').get(
                        'NOT_KNOW_MODULE')) + "/" + str(
                        0 if assetVv.get('moduleApp').get('NOT_KNOW_MODULE') == None else assetVv.get('moduleApp').get(
                            'NOT_KNOW_MODULE')))
                for i in range(5):
                    list_sub.append('')
                list_sub.append(str(assetOther.get('all').get('count')) + '(' + str(assetChange.get('all')) + ')')
                list_sub.append(str(assetSatus.get('receive').get('count')) + '(' + str(assetChange.get('receive')) + ')')
                list_sub.append(str(assetSatus.get('borrow').get('count')) + '(' + str(assetChange.get('borrow')) + ')')
                list_sub.append(str(assetSatus.get('free').get('count')) + '(' + str(assetChange.get('free')) + ')')
                list_sub.append(str(assetSatus.get('delFromDepotHistory').get('count')) + '(' + str(assetChange.get('delFromDepotHistory')) + ')')
                list_sub.append(str(companyOverview.get('subCompanyCount')) + '(' + str(companyChange.get('subCompanyCount')) + ')')
                list_sub.append(str(companyOverview.get('departmentCount')) + '(' + str(companyChange.get('departmentCount')) + ')')
                list_sub.append(str(companyOverview.get('memberCount')) + '(' + str(companyChange.get('memberCount')) + ')')

                csv_list.append(list_sub)
                if flag == len(list(data_sub)):
                    csv_list.append('')

    csv = decsv.Excel_csv()
    csv.write_csv(csv_list)


def getCompanyName(companyId):
    try:
        dbClient = db.getConnectDb()
        cursor = dbClient.cursor()
        sql = 'select name from asset_company where id = %s'
        cursor.execute(sql, [companyId])
        data = cursor.fetchone()
        dbClient.commit()
        if data == '':
            return 'no get companyId by company_id'
        else:
            return data[0]
    except:
        print('MySql connect fail...')


print(dw.write_log_into_db())
print(query_asset_basic_data())
print(sm.send_mail())

# print(test())
