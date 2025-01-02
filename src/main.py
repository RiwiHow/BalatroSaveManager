from keyboard_handler import KeyboardHandler
from launch_balatro import launch_balatro
from read_config import ConfigReader


if ConfigReader().read_config().get("launch_balatro", False):
    launch_balatro()


KeyboardHandler().start()
