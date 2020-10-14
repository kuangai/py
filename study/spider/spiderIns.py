import requests,json
# import Brotli as brotli
next = 'QVFEYklRbXN4RVVHNTZEUXAzaThVZnZtZThoeXRaQ2Y0am9yRnotWjJvajZIWXpfdTJEQ21zc2RTQzF4RTZ0X3JGaTJXNzctYjFsWFY2UmtCU1p4eVRUZg=='
url = 'https://www.veryins.com/user/post?next=' + next + '&uid=d198d673cb83f257634b1025a9073fa9&tag=1'
headers = {
  "authority": "www.veryins.com",
  "method": "POST",

  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate",
  "accept-language": "zh-CN,zh;q=0.9",
  "content-length": "0",
  "cookie":"__cfduid=dc09fea491115f0a37ecf5379562961b91602508946; connect.sid=s%3AJ03YKMk8_1yusA_vKgsX15JEWqxgH6Nt.S%2B98awcJMiTB5BEZLGIR5rjb%2BUVz5f3L2n8MsrxVyp8; Hm_lvt_453ab3ca06e82d916be6d6937c3bf101=1602508951; _ga=GA1.2.355468440.1602508950; _gid=GA1.2.300613207.1602508952; __gads=ID=45b0ea3deb051c2e:T=1602509107:S=ALNI_Mbz1-Xx6BtqURpgBx1gQkL7NUDGGA; hd_hongbao=1; Hm_lpvt_453ab3ca06e82d916be6d6937c3bf101=1602573405; _gat_gtag_UA_144009771_1=1",
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
  print("开始第" + str(i) + "次处理")
  if i > 1:
    next = jsonstr["page_info"]["end_cursor"]
  url = 'https://www.veryins.com/user/post?next=' + next + '&uid=d198d673cb83f257634b1025a9073fa9&tag=1'
  res = requests.post(url=url,headers=headers)

  data1 = res.text
  jsonstr = json.loads(data1)
  hasMore = jsonstr["page_info"]["has_next_page"]
  nodes = jsonstr["nodes"]
  if len(nodes) > 0:
    for j in range(0, len(nodes)):
      data.append(nodes[j]["display_src"])
    print("本次共新增：" + str(len(nodes)) + "个");
  else:
    print("处理结束共操做" + str(i) + "次")
    break

print(data)