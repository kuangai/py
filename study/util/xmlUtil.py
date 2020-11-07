# coding=utf-8
import xml.etree.ElementTree as ET

from pandas import DataFrame
import excelUtil

def xml2excel(xml_path=None,excel_path=None):
    if xml_path==None or excel_path==None:
        return
    date = []
    with open(xml_path, 'tr', encoding='utf-8') as rf:
        tree = ET.parse(rf)
        root = tree.getroot()
        basic = root.find('basic')
        systemType = basic.find('systemType').text
        appType = basic.find('appType').text
        appName = basic.find('appName').text
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
                    one["参数"] = fields[j].attrib['name']
                    one["参数说明"] = fields[j].attrib['label']
                    date.append(one)
    # print (date)
    df = DataFrame(columns=('一级类型', '二级类型', '应用名称','节点id','参数','参数说明','参数值'))  # 生成空的pandas表
    sheet_name = '参数配置表'
    try:
        for k in range(0, len(date)):
            var = date[k]
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
        excelUtil.write_excel_append(excel_path, sheet_name, df)
        print("写入excel成功……")
    except Exception as e:
        print("写入excel失败……")
        print("Error: " + e.__doc__)
    print("this time xml2excel execute is fine")
