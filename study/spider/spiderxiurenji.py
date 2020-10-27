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

    url = "https://www.xiurenji.com/XiuRen/6720_" + str(i) + ".html"
    resp = requests.get(url, timeout=5)
    html_doc = resp.content.decode("GB2312")
    print(html_doc)
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="GB2312")
    # 获取所有的链接
    div = soup.find('div', class_="img")

    print("已处理： " + str(i) + "次")
    i = i + 1

    imgs = div.find_all("img")

    for img in imgs:
        name = str(img.get("src")).split("/")
        file = name[len(name)-1]
        print(img.get("src"))
        print(file)
        p = save("https://www.xiurenji.com/" + img.get("src"),file)
        if p == 1:
            break
    else: continue
    break



