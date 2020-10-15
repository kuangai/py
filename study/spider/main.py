import os
import requests,json,ImgUtil
import proxyUtil

# https://www.veryins.com/vivian19941008 接口

def save(data, k,n):
  imgurl = data[k]["display_src"]
  path = "../../../img/vva/"
  file_name ='{}{}.jpg'.format(path,data[k]["code"])
  if os.path.exists(file_name):
    print("文件已存在,不再下载")
  else:
    ImgUtil.save_pictureurl(imgurl,file_name)
    print("已下载{}个".format(str(n)))

# import Brotli as brotli
next = 'QVFDZHlVZjY5cEY4eGpHMGVKX3BFaGsyeHRsWmctUVNzTTZISEh2cks4Z0ZGTkNIREREaWRPTUduNkdZOHYzSS0wbEY0dE9KM0ZzUFg3cUxmRVM0WUNRNg=='
url = 'https://www.veryins.com/user/post?next=' + next + '&uid=d198d673cb83f257634b1025a9073fa9&tag=1'
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

data = []
hasMore = True
i = 0
while hasMore:
  i = i + 1
  # if i > 1:
  #   print("结果：%s " % json.dumps(data))
  #   print("处理结束共操做" + str(i) + "次")
  #   break
  print("开始第" + str(i) + "次处理")
  if i > 1:
    next = jsonstr["page_info"]["end_cursor"]
    print("next:" + next)
  url = 'https://www.veryins.com/user/post?next=' + next + '&uid=d198d673cb83f257634b1025a9073fa9&tag=1'
  res = requests.post(url=url,headers=headers,proxies=proxyUtil.get_random_proxy())

  if i == 7:
    print(7)
  data1 = res.text
  jsonstr = json.loads(data1)
  hasMore = jsonstr["page_info"]["has_next_page"]
  nodes = jsonstr["nodes"]
  if len(nodes) > 0:
    for j in range(0, len(nodes)):
      data.append(nodes[j]["code"])
      if i >= 0:
        save(nodes,j,len(data))
      # data.append(nodes[j]["display_src"])
      print("第 {} 个标题：【{}】".format(str(j),nodes[j]["code"]))
    print("本次共新增：" + str(len(nodes)) + "个");
  else:
    print("处理结束共操做" + str(i) + "次")
    break

print("done!" + str(len(data)) + "张")
