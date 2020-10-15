import json

import requests
from bs4 import BeautifulSoup
res = requests.get("http://wapi.http.cnapi.cc/index/index/get_free_ip")

if res.status_code == 200:
    html = json.loads(res.text)
    print(html)
#
# html = file.read()
# bs = BeautifulSoup(html,"html.parser") # 缩进格式
# print(bs.prettify()) # 格式化html结构
# print(bs.title) # 获取title标签的名称
# print(bs.title.name) # 获取title的name
# print(bs.title.string) # 获取head标签的所有内容
# print(bs.head)
# print(bs.div)  # 获取第一个div标签中的所有内容
# print(bs.div["id"]) # 获取第一个div标签的id的值
# print(bs.a)
# print(bs.find_all("a")) # 获取所有的a标签
# print(bs.find(id="u1")) # 获取id="u1"
# for item in bs.find_all("a"):
#     print(item.get("href")) # 获取所有的a标签，并遍历打印a标签中的href的值
# for item in bs.find_all("a"):
#     print(item.get_text())