import openai
import json
import ast
import os

# apikey
#sk-QjEm9wh7KITiF0hx8338056b3cE34d0cB49d3aBaF07e4916
#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  淘宝买的
#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 gpt4,gpt3.5
openai.api_key = "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"

def ADS_main_responsibility_check(description):   #关于ADS的事故描述要经过llm的责任筛查
    messages = [
        {"role": "system", "content": "You are a police officer who specializes in dealing with traffic accidents."},
        {"role": "assistant","content": "On May [XXX], 2023 at 10:32 AM PST a Waymo Autonomous Vehicle (""Waymo AV"") operating in San Francisco, California was in a collision involving an SUV on [XXX] near [XXX].The Waymo AV was fraveling in autonomous mode in the middle lane on westbound [XXX] between [XXX] and [XXX].  A slower traveling van in the left adjacent lane began to initiate a right lane change in front of the Waymo AV, and the Waymo AV test driver transitioned to manual mode and braked.  The SUV traveling behind the Waymo AV then made contact with the rear of the Waymo AV.  At the time of the impact, the Waymo AV's Level 4 ADS was not engaged and a test driver was operating the Waymo AV in manual mode.  The Waymo AV and SUV sustained damage.This is a duplicate of report 30270-5429-1."},
        {"role": "user", "content": "Whether a self-driving vehicle caused the accident?"},
        {"role": "assistant","content": "NO"},
        {"role": "assistant", "content":f"{description}"},
        {"role": "user", "content": "Whether a self-driving vehicle caused the accident?Answer yes or no!"},
    ]

    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-0613",
        model="gpt-3.5-turbo",
        messages=messages,
        # max_tokens = 100
    )
    return response.choices[0].message.content


def get_road_info(description):        #get information of road condition around collison scenario
    messages = [
        {"role": "assistant", "content": f"{description}"},
        {"role": "user", "content": "Does it mention information about the specific location of the collision, such as longitude and latitude, such as the direction of the road and the number of lanes?"},
        {"role": "user", "content": "Please analyze description and then form a table,table's attributions is longitude,latitude,the direction of the road,the number of lanes,the length of road"},
        {"role": "user", "content": "If an attribute does not exist, write None"},
        {"role": "user", "content": "if value is not complete,write similar value"},
        {"role": "user", "content": "Please convert the contents in the above table into a list data structure and don't need code comments.The format is as follows:[{'longitude': float or None,'latitude': float or None,'direction':float or None, 'number of lanes':int or None,'length': float or None},]"}
    ]
    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-0613",
        model="gpt-3.5-turbo",
        messages=messages,
        # max_tokens = 100
    )
    return response.choices[0].message.content

def get_vehicle_info(description):   #get information of vehicle when driving
    messages = [
        {"role": "assistant", "content": f"{description}"},
        {"role": "user","content": "Does it mention information about the specific manoeuvre of all vehicles, such as left change lane,right lane change,cut in,overtake,speed up,emergency brake,slow down?"},
        {"role": "user","content": "Please analyze description and then form a table,table's attributions is vehicle's id ,initial speed, initial position, final position,left change lane,right lane change,cut in,overtake,speed up,emergency brake,slow down"},
        {"role": "user", "content": "If an attribute does not exist, write None."},
        {"role": "user", "content": "vehicle's id is string,please add '' "},
        {"role": "user", "content": "{ and } must be in pairs"},
        {"role": "user","content": "Please convert the contents in the above table into a list data structure and don't need code comments.And The format is as follows:[{'Vehicle ID': 'xxx', 'Left Change Lane': False or True, 'initial speed': int , 'initial position':[float,float] or None, 'final position':[float,float] or None,'Right Change Lane': False or True, 'Cut In': False or True, 'Overtake': False or True, 'Speed Up': False or True, 'Emergency Brake': False or True, 'Slow Down': False or True},{'Vehicle ID': 'xxx', 'Left Change Lane': False or True, 'Right Change Lane': False or True, 'Cut In': False or True, 'Overtake': False or True, 'Speed Up': False or True, 'Emergency Brake': False or True, 'Slow Down': False or True}]"}
    ]
    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-0613",
        model="gpt-3.5-turbo",
        messages=messages,
        # max_tokens = 100
    )
    return response.choices[0].message.content


