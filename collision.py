import traci
import sys
import os
import optparse
from sumolib import checkBinary
import random
import time
import xlrd2
class ExampleListener(traci.StepListener):
    def step(self, t):
        print("ExampleListener called with parameter %s.",t)
        return True


# 检测是否已经添加环境变量
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# sumo自带的，检查gui版本的sumo是否存在
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# 真正的所需操作在这里写
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:  # 意思就是还有车需要处理就处理
        traci.simulationStep()  # 仿真一步
        simulation_time = traci.simulation.getTime()
        traci.vehicle.subscribe('veh1', (0X40, 0X42))
        traci.junction.subscribeContext('9486203908',0XA4,100,(0X40, 0X42))
        print("仿真时间是",simulation_time)
        try:
            #vspeed = traci.vehicle.getSpeed('veh1')
            #vpos = traci.vehicle.getPosition('veh1')
            #print(traci.vehicle.getSubscriptionResults('veh1'))
            #print(traci.junction.getContextSubscriptionResults('9486203908'))
            listener = ExampleListener()
            traci.addStepListener(listener)
        except traci.TraCIException:  # 避免车辆离开路网时引起程序中断
            pass
        step += 1
    traci.close()  # 仿真结束 关闭TraCI
    sys.stdout.flush()  # 清除缓冲区

def runn():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:  # 意思就是还有车需要处理就处理
        traci.simulationStep()  # 仿真一步
        step += 1
    traci.close()  # 仿真结束 关闭TraCI
    sys.stdout.flush()  # 清除缓冲区

def run1():   #test地图 直线地图运行
    for step in range(0, 200):
        time.sleep(0.5)
        if step > 5:
            traci.vehicle.subscribe('vehicle_1', (0X40, 0X42))
            traci.vehicle.subscribe('vehicle_2', (0X40, 0X42))
            traci.vehicle.setLaneChangeMode("vehicle_1",0b000000000000)
            traci.vehicle.setLaneChangeMode("vehicle_2", 0b000000000000)
            traci.vehicle.setSpeedMode("vehicle_1",00000)
            traci.vehicle.setSpeedMode("vehicle_2",00000)
            print(traci.vehicle.getSubscriptionResults("vehicle_1"))
            print("vehicle2",traci.vehicle.getSubscriptionResults("vehicle_2"))
            traci.vehicle.setSpeed("vehicle_1", 10)
            traci.vehicle.setSpeed("vehicle_2", 30)
        traci.simulationStep()
    sys.stdout.flush()  # 清除缓冲区
    traci.close()

def run2():   #circle地图运行
    for step in range(0, 200):
        time.sleep(0.5)
        if step > 5:
            traci.vehicle.setLaneChangeMode("vehicle_1", 0b000000000000)
            traci.vehicle.setLaneChangeMode("vehicle_2", 0b000000000000)
            traci.vehicle.setSpeedMode("vehicle_1", 00000)
            traci.vehicle.setSpeedMode("vehicle_2", 00000)
            traci.vehicle.setSpeed("vehicle_1", 10)
            traci.vehicle.setSpeed("vehicle_2", 30)
            #traci.vehicle.setSpeed("vehicle_1", 10)
        traci.simulationStep()
    sys.stdout.flush()  # 清除缓冲区
    traci.close()

def run3():   #circle地图运行
    for step in range(0, 900):
        traci.simulationStep()
        if step > 0 and step < 100:
            current = traci.vehicle.getIDList()
            for i in range(0,50):
                string = f"veh{i}"
                if string in current:
                    traci.vehicle.setLaneChangeMode(string, 0b000000000000)
                    traci.vehicle.setSpeedMode(string, 00000)
                    traci.vehicle.changeLaneRelative(string,1,2)
                    #traci.vehicle.setSpeed(string, 1)
        if step > 450:
            current = traci.vehicle.getIDList()
            for i in range(765,800):
                string = f"veh{i}"
                if string in current:
                    traci.vehicle.setLaneChangeMode(string, 0b000000000000)
                    traci.vehicle.setSpeedMode(string, 00000)
                    traci.vehicle.changeLaneRelative(string,1,5.0)
                    #traci.vehicle.setSpeed(string, 1)
    sys.stdout.flush()  # 清除缓冲区
    traci.close()


# 主函数
if __name__ == "__main__":
    # 根据下载的sumo决定打开gui版本的sumo还是cmd版本的sumo
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # 根据指定路径打开sumocfg文件
    #sumocfgfile = 'E:\pycharmcode\pythonProject\maps\Test\Test.sumocfg'  # sumocfg文件的位置
    sumocfgfile = 'E:\pycharmcode\pythonProject\maps\HHlane\quickstart.sumocfg'
    #traci.start([sumoBinary, "-c", sumocfgfile, "--collision.action", "warn", "--collision.mingap-factor", "0"])  # 打开sumocfg文件
    traci.start([sumoBinary, "-c", sumocfgfile, "--collision.action", "remove", "--collision-output", "maps/HHlane/collison.xml"])
    # 运行自定义的逻辑
    run3()