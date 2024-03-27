import xml.etree.ElementTree as ET
import random

def generate_random_types_data(num_types):
    types_data_list = []
    priorities = [1, 2, 3]
    num_lanes_options = [1, 2, 3]

    for i in range(num_types):
        type_data = {
            "id": chr(ord('a') + i),
            "priority": str(random.choice(priorities)),
            "numLanes": str(random.choice(num_lanes_options)),
            "speed": str(round(random.uniform(2, 20), 3))
        }
        types_data_list.append(type_data)

    return types_data_list

def create_types_xml(types_data_list, output_file_path):
    # 创建根元素
    root = ET.Element('types')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:noNamespaceSchemaLocation', 'http://sumo.dlr.de/xsd/types_file.xsd')

    # 遍历 types_data_list 生成 type 元素
    for type_data in types_data_list:
        # 生成 type 元素
        type_element = ET.SubElement(root, "type", id=type_data["id"], priority=type_data["priority"],
                                     numLanes=type_data["numLanes"], speed=type_data["speed"])

    # 创建 ElementTree 对象
    tree = ET.ElementTree(root)

    # 将 XML 写入文件
    with open(output_file_path, 'w', encoding='utf-8') as xml_file:
        for line in ET.tostringlist(root, encoding='utf-8'):
            xml_file.write(line.decode('utf-8') + '\n')

# 示例数据
types_data_list = [
    {"id": "a", "priority": "3", "numLanes": "3", "speed": "13.889"},
    {"id": "b", "priority": "2", "numLanes": "2", "speed": "11.111"},
    {"id": "c", "priority": "1", "numLanes": "1", "speed": "11.111"},
    {"id": "d", "priority": "1", "numLanes": "1", "speed": "02.901"},
]

# 指定输出文件路径
output_file_path = 'E:\pycharmcode\pythonProject\maps\cross_notypes\Type.typ.xml'

# 生成 XML 文件
create_types_xml(types_data_list, output_file_path)
#rint(generate_random_types_data(5))