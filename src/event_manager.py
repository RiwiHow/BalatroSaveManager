class EventManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.gui = None
            cls._instance.keyboard_handler = None
        return cls._instance

    def set_gui(self, gui):
        self.gui = gui

    def set_keyboard_handler(self, handler):
        self.keyboard_handler = handler

    def refresh_save_list(self):
        if self.gui:
            self.gui.refresh_save_list()
