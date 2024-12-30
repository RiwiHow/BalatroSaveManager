from pynput import keyboard
from save_handler import copy_saves


def keyboard_monitor():
    def on_press(key):
        try:
            if key.char == '[':
                copy_saves()
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(key):
        print('{0} released'.format(key))
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(
            on_press=on_press,  # type: ignore
            on_release=on_release) as listener:  # type: ignore
        listener.join()
