import time
from pynput import keyboard
from pynput.keyboard import Controller
from save_handler import backup_saves, restore_save, get_sorted_saves, delete_saves, refresh_saves


class KeyboardHandler:
    def __init__(self):
        self.current_index = -1
        self.saves = []
        self.keyboard_controller = Controller()
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)  # type: ignore

    def on_press(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char == "[":
                    backup_saves()
                    refresh_saves()
                    self.current_index = -1
                elif key.char == "e":
                    delete_saves()
                    refresh_saves()
                    self.current_index = -1
            elif key == keyboard.Key.up:
                self.saves = get_sorted_saves()
                if refresh_saves():
                    self.current_index = (
                        self.current_index + 1) % len(self.saves)
                    print(f"Selected save: {
                          self.saves[self.current_index].name}")
            elif key == keyboard.Key.enter:
                self.saves = get_sorted_saves()
                if self.saves and 0 <= self.current_index < len(self.saves):
                    restore_save(self.saves[self.current_index])
                    print(f"The Save: {
                          self.saves[self.current_index].name} has been restored.")
                    self.current_index = -1

                    self.keyboard_controller.press('f')
                    time.sleep(0.8)
                    self.keyboard_controller.release('f')
        except AttributeError:
            pass

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False

    def start(self):
        self.listener.start()
        self.listener.join()

    def stop(self):
        self.listener.stop()
