#!/usr/local/bin/python3
# coding:utf-8
# encoding=utf8

import sys

sys.path.append(r"/data/bifenghui/countData20170306")  # todo 可据实际环境修改
import csv
import openpyxl


class Excel_csv():
    def __init__(self):
        self.name = 'bifenghui.csv'  # todo 生成的csv文件路径
        self.space = ['']
        self.uv = ['UV（PC/APP）']
        self.pv = ['PV（PC/APP']
        self.moudle_look_pc_app = [
                                      '模块浏览量(PC/APP)'] + self.space + self.space + self.space + self.space
        self.module_time_pc_app = [
                                      '模块总使用时间(PC/APP)'] + self.space + self.space + self.space + self.space
        self.asset = ['资产概况'] + self.space + self.space + self.space + self.space
        self.company = ['公司概况'] + self.space + self.space + self.space
        self.header = self.space + self.uv + self.pv + self.moudle_look_pc_app + self.module_time_pc_app + self.asset + self.company

        # self.modules = ['资产管理', '盘点管理', '数据报表', '组织架构', '位置管理', '模版列表', '管理员列表']
        self.modules = ['资产管理', '数据报表', '盘点管理', '用户管理', '未知模块']
        self.assets = ['资产总数', '领用', '借用', '闲置', '退库']
        self.company_info = ['子公司', '部门', '人员']
        self.attr = ['', '', ''] + self.modules + self.modules + self.assets + self.company_info

    def write_csv(self, show_list):
        outputFile = open(self.name, 'w', encoding='utf-8', newline='')
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(self.header)
        outputWriter.writerow(self.attr)
        for data1 in show_list:
            outputWriter.writerow(data1)

        outputFile.close()

    def write_excel(self):
        wb = openpyxl.Workbook()
        wb.create_sheet()
        wb.get_sheet_names()


def main():
    csv = Excel_csv()
    csv.write_csv()


if __name__ == '__main__':
    pass
    main()
