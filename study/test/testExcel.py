# coding=utf-8

import xlrd
from xlutils.copy import copy

# 打开文件
book = xlrd.open_workbook("A.xlsx")
new_book = copy(book)
new_sheet = new_book.get_sheet(0)


new_sheet.write(1,0,"asdfgh")
new_book.save("12.xlsx")
print("fine")
