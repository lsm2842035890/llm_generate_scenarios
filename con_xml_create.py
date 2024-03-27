import xml.etree.ElementTree as ET
import os
import random
def create_connections_xml(connections_data_list, output_path, connect_filename):
    # 创建根元素
    root = ET.Element('connections')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:noNamespaceSchemaLocation', 'http://sumo.dlr.de/xsd/connections_file.xsd')

    # 遍历 connections_data_list 生成 connection 元素
    for connection_data in connections_data_list:
        # 生成 connection 元素
        connection = ET.SubElement(root, "connection", attrib=connection_data)

    # 创建 ElementTree 对象
    tree = ET.ElementTree(root)
    output_file = os.path.join(output_path, f"{connect_filename}.con.xml")
    # 构建输出文件名，确保以 ".con.xml" 结尾

    # 将 XML 写入文件
    tree.write(output_file, xml_declaration=True, encoding="UTF-8", method="xml")
    return output_file

def generate_connect_data_list(num_pairs,from_to_pairs):
    # 生成 edge_data_list
    connect_data_list = []
    for i in range(0, num_pairs):
        from_edge = random.choice(from_to_pairs)
        to_edge = random.choice(from_to_pairs)
        while from_edge == to_edge:  # 确保 from 和 to 不相等
            to_edge = random.choice(from_to_pairs)
        connect_data = {
            "from": from_edge,
            "to": to_edge,
        }
        connect_data_list.append(connect_data)
    return connect_data_list

# 示例数据
connections_data_list = [
    {"from": "1si", "to": "3o"},
    {"from": "1si", "to": "2o"},
    {"from": "2si", "to": "4o"},
    {"from": "2si", "to": "1o"},
]

# 生成 XML 文件
#create_connections_xml(connections_data_list, "E:\pycharmcode\pythonProject\maps\cross3l_edge2edge_conns", "connect")
#print(generate_connect_data_list(5,['a','b','c','d','e']))