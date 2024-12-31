import time
from pynput import keyboard
from pynput.keyboard import Controller
from save_handler import backup_saves, restore_save, get_sorted_saves


def keyboard_monitor():
    current_index = -1
    saves = []

    def refresh_saves():
        nonlocal saves
        saves = get_sorted_saves()
        return len(saves) > 0

    def on_press(key):
        nonlocal current_index
        try:
            if key.char == '[':
                backup_saves()
                refresh_saves()
                current_index = -1
        except AttributeError:
            if key == keyboard.Key.up:
                if refresh_saves():
                    current_index = (current_index + 1) % len(saves)
                    print(f"Selected save: {saves[current_index].name}")
            elif key == keyboard.Key.enter:
                if saves and 0 <= current_index < len(saves):
                    print(f"Restoring save: {saves[current_index].name}")
                    restore_save(saves[current_index])
                    current_index = -1

                    keyboard_control = Controller()
                    keyboard_control.press('f')
                    time.sleep(0.8)
                    keyboard_control.release('f')

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(
            on_press=on_press,  # type: ignore
            on_release=on_release) as listener:  # type: ignore
        listener.join()
