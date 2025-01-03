import json
from pynput import keyboard


class ConfigReader:
    def __init__(self) -> None:
        self.config_file = "config.json"
        self.config = {
            "screenshot_enable": True,
            "launch_balatro": False,
            "GUI": {
                "window_opacity": 0.8,
                "always_on_top": True,
                "window_position": {
                    "x": 100,
                    "y": 100
                }
            },
            "key_mapping": {
                "backup": "[",
                "delete": "e",
                "select": "up",
                "load": "enter",
                "exit": "esc"
            }
        }

    def validate_key_mapping(self) -> list:
        missing_keys = []
        required_keys = ["backup", "delete", "select", "load", "exit"]

        for key in required_keys:
            if not self.config["key_mapping"].get(key):
                missing_keys.append(key)

        return missing_keys

    def write_config(self) -> dict:
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
        return self.config

    def read_config(self) -> dict:
        try:
            missing_keys = self.validate_key_mapping()
            if missing_keys:
                print(f"Warning: Missing key mappings for: {
                      ', '.join(missing_keys)}, using default keys")
                return self.config
            else:
                return json.load(open("config.json", encoding="utf-8"))
        except FileNotFoundError:
            return self.write_config()
        except json.JSONDecodeError:
            return self.write_config()


class KeyMapping:
    def __init__(self) -> None:
        self.config = ConfigReader().read_config()
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
