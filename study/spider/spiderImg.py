import os
import re
import urllib.request
import sys
from bs4 import BeautifulSoup

import ImgUtil
# https://www.uyn8.cn/
sys.path.append('..')
import ImgUtil as imgutil

def save(imgurl,code):
  path = "../../../img/A/"
  file_name ='{}{}.jpg'.format(path,code)
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
  else:
    ImgUtil.save_pictureurl(imgurl,file_name)

url = "https://www.uyn8.cn/archives/1084"

html_doc = urllib.request.urlopen(url, timeout=5).read()

soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
#获取所有的链接

for i in soup.find_all('img',class_="aligncenter"):
    name = str(i.get("src")).split("/")
    file = name[len(name)-1]
    print(i.get("src"))
    print(file)
    save(i.get("src"),file)



