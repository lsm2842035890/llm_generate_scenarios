import json
txt = '''
[
    {
        "Vehicle ID": "Waymo AV",
        "Self-Driving": "Yes",
        "Following Vehicle": "No",
        "Accelerating to Overtake": "No",
        "Changing Lanes to Overtake": "Yes"
    },
    {
        "Vehicle ID": "SUV",
        "Self-Driving": "No",
        "Following Vehicle": "Yes",
        "Accelerating to Overtake": "Yes",
        "Changing Lanes to Overtake": "No"
    }
]
'''
with open("E:\pycharmcode\pythonProject\example.txt", 'r') as file:
    file_content = file.read()
print(file_content)
a = json.loads(file_content)
print(a)