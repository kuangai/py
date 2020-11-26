import datetime
import os
import time

path = "../../../img/vva/B_1T7yaHXn4.jpg"
print("判断文件或文件夹是否存在，结果：" + ("存在" if os.path.exists(path) else "不存在"))

# 遍历文件夹下的文件
def oop_files(path = "../util"):
    for (root, dirs, files) in os.walk(path):
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            print(os.path.join(root, f))

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))

oop_files("E:\O4.5202003.00.000-20201115-Beta\IPS")