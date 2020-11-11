import configparser
import os
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
import pandas as pd
from openpyxl import load_workbook
from pandas import DataFrame


def get_map(path='D:\\test\\test.xlsx', sheet_name='Sheet1', k_col_index=3, v_col_index=4):
    """
    两列转map
    :param k_col_index:
    :param v_col_index:
    :return:
    """
    map = {}
    workbook = load_workbook(path)
    worksheet = workbook[sheet_name]
    for i in range(1, worksheet.max_row):
        key = worksheet.cell(row=i + 1, column=k_col_index).value
        # val = worksheet.cell(row=i, column=v_col_index).value
        val = [item.value for item in list(worksheet.rows)[i]]
        if key is None:
            # map[key] = val 不会报错
            print('\033[4;33m' + '第【{}】行【{}】列为空，已跳过……'.format(i, k_col_index) + '\033[0m')
        else:
            if val is None:
                print('\033[4;33m' + '第【{}】行【{}】列为空'.format(i, v_col_index) + '\033[0m')
            map[key] = val

    print(map)
    return map


def hidden_sheet(path='D:\\test\\test.xlsx', sheet_name='服务信息'):
    workbook = load_workbook(path)  # 打开要写入数据的工作簿
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]  # 打开要编辑的工作表
        sheet.sheet_state = 'hidden'
    workbook.save(path)


def write_excel_append(path, sheet_name, dateframe=None):
    # 参数说明: [变量顺序可改变，依次是：sheet页对象，要写入的dataframe对象，从哪一行开始写入]

    writer = pd.ExcelWriter(path, engine='openpyxl', mode='a')  # 用于首次写入还可自动加表头
    workbook = load_workbook(path)  # 打开要写入数据的工作簿
    writer.book = workbook
    rows = dateframe.shape[0]  # 获得行数
    cols = dateframe.shape[1]  # 列数
    # 如果sheet不存在,直接写入，存在，从指定位置写入
    if sheet_name in workbook.sheetnames:
        start_row = workbook[sheet_name].max_row
    else:
        dateframe.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
        writer.save()
        return
    sheet = workbook[sheet_name]  # 打开要编辑的工作表

    if start_row <= 1:
        #  sheet 已存在，直接追加会新增一个同名的sheet页，所以先复制再追加。
        writer.sheets = dict((ws.title, ws) for ws in workbook.worksheets)  # 复制已存在的sheet
        dateframe.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
        writer.save()
        return

    for i in range(0, rows):
        for j in range(0, cols):  # value.shape[1]获得列数
            sheet.cell(row=start_row + 1 + i, column=j + 1, value=dateframe.iloc[i][j])
    workbook.save(path)


def r_find_all(root_tag, target='field', type=None):
    """
    遍历根标签，查询目标属性的标签
    :param root_tag: 根标签
    :param target: 需要查找的标签
    :param type: 需要查找的标签属性
    :return: 命中的标签列表
    """
    if root_tag is None or target is None: return []
    try:
        lists = list(root_tag.iter())  # 当前根节点对应的所有子元素包含当前标签
    except:
        lists = []
        print("子节点为空……")

    re = []
    while len(lists) > 0:
        root = lists.pop(0)
        if root.tag == target:
            if type is not None:
                if root.attrib["type"] == type:
                    re.append(root)
            else:
                re.append(root)
    return re


def xml2excel(xml_path=None, excel_path=None, lists={}):
    try:
        if xml_path == None or excel_path == None:
            return
        params = []
        nodemap = {}
        package = []

        with open(xml_path, 'tr', encoding='utf-8') as rf:
            tree = ET.parse(rf)
            root = tree.getroot()
            basic = root.find('basic')
            systemType = lists[0]

            appType = lists[1]

            appName = lists[2]
            subSystems = root.find('subSystems')
            systems = subSystems.findall('system')
            for i in range(0, len(systems)):
                sys = systems[i]
                if sys == None:
                    continue
                variables = sys.find('variables')
                if variables == None:
                    continue

                fields = variables.findall('field')
                for j in range(0, len(fields)):
                    if fields[j].text != None:
                        one = {}
                        one['参数值'] = fields[j].text
                        one["一级类型"] = systemType
                        one["二级类型"] = appType
                        one["应用名称"] = appName
                        one["节点id"] = sys.attrib['id']
                        one["参数"] = fields[j].attrib.get('name')
                        one["参数说明"] = fields[j].attrib.get('label')
                        # one["参数类型"]
                        params.append(one)
        # print (date)
        df = DataFrame(
            columns=('一级类型', '二级类型', '应用名称', '节点id', '参数', '参数说明', '参数值', '参数类型', '参数覆盖', '参数新增时间'))  # 生成空的pandas表
        sheet_name = '参数配置表'
        try:
            for k in range(0, len(params)):
                var = params[k]
                s = []
                s.append(var['一级类型'])
                s.append(var['二级类型'])
                s.append(var['应用名称'])
                s.append(var['节点id'])
                s.append(var['参数'])
                s.append(var['参数说明'])
                s.append(var['参数值'])
                df.loc[k] = s
            print('本次读取参数如下：')
            print(df)
            print("开始写入excel……")
            write_excel_append(excel_path, sheet_name, df)
            print("写入excel成功……")
        except Exception as e:
            print("写入excel失败……")
            if e.args.__contains__('Permission denied'):
                print("Error: 【请关闭待写入的excel】")
                return False
        rf.close()
        print("this time xml2excel execute is fine")
        return True
    except:
        print('解析xml出错了……')
        return False


