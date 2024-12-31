from keyboard_monitor import keyboard_monitor
from launch_balatro import launch_balatro
from read_config import read_config


if read_config()["launch_balatro"]:
    launch_balatro()


keyboard_monitor()
