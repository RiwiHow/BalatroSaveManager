from pynput import keyboard
from save_handler import backup_saves, restore_save, get_sorted_saves
from datetime import datetime


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
                print(f"{datetime.now().strftime("%m.%d %H%M%S")} save has been backed up.")
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

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(
            on_press=on_press,  # type: ignore
            on_release=on_release) as listener:  # type: ignore
        listener.join()
