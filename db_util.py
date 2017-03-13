#!/usr/local/bin/python3
# coding:utf-8

import sys

sys.path.append(r"/data/bifenghui/countData20170306")
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s-%(levelname)s-%(message)s')

# todo 添加mysql数数据库信息，后续可优化到mongo查询
host = '127.0.0.1'
user = 'root'
password = ''
db = 'db_cloud_assets'
port = 3306


def getConnectDb():
    try:
        connection = pymysql.connect(host, user, password, db, port, charset='utf8')
        return connection
    except:
        logging.error('connect db fail')


def closeConnectDb(connection):
    try:
        connection.close()
    except:
        logging.error('close db fail')
