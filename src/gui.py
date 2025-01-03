import tkinter as tk
from tkinter import ttk
from datetime import datetime


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

            self.text_area = tk.Text(self.root, wrap=tk.WORD, height=15)
            self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(self.root, command=self.text_area.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.text_area.config(yscrollcommand=scrollbar.set)

            self.text_area.config(state=tk.DISABLED)

    def show_message(self, message: str):
        self.text_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def start(self):
        self.root.mainloop()