def deal_zip(zip=None, zip_name='', excel_path=None, lists={}):
    re = False
    if zip == None or excel_path == None:
        print('excel路径错误，本次跳过……')
        return
    # 打印zip文件中的文件列表
    contains = [x for i, x in enumerate(zip.namelist()) if x.find('deploy.xml') != -1]
    if len(contains) > 0:
        print('当前压缩文件【{}】存在deploy.xml，提取文件。'.format(zip_name))
        xml = zip.extract(contains[0], path=None, pwd=None)
        re = xml2excel(xml, excel_path, lists)
        os.remove(xml)
        print('当前压缩文件【{}】处理完成！\n'.format(zip_name))
    else:

        for filename in zip.namelist():
            if filename.__contains__('core_sdk'):
                coresdk = zip.extract(filename, path=None, pwd=None)
                sdkzip = zipfile.ZipFile(coresdk, "r")

                contains1 = [x for i, x in enumerate(sdkzip.namelist()) if x.find('deploy.xml') != -1]
                if len(contains1) > 0:
                    xml = sdkzip.extract(contains1[0], path=None, pwd=None)
                    re = xml2excel(xml, excel_path, lists)
                    os.remove(xml)
                    print('当前压缩文件【{}】处理完成！\n'.format(zip_name))
                else:
                    print('当前压缩文件【{}】未找到deploy.xml,跳过……'.format(zip_name))
                    re = False

                sdkzip.close()
                os.remove(str(coresdk))
                break

    zip.close()
    return re


def main(excel_path):
    succ = []
    fail = []
    success_count = 0
    fail_count = 0

    map = get_map(excel_path)

    for f in map:
        curpath = map[f][4]
        print(f, ':', '【' + curpath + '】')
        try:
            z = zipfile.ZipFile(curpath, "r")
            result = deal_zip(z, curpath, excel_path, map[f])
            if result:
                success_count = success_count + 1
                succ.append(curpath)
            else:
                fail_count = fail_count + 1
                fail.append(curpath)

        except Exception as e:
            fail_count = fail_count + 1
            fail.append(curpath)
            print('Error:' + str(e.args))
            print('文件：【' + curpath + '】读取失败，本次跳过……')
            continue

    print('本次处理压缩文件成功：【{}】个，失败【{}】个'.format(success_count, fail_count))
    print('success: ')
    for s in succ:
        print(s)

    print('fail: ')
    for s in fail:
        print(s)


def load_conf(path='./conf/conf.ini'):
    print('正在加载配置文件……')
    config = configparser.ConfigParser()
    try:
        config.read(filenames=path, encoding='utf-8')  # utf-8-sig
        print("安装包路径：【{}】".format(config.get("path", "dir")))
        print("excel路径：【{}】".format(config.get("path", "excel_path")))
    except:
        print('加载失败，请检查配置文件conf/conf.ini……')
        print('3秒后自动退出……')
        for i in range(0, 3):
            print(str(3 - i) + '……')
            time.sleep(1)
        sys.exit('end……')
    return {'dir': config.get("path", "dir"), 'excel_path': config.get("path", "excel_path")}


if __name__ == '__main__':

    while True:
        conf = load_conf()
        if os.path.isdir(conf.get('dir')):
            print('安装包路径OK……')
        else:
            print('安装包路径不存在，请修改配置后按 enter……')
            skip = input()
            continue

        if os.path.exists(conf.get('excel_path')) and conf.get('excel_path').endswith('.xlsx'):
            print('excel路径OK……')
            break
        else:
            print('excel路径错误，请修改配置后按 enter……')
            skip = input()
            continue

    print('---start---')
    main(conf.get('excel_path'))
    print('---end---')
    skip = input()
