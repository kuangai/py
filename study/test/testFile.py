import os
path = "../../../img/vva/B_1T7yaHXn4.jpg"
print("判断文件或文件夹是否存在，结果：" + ("存在" if os.path.exists(path) else "不存在"))