#-*- coding:utf-8 -*-
import json
import os,sys,string
output = open('output.txt', 'w')
names = []
for root,dirs,files in os.walk('E:\component'):
    for f in files:
        # print f.decode('gbk').encode('utf8')
        print f.decode('utf8').encode('cp936')