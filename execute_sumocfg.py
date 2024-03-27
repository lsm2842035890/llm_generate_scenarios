import random

import traci
import sys
import os
import optparse
from sumolib import checkBinary

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

def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:  # 意思就是还有车需要处理就处理
        traci.simulationStep()  # 仿真一步
        simulation_time = traci.simulation.getTime()

        try:
             traci.vehicle.setLaneChangeMode(f"veh{0}", 0b000000000000)
             traci.vehicle.setSpeedMode(f"veh{0}", 00000)
             traci.vehicle.setSpeed("vhe0",1)
             #traci.vehicle.changeSublane(f"veh{4}", random.choice([-1,1]))
        except traci.TraCIException:  # 避免车辆离开路网时引起程序中断
            pass
        step += 1
    traci.close()  # 仿真结束 关闭TraCI
    sys.stdout.flush()  # 清除缓冲区

# 主函数
if __name__ == "__main__":
    # 根据下载的sumo决定打开gui版本的sumo还是cmd版本的sumo
    options = get_options()
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # 根据指定路径打开sumocfg文件
    sumocfgfile = 'E:\pycharmcode\pythonProject\Fianl.sumocfg'
    traci.start([sumoBinary, "-c", sumocfgfile])  # 打开sumocfg文件

    # 运行自定义的逻辑
    run()