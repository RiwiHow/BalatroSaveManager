import os
import win32gui
from PIL import ImageGrab
from ctypes import windll
from event_manager import EventManager


def screenshot(save_path) -> bool:
    window = win32gui.FindWindow(None, "Balatro")

    if not window:
        EventManager().show_message("Window 'Balatro' not found!")
        return False

    win32gui.SetForegroundWindow(window)
    user32 = windll.user32
    user32.SetProcessDPIAware()

    left, top, right, bottom = win32gui.GetWindowRect(window)

    try:
        path = os.path.join(save_path, "screenshot.png")

        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        screenshot.save(path)
        screenshot.close()

        return True
    except Exception as e:
        EventManager().show_message(f"Screenshot failed: {e}")
        return False
