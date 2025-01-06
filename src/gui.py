import tkinter as tk
from tkinter import ttk
from read_config import ConfigReader
from event_manager import EventManager
from preview_window import PreviewWindow
from save_handler import get_sorted_saves, restore_save


class GUI:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if GUI._initialized:
            return
        GUI._initialized = True

        # Declaration of a class variable
        self.root = tk.Tk()
        EventManager().set_gui(self)
        self.config_reader = ConfigReader()
        config = self.config_reader.read_config()
        self.screen_width = self.root.winfo_screenwidth()

        # Set windows position and size
        window_pos = config["GUI"].get(
            'window_position', {'x': 100, 'y': 100})
        width = config["GUI"]["window_size"].get("width", 250)
        height = config["GUI"]["window_size"].get("height", 150)
        self.root.geometry(
            f"{width}x{height}+{window_pos['x']}+{window_pos['y']}")

        # Windows attributes
        self.root.overrideredirect(True)  # Remove title bar
        # Set transparency
        self.root.attributes(
            '-alpha', config["GUI"].get('window_opacity', 0.8))
        # Always on top
        self.root.attributes(
            '-topmost', config["GUI"].get('always_on_top', True))

        # Create a frame for drag area - remove padding here
        self.drag_frame = tk.Frame(self.root)
        self.drag_frame.pack(fill=tk.BOTH, expand=True)

        # Create inner frame for content with padding
        self.content_frame = tk.Frame(self.drag_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create save list with custom style
        self.save_list = tk.Listbox(
            self.content_frame,  # Changed parent to content_frame
            height=5,
            selectmode=tk.SINGLE,
            borderwidth=0,  # Remove border
            highlightthickness=0,  # Remove the highlight border
            activestyle='none'  # Remove the underline from the selected item
        )
        self.save_list.pack(side=tk.LEFT, fill=tk.BOTH,
                            expand=True)

        # Create custom scrollbar style
        style = ttk.Style()
        style.layout('Vertical.TScrollbar',
                     [('Vertical.Scrollbar.trough',
                       {'children':
                        [('Vertical.Scrollbar.thumb',
                          {'expand': '1', 'sticky': 'nswe'})],
                           'sticky': 'ns'})])

        # Optionally configure colors and other properties
        style.configure('Vertical.TScrollbar',
                        troughcolor='#F0F0F0',
                        background='#C0C0C0',
                        relief='flat',
                        arrowsize=10)

        # Create Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.content_frame,
            style='Vertical.TScrollbar')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.save_list.config(yscrollcommand=self.on_scroll)
        self.scrollbar.config(command=self.save_list.yview)

        # Bind drag events to frame instead of scrollbar
        self.drag_frame.bind('<Button-1>', self.start_move)
        self.drag_frame.bind('<B1-Motion>', self.do_move)

        # Bind keyboard events
        self.root.bind('<Return>', self.restore_selected_save)
        self.root.bind('<Up>', self.select_previous)
        self.root.bind('<Down>', self.select_next)

        # Create preview window
        self.preview_window = PreviewWindow(self.root)

        # Add mouse event bindings for preview
        self.save_list.bind('<Motion>', self.on_motion)
        self.save_list.bind('<Leave>', self.on_leave)

        # Store saves for quick lookup
        self.saves = []

        # Initial save list update
        self.refresh_save_list()

    def refresh_save_list(self):
        self.save_list.delete(0, tk.END)
        self.saves = get_sorted_saves()  # Store saves
        for save in self.saves:
            self.save_list.insert(tk.END, save.name)

    def restore_selected_save(self, event=None):
        selection = self.save_list.curselection()
        if not selection:
            return
        save_name = self.save_list.get(selection[0])
        saves = get_sorted_saves()
        for save in saves:
            if save.name == save_name:
                if restore_save(save):
                    print(f"Restored save: {save_name}")
                break

    def select_previous(self, event=None):
        if self.save_list.size() == 0:
            return
        try:
            current = self.save_list.curselection()[0]
            if current > 0:
                self.save_list.selection_clear(0, tk.END)
                self.save_list.selection_set(current - 1)
                self.save_list.see(current - 1)
        except IndexError:
            self.save_list.selection_set(0)

    def select_next(self, event=None):
        if self.save_list.size() == 0:
            return
        try:
            current = self.save_list.curselection()[0]
            if current < self.save_list.size() - 1:
                self.save_list.selection_clear(0, tk.END)
                self.save_list.selection_set(current + 1)
                self.save_list.see(current + 1)
        except IndexError:
            self.save_list.selection_set(0)

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

    def on_motion(self, event):
        index = self.save_list.nearest(event.y)
        if 0 <= index < len(self.saves):
            window_x = self.root.winfo_x()
            window_width = self.root.winfo_width()
            preview_width = 400
            y = self.root.winfo_y() + event.y

            if window_x + window_width + preview_width + 10 > self.screen_width:
                x = window_x - preview_width - 10
            else:
                x = window_x + window_width + 10

            self.preview_window.show(self.saves[index], x, y)

    def on_leave(self, event):
        self.preview_window.hide()

    def on_scroll(self, *args):
        self.scrollbar.set(*args)

    def start(self):
        self.root.mainloop()
