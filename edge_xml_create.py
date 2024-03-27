import xml.etree.ElementTree as ET
import random

def create_edges_xml(edge_data_list, output_file_path):
    # 创建根元素
    #root = ET.Element("edges", xmlns="http://www.w3.org/2001/XMLSchema-instance", xsi="http://sumo.dlr.de/xsd/edges_file.xsd")
    #root.set("{" + "http://www.w3.org/2001/XMLSchema-instance" + "}noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/edges_file.xsd")
    root = ET.Element('edges')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:noNamespaceSchemaLocation', 'http://sumo.dlr.de/xsd/edges_file.xsd')

    # 遍历 edge_data_list 生成 edge 元素
    for edge_data in edge_data_list:
        # 生成 edge 元素
        #edge = ET.SubElement(root, "edge", id=edge_data["id"], from_=edge_data["from"], to=edge_data["to"],
        #                     priority=edge_data["priority"], numLanes=edge_data["numLanes"], speed=edge_data["speed"])
        #edge = ET.SubElement(root, "edge", id=edge_data["id"], from=edge_data["from"], to=edge_data["to"],
        #                     priority=edge_data["priority"], numLanes=edge_data["numLanes"], speed=edge_data["speed"])
        edge = ET.SubElement(root, "edge", attrib=edge_data)
    #ET.SubElement(edge, "\n")
    # 创建 ElementTree 对象
    tree = ET.ElementTree(root)

    # 将 XML 写入文件
    #tree.write(output_file_path, xml_declaration=True, encoding="UTF-8", method="xml")
    with open(output_file_path, 'w', encoding='utf-8') as xml_file:
        for line in ET.tostringlist(root, encoding='utf-8'):
            xml_file.write(line.decode('utf-8').strip() + '\n')

def generate_edge_data_list(num_pairs,from_to_pairs):
    # 生成 edge_data_list
    edge_data_list = []
    for i in range(0, num_pairs):
        from_node = random.choice(from_to_pairs)
        to_node = random.choice(from_to_pairs)
        while from_node == to_node:  # 确保 from 和 to 不相等
            to_node = random.choice(from_to_pairs)
        edge_data = {
            "id": f"{i}fi",
            "from": from_node,
            "to": to_node,
            "priority": str(random.randint(1, 3)),
            "numLanes": str(random.randint(1, 3)),
            "speed": "{:.3f}".format(random.uniform(10, 15))
        }
        edge_data_list.append(edge_data)
    return edge_data_list

# 生成 from 和 to 的集合
from_to_pairs = ["1", "m1", "2", "m2", "3", "m3", "4", "m4"]

def get_edge_ids(edge_data_list):
    return sorted({edge["id"] for edge in edge_data_list})


edge_data_list = [
    {"id": "1fi", "from": "1", "to": "m1", "priority": "2", "numLanes": "2", "speed": "11.111"},
    {"id": "1si", "from": "m1", "to": "0", "priority": "3", "numLanes": "3", "speed": "13.889"},
    {"id": "1o", "from": "0", "to": "1", "priority": "1", "numLanes": "1", "speed": "11.111"},
    {"id": "2fi", "from": "2", "to": "m2", "priority": "2", "numLanes": "2", "speed": "11.111"},
    {"id": "2si", "from": "m2", "to": "0", "priority": "3", "numLanes": "3", "speed": "13.889"},
    {"id": "2o", "from": "0", "to": "2", "priority": "1", "numLanes": "1", "speed": "11.111"},
    {"id": "3fi", "from": "3", "to": "m3", "priority": "2", "numLanes": "2", "speed": "11.111"},
    {"id": "3si", "from": "m3", "to": "0", "priority": "3", "numLanes": "3", "speed": "13.889"},
    {"id": "3o", "from": "0", "to": "3", "priority": "1", "numLanes": "1", "speed": "11.111"},
    {"id": "4fi", "from": "4", "to": "m4", "priority": "2", "numLanes": "2", "speed": "11.111"},
    {"id": "4si", "from": "m4", "to": "0", "priority": "3", "numLanes": "3", "speed": "13.889"},
    {"id": "4o", "from": "0", "to": "4", "priority": "1", "numLanes": "1", "speed": "11.111"},
]

# 指定输出 XML 文件的位置
output_file_path = "E:\pycharmcode\pythonProject\maps\cross_notypes\edge.edg.xml"

# 调用函数生成 XML 文件

#a = generate_edge_data_list(5,from_to_pairs)
#create_edges_xml(edge_data_list, output_file_path)
#print(get_edge_ids(edge_data_list))