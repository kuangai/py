import configparser
import os
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
import pandas as pd
from openpyxl import load_workbook
from pandas import DataFrame
import shutil

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def deal_inner_field_self(field, params, systemType, appType, appName, nodeId, filter_map):
    # 加入参数
    one = {}
    if field.text is None:
        text = ""
        if field.attrib.get("default") is not None:
            text = field.attrib.get("default")
    else:
        text = field.text.strip()

    one['参数值'] = text
    one["一级类型"] = systemType
    one["二级类型"] = appType
    one["应用名称"] = appName
    one["节点id"] = nodeId
    one["参数"] = field.attrib.get('name')
    one["参数说明"] = field.attrib.get('label')

    zgfieldtype = field.attrib.get('zgfieldtype')
    if zgfieldtype is None or str(zgfieldtype) == '':
        zgfieldtype = "默认"
    one["参数类型"] = zgfieldtype
    zgfiledtime = field.attrib.get('zgfiledtime')
    if zgfiledtime is None:
        zgfiledtime = ""
    one["参数新增时间"] = zgfiledtime
    isfilter = filter_map.get(str(appName + "#" + one["节点id"] + "#" + one["参数"] + "#"))
    if isfilter is None or isfilter is not True:
        params.append(one)


def deal_inner_field(field1, support_param_types, params, systemType, appType, appName, nodeId, filter_map):
    listfield = []
    listfield.append(field1)
    while len(listfield) > 0:
        tmpfield = listfield.pop(0)
        if tmpfield.attrib.get("type") is not None  and  tmpfield.attrib.get('type') == "switchForm":
            deal_inner_field_self(tmpfield, params, systemType, appType, appName, nodeId, filter_map)

        if tmpfield is None:
            continue
        innerfields = tmpfield.findall("field")


        if len(innerfields) > 0:
            for field in innerfields:
                aa = field.attrib.get("type")
                bb = field.attrib.get("name")
                if field.attrib.get("type") is not None \
                        and (support_param_types.__contains__(field.attrib.get('type'))):
                    # 加入参数
                    one = {}
                    if field.text is None:
                        text = ""
                        if field.attrib.get("default") is not None:
                            text = field.attrib.get("default")
                    else:
                        text = field.text.strip()

                    one['参数值'] = text
                    one["一级类型"] = systemType
                    one["二级类型"] = appType
                    one["应用名称"] = appName
                    one["节点id"] = nodeId
                    one["参数"] = field.attrib.get('name')
                    one["参数说明"] = field.attrib.get('label')

                    zgfieldtype = field.attrib.get('zgfieldtype')
                    if zgfieldtype is None or str(zgfieldtype) == '':
                        zgfieldtype = "默认"
                    one["参数类型"] = zgfieldtype
                    zgfiledtime = field.attrib.get('zgfiledtime')
                    if zgfiledtime is None:
                        zgfiledtime = ""
                    one["参数新增时间"] = zgfiledtime
                    isfilter = filter_map.get(str(appName + "#" + one["节点id"] + "#" + one["参数"] + "#"))
                    if isfilter is None or isfilter is not True:
                        params.append(one)

                else:
                    if field.attrib.get("type") is not None and field.attrib.get("type") == 'grid':
                        pass
                    # 其他类型，判断是否有嵌套
                    else:
                        if len(field.findall("field")) > 0:
                            listfield.append(field)

        else:
            continue


def get_real_sheet_name(excel_path, sheet_name):
    writer = pd.ExcelWriter(excel_path, engine='openpyxl', mode='a')  # 用于首次写入还可自动加表头
    workbook = load_workbook(excel_path)  # 打开要写入数据的工作簿
    writer.book = workbook
    tmpi = 2
    tmp_sheet_name = sheet_name
    while tmp_sheet_name in workbook.sheetnames:
        tmp_sheet_name = sheet_name + str(tmpi)
        tmpi = tmpi + 1
    workbook.close()
    return tmp_sheet_name


