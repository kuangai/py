import datetime
import os
import time

path = "../../../img/vva/B_1T7yaHXn4.jpg"
print("判断文件或文件夹是否存在，结果：" + ("存在" if os.path.exists(path) else "不存在"))

# 遍历文件夹下的文件
def oop_files(path = "../util"):
    a=0
    for (root, dirs, files) in os.walk(path):
        print("root:" + root)
        print("dirs: " + str(dirs))
        print("files:" + str(files))
        a=a+1
        print("循环次数：",a)

#判断文件的最后修改时间
