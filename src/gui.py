import tkinter as tk
from tkinter import ttk
from datetime import datetime
from read_config import ConfigReader


class GUI:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'root'):
            self.root = tk.Tk()
            self.config_reader = ConfigReader()
            config = self.config_reader.read_config()

            window_pos = config["GUI"].get(
                'window_position', {'x': 100, 'y': 100})
            self.root.geometry(f"400x150+{window_pos['x']}+{window_pos['y']}")

            self.root.title("Balatro Save Manager")

            # Remove title bar
            self.root.overrideredirect(True)
            # Set transparency
            self.root.attributes(
                '-alpha', config["GUI"].get('window_opacity', 0.8))

            # Always on top
            self.root.attributes(
                '-topmost', config["GUI"].get('always_on_top', True))

            # Bind drag events directly to the root window
            self.root.bind('<Button-1>', self.start_move)
            self.root.bind('<B1-Motion>', self.do_move)

            bg_color = self.root.cget('bg')

            self.text_area = tk.Text(
                self.root,
                wrap=tk.WORD,
                height=15,
                cursor="arrow",
                selectbackground=bg_color,
                selectforeground=bg_color,
                inactiveselectbackground=bg_color,
                takefocus=0
            )
            self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            self.text_area.configure(
                insertwidth=0,
                highlightthickness=0,
            )

            # Disable all text-related events
            self.text_area.bind('<Key>', lambda e: 'break')
            self.text_area.bind('<Button-1>', lambda e: self.start_move(e))
            self.text_area.bind('<B1-Motion>', lambda e: self.do_move(e))

            scrollbar = ttk.Scrollbar(self.root, command=self.text_area.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.text_area.config(yscrollcommand=scrollbar.set)

            self.text_area.config(state=tk.DISABLED)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

        config = self.config_reader.read_config()
        config["GUI"]['window_position'] = {'x': x, 'y': y}
        self.config_reader.config = config
        self.config_reader.write_config()

    def show_message(self, message: str):
        self.text_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.root.update()

    def start(self):
        self.root.mainloop()
