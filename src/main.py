from gui import GUI
from ctypes import windll, c_void_p
from read_config import ConfigReader
from launch_balatro import launch_balatro
from keyboard_handler import KeyboardHandler


def main():
    DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = c_void_p(-4)
    windll.user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)

    gui = GUI()
    keyboard_handler = KeyboardHandler()

    if ConfigReader().read_config().get("launch_balatro", False):
        launch_balatro()

    keyboard_handler.start()
    gui.start()


if __name__ == "__main__":
    main()
