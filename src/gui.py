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
            self.root.title("Balatro Save Manager")
            self.root.geometry("400x300")

            # Remove title bar
            self.root.overrideredirect(True)
            # Set transparency
            self.root.attributes('-alpha', ConfigReader().read_config().get('window_opacity', 0.5))

            # Always on top
            self.root.attributes(
                '-topmost', ConfigReader().read_config().get('always_on_top', True))

            self.root.bind('<Button-1>', self.start_move)
            self.root.bind('<B1-Motion>', self.do_move)

            self.text_area = tk.Text(self.root, wrap=tk.WORD, height=15)
            self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

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

    def show_message(self, message: str):
        self.text_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.root.update()  # 使用 update 替代 mainloop

    def start(self):
        self.root.mainloop()
