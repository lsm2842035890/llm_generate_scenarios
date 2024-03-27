from beamngpy import BeamNGpy, Scenario, Vehicle, Road, MeshRoad
from matplotlib import pyplot as plt
from shapely.geometry import MultiLineString
import time
import random

# Instantiate BeamNGpy instance running the simulator from the given path,
# communicating over localhost:64256
def start_scenario():
    bng = BeamNGpy('localhost', 64256, home=r'E:\BeamNG\BeamNG.tech.v0.31.3.0', user=r'E:\pycharmcode\pythonProject\beamng')
    # Launch BeamNG.tech
    bng.open()
    # Create a scenario in west_coast_usa called 'example'
    scenario = Scenario('italy', 'beamngpy_feature_overview')
    # Create an ETK800 with the licence plate 'PYTHON'
    vehicle = Vehicle('ego_vehicle', model='etk800', license='PYTHON')
    # Add it to our scenario at this position and rotation
    #scenario.add_vehicle(vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795))
    scenario.add_vehicle(vehicle, pos=(245.11, -906.94, 247.46),
                         rot_quat=(0.0010, 0.1242, 0.9884, -0.0872))
    # Place files defining our scenario for the simulator to read
    scenario.make(bng)

    # Load and start our scenario
    bng.scenario.load(scenario)
    bng.scenario.start()
    # Make the vehicle's AI span the map
    vehicle.ai.set_mode('span')
    vehicle.ai.set_speed(50)
    input('Hit enter when done...')


def get_scenarios():
    bng = BeamNGpy('localhost', 64256, home=r'E:\BeamNG\BeamNG.tech.v0.31.3.0',
                   user=r'E:\pycharmcode\pythonProject\beamng')
    bng.open()
    #scenarios = bng.scenario.get_scenarios()
    #print(scenarios.keys())
    #dict_keys(['jungle_rock_island', 'automation_test_track', 'Utah', 'gridmap_v2', 'italy', 'johnson_valley', 'east_coast_usa', 'west_coast_usa', 'derby', 'small_island', 'driver_training', 'Industrial', 'Cliff'])
    #print(f'There are {len(west_coast_scenarios)} West Coast USA scenarios that can be loaded.')
    #print(west_coast_scenarios[:10])
    scenario = Scenario(level='west_coast_usa', name='极速争抢', path='/gameplay/missions/west_coast_usa/collection/005-Speedy/info.json')
    vehicle = Vehicle('ego_vehicle', model='etk800', license='LSM')
    scenario.add_vehicle(vehicle, pos=(245.11, -906.94, 247.46),
                         rot_quat=(0.0010, 0.1242, 0.9884, -0.0872))
    #scenario.make(bng)
    bng.scenario.load(scenario)
    bng.scenario.start()
    vehicle.ai.set_mode('span')
    vehicle.ai.set_speed(10)

def plot_lines(ax, ob):
    blue = '#6699cc'
    for line in ob.geoms:
        x, y = line.xy
        ax.plot(x, y, color=blue, linewidth=1,
                    solid_capstyle='round', zorder=2, alpha=0.7)

def show_scenario_network():
    beamng = BeamNGpy('localhost', 64256)
    beamng.open()
    scenario = Scenario('west_coast_usa', 'road_map_example')
    orig = (568.908386, 13.4217358, 148.56546)
    vehicle = Vehicle('ego_vehicle', model='pickup', license='PYTHON')
    scenario.add_vehicle(vehicle, pos=orig)
    scenario.make(beamng)
    beamng.scenario.load(scenario)
    beamng.scenario.start()
    roads = beamng.scenario.get_roads()
    road_names = list(roads.keys())
    road_spec = {}
    for r_id, r_inf in roads.items():
        if r_inf['drivability'] != '-1':
            road_spec[r_id] = beamng.scenario.get_road_edges(r_id)
    road = list()
    lines = list()
    for r_id in road_spec.keys():
        left = list()
        right = list()
        for r_point in road_spec[r_id]:
            x = r_point['left'][0]
            y = r_point['left'][1]
            left.append((x, y))
            x = r_point['right'][0]
            y = r_point['right'][1]
            right.append((x, y))
        if left:
            lines.append(tuple(left))
        if right:
            lines.append(tuple(right))
    network = MultiLineString(lines)
    # plot map
    fig = plt.figure(1, figsize=[9.6, 9.6], dpi=100)
    ax = fig.add_subplot()
    plot_lines(ax, network)
    _ = ax.set_axis_off()
    _ = ax.set_title('road network West Coast, USA')
    plt.savefig('leftright.png')

