import time
from pynput import keyboard
from pynput.keyboard import Controller
from save_handler import backup_saves, restore_save, get_sorted_saves, delete_saves, refresh_saves
from read_config import KeyMapping


class KeyboardHandler:
    def __init__(self) -> None:
        self.current_index = -1
        self.saves = []
        self.keyboard_controller = Controller()
        self.listener = keyboard.Listener(
            on_press=self.on_press)  # type: ignore

    def on_press(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char == KeyMapping().key_backup():
                    backup_saves()
                    refresh_saves()
                    self.current_index = -1
                elif key.char == KeyMapping().key_delete():
                    delete_saves()
                    refresh_saves()
                    self.current_index = -1
            elif key == KeyMapping().key_select():
                self.saves = get_sorted_saves()
                if refresh_saves():
                    self.current_index = (
                        self.current_index + 1) % len(self.saves)
                    print(f"Selected save: {
                          self.saves[self.current_index].name}")
            elif key == KeyMapping().key_load():
                self.saves = get_sorted_saves()
                if self.saves and 0 <= self.current_index < len(self.saves):
                    restore_save(self.saves[self.current_index])
                    print(f"The Save: {
                          self.saves[self.current_index].name} has been restored.")
                    self.current_index = -1

                    self.keyboard_controller.press('f')
                    time.sleep(0.8)
                    self.keyboard_controller.release('f')
            elif key == KeyMapping().key_exit():
                self.stop()
                return False
        except AttributeError:
            pass

    def start(self):
        self.listener.start()
        self.listener.join()

    def stop(self):
        self.listener.stop()
