#!/usr/bin/env python2.7.6
# -*- coding: gbk -*-
'''
�ƶ�ָ��Ŀ¼��ָ����׺��ָ�������ļ�����һ��Ŀ¼
������1.Դ�ļ�·����2.Ŀ���ļ�·����3.�ļ����ͣ���׺������4.�ļ����а������ڣ�5.�Ƿ��滻ͬ���ļ�

@author: ���.20550
'''

import os
import re
import sys
import shutil
from sys import argv

source_file_path = "D:\\test\\scripts"
dest_file_path = "D:\\test\\temp"
file_type = ""
file_date = "2018-03-20"
replace_same_name_file = "true"

# source_file_path = argv[1]
# dest_file_path = argv[2]
# file_type = argv[3]
# file_date = argv[4]
# replace_same_name_file = argv[5]

allfile = []


def getallfile(path):
    allfilelist = os.listdir(path)
    for file in allfilelist:
        filepath = os.path.join(path, file)
        allfile.append(filepath)
        # �ж��ǲ����ļ���
        if os.path.isdir(filepath):
            getallfile(filepath)
    return allfile


if not os.path.exists(source_file_path):
    print "Դ�ļ������ڣ�Ŀ¼·��" + source_file_path
    sys.exit(-1)
if not os.path.exists(dest_file_path):
    os.makedirs(dest_file_path)

allfiles = getallfile(source_file_path)
source_file_path_list = source_file_path.split("\\")
for tempfile in allfiles:
    file_list = tempfile.split("\\")
    if dest_file_path.endswith(os.path.sep):
        dest_path_ext = dest_file_path[:-1]
    else:
        dest_path_ext = dest_file_path
    # print file_list
    for i in range(len(source_file_path_list), len(file_list)):
        dest_path_ext = dest_path_ext + os.path.sep + file_list[i]
    # print dest_path_ext
    if os.path.isdir(tempfile):
        if not os.path.isdir(dest_path_ext):
            os.makedirs(dest_path_ext)
    else:
        filename = file_list[len(file_list) - 1]
        if file_type == " " and file_date == " ":
            if os.path.isfile(dest_path_ext) and replace_same_name_file == "false":
                continue
            else:
                shutil.move(tempfile, dest_path_ext)
        elif (file_type != " ") and (file_type in filename) and \
                (file_date != " ") and (file_date in filename):
            if os.path.isfile(dest_path_ext) and replace_same_name_file == "false":
                continue
            else:
                shutil.move(tempfile, dest_path_ext)
        elif (file_type != " ") and (file_type in filename) and (file_date == " "):
            if os.path.isfile(dest_path_ext) and replace_same_name_file == "false":
                continue
            else:
                shutil.move(tempfile, dest_path_ext)
        elif (file_date != " ") and (file_date in filename) and (file_type == " "):
            if os.path.isfile(dest_path_ext) and replace_same_name_file == "false":
                continue
            else:
                shutil.move(tempfile, dest_path_ext)
print "�ƶ��ļ��ɹ�"
sys.exit(0)