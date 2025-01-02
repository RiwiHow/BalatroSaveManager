import json
from pynput import keyboard


def read_config() -> dict:
    return json.load(open("config.json", encoding="utf-8"))


class KeyMapping:
    def __init__(self) -> None:
        self.config = read_config()
        self.special_keys = {
            "up": keyboard.Key.up,
            "down": keyboard.Key.down,
            "left": keyboard.Key.left,
            "right": keyboard.Key.right,
            "enter": keyboard.Key.enter,
            "esc": keyboard.Key.esc,
            "space": keyboard.Key.space
        }

    def _is_special_key(self, key_str) -> bool:
        return key_str.lower() in self.special_keys

    def _get_key(self, key_name):
        if self._is_special_key(key_name):
            return self.special_keys[key_name.lower()]
        return key_name

    def key_backup(self):
        return self._get_key(self.config["key_mapping"]["backup"])

    def key_delete(self):
        return self._get_key(self.config["key_mapping"]["delete"])

    def key_select(self):
        return self._get_key(self.config["key_mapping"]["select"])

    def key_load(self):
        return self._get_key(self.config["key_mapping"]["load"])

    def key_exit(self):
        return self._get_key(self.config["key_mapping"]["exit"])