def create_road():
    beamng = BeamNGpy('localhost', 64256,home=r'E:\BeamNG\BeamNG.tech.v0.31.3.0',user=r'E:\pycharmcode\pythonProject\beamng')
    beamng.open(launch=True)

    scenario = Scenario('gridmap_v2', 'road_test')
    vehicle = Vehicle('ego_vehicle', model='etk800')
    scenario.add_vehicle(vehicle, pos=(-25, 300, 100), rot_quat=(0, 0, 0, 1))

    # create a decal road
    road_a = Road('track_editor_C_center', rid='circle_road', looped=True)
    road_a.add_nodes(
        (-25, 300, 100, 5),
        (25, 300, 100, 6),
        (25, 350, 100, 4),
        (-25, 350, 100, 5),
    )
    scenario.add_road(road_a)

    road_b = Road('track_editor_C_center', rid='center_road')
    road_b.add_nodes(
        (0, 325, 100, 5),
        (50, 375, 100, 5)
    )
    scenario.add_road(road_b)

    # create a mesh road
    mesh_road = MeshRoad('track_editor_C_center', rid='main_road')
    mesh_road.add_nodes(
        (-107, 20, 100),
        (-157, 20, 110),
        (-207, 25, 120, 15, 10),  # the 4th and 5th arguments are width and depth of the node
        (-257, 15, 110),
        (-307, 20, 100, 30),
    )
    scenario.add_mesh_road(mesh_road)

    scenario.make(beamng)

    try:
        beamng.scenario.load(scenario)
        beamng.scenario.start()
        #input('Press Enter to teleport to the other road...')
        vehicle.teleport((-107, 20, 100), reset=False)
        #input('Press Enter when done...')
        #scenario._get_roads_list()
        #list = scenario.find_waypoints()
        #print(list)
        #vehicle.ai.drive_in_lane(True)
        vehicle.ai.set_mode('span')
        vehicle.ai.set_speed(20)
        #vehicle.ai.set_waypoint('center_road')
    finally:
        beamng.close()

def simple_create_road():
    bng = BeamNGpy('localhost', 64256, home=r'E:\BeamNG\BeamNG.tech.v0.31.3.0', user=r'E:\pycharmcode\pythonProject\beamng')
    bng.open()
    scenario = Scenario('smallgrid', 'custom_road_network')
    # 创建道路网络
    # create a decal road
    road_a = Road('track_editor_C_center', rid='center_road', looped=True)
    road_a.add_nodes(
        (0, 300, 0, 6),
        (0, 400, 0, 6),
        (0, 500, 0, 6),
        (0, 600, 0, 6),
    )
    scenario.add_road(road_a)
    vehicle = Vehicle('ego_vehicle', model='etk800')
    scenario.add_vehicle(vehicle,pos=(0, 300, 0), rot_quat=(0, 0, 1, 0))
    # 保存场景为prefab文件
    positions = [(0, 400, 0), (0, 500, 0), (0, 600, 0)]
    scales = [(1, 1, 1)] * 3
    ids = ['my_waypoint_1', 'my_waypoint_2', 'my_waypoint_3']
    scenario.add_checkpoints(positions, scales, ids)

    scenario.make(bng)
    bng.scenario.load(scenario)
    bng.scenario.start()
    #vehicle.teleport((-25, 300, 100), reset=False)
    print(scenario.find_waypoints())
    print('ssss')
    #vehicle.ai.drive_in_lane(True)
    vehicle.ai.set_waypoint('my_waypoint_1')
    vehicle.ai.set_speed(30,'set')
    frozen_time(10)
    vehicle.ai.set_waypoint('my_waypoint_2')
    vehicle.ai.set_speed(30, 'set')

    '''
        vehicle.ai.set_waypoint('my_waypoint_2')
        duration = 10
        start_time = time.time()
        # 进入循环
        while True:
    
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= duration:
                break
    
        vehicle.ai.set_waypoint('my_waypoint_3')
        vehicle.ai.set_waypoint('my_waypoint_1')
    '''
    input('Hit enter when done...')

