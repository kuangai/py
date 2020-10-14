import os
import sys,requests

from bs4 import BeautifulSoup

import ImgUtil

sys.path.append('..')
# https://www.veryins.com/vivian19941008 首页

def save(imgurl,code):
  path = "../../../img/vva/"
  file_name ='{}{}.jpg'.format(path,code)
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
  else:
    ImgUtil.save_pictureurl(imgurl,file_name)

headers = {
  "authority": "www.veryins.com",
  "method": "POST",

  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate",
  "accept-language": "zh-CN,zh;q=0.9",
  "content-length": "0",
  "cookie":"__cfduid=dee661c3c1603d972ddb10e0d1f3346ee1602509634; _ga=GA1.2.1032098640.1602509640; _gid=GA1.2.986060369.1602509641; __gads=ID=371a0da37fb43a1c:T=1602509774:S=ALNI_MYXSmH2NoAyaKJquvN46yFovaPADQ; Hm_lvt_453ab3ca06e82d916be6d6937c3bf101=1602509642,1602510065; connect.sid=s%3AYKJ5aH6MgkOpf0iZ_pO6Oku9_7aQyW4F.bRy6x3u7hzhtVucHRUqjYmmZ3u3Wr3rXlFkaxdA%2FvtM; hd_hongbao=1; Hm_lpvt_453ab3ca06e82d916be6d6937c3bf101=1602590764",
  "origin":"https://www.veryins.com",
  "referer" :"https://www.veryins.com/vivian19941008",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
  "x-requested-with": "XMLHttpRequest"
}

url = "https://www.veryins.com/vivian19941008"


resp = requests.get(url,headers=headers, timeout=5)
html_doc = resp.content.decode("utf-8")
print(html_doc)
soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
#获取所有的链接

for i in soup.find_all('div',class_="img-wrap"):
    name = str(i.get("data-code"))
    print(name)
    save(i.get("data-src"),name)


