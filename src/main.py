from read_config import ConfigReader
from launch_balatro import launch_balatro
from keyboard_handler import KeyboardHandler


if ConfigReader().read_config().get("launch_balatro", False):
    launch_balatro()


KeyboardHandler().start()
