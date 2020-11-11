"""
基础测试
"""

import difflib



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

list = [1, 2, 3, 4]
list.append(50)
print(list)
a = list.pop(0)
print(a)
print(list)

# 绿色字体
print('\033[1;32m' + 'green' + '\033[0m')

# 蓝色字体
print('\033[1;34m' + 'blue' + '\033[0m')

# 黄字下划线


# 红底黑字
print('\033[1;30;41m' + 'black' + '\033[0m')

# 白底黑字
print('\033[1;30;47m' + 'white' + '\033[0m')

