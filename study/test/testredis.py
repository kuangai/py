#-*- coding:utf-8 -*-

import redis   # 导入redis 模块

r = redis.Redis(host='10.20.32.240',password='redis@123', port=26380)

print r.get('a')
