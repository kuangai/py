# coding=utf-8
import xml.etree.ElementTree as ET

from pandas import DataFrame
import excelUtil


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


        primaryType = basic.find('primaryType').text
        secondaryType = basic.find('secondaryType').text
        appName = basic.find('appName').text
        subSystems = root.find('subSystems')
        systems = subSystems.findall('system')

        print(primaryType)
        print(secondaryType)
        print(appName)
        globalConfig = root.find('globalConfig')
        variables = globalConfig.find('variables')
        field = variables.findall('field')
        field1 = field[7].find('field')
        field2 = field1.findall('field')
    print("this time xml2excel execute is fine")


def r_find_all(root_tag, target='field', type=None):
    """
    遍历根标签，查询目标属性的标签
    :param root_tag: 根标签
    :param target: 需要查找的标签
    :param type: 需要查找的标签属性
    :return: 命中的标签列表
    """
    if root_tag is None or target is None : return []
    list = [root_tag]
    while len(list) > 0:
        root = list.pop(0)
        all = root.findall()




if __name__ == '__main__':
    read_xml()
