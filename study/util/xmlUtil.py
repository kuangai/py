# coding=utf-8
import xml.etree.ElementTree as ET

from pandas import DataFrame
import excelUtil


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




def read_xml(xml_path='./deploy.xml'):
    """
    读 xml文件
    :param xml_path:
    :return:
    """

    if xml_path is None:
        return

    with open(xml_path, 'tr', encoding='utf-8') as rf:
        tree = ET.parse(rf)
        root = tree.getroot()
        basic = root.find('basic')
        globalConfig = root.find('globalConfig')

        primaryType = basic.find('primaryType').text
        secondaryType = basic.find('secondaryType').text
        appName = basic.find('appName').text
        subSystems = root.find('subSystems')
        # systems = subSystems.findall('system')


        re = r_find_all(globalConfig,'field','grid')

        print('grid',re)

        print(primaryType)
        print(secondaryType)
        print(appName)
        globalConfig = root.find('globalConfig')
        variables = globalConfig.find('variables')
        res = variables.findall('field')
        print(res)
    print("this time xml2excel execute is fine")


if __name__ == '__main__':
    read_xml()
