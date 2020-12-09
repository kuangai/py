import os
import time
import urllib.request

import requests
from bs4 import BeautifulSoup
import ImgUtil

# https://www.uyn8.cn/




def save(imgurl, code):

  file_name ='{}/{}.jpg'.format(path, code)
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
  else:
    ImgUtil.save_pictureurl(imgurl, file_name)


headers = {
  "authority": "inswanghong.xyz",
  "method": "GET",

  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate",
  "accept-language": "zh-CN,zh;q=0.9",
  "referer" :"https://www.inswanghong.xyz",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
}

#
#
has = True
o = 9
count = 0
while has:
    o = o + 1
    print("当前批次："+ str(o))
    path = "../../../img/inswh/"
    url = 'https://inswanghong.xyz/list_45_'+str(o)+'.html'
    dir = url.split("/")[len(url.split("/")) - 1]
    path = path + dir

    resp = requests.get(url,headers=headers, timeout=4)
    html_doc = resp.content.decode("utf-8")
    soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
    #获取所有的链接
    div = soup.find('div',class_="index-page")
    imgs = div.find_all('img')
    if len(imgs) == 0 :
        break

    if not os.path.exists(path):
        os.makedirs(path)

    for i in imgs:
        count = count + 1
        name = str(i.get("src")).split("/")
        file = name[len(name)-1]
        print(i.get("src"))
        print(file)
        save("https://inswanghong.xyz/"+ i.get("src"),file)
        print("已处理{}张！".format(str(count)))
    time.sleep(1)



