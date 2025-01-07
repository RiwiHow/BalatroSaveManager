import time
import threading
from gui import GUI
from pynput import keyboard
from read_config import KeyMapping
from pynput.keyboard import Controller
from event_manager import EventManager
from save_handler import backup_saves, restore_save, get_sorted_saves, delete_saves, refresh_saves


class KeyboardHandler:
    def __init__(self) -> None:
        self.current_index = -1
        self.saves = []
        self.keyboard_controller = Controller()
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            suppress=False)
        self.gui = GUI()
        self.running = True
        EventManager().set_keyboard_handler(self)

    def on_press(self, key):
        try:
            if hasattr(key, 'char'):
                if key.char == KeyMapping().key_backup():
                    backup_saves()
                    refresh_saves()
                    self.gui.update_selection(self.current_index)
                elif key.char == KeyMapping().key_delete():
                    delete_saves()
                    refresh_saves()
                    self.gui.update_selection(self.current_index)
            elif key == KeyMapping().key_select():
                self.saves = get_sorted_saves()
                if refresh_saves():
                    self.current_index = (
                        self.current_index + 1) % len(self.saves)
                    print(f"Selected save: {
                          self.saves[self.current_index].name}")
                    self.gui.update_selection(self.current_index)
            elif key == KeyMapping().key_load():
                self.saves = get_sorted_saves()
                if self.saves and 0 <= self.current_index < len(self.saves):
                    restore_save(self.saves[self.current_index])
                    print(
                        f"The Save: {self.saves[self.current_index].name} has been restored.")
                    self.gui.update_selection(self.current_index)

                    self.keyboard_controller.press('f')
                    time.sleep(0.8)
                    self.keyboard_controller.release('f')
            elif key == KeyMapping().key_exit():
                self.running = False
                self.stop()
                self.gui.root.after(100, self.gui.root.quit)
                return False
        except AttributeError:
            pass

    def start(self):
        self.thread = threading.Thread(target=self._start_listener)
        self.thread.daemon = True
        self.thread.start()

    def _start_listener(self):
        with self.listener as listener:
            while self.running:
                if not listener.running:
                    break
                time.sleep(0.1)

    def stop(self):
        self.running = False
        if hasattr(self, 'listener') and self.listener.is_alive():
            self.listener.stop()
        if self.thread and self.thread.is_alive():
            self.thread.join()
