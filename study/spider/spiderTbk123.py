import os
import urllib.request
from bs4 import BeautifulSoup
import ImgUtil

# https://www.uyn8.cn/

def save(imgurl, code):
  path = "../../../img/A/"
  file_name ='{}{}.jpg'.format(path, code)
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
  else:
    ImgUtil.save_pictureurl(imgurl, file_name)


url = '''
https://www.tbk123.com/xgmn/59820.html
'''
#
#
html_doc = urllib.request.urlopen(url, timeout=5).read()

soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
#获取所有的链接
div = soup.find('div',class_="post row")
imgs = div.find_all('img',class_="post-item-img lazy")
count = 0
for i in imgs:
    count = count + 1
    name = str(i.get("data-original")).split("/")
    file = name[len(name)-1]
    print(i.get("data-original"))
    print(file)
    save(i.get("data-original"),file)
    print("已处理{}张！".format(str(count)))



