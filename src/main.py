from gui import GUI
from read_config import ConfigReader
from launch_balatro import launch_balatro
from keyboard_handler import KeyboardHandler


def main():
    gui = GUI()
    keyboard_handler = KeyboardHandler()

    if ConfigReader().read_config().get("launch_balatro", False):
        launch_balatro()

    keyboard_handler.start()
    gui.start()


if __name__ == "__main__":
    main()