def set_line():
    bng = BeamNGpy('localhost', 64256, home=r'E:\BeamNG\BeamNG.tech.v0.31.3.0',
                   user=r'E:\pycharmcode\pythonProject\beamng')
    bng.open()
    scenario = Scenario('smallgrid', 'custom_road_network')
    # 创建道路网络
    # create a decal road
    road_a = Road('track_editor_C_center', rid='center_road', looped=True)
    road_a.add_nodes(
        (0, 300, 0, 6),
        (0, 400, 0, 6),
        (0, 500, 0, 6),
        (0, 600, 0, 6),
    )
    scenario.add_road(road_a)
    vehicle = Vehicle('ego_vehicle', model='etk800')
    scenario.add_vehicle(vehicle, pos=(0, 300, 0), rot_quat=(0, 0, 1, 0))
    #positions = [(0, 400, 0), (0, 500, 0), (0, 600, 0)]
    #scales = [(1, 1, 1)] * 3
    #ids = ['my_waypoint_1', 'my_waypoint_2', 'my_waypoint_3']
    #scenario.add_checkpoints(positions, scales, ids)

    scenario.make(bng)
    print('lsm')
    try:
        bng.scenario.load(scenario)
        bng.scenario.start()
        line = generate_line()
        #vehicle.teleport((0, 301, 0),reset=False)
        #vehicle.ai.set_mode('manual')
        #bng.debug.add_spheres([(0, 400, 0),(0, 405, 0),(0, 410, 0)], (), (), cling=True, offset=0.1)
        bng.debug.add_polyline(line, (0,0,0,0.1), cling=True, offset=0.1)
        print('ssss')
        vehicle.ai.set_line(line)
        print('sssssss')
        while True:
            bng.control.step(60)
            print('sss')
    finally:
        bng.close()

def set_scripts():
    bng = BeamNGpy('localhost', 64256, home=r'E:\BeamNG\BeamNG.tech.v0.31.3.0',
                   user=r'E:\pycharmcode\pythonProject\beamng1')
    bng.open()
    scenario = Scenario('smallgrid', 'custom_road_network')
    # 创建道路网络
    # create a decal road
    road_a = Road('track_editor_C_center', rid='center_road', looped=True)
    road_a.add_nodes(
        (0, 300, 0, 6),
        (0, 400, 0, 6),
        (0, 500, 0, 6),
        (0, 600, 0, 6),
        (0, 700, 0, 6),
    )
    scenario.add_road(road_a)
    vehicle = Vehicle('ego_vehicle', model='etk800')
    scenario.add_vehicle(vehicle, pos=(0, 300, 0), rot_quat=(0, 0, 1, 0))
    #positions = [(0, 400, 0), (0, 500, 0), (0, 600, 0)]
    #scales = [(1, 1, 1)] * 3
    #ids = ['my_waypoint_1', 'my_waypoint_2', 'my_waypoint_3']
    #scenario.add_checkpoints(positions, scales, ids)
    scripts = generate_scripts()
    scenario.make(bng)
    bng.scenario.load(scenario)
    bng.scenario.start()
    #vehicle.ai.set_speed(30, 'set')
    #vehicle.set_velocity(10,5)
    #time.sleep(10)
    #vehicle.ai.set_line(scripts)\
    vehicle.ai.set_mode('manual')
    #vehicle.ai.execute_script(scripts)
    time.sleep(10)
    input('Hit enter when done...')

def generate_line():
    line = []
    node = {'pos': (0, 400, 0), 'speed': 30}
    line.append(node)
    node = {'pos': (0, 500, 0), 'speed': 30}
    line.append(node)
    node = {'pos': (0, 600, 0), 'speed': 30}
    line.append(node)
    print('abc')
    return line

def generate_scripts():
    script = []
    node = {'x': 0, 'y': 400, 'z': 0, 't': 20}
    script.append(node)
    node = {'x': 0, 'y': 500, 'z': 0, 't': 20}
    script.append(node)
    node = {'x': 0, 'y': 600, 'z': 0, 't': 20}
    script.append(node)
    return script


def frozen_time(duration):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= duration:
            break
    pass

def vehicle_no_run():
    from beamngpy import BeamNGpy, Scenario, Vehicle

    bng = BeamNGpy('localhost', 64256)
    bng.open()

    scenario = Scenario('west_coast_usa', 'waypoint demo')
    vehicle = Vehicle('ego', model='etk800')
    scenario.add_vehicle(vehicle, pos=(-712.76, 105.05, 118.66), rot_quat=(0.0010, 0.0057, 0.9187, -0.3949))

    positions = [(-705.03, 112.40, 118.67), (-696.67, 120.39, 118.65), (-687.03, 129.76, 118.15)]
    scales = [(1, 1, 1)] * 3
    ids = ['my_waypoint_1', 'my_waypoint_2', 'my_waypoint_3']
    scenario.add_checkpoints(positions, scales, ids)
    scenario.make(bng)

    bng.load_scenario(scenario)
    bng.start_scenario()

    waypoints = {waypoint.name: waypoint for waypoint in scenario.find_waypoints()}
    print(f'{len(waypoints)} waypoints found.')
    print(f'Waypoints: [', ', '.join(waypoints.keys()), ']')

    vehicle.ai_drive_in_lane(True)
    vehicle.ai_set_waypoint('my_waypoint_3')

if __name__ == '__main__':
    #get_scenarios()
    #start_scenario()
    #show_scenario_network()
    #create_road()
    #simple_create_road()
    set_line()
    #set_scripts()