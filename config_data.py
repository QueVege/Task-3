import json

with open("config.json", 'r') as f:
    config_data = json.loads(f.read())

consts = config_data["consts"]

SQUADS_COUNT = consts["SQUADS_COUNT"]
SOLDIERS_COUNT = consts["SOLDIERS_COUNT"]
VEHICLES_COUNT = consts["VEHICLES_COUNT"]
OPERATORS_COUNT = consts["OPERATORS_COUNT"]
SOLDIERS_HP = consts["SOLDIERS_HP"]
VEHICLES_HP = consts["VEHICLES_HP"]

seed = config_data["seed"]

armies_config = config_data["armies"]

f.close()
