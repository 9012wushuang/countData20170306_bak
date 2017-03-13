#!/usr/local/bin/python3
# coding:utf-8

import sys

sys.path.append(r"/data/bifenghui/countData20170306")

import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(message)s')

'''
 read sass countIpUvPvVv.log
 count all pv
 count all uv
 count root name all pv
            root company pv
                web
                app
            sub company pv
                web
                app
            ...
 count root name all uv
            root company pv
                web
                app
            sub company pv
                web
                app
            ...
'''


class Read_write_log(object):
    def __init__(self, file_path, auth):
        self.file_path = file_path
        self.auth = auth

    def read_web(self):

        uv = 0
        pv = 0

        pvCompanyDict = {}

        pvRootCompanyDict = {}

        uvCompanyDict = {}
        uvRootCompanyDict = {}

        pvModuleCompanyDict = {}

        pvModuleCompanyDict_sub = {}

        logging.info('read web log')
        fo = open(self.file_path, self.auth, encoding='utf-8')
        print("Name of the file: ", fo.name)
        while True:
            line = fo.readline()
            if line == '':
                break
            else:
                pv += 1
                logging.info(line)
                data = json.loads(line)
                if data['userId'] == 'null':
                    pass
                else:
                    uv += 1
                logging.info(data['module'])

                if data['companyId'] in pvCompanyDict:
                    dict = {data['companyId']: pvCompanyDict.get(data['companyId']) + 1}
                    pvCompanyDict.update(dict)
                else:
                    dict = {data['companyId']: 1}
                    pvCompanyDict.update(dict)

                if data['rootCompanyId'] in pvRootCompanyDict:
                    dict = {data['rootCompanyId']: pvRootCompanyDict.get(data['rootCompanyId']) + 1}
                    pvRootCompanyDict.update(dict)
                else:
                    dict = {data['companyId']: 1}
                    pvRootCompanyDict.update(dict)

                # ---------
                if data['rootCompanyId'] in uvRootCompanyDict:
                    # pass
                    userIdList = uvRootCompanyDict.get(data['rootCompanyId'])
                    logging.info(userIdList)
                    if data['userId'] in userIdList:
                        pass
                    else:
                        userIdList.append(data['userId'])
                        dict = {data['rootCompanyId']: userIdList}
                        uvRootCompanyDict.update(dict)
                else:
                    if data['userId'] != 'null':
                        list = []
                        list.append(data['userId'])
                        dict = {data['rootCompanyId']: list}
                        uvRootCompanyDict.update(dict)

                if data['companyId'] in uvCompanyDict:
                    # pass
                    userIdList = uvCompanyDict.get(data['companyId'])
                    if data['userId'] in userIdList:
                        pass
                    else:
                        userIdList.append(data['userId'])
                        dict = {data['companyId']: userIdList}
                        uvCompanyDict.update(dict)
                else:
                    if data['userId'] != 'null':
                        list = [data['userId']]
                        dict = {data['companyId']: list}
                        uvCompanyDict.update(dict)
                # *********

                if data['rootCompanyId'] in pvModuleCompanyDict:
                    dict1 = pvModuleCompanyDict.get(data['rootCompanyId'])
                    if data['module'] in dict1:
                        dict2 = {data['module']: dict1.get(data['module']) + 1}
                        dict1.update(dict2)
                    else:
                        dict2 = {data['module']: 1}
                        dict1.update(dict2)
                    dict = {data['rootCompanyId']: dict1}
                    pvModuleCompanyDict.update(dict)
                else:
                    dict1 = {}
                    dict2 = {data['module']: 1}
                    dict1.update(dict2)
                    dict = {data['rootCompanyId']: dict1}
                    pvModuleCompanyDict.update(dict)

                if data['companyId'] in pvModuleCompanyDict_sub:
                    dict1 = pvModuleCompanyDict_sub.get(data['companyId'])
                    if data['module'] in dict1:
                        dict2 = {data['module']: dict1.get(data['module']) + 1}
                        dict1.update(dict2)
                    else:
                        dict2 = {data['module']: 1}
                        dict1.update(dict2)
                    dict = {data['companyId']: dict1}
                    pvModuleCompanyDict_sub.update(dict)
                else:
                    dict1 = {}
                    dict2 = {data['module']: 1}
                    dict1.update(dict2)
                    dict = {data['companyId']: dict1}
                    pvModuleCompanyDict_sub.update(dict)

        showDict = {
            'pv': uv,
            'uv': uv,
            'rootPv': pvRootCompanyDict,
            'subPv': pvCompanyDict,
            'rootUv': uvRootCompanyDict,
            'subUv': uvCompanyDict,
            'rootModulePv': pvModuleCompanyDict,
            'subModulePv': pvModuleCompanyDict_sub
        }

        logging.info(showDict)
        logging.info('read web log end')
        return showDict


def main():
    rwl = Read_write_log('/data/bifenghui/countData20170306/countIpUvPvVv_new.log', 'r')
    rwl.read_web()


if __name__ == '__main__':
    main()