def read_txt(file_path):
    with open(file_path, 'r') as file:
        # 读取文本内容
        text = file.read()
    return text

def get_json(file_path, resopnse):
    text_content = f"{resopnse}"
    start_index = text_content.find('[')
    end_index = text_content.find(']')
    if start_index != -1:
        # 截取从`[`开始到字符串末尾的部分
        json_text = text_content[start_index:end_index + 1]
        print(json_text)
        # 将截取的部分写入文件
        txt = ast.literal_eval(json_text)
    else:
        print("未找到字符`[`")
    # 将Python对象保存为JSON格式文件
    with open(file_path, 'w') as json_file:
        json.dump(txt, json_file, indent=4)


path = r"C:\Users\28420\Desktop\ADS_collision\1.txt"
get_json(r"E:\pycharmcode\pythonProject\extracted_info\road_1.json",get_road_info(read_txt(path)))
get_json(r"E:\pycharmcode\pythonProject\extracted_info\vehicle_1.json",get_vehicle_info(read_txt(path)))


'''
for filename in os.listdir(path):
    # 检查文件名后缀是否为txt
    if filename.endswith('.txt'):
        # 拼接文件路径
        file_path = os.path.join(path, filename)
    print(get_vehicle_info(read_txt(file_path)))
    #print(ADS_main_responsibility_check(read_txt(file_path)))
'''





'''
messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        #{"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "On May [XXX], 2023 at 10:32 AM PST a Waymo Autonomous Vehicle (""Waymo AV"") operating in San Francisco, California was in a collision involving an SUV on [XXX] near [XXX].The Waymo AV was fraveling in autonomous mode in the middle lane on westbound [XXX] between [XXX] and [XXX].  A slower traveling van in the left adjacent lane began to initiate a right lane change in front of the Waymo AV, and the Waymo AV test driver transitioned to manual mode and braked.  The SUV traveling behind the Waymo AV then made contact with the rear of the Waymo AV.  At the time of the impact, the Waymo AV's Level 4 ADS was not engaged and a test driver was operating the Waymo AV in manual mode.  The Waymo AV and SUV sustained damage.This is a duplicate of report 30270-5429-1."},
        {"role": "user", "content": "Please analyze description and then form a table"},
        {"role": "user","content": "table's attributions is vehicle's id,Whether it is a self-driving vehicle, whether it is following a vehicle, whether it is accelerating to overtake, whether it is changing lanes to overtake it."},
        #{"role": "user","content":"The answer content only needs to have a form."}
        #{"role": "user", "content": "Does the description contain a description of the incident?"},
        {"role": "user", "content": "Please convert the contents in the above table into a list data structure and don't need code comments"},
        {"role": "user", "content": "Keep only the code part"}
    ]
'''

'''
text_content = f"{response.choices[0].message.content}"
start_index = text_content.find('[')
end_index = text_content.find(']')

if start_index != -1:
    # 截取从`[`开始到字符串末尾的部分
    json_text = text_content[start_index:end_index+1]
    # 将截取的部分写入文件
    txt = ast.literal_eval(json_text)
else:
    print("未找到字符`[`")

# 将Python对象保存为JSON格式文件
file_path =  "E:\pycharmcode\pythonProject\Result.json"
with open(file_path, 'w') as json_file:
    json.dump(txt, json_file, indent=4)
    
messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        #{"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": f"{response.choices[0].message.content}"},
        {"role": "user", "content": "Please convert the contents in the above table into a list data structure"}
    ]

response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
#model="gpt-4",
messages=messages,
#max_tokens = 100
)
print(response.choices[0].message.content)

messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        #{"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": f"{response.choices[0].message.content}"},
        {"role": "user", "content": "Keep only the code part"}
    ]

response = openai.ChatCompletion.create(
model="gpt-3.5-turbo-0613",
#model="gpt-4",
messages=messages,
#max_tokens = 100

)
print(response.choices[0].message.content)
'''