def deal_database_param(databases=None, params=None, systemType=None, appType=None, appName=None, nodeId=None,
                        filter_map={}):
    if databases is None or params is None:
        return
    if databases is not None:
        database_list = databases.findall("database")
        if database_list is not None and len(database_list) > 0:
            for database in database_list:
                if database.attrib.get("id") is not None:
                    auth = database.find("auth")
                    if auth is not None:
                        user = auth.attrib.get("user")
                        if user is None:
                            user = ""
                        one = {}
                        one['参数值'] = "user#" + user
                        one["一级类型"] = systemType
                        one["二级类型"] = appType
                        one["应用名称"] = appName
                        one["节点id"] = nodeId
                        one["参数"] = "database|" + database.attrib.get("id") + ":" + "auth"
                        one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库user,参数值#后配置用户名"
                        one["参数类型"] = "数据库"
                        one["参数新增时间"] = ''
                        isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(one)

                        # 't2_grid_channel_mgr_servers服务治理集群'
                        password = auth.attrib.get("password")
                        if password is None:
                            password = ""
                        one = {}
                        one['参数值'] = "password#" + password
                        one["一级类型"] = systemType
                        one["二级类型"] = appType
                        one["应用名称"] = appName
                        one["节点id"] = nodeId
                        one["参数"] = "database|" + database.attrib.get("id") + ":" + "auth"
                        one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库密码,参数值#后配置密码"
                        one["参数类型"] = "数据库"
                        one["参数新增时间"] = ''
                        isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(one)

                    type = database.attrib.get("type")
                    if type is None:
                        type = "mysql"
                    one = {}
                    one['参数值'] = type
                    one["一级类型"] = systemType
                    one["二级类型"] = appType
                    one["应用名称"] = appName
                    one["节点id"] = nodeId
                    one["参数"] = "database|" + database.attrib.get("id") + ":" + "type"
                    one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库类型"
                    one["参数类型"] = "数据库"
                    one["参数新增时间"] = ''
                    isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                    if isfilter is None or isfilter is not True:
                        params.append(one)

                    enable = database.attrib.get("enable")
                    enabled = database.attrib.get("enabled")

                    if enable is None:
                        if enabled is None:
                            enables = "true"
                        else:
                            enables = enabled
                    else:
                        enables = enable
                    one = {}
                    one['参数值'] = enables
                    one["一级类型"] = systemType
                    one["二级类型"] = appType
                    one["应用名称"] = appName
                    one["节点id"] = nodeId
                    one["参数"] = "database|" + database.attrib.get("id") + ":" + "enable"
                    one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库是否启用"
                    one["参数类型"] = "数据库"
                    one["参数新增时间"] = ''
                    isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                    if isfilter is None or isfilter is not True:
                        params.append(one)

                    backup = database.attrib.get("backup")
                    if backup is None:
                        backup = "true"
                    one = {}
                    one['参数值'] = backup
                    one["一级类型"] = systemType
                    one["二级类型"] = appType
                    one["应用名称"] = appName
                    one["节点id"] = nodeId
                    one["参数"] = "database|" + database.attrib.get("id") + ":" + "backup"
                    one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库是否备份"
                    one["参数类型"] = "数据库"
                    one["参数新增时间"] = ''
                    isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                    if isfilter is None or isfilter is not True:
                        params.append(one)

                    user = database.attrib.get("user")
                    if user is not None:
                        one = {}
                        one['参数值'] = user
                        one["一级类型"] = systemType
                        one["二级类型"] = appType
                        one["应用名称"] = appName
                        one["节点id"] = nodeId
                        one["参数"] = "databases|selectedDatabases|user:" + database.attrib.get("id")
                        one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库user"
                        one["参数类型"] = "数据库"
                        one["参数新增时间"] = ''
                        isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(one)

                    host = database.attrib.get("host")
                    if host is None:
                        host = ""
                    one = {}
                    one['参数值'] = host
                    one["一级类型"] = systemType
                    one["二级类型"] = appType
                    one["应用名称"] = appName
                    one["节点id"] = nodeId
                    one["参数"] = "database|" + database.attrib.get("id") + ":" + "host"
                    one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库host"
                    one["参数类型"] = "数据库"
                    one["参数新增时间"] = ''
                    isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                    if isfilter is None or isfilter is not True:
                        params.append(one)

                    port = database.attrib.get("port")
                    if port is None:
                        port = ""
                    one = {}
                    one['参数值'] = port
                    one["一级类型"] = systemType
                    one["二级类型"] = appType
                    one["应用名称"] = appName
                    one["节点id"] = nodeId
                    one["参数"] = "database|" + database.attrib.get("id") + ":" + "port"
                    one["参数说明"] = "id为【" + database.attrib.get("id") + "】的数据库port"
                    one["参数类型"] = "数据库"
                    one["参数新增时间"] = ''
                    isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
                    if isfilter is None or isfilter is not True:
                        params.append(one)

                        # 服务名


def excel2map(path='D:\\test\\test.xlsx', sheet_name='Sheet1', k_col_index=3, v_col_index=4):
    """
    excel2map
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
        val = [item.value for item in list(worksheet.rows)[i]]  # 整行
        if key is None:
            # map[key] = val 不会报错
            print('\033[4;33m' + '第【{}】行【{}】列为空，已跳过……'.format(i, k_col_index) + '\033[0m')
        else:
            if val is None:
                print('\033[4;33m' + '第【{}】行为空'.format(i) + '\033[0m')
            map[key] = val

    print(map)
    return map


def hidden_sheet(path='D:\\test\\test.xlsx', sheet_name='方案名称'):
    workbook = load_workbook(path)  # 打开要写入数据的工作簿
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]  # 打开要编辑的工作表
        sheet.sheet_state = 'hidden'
    workbook.save(path)
    workbook.close()


def write_excel_node(path, sheet_name, listmap=[]):
    if len(listmap) == 0:
        return True
    try:
        workbook = load_workbook(path)  # 打开要写入数据的工作簿
        sheet = workbook[sheet_name]  # 打开要编辑的工作表
        for j in range(0, len(listmap)):  # value.shape[1]获得列数
            nodecell = sheet.cell(row=1, column=j + 6).value
            usercell = sheet.cell(row=2, column=j + 6).value
            if usercell is not None and str(usercell) != "":
                continue
            if nodecell is None or str(nodecell) == '':
                break
            else:
                for k in range(0, len(listmap)):
                    if str(nodecell).lower().replace(".", "") == str(listmap[k]['node']).lower().replace(".", ""):
                        sheet.cell(row=2, column=j + 6, value=listmap[k]['user'])

            #  sheet.cell(row=3, column=j + 6, value=listmap[j]['selected'])
        workbook.save(path)
        workbook.close()
        print('方案名称 sheet 写入成功……')
        return True
    except Exception as e:
        print('Error 方案名称 sheet 写入失败……', e.args, e.__traceback__.tb_lineno)
        if e.args.__contains__('Permission denied'):
            print("Error: 【请关闭待写入的excel】")
        return False


def deal_node_params(node=None, params=None, systemType=None, appType=None, appName=None, nodeId=None,
                     support_param_types=None, filter_map={}):
    if node is None or nodeId is None:
        return
    variables = node.find('variables')
    if variables is None:
        return
    fields = variables.findall('field')
    for field in fields:
        if field is not None \
                and field.attrib.get('type') is not None \
                and support_param_types.__contains__(field.attrib.get('type')):
            one = {}

            if field.text is None:
                text = ""
            else:
                text = field.text.strip()

            param_val = text
            if param_val is None or param_val.strip() == '':
                param_val = field.attrib.get('default')

            if field.attrib.get('name') != "grid":
                param_val = "[all|" + str(param_val) + "]"

            one['参数值'] = param_val
            one["一级类型"] = systemType
            one["二级类型"] = appType
            one["应用名称"] = appName
            one["节点id"] = nodeId
            one["参数"] = field.attrib.get('name')
            one["参数说明"] = field.attrib.get('label')
            zgfieldtype = field.attrib.get('zgfieldtype')
            if zgfieldtype is None or str(zgfieldtype) == '':
                zgfieldtype = "默认"
            one["参数类型"] = zgfieldtype
            zgfiledtime = field.attrib.get('zgfiledtime')
            if zgfiledtime is None:
                zgfiledtime = ""
            one["参数新增时间"] = zgfiledtime
            isfilter = filter_map.get(str(appName + "#" + nodeId + "#" + one["参数"] + "#"))
            if isfilter is None or isfilter is not True:
                params.append(one)
        else:
            if field is not None:
                deal_inner_field(field, support_param_types, params, systemType, appType, appName, nodeId,
                                 filter_map)


def deal_grid_params(excel_path=None, grid_tag=None, sheet_name=None):
    """
    grid参数生成sheet
    :param sheet_name:
    :param excel_path:
    :param grid_tag: grid标签对象
    :return: 处理结果 True or False
    """
    if excel_path is None or grid_tag is None or sheet_name is None:
        return False

    grid_name = grid_tag.attrib.get('label')
    if grid_name is None:
        grid_name = grid_tag.attrib.get('name')
    fields = grid_tag.findall('field')
    if len(fields) == 0:
        print('grid：【{}】 缺少field字段,请检查deploy.xml，本次不再处理……'.format(grid_name))
        return False

    col = []
    for field in fields:
        col.append(field.attrib.get('name'))
    grid_df = DataFrame(columns=tuple(col))  # 生成空的pandas表

    data_str = grid_tag.text
    print("grid内容如下：")
    print(data_str.strip())
    print("grid标签如下：")
    for field in fields:
        print(field.attrib.get("name"))
    if data_str is None or data_str.strip() == '':
        tmp = []
        for field in fields:
            str = field.text
            if str is None:
                str = ""

            tmp.append(str.strip())
        grid_df.loc[0] = tmp
    else:
        tmp_arr = data_str.strip().split(';')
        if len(tmp_arr) == 0:
            return
        for k in range(0, len(tmp_arr)):
            if (len(tmp_arr[k].split(',')) == len(fields)):
                grid_df.loc[k] = tmp_arr[k].split(',')
    print(grid_name + '  参数如下：')
    print(grid_df)

    try:
        re = write_excel_append(excel_path, sheet_name, grid_df)
        if re:
            print(grid_name, " grid sheet写入成功……")
            print('\n')
            return True
        else:
            print(grid_name, " grid sheet写入失败……")
            return False
    except Exception as e:
        print("Error" + grid_name + " grid sheet写入失败……", e.args, e.__traceback__.tb_lineno)
        if e.args.__contains__('Permission denied'):
            print("Error: 【请关闭待写入的excel】")
            print('\n')
        return False


def write_excel_append(path, sheet_name, dateframe=None):
    # 参数说明: [变量顺序可改变，依次是：sheet页对象，要写入的dataframe对象，从哪一行开始写入]

    try:
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
            writer.close()
            return True
        sheet = workbook[sheet_name]  # 打开要编辑的工作表

        if start_row <= 1:
            #  sheet 已存在，直接追加会新增一个同名的sheet页，所以先复制再追加。
            writer.sheets = dict((ws.title, ws) for ws in workbook.worksheets)  # 复制已存在的sheet
            dateframe.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
            writer.save()
            writer.close()
            return True

        for i in range(0, rows):
            for j in range(0, cols):  # value.shape[1]获得列数
                sheet.cell(row=start_row + 1 + i, column=j + 1, value=dateframe.iloc[i][j])
        workbook.save(path)
        workbook.close()
        return True
    except Exception as e:
        print("Error 参数配置表sheet 写入失败…… ", e.args, e.__traceback__.tb_lineno)
        if e.args.__contains__('Permission denied'):
            print("Error: 【请关闭待写入的excel】")
        return False


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


def write_excel_package(excel_path=None, sheet_name="安装包列表", packagelist=[]):
    packagedf = DataFrame(columns=('部署包类型', '一级类型', '二级类型', '应用名称', '安装顺序', '部署包名称', '最低兼容版本', '最高兼容版本'))  # 生成空的pandas表

    try:
        writer = pd.ExcelWriter(excel_path, engine='openpyxl', mode='a')  # 用于首次写入还可自动加表头
        workbook = load_workbook(excel_path)  # 打开要写入数据的工作簿
        writer.book = workbook

        for k in range(0, len(packagelist)):
            var = packagelist[k]
            s = []
            s.append(var['部署包类型'])
            s.append(var['一级类型'])
            s.append(var['二级类型'])
            s.append(var['应用名称'])
            s.append(var['安装顺序'])
            s.append(var['部署包名称'])
            s.append(var['最低兼容版本'])
            s.append(var['最高兼容版本'])
            packagedf.loc[k] = s

        if sheet_name in workbook.sheetnames:
            workbook.remove(workbook[sheet_name])

        packagedf.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
        writer.save()
        workbook.close()
        print("安装包列表 sheet写入成功……")
        return True
    except Exception as e:
        print("Error 安装包列表sheet写入失败……", e.args, e.__traceback__.tb_lineno)
        if e.args.__contains__('Permission denied'):
            print("Error: 【请关闭待写入的excel】")
        return False


def xml2excel(xml_path=None, excel_path=None, lists={}, nodemaplist=[], packagelist=[], filter_map={}):
    """
    xml数据以追加的方式转存excel
    :param xml_path:
    :param excel_path:
    :param lists: 从上层穿过来的部分参数，（excel部署包配置页 的数据）
    :param packagelist 每次解析时补充安装的信息到列表，用于最后生成 安装包列表sheet
    :param nodemaplist 每次解析时补充节点的信息到列表，用于最后补入 方案名称sheet
    :return: 处理结果
    """

    support_param_types = ['password', 'input', 'select', 'timestamp', 'switch', 'complexSelect']
    try:
        if xml_path == None or excel_path == None:
            return
        params = []

        with open(xml_path, 'tr', encoding='utf-8') as rf:
            tree = ET.parse(rf)
            root = tree.getroot()
            basic = root.find('basic')
            systemType = lists[0]
            version = str(basic.find('version').text).strip()
            appType = lists[1]
            appName = basic.find('appName').text

            # 收集部署包sheet需要的数据
            packagemap = {}
            packagemap["部署包类型"] = "组件" if 'inner' == systemType else "应用"
            packagemap["一级类型"] = systemType
            packagemap["二级类型"] = appType
            packagemap["应用名称"] = appName
            packagemap["安装顺序"] = lists[3]
            packagemap["部署包名称"] = str(lists[4]).split('\\')[-1]
            packagemap["最低兼容版本"] = version  # todo
            packagemap["最高兼容版本"] = version
            packagelist.append(packagemap)

            # 全局参数
            global_config = root.find('globalConfig')

            # 数据库参数
            databases = global_config.find('databases')
            deal_database_param(databases, params, systemType, appType, appName, "", filter_map)

            # 常规参数
            global_variables = global_config.find('variables')
            if global_variables is not None:
                # grid
                global_grid_fields = r_find_all(global_variables, target='field', type='grid')
                if len(global_grid_fields) > 0:
                    print(appName, ' 全局参数中对应的grid类型参数共【{}】个'.format(len(global_grid_fields)))
                    for grid in global_grid_fields:

                        sheet_name = grid.attrib.get('label')
                        sheet_name = get_real_sheet_name(excel_path, sheet_name)  # TODO
                        grid_param = {'参数值': "grid：" + sheet_name, "一级类型": systemType, "二级类型": appType, "应用名称": appName,
                                      "节点id": '', "参数": grid.attrib.get('name'),
                                      "参数说明": grid.attrib.get('label')}

                        zgfieldtype = grid.attrib.get('zgfieldtype')
                        if zgfieldtype is None or str(zgfieldtype) == '':
                            zgfieldtype = "默认"
                        grid_param["参数类型"] = zgfieldtype
                        zgfiledtime = grid.attrib.get('zgfiledtime')
                        if zgfiledtime is None:
                            zgfiledtime = ""
                        grid_param["参数新增时间"] = zgfiledtime
                        isfilter = filter_map.get(str(appName + "#" + "#" + grid_param["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(grid_param)
                            deal_grid_params(excel_path, grid, sheet_name)
                # 常规参数
                fields = global_variables.findall('field')
                for field in fields:
                    if field is not None \
                            and field.attrib.get('type') is not None \
                            and support_param_types.__contains__(field.attrib.get('type')):
                        one = {}
                        if field.text is None:
                            text = ""
                        else:
                            text = field.text.strip()
                        one['参数值'] = text
                        one["一级类型"] = systemType
                        one["二级类型"] = appType
                        one["应用名称"] = appName
                        one["节点id"] = ''
                        one["参数"] = field.attrib.get('name')
                        one["参数说明"] = field.attrib.get('label')

                        zgfieldtype = field.attrib.get('zgfieldtype')
                        if zgfieldtype is None or str(zgfieldtype) == '':
                            zgfieldtype = "默认"
                        one["参数类型"] = zgfieldtype
                        zgfiledtime = field.attrib.get('zgfiledtime')
                        if zgfiledtime is None:
                            zgfiledtime = ""
                        one["参数新增时间"] = zgfiledtime
                        isfilter = filter_map.get(str(appName + "#" + one["节点id"] + "#" + one["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(one)
                    else:
                        if field is not None:
                            deal_inner_field(field, support_param_types, params, systemType, appType, appName, "",
                                             filter_map)
            # 节点参数
            subSystems = root.find('subSystems')
            systems = subSystems.findall('system')
            for i in range(0, len(systems)):
                sys = systems[i]
                if sys is None:
                    continue
                nodemap = {}

                # 收集方案名称sheet需要的参数
                nodemap['user'] = ""  # todo 用户
                nodemap['node'] = sys.attrib.get('id')
                # nodemap['selected'] = '√'

                # 数据库参数
                databases = sys.find('databases')
                deal_database_param(databases, params, systemType, appType, appName, sys.attrib.get('id'), filter_map)

                # 常规参数
                variables = sys.find('variables')
                if variables is None:
                    continue

                # 单独处理grid参数，由于grid参数标签层级不固定，因此类似递归查询，每个grid单独生成新的sheet页
                grid_fields = r_find_all(sys, target='field', type='grid')
                if len(grid_fields) > 0:
                    print(appName, ' 当前节点【{}】对应的grid类型参数共【{}】个'.format(sys.attrib.get('id'), len(grid_fields)))
                    for grid in grid_fields:
                        sheet_name = grid.attrib.get('label')
                        sheet_name = get_real_sheet_name(excel_path, sheet_name)  # TODO
                        grid_param = {'参数值': "grid：" + sheet_name, "一级类型": systemType, "二级类型": appType, "应用名称": appName,
                                      "节点id": sys.attrib.get('id'), "参数": grid.attrib.get('name'),
                                      "参数说明": grid.attrib.get('label')}

                        zgfieldtype = grid.attrib.get('zgfieldtype')
                        if zgfieldtype is None or str(zgfieldtype) == '':
                            zgfieldtype = "默认"
                        grid_param["参数类型"] = zgfieldtype
                        zgfiledtime = grid.attrib.get('zgfiledtime')
                        if zgfiledtime is None:
                            zgfiledtime = ""
                        grid_param["参数新增时间"] = zgfiledtime
                        isfilter = filter_map.get(
                            str(appName + "#" + grid_param["节点id"] + "#" + grid_param["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(grid_param)
                            deal_grid_params(excel_path, grid, sheet_name)

                # 私有节点参数
                node = sys.find('node')
                if node is not None and sys.attrib.get('id') is not None:
                    deal_node_params(node, params, systemType, appType, appName, sys.attrib.get('id'),
                                     support_param_types, filter_map)

                fields = variables.findall('field')
                for field in fields:

                    if field.attrib.get("name") is not None and field.attrib.get(
                            "name") == 'user' and field.text is not None:
                        nodemap['user'] = field.text.strip()

                    if field is not None \
                            and field.attrib.get('type') is not None \
                            and support_param_types.__contains__(field.attrib.get('type')):
                        one = {}
                        if field.text is None:
                            text = ""
                        else:
                            text = field.text.strip()

                        param_val = text
                        if param_val is None or param_val.strip() == '':
                            param_val = field.attrib.get('default')
                        one['参数值'] = param_val
                        one["一级类型"] = systemType
                        one["二级类型"] = appType
                        one["应用名称"] = appName
                        one["节点id"] = sys.attrib.get('id')
                        one["参数"] = field.attrib.get('name')
                        one["参数说明"] = field.attrib.get('label')
                        zgfieldtype = field.attrib.get('zgfieldtype')
                        if zgfieldtype is None or str(zgfieldtype) == '':
                            zgfieldtype = "默认"
                        one["参数类型"] = zgfieldtype
                        zgfiledtime = field.attrib.get('zgfiledtime')
                        if zgfiledtime is None:
                            zgfiledtime = ""
                        one["参数新增时间"] = zgfiledtime
                        isfilter = filter_map.get(str(appName + "#" + one["节点id"] + "#" + one["参数"] + "#"))
                        if isfilter is None or isfilter is not True:
                            params.append(one)
                    else:
                        if field is not None:
                            deal_inner_field(field, support_param_types, params, systemType, appType, appName,
                                             sys.attrib.get('id'),
                                             filter_map)

                nodemaplist.append(nodemap)
        # print (date)
        paramsdf = DataFrame(
            columns=('一级类型', '二级类型', '应用名称', '节点id', '参数', '参数说明', '参数值', '参数类型', '参数覆盖', '参数新增时间'))  # 生成空的pandas表

        re = False
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
                s.append(var['参数类型'])
                s.append("")
                s.append(var['参数新增时间'])
                paramsdf.loc[k] = s
            print('本次读取常规参数如下：')
            print(paramsdf)
            print("开始写入参数配置表 sheet……")
            re = write_excel_append(excel_path, sheet_name, paramsdf)
            if re:
                print("写入参数配置表 sheet成功……")
            else:
                print("写入参数配置表 sheet失败……")

        except Exception as e:
            print("Error 写入参数配置表 sheet失败……", e.args, e.__traceback__.tb_lineno)
            if e.args.__contains__('Permission denied'):
                print("Error: 【请关闭待写入的excel】")
            return False
        rf.close()
        print("this time xml2excel execute is fine")
        return re
    except Exception as e:
        print('Error 解析xml出错了……', e.args, e.__traceback__.tb_lineno)
        return False


def deal_zip(zip=None, zip_name='', excel_path=None, lists={}, nodemaplist=[], packagelist=[]):
    filter_map = sheet2set(excel_path, "默认参数配置页", [3, 4, 5])
    re = False
    if zip == None or excel_path == None:
        print('excel路径错误，本次跳过……')
        return
    # 打印zip文件中的文件列表
    contains = [x for i, x in enumerate(zip.namelist()) if x.find('deploy.xml') != -1]
    if len(contains) > 0:
        print('当前压缩文件【{}】存在deploy.xml，提取文件。'.format(zip_name))
        xml = zip.extract(contains[0], path=None, pwd=None)
        re = xml2excel(xml, excel_path, lists, nodemaplist, packagelist, filter_map)
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
                    re = xml2excel(xml, excel_path, lists, nodemaplist, packagelist, filter_map)
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


# sheet页复制，未包含样式复制
def copySheet(old_sheet_name="全局变量配置页", new_sheet_name="全局变量配置页copy", path="F:\\test\\test.xlsx"):
    workbook = load_workbook(path)
    old_sheet = workbook[old_sheet_name]
    if new_sheet_name in workbook.sheetnames:
        workbook.remove(workbook[new_sheet_name])
    new_sheet = workbook.create_sheet(new_sheet_name)
    for row in old_sheet:
        for cell in row:
            new_sheet[cell.coordinate].value = cell.value
    workbook.save(path)
    workbook.close()


def create_global_var_sheet(path="F:\\test\\test.xlsx"):
    try:
        copySheet("全局变量配置页", "全局参数", path)
        hidden_sheet(path, "全局变量配置页")
        print("复制全局变量sheet页成功……")
    except:
        print("复制全局变量sheet页失败……")


# 将sheet页中的其中几列作为key（k_col_indexs控制列号集合），整行作为value
def sheet2map(path='F:\\test\\test.xlsx', sheet_name='参数配置表', k_col_indexs=[], isConfig=False, cols=10):
    map = {}
    workbook = load_workbook(path)
    worksheet = workbook[sheet_name]
    if len(k_col_indexs) == 0:
        # 默认参数配置页的3、4、5列，对应应用名称、节点id、参数
        k_col_indexs = [3, 4, 5]

    for i in range(1, worksheet.max_row):
        key = ""
        if isConfig and str(worksheet.cell(row=i + 1, column=11).value) != "覆盖":
            continue
        for k_col_index in k_col_indexs:
            tmp = worksheet.cell(row=i + 1, column=k_col_index).value
            if tmp is None:
                tmp = ""
            key = key + "#" + str(tmp).strip()
        val = []
        tmpi = 1
        for item in list(worksheet.rows)[i]:
            if tmpi > cols:
                break
            val.append(item.value)
            tmpi = tmpi + 1
        if key.startswith('##'):
            # map[key] = val 不会报错
            print('\033[4;33m' + '第【{}】行【{}】列为空，已跳过……'.format(i, k_col_indexs[0]) + '\033[0m')
        else:
            if val is None:
                print('\033[4;33m' + '第【{}】行为空'.format(i) + '\033[0m')
            map[key] = val
    print("读取【" + sheet_name + "】sheet页转为json如下：")
    workbook.close()
    print(map)
    return map


# 将sheet页中的其中几列作为key（k_col_indexs控制列号集合），整行作为value
def sheet2set(path='F:\\test\\test.xlsx', sheet_name='参数配置表', k_col_indexs=[]):
    map = {}
    workbook = load_workbook(path)
    worksheet = workbook[sheet_name]
    if len(k_col_indexs) == 0:
        # 默认参数配置页的3、4、5列，对应应用名称、节点id、参数
        k_col_indexs = [3, 4, 5]

    for i in range(1, worksheet.max_row):
        key = ""
        if str(worksheet.cell(row=i + 1, column=11).value) == "过滤":
            for k_col_index in k_col_indexs:
                tmp = worksheet.cell(row=i + 1, column=k_col_index).value
                if tmp is None:
                    tmp = ""
                key = key + str(tmp).strip() + "#"
            map[key] = True

    print("读取【" + sheet_name + "】sheet页转为set如下：")
    workbook.close()
    print(map)
    return map


def modify_parameter_config(path="F:\\test\\test.xlsx"):
    update_map = sheet2map(path, "默认参数配置页", [3, 4, 5], True, 10)
    if update_map is None or len(update_map.keys()) == 0:
        return
    target_map = sheet2map(path, "参数配置表", [3, 4, 5], False, 10)
    params = {}
    for update_key in update_map.keys():
        target_map[update_key] = update_map[update_key]

    paramsdf = DataFrame(
        columns=('一级类型', '二级类型', '应用名称', '节点id', '参数', '参数说明', '参数值', '参数类型', '参数覆盖', '参数新增时间'))  # 生成空的pandas表
    sheet_name = '参数配置表'
    for k in range(0, len(target_map)):
        paramsdf.loc[k] = list(target_map.values())[k]

    print("开始写入参数配置表 sheet……")

    workbook = load_workbook(path)
    if sheet_name in workbook.sheetnames:
        workbook.remove(workbook[sheet_name])
        workbook.save(path)
        workbook.close()

    re = write_excel_append(path, sheet_name, paramsdf)
    hidden_sheet(path, "默认参数配置页")
    if re:
        print("根据'默认参数配置页'修改'参数配置表'成功……")
    else:
        print("根据'默认参数配置页'修改'参数配置表'失败……")


def check_default_parameter_config(excel_path):
    map = sheet2map(excel_path, "默认参数配置页", [], False, 11)
    is_exception = False
    print("检查默认参数配置页sheet...")
    for line_num in map:
        judge_field = str(map[line_num][10]).strip()
        if judge_field != "过滤" and judge_field != "覆盖":
            print("应用名称：" + str(map[line_num][2]).strip()
                  + " 节点id：" + str(map[line_num][3]).strip()
                  + " 参数：" + str(map[line_num][4]).strip()
                  + " 所在行的 过滤/覆盖 列配置有误")
            is_exception = True
    return is_exception


def main(excel_path):
    excel_path_arr = excel_path.split(".xlsx")
    excel_path = excel_path_arr[0] + "-方案.xlsx"
    old_path = excel_path_arr[0] + ".xlsx"
    if os.path.exists(excel_path):
        try:
            os.remove(excel_path)

        except:
            print("请关闭打开的excel文件后重试……")
            return
    shutil.copy(old_path, excel_path)

    succ = []
    fail = []
    success_count = 0
    fail_count = 0
    nodemaplist = []
    packagelist = []
    map = excel2map(excel_path, "部署包配置页")

    checks = []
    for f in map:
        ppath = map[f][4]
        if not os.path.exists(ppath):
            checks.append(ppath)
            continue

    if len(checks) > 0:
        print('以下安装包路径填写错误，请检查……')
        print(checks)
        return False

    if check_default_parameter_config(excel_path):
        print('请先修改默认参数配置页中的异常配置...')
        return False

    sheet_name = "参数配置表"
    workbook = load_workbook(excel_path)
    if sheet_name in workbook.sheetnames:
        workbook.remove(workbook[sheet_name])
        workbook.save(excel_path)
        workbook.close()

    for f in map:
        curpath = map[f][4]
        print(f, ':', '【' + curpath + '】')
        try:
            z = zipfile.ZipFile(curpath, "r")
            result = deal_zip(z, curpath, excel_path, map[f], nodemaplist, packagelist)
            if result:
                success_count = success_count + 1
                succ.append(curpath)
            else:
                fail_count = fail_count + 1
                fail.append(curpath)

        except Exception as e:
            fail_count = fail_count + 1
            fail.append(curpath)
            print('Error:', e.args, e.__traceback__.tb_lineno)
            print('文件：【' + curpath + '】读取失败，本次跳过……')
            continue

    print("nodemaplist", nodemaplist)
    print("packagelist", packagelist)

    write_excel_node(excel_path, "方案名称", nodemaplist)
    write_excel_package(excel_path, "安装包列表", packagelist)
    create_global_var_sheet(excel_path)
    modify_parameter_config(excel_path)

    print('本次处理压缩文件成功：【{}】个，失败【{}】个'.format(success_count, fail_count))
    print('success: ')
    for s in succ:
        print(s)

    print('fail: ')
    for s in fail:
        print(s)

    hidden_sheet(excel_path, '部署包配置页')
    hidden_sheet(excel_path, '默认参数配置页')


def load_conf(path='./conf/conf.ini'):
    print('正在加载配置文件……')
    config = configparser.ConfigParser()
    try:
        config.read(filenames=path, encoding='utf-8')  # 搞不定就换 utf-8-sig
        print("excel路径：【{}】".format(config.get("path", "excel_path")))
    except:
        print('加载失败，请检查配置文件conf/conf.ini……')
        print('3秒后自动退出……')
        for i in range(0, 3):
            print(str(3 - i) + '……')
            time.sleep(1)
        sys.exit('end……')
    return {'excel_path': config.get("path", "excel_path")}


if __name__ == '__main__':

    print("当前程序：", sys.argv[0])
    print("命令行参数：")
    for i in range(0, len(sys.argv)):
        print(sys.argv[i])
    if len(sys.argv) >= 2 and sys.argv[1].endswith('.xlsx'):
        excel_path = sys.argv[1]
        print('excel路径OK……')
    else:
        while True:
            conf = load_conf()
            if os.path.exists(conf.get('excel_path')) and conf.get('excel_path').endswith('.xlsx'):
                print('excel路径OK……')
                excel_path = conf.get('excel_path')
                break
            else:
                print('excel路径错误，请修改配置后按 enter……')
                skip = input()
            continue

    print('---start---')
    time1 = time.time()
    main(excel_path)
    time2 = time.time()
    print('---end---spent time: ' + str(int(time2 - time1)) + 's')
    print(input('enter键结束……'))
