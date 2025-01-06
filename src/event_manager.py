class EventManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.gui = None
        return cls._instance

    def set_gui(self, gui):
        self.gui = gui

    def show_message(self, message: str):
        if self.gui:
            self.gui.show_message(message)

    def refresh_save_list(self):
        if self.gui:
            self.gui.refresh_save_list()
