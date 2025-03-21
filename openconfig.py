import json


def openconfig():
    with open("config.text", "r", encoding="utf-8") as file:
        GENERATOR_CONFIG_JSON = file.read()
    return json.loads(GENERATOR_CONFIG_JSON)