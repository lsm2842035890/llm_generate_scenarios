import xml.etree.ElementTree as ET
import random
import os

def generate_random_float(min_value, max_value):
    return round(random.uniform(min_value, max_value), 2)

def create_route_chain(num_chains, connections_data_list):
    all_chains = []

    for _ in range(num_chains):
        # 从 connections_data_list 随机选择链的起始元组
        start_tuple = random.choice(connections_data_list)
        current_tuple = start_tuple
        chain_length = random.randint(3, 5)

        connection_chain = [start_tuple]

        for _ in range(chain_length - 1):
            # 从 connections_data_list 中选择下一个元组，确保首尾相等但不完全相等
            next_tuples = [item for item in connections_data_list if
                           item[0] == current_tuple[1] and item != connection_chain[-1]]

            if not next_tuples:
                break  # 如果找不到符合条件的下一个元组，终止链的生成

            next_tuple = random.choice(next_tuples)
            connection_chain.append(next_tuple)
            current_tuple = next_tuple

        # 将结果添加到所有链的列表中
        all_chains.append(connection_chain)

    return all_chains

def change_chain_format(result_chain):
    final_result = []
    for chain in result_chain:
        formatted_result = f"{chain[0][0]}"
        for item in chain:
            formatted_result = formatted_result + f" {item[1]}"
        final_result.append(f"{formatted_result}")
    return final_result

def change_connection_data_list_format(connection_data_list):
    converted_list = [(item["from"], item["to"]) for item in connection_data_list]
    return converted_list


def create_routes_xml(con_data_list, num_vtypes, num_routes, num_vehicles, output_path, route_filename):
    #a = change_connection_data_list_format(con_data_list)
    #result = create_route_chain(num_routes+5, a)
    #edges_collection = change_chain_format(result)
    #print(edges_collection)
    # 创建根元素
    root = ET.Element("routes")

    # 随机生成 vType 标签数量（3-5）
    for _ in range(num_vtypes):
        vtype = ET.SubElement(root, "vType")
        vtype.set("accel", str(generate_random_float(1.0, 3.0)))
        vtype.set("decel", str(generate_random_float(5.0, 6.0)))
        vtype.set("id", "Car" + chr(65 + _))
        vtype.set("carFollowModel", random.choice(["IDM", "ACC"]))
        vtype.set("length", str(generate_random_float(5.0, 7.5)))
        vtype.set("minGap", str(generate_random_float(2.0, 2.5)))
        vtype.set("maxSpeed", str(generate_random_float(40.0, 50.0)))
        vtype.set("sigma", "0.5")

    # 随机生成 route 标签数量（3-5）
    for i in range(1, num_routes + 1):
        route = ET.SubElement(root, "route")
        route.set("id", "route" + str(i).zfill(2))

        # 从集合中随机选择edges值

        route.set("edges", random.choice(con_data_list))

    # 随机生成 vehicle 标签数量（3-5）
    for i in range(num_vehicles):
        vehicle = ET.SubElement(root, "vehicle")
        vehicle.set("depart", "0")
        vehicle.set("id", "veh" + str(i))

        # 从route标签内不同的id选取
        vehicle.set("route", "route" + str(random.randint(1, num_routes)).zfill(2))

        # 从vType不同的id选取
        vehicle.set("type", "Car" + chr(65 + i))
        vehicle.set("color", ",".join([str(random.choice([0,1])) for _ in range(3)]))

    flow_count = random.randint(3, 5)
    for i in range(flow_count):
        flow_type = f"Car{chr(65+random.randint(1, num_vehicles-1))}"
        flow_route = f"route0{random.randint(1,num_routes)}"
        flow = ET.SubElement(root, "flow", id=f"flo{i}", type=flow_type, route=flow_route, number="3", period="1",
                             departPos="0", departLane="random")

    # 创建 ElementTree 对象
    tree = ET.ElementTree(root)
    output_file = os.path.join(output_path, f"{route_filename}.rou.xml")
    # 将 XML 写入文件
    tree.write(output_file, xml_declaration=True, encoding="UTF-8", method="xml")
    return output_file


#edges_collection = ["D2 L2 L12 L10 L7 D7", "D2 L2 L12 L15 L18 L5 D5", "D2 L2 L12 L15 L13 L3 D3"]
# 示例：生成路由文件
#create_routes_xml(edges_collection,3,3,3,"E:\pycharmcode\pythonProject","Route")
con_data_list = [
    {"from": "1si", "to": "3o"},
    {"from": "1si", "to": "2o"},
    {"from": "2si", "to": "4o"},
    {"from": "3o", "to": "1o"},
]

connections_data_list = [
    ("1si", "3o"),
    ("3o", "2o"),
    ("2o", "4o"),
    ("2si", "1si"),
]
#print(connections_data_list[0][0])
create_routes_xml(con_data_list,3,3,3,"E:\pycharmcode\pythonProject","Route")







