import json
import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import fileUtil


#随机代理一天一换

def get_hosts(url="https://www.kuaidaili.com/free"):

    html_doc = urllib.request.urlopen(url, timeout=5).read()
    soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
    tables = soup.find_all('table', class_="table table-bordered table-striped")
    tbody = tables[0].find("tbody")
    trs = tbody.find_all("tr")
    host_list = []
    for tr in trs:
        tds = tr.find_all("td")
        host_list.append(tds[0].text + ":" + tds[1].text)
    print(host_list)
    return host_list

def get_proxy_list():

    path = "../util/proxy.json"
    diff_time = fileUtil.diff_lastModifyTime_now(path)
    if diff_time > 12:
        with open(path, 'w', encoding='utf-8') as f1:
            f1.write(json.dumps("[]", indent=4, ensure_ascii=False))
            print("代理文件距离现在{} 小时，可能已过期，清空重新抓取！")
            print("已清除！")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            info_dict = json.load(f,strict=False)
            if info_dict and len(info_dict) > 0:
                print("本次从文件获取代理对象：")
                print(info_dict)
                return info_dict
            else:
                print("未初始化，从网站爬取初始化到代理文件")
        except:
            print("未初始化，从网站爬取初始化到代理文件")

    proxy_list = []
    host_list = get_hosts()

#检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    for host in host_list:
        try:
            # 用百度检测ip代理是否成功
            url = 'https://www.baidu.com/s?'
            # 请求网页传的参数
            params = {
                'wd': 'ip地址'
            }
            # 请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
            }
            proxy_temp = {"http": host}
            # 发送get请求
            response = requests.get(url=url, headers=headers, params=params, proxies=proxy_temp,timeout=1)
            proxy_list.append(proxy_temp)
        except Exception as e:
            try:
                proxy_temp = {"https": host}
                response = requests.get(url=url, headers=headers, params=params, proxies=proxy_temp,timeout=1)
                proxy_list.append(proxy_temp)
            except Exception as e:
                host_list.remove(host)
            continue
    if len(proxy_list) > 0:
        for i in range(0,len(proxy_list)):
            print("过滤后的代理：" + str(proxy_list[i]) )
    else:
        print("该网站无可用代理！")

    with open(path, 'w', encoding='utf-8') as f1:
        f1.write(json.dumps(proxy_list, indent=4, ensure_ascii=False))
        print("代理对象已存入文件！")
    return proxy_list

#从代理代理列表中随机取出一个代理并返回
def get_random_proxy():
    ip = random.choice(get_proxy_list())
    print("本次使用的随机代理：" + str(ip))
    return ip


if __name__=="__main__":
    print(get_random_proxy())
