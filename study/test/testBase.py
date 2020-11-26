"""
基础测试
"""

import difflib
import time


def findstrinfile(filename, lookup):
    return lookup in open(filename, 'rt').read()


# 对付dao大文件dao:
def findstrinlargefile(filename, lookup):
    with open(filename, 'rt') as handle:
        for ln in handle:
            if lookup in ln:
                return True
            else:
                return False

# 判断列表里是否包含某个字符串 --模糊匹配 --精确匹配
# 说明：cutoff参数是0到1的浮点数, 可以调试模糊匹配的精度, 1为精确匹配
list1 = ['qqaabb', 'wweerr', '121', 'qbcd', 'plqs']
data = difflib.get_close_matches('qs', list1, 1, cutoff=0.5)
print(data)  # 返回值为：['plqs']

# 判断列表里是否包含某个字符串--模糊匹配
list1 = ['qqaabb', 'wweerr', '121', 'qbcqsd', 'plqs']
data = [x for i, x in enumerate(list1) if x.find('qs') != -1]
print(data)  # 返回值为：['qbcqsd','plqs']

# 绿色字体
print('\033[1;32m' + 'green' + '\033[0m')

time1 = time.time()
print(int(time1))

# 异常
try:
  print(2/0)
except Exception as e:
  print(e)
  print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
  print(e.__traceback__.tb_lineno)            # 发生异常所在的行数

print(input('Y/N?'))

