import os
import random
import xml.etree.ElementTree as ET
import subprocess

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

def generate_random_node_data(num_nodes):
    node_data_list = []

    for i in range(num_nodes):
        node_id = str(i)
        x = "{:.1f}".format(random.uniform(-500.0, 500.0))
        y = "{:.1f}".format(random.uniform(-500.0, 500.0))
        node_type = random.choice(["traffic_light", "priority"])

        node_data = {"id": node_id, "x": x, "y": y, "type": node_type}
        node_data_list.append(node_data)

    return node_data_list

def node_id_set(node_data_list):
    id_set = sorted({node["id"] for node in node_data_list})
    return id_set

def create_nodes_xml(output_path, node_data):
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
    output_file = os.path.join(output_path, "nodes.nod.xml")

    # Write the formatted XML string to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(xml_str)
    return output_file

if __name__ == "__main__":
    # Specify the desired output directory
    output_directory = "E:\pycharmcode\pythonProject\maps\cross_notypes"

    # Specify the node data as a list of dictionaries
    node_data_list = [
        {"id": "0", "x": "0.0", "y": "0.0", "type": "traffic_light"},
        {"id": "1", "x": "-500.0", "y": "0.0", "type": "priority"},
        {"id": "2", "x": "+500.0", "y": "0.0", "type": "priority"},
        {"id": "3", "x": "0.0", "y": "-500.0", "type": "priority"},
        {"id": "4", "x": "0.0", "y": "+500.0", "type": "priority"},
        {"id": "m1", "x": "-250.0", "y": "0.0", "type": "priority"},
        {"id": "m2", "x": "+250.0", "y": "0.0", "type": "priority"},
        {"id": "m3", "x": "0.0", "y": "-250.0", "type": "priority"},
        {"id": "m4", "x": "0.0", "y": "+250.0", "type": "priority"}
    ]

    #node节点的id集合



    # Create nodes.nod.xml in the specified directory with the provided node data
    #node_data_list = generate_random_node_data(3)
    #print(node_id_set(node_data_list))
    node_file = create_nodes_xml(output_directory, node_data_list)



    # Specify the input and output file paths
    input_nodes_file = node_file  #"E:\pycharmcode\pythonProject\maps\cross_notypes\nodes.nod.xml"
    #input_nodes_file = "E:\pycharmcode\pythonProject\maps\cross_notypes\input_nodes.nod.xml"
    input_edges_file = "E:\pycharmcode\pythonProject\maps\cross_notypes\edge.edg.xml"
    type_file = "E:\pycharmcode\pythonProject\maps\cross_notypes\Type.typ.xml"
    output_net_file = "E:\pycharmcode\pythonProject\maps\cross_notypes\lsm.net.xml"

    # Run netconvert command
    run_netconvert(input_nodes_file, input_edges_file, type_file, output_net_file)
