import json


def read_config() -> dict:
    return json.load(open("config.json", encoding="utf-8"))
