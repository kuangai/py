import datetime
import os
import time


# 判断文件的最后修改时间
def diff_lastModifyTime_now(filePath = os.getcwd()+"/proxy.json"):
    fileName = os.path.join(filePath)
    filemt = time.localtime(os.stat(fileName).st_mtime)
    filetime = datetime.datetime(filemt[0], filemt[1], filemt[2], filemt[3])
    timenow = datetime.datetime.now()
    diffours = (timenow - filetime).seconds / 60 / 60
    print("文件：{}， 距离现在{}小时".format(filePath,diffours))

# diff_lastModifyTime_now();

def readtxt(path="sql.txt"):
    with open(path, encoding='UTF-8-sig', errors="ignore") as file_obj:
        return file_obj.read()
