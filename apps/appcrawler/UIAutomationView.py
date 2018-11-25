# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
import yaml
import os

# 全局唯一标识
unique_id = 0


def write_yaml(json, path):
    # 写
    if type(json) != dict:
        json = eval(json)
    with open(path, 'w+') as f:
        yaml.dump(json, f, default_flow_style=False, allow_unicode=True, encoding='utf-8')

def read_yaml(path):
    # 读取案例yaml数据
    with open(path, 'r') as f:
        return yaml.load(f)

# 遍历所有的节点
def walkData(root_node, level, result_list, file_name, myyaml):
    ul = '<ul id="%s"><li id="%s">%s:%s%s</li>'
    global unique_id
    try:
        cls = root_node.attrib['class'].split('.')[-1]
        text = root_node.attrib['text']
    except:
        cls = root_node.tag
        text = ''
    if root_node.attrib.has_key('bounds'):
        ul_temp = ul % (level, unique_id, cls, text, root_node.attrib['bounds'])
    else:
        ul_temp = ul % (level, unique_id, cls, text, '[][]')
    result_list.append(ul_temp)
    myyaml.__setitem__(unique_id, root_node.attrib)

    # 全局唯一标识，递增
    unique_id += 1

    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        result_list.append('</ul>')
        write_yaml(myyaml, file_name)
        return
    for child in children_node:
        walkData(child, level + 1, result_list, file_name, myyaml)
    result_list.append('</ul>')
    write_yaml(myyaml, file_name)
    return result_list


# 获得原始数据
# out:
# <ul><li><span>xx</span></li></ul>
def getXmlData(file_name, name):
    level = 0  # 节点的深度从0开始
    myyaml = {}
    result_list = []
    root = ET.parse(file_name).getroot()
    os.remove(file_name)  #清除xml文件
    # yml
    file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                             'appcrawler/UIxml/%s.yml' % str(name))
    walkData(root, level, result_list, file_name, myyaml)
    # 运行结束，归0
    unique_id = 0

    return ''.join(result_list)

def getXmlDetail(id, path):
    js = read_yaml(path)
    return js[int(id)]

def getXY(string):
    ls = string.split('][')
    start = ls[0][1:].split(',')
    len = ls[-1][:-1].split(',')
    return start[0], start[-1], len[0], len[-1]

if __name__ == '__main__':
    # file_name = 'ui.xml'
    # R = getXmlData(file_name)
    # print read_yaml('/Users/yyfaxx/MAT/apps/appcrawler/UIxml/1529981242.yml')
    # print getXmlDetail(0,'/Users/yyfaxx/MAT/apps/appcrawler/UIxml/1529981242.yml')
    s = '[0,63][1080,1920]'
    import socket
    client = socket.socket()
    client.connect(('localhost', 1119))
    print client







