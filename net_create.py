import os
import random
import xml.etree.ElementTree as ET
import subprocess
from nod_xml_create import generate_random_node_data
from nod_xml_create import node_id_set
from edge_xml_create import generate_edge_data_list
from type_xml_create import generate_random_types_data
from edge_xml_create import get_edge_ids
from con_xml_create import generate_connect_data_list
from route_create import create_routes_xml

def run_netconvert(input_nodes, input_edges, type_files, output_file):
    command = [
        "netconvert",
        f"--node-files={input_nodes}",
        f"--edge-files={input_edges}",
        f"--type-files={type_files}",
        f"--output-file={output_file}"
    ]

    try:
        subprocess.run(command, check=True)
        print("netconvert command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing netconvert command: {e}")

def run_netconvert_connect(input_nodes, input_edges, connect_files, output_file):
    command = [
        "netconvert",
        f"-n={input_nodes}",
        f"-e={input_edges}",
        f"-x={connect_files}",
        f"-o={output_file}"
    ]

    try:
        subprocess.run(command, check=True)
        print("netconvert command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing netconvert command: {e}")

def create_nodes_xml(output_path, node_data, node_filename):
    root = ET.Element("nodes")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/nodes_file.xsd")

    for data in node_data:
        node = ET.SubElement(root, "node", attrib=data)

    # Create a pretty-printed XML string
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    xml_str = xml_str.decode("utf-8")
    xml_str = xml_str.replace("><", ">\n<")  # Add newline after each closing bracket

    # Specify the output file path with "nodes" as the filename and "nod.xml" as the extension
    output_file = os.path.join(output_path, f"{node_filename}.nod.xml")

    # Write the formatted XML string to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(xml_str)
    return output_file

def create_edges_xml(edge_data_list, output_path, edge_filename):
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
    output_file = os.path.join(output_path, f"{edge_filename}.edg.xml")
    # 将 XML 写入文件
    #tree.write(output_file_path, xml_declaration=True, encoding="UTF-8", method="xml")
    with open(output_file, 'w', encoding='utf-8') as xml_file:
        for line in ET.tostringlist(root, encoding='utf-8'):
            xml_file.write(line.decode('utf-8').strip() + '\n')
    return output_file

def create_types_xml(types_data_list, output_path, type_filename):
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
    output_file = os.path.join(output_path, f"{type_filename}.typ.xml")
    # 将 XML 写入文件
    with open(output_file, 'w', encoding='utf-8') as xml_file:
        for line in ET.tostringlist(root, encoding='utf-8'):
            xml_file.write(line.decode('utf-8') + '\n')
    return output_file

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

def create_net(num_nodes, num_pairs, num_types, output_path, final_net_path, node_filename, edge_filename, type_filename):
    node_data_list = generate_random_node_data(num_nodes)
    id_set = node_id_set(node_data_list)
    node_outputfile = create_nodes_xml(output_path, node_data_list, node_filename)
    edge_data_list = generate_edge_data_list(num_pairs, id_set)
    edge_outputfile = create_edges_xml(edge_data_list,output_path,edge_filename)
    types_data_list = generate_random_types_data(num_types)
    type_outputfile = create_types_xml(types_data_list, output_path, type_filename)
    run_netconvert(node_outputfile, edge_outputfile, type_outputfile, final_net_path)

def create_net_connection(num_nodes, num_pairs, num_connect, output_path, final_net_path, node_filename, edge_filename, connect_filename):
    node_data_list = generate_random_node_data(num_nodes)
    id_set = node_id_set(node_data_list)
    node_outputfile = create_nodes_xml(output_path, node_data_list, node_filename)
    edge_data_list = generate_edge_data_list(num_pairs, id_set)
    edge_set = get_edge_ids(edge_data_list)
    edge_outputfile = create_edges_xml(edge_data_list, output_path, edge_filename)
    connect_data_list = generate_connect_data_list(num_connect, edge_set)
    connect_outputfile = create_connections_xml(connect_data_list, output_path, connect_filename)
    run_netconvert_connect(node_outputfile,edge_outputfile,connect_outputfile,final_net_path)
    create_routes_xml(edge_set,5,5,5,output_path,"Route")



#create_net(6,6, 6, "E:\pycharmcode\pythonProject", "E:\pycharmcode\pythonProject\Finalnet.net.xml", "aaa","bbb", "ccc")
create_net_connection(6,6,6,"E:\pycharmcode\pythonProject","E:\pycharmcode\pythonProject\Finalnet_CON.net.xml", "AAA1", "BBB1","CCC")
