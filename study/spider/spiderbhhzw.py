import os
import urllib.request

import requests
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


headers = {
  "authority": "https://www.bhhzw.com",
  "method": "GET",

  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate",
  "accept-language": "zh-CN,zh;q=0.9",
  "content-length": "0",
  "cookie":"__cfduid=d61bf35c7645b248ec3945d3c3521d39a1603005552; X_CACHE_KEY=60a11eee707486e6d096190ac68ba20f; _ga=GA1.2.1802991227.1603195437; _gid=GA1.2.1914316790.1603195437",
  "origin":"https://www.bhhzw.com",
  "referer" :"https://www.bhhzw.com/category/xinggan/",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
}


url = '''
https://www.bhhzw.com/archives/1736.html
'''
#
#
resp = requests.get(url,headers=headers, timeout=4)
html_doc = resp.content.decode("utf-8")
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



