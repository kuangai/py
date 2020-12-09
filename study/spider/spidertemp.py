import os
import urllib.request
from bs4 import BeautifulSoup
import ImgUtil

# https://www.uyn8.cn/
path = "../../../img/cos/"
url = """https://www.uyn8.cn/archives/379"""
dir = url.split("/")[len(url.split("/"))-1]
path = path + dir
if not os.path.exists(path):
    os.makedirs(path)

def save(imgurl, code):
  file_name ='{}/{}.jpg'.format(path, code)
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
  else:
    ImgUtil.save_pictureurl(imgurl, file_name)

html_doc = urllib.request.urlopen(url, timeout=5).read()

soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
#获取所有的链接
div = soup.find('div',class_="entry-content u-text-format u-clearfix")
imgs = div.find_all('img')
for i in imgs:
    name = str(i.get("src")).split("/")
    file = name[len(name)-1]
    print(i.get("src"))
    print(file)
    save(i.get("src"),file)



