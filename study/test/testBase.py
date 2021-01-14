# -*- coding: UTF-8 -*-
import sys
from time import mktime
from datetime import datetime
reload(sys)
sys.setdefaultencoding('UTF-8')

import time


def datetime_verify(date):
    """判断是否是一个有效的日期字符串"""
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except Exception as e:
        print(e)
        return False
def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    try:
        time.strptime(str, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False




if __name__ == '__main__':
    s = "2020-12-30"
    ss = "2020-11-20 12:11:00"

    sd = time.strptime(s, "%Y-%m-%d")
    ssd = time.strptime(ss, "%Y-%m-%d %H:%M:%S")
    datetime.fromtimestamp(mktime(ssd))
    print "s"

