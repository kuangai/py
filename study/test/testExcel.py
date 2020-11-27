# coding=utf-8
import json

import pandas as pd

from openpyxl import load_workbook


def write_excel_append(path, sheet_name, dateframe=None):
    # 参数说明: [变量顺序可改变，依次是：sheet页对象，要写入的dataframe对象，从哪一行开始写入]

    writer = pd.ExcelWriter(path, engine='openpyxl', mode='a')  # 用于首次写入还可自动加表头
    workbook = load_workbook(path)  # 打开要写入数据的工作簿
    writer.book = workbook  # 激活工作薄
    rows = dateframe.shape[0]  # 获得行数
    cols = dateframe.shape[1]  # 列数
    # 如果sheet不存在,直接写入，存在，从指定位置写入
    if sheet_name in workbook.sheetnames:
        start_row = workbook[sheet_name].max_row
    else:
        dateframe.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
        writer.save()
        return
    sheet = workbook[sheet_name]  # 打开要编辑的工作表

    if start_row <= 1:
        #  sheet 已存在，直接追加会新增一个同名的sheet页，所以先复制再追加。
        writer.sheets = dict((ws.title, ws) for ws in workbook.worksheets)  # 复制已存在的sheet
        dateframe.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
        writer.save()
        return

    for i in range(0, rows):
        for j in range(0, cols):  # value.shape[1]获得列数
            sheet.cell(row=start_row + 1 + i, column=j + 1, value=dateframe.iloc[i][j])
    workbook.save(path)


def hidden_sheet(path='D:\\test\\test.xlsx', sheet_name='服务信息'):
    workbook = load_workbook(path)  # 打开要写入数据的工作簿
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]  # 打开要编辑的工作表
        sheet.sheet_state = 'hidden'
    workbook.save(path)


def read_excel(path='D:\\test\\test.xlsx', sheet_name='Sheet1'):
    workbook = load_workbook(path)

    worksheet = workbook.get_sheet_by_name(sheet_name)

    row3 = [item.value for item in list(worksheet.rows)[2]]

    print('第3行值', row3)

    col3 = [item.value for item in list(worksheet.columns)[2]]

    print('第3行值', col3)

    cell_2_3 = worksheet.cell(row=2, column=3).value

    print('第2行第3列值', cell_2_3)

    max_row = worksheet.max_row

    print('最大行', max_row)

def excel_to_json(excel_file,json_file=''):
    wb= load_workbook(excel_file)#读取excel文件
    excel_data={}#定义字典excel_data存储每个表的数据{表名:数据}
    for sheet in wb.sheetnames:
        result = []  # 定义列表result存储所有读取数据
        for rows in wb[sheet]:#获取表的每一行数据
            tmp=[]#定义列表tmp存储每一行的数据
            for cell in rows:#遍历一行每个单元格的数据
                tmp.append(cell.value)
            result.append(tmp)
        excel_data[sheet]=result
    print(excel_data)
    #覆盖写入json文件
    # with open(json_file, mode='w', encoding='utf-8') as jf:
      #  json.dump(excel_data, jf, indent=2, sort_keys=True, ensure_ascii=False)


import configparser
import os
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
import pandas as pd
from openpyxl import load_workbook
from pandas import DataFrame
from openpyxl.styles import Color,Font,Alignment,PatternFill,Border,Side,Protection

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# 将列数转成列名对应单元格
def num2column(num):
    interval = ord('Z') - ord('A')
    tmp = ''
    multiple = num // interval
    remainder = num % interval
    while multiple > 0:
        if multiple > 25:
            tmp += 'A'
        else:
            tmp += chr(64 + multiple)
        multiple = multiple // interval
    tmp += chr(64 + remainder)
    return tmp


# 对Excel格式进行设置
def func_openpyxl_modify_excel(excel_path):
    wb = load_workbook(excel_path)
    ws_list = wb.sheetnames

    for i in range(len(ws_list)):
        ws = wb[ws_list[i]]

        df_list = pd.read_excel(excel_path)

        # 关闭默认灰色网格线
        ws.sheet_view.showGridLines = False

        # 第一行行高设置为22
        ws.row_dimensions[1].height = 22

        df = df_list[i]
        # ws自动设置列宽
        df_len = df.apply(lambda x: [(len(str(i).encode('utf-8')) - len(str(i))) / 2 + len(str(i)) for i in x], axis=0)
        df_len_max = df_len.apply(lambda x: max(x), axis=0)
        for i in df.columns:
            # 列的字母
            j = list(df.columns)
            column_letter = [chr(j.index(i) + 65) if j.index(i) <= 25 else 'A' + chr(j.index(i) - 26 + 65)][0]
            # 列的宽度
            columns_length = (len(str(i).encode('utf-8')) - len(str(i))) / 2 + len(str(i))
            data_max_length = df_len_max[i]
            column_width = [data_max_length if columns_length < data_max_length else columns_length][0]
            column_width = [column_width if column_width <= 50 else 50][0] + 3  # 列宽不能超过50
            # 更改列的宽度
            ws.column_dimensions['{}'.format(column_letter)].width = column_width

    wb.save(filename=excel_path)
    wb.close()

if __name__ == '__main__':
    #  hidden_sheet()
    #  read_excel()
    func_openpyxl_modify_excel("D://test//test1.xlsx")