from keyboard_handler import KeyboardHandler
from launch_balatro import launch_balatro
from read_config import read_config


if read_config()["launch_balatro"]:
    launch_balatro()


KeyboardHandler().start()
