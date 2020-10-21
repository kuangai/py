import os
import requests
from bs4 import BeautifulSoup
import ImgUtil

# http://desk.tooopen.com/
import proxyUtil


def save(imgurl, code):
  path = "../../../img/A/"
  file_name ='{}{}.jpg'.format(path, code)
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
    return 1
  else:
    ImgUtil.save_pictureurl(imgurl, file_name)
    return 0

i = 1


while True:

    url = "https://www.junmeitu.com/beauty/enlvbabe_tongyanjuruxingganmeinv_mfstar_vol_237-" + str(i) + ".html"
    resp = requests.get(url, timeout=5)
    html_doc = resp.content.decode("utf-8")
    print(html_doc)
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
    # 获取所有的链接
    div = soup.find('div', class_="pictures")

    print("已处理： " + str(i) + "次")
    i = i + 1
    img = div.find("img")
    name = str(img.get("src")).split("/")
    file = name[len(name)-1]
    print(img.get("src"))
    print(file)
    p = save( img.get("src"),file)
    if p == 1:
        break



