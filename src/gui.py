import time
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
        self.saves = []
        self.last_hover_index = None
        self.item_height = None

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
            activestyle='none',  # Remove the underline from the selected item
            font=('Arial', 20)
        )
        self.save_list.configure(
            selectbackground='#4a6984',
            selectforeground='white',
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
            self.save_list,  # Changed from self.content_frame to self.save_list
            style='Vertical.TScrollbar')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Ensure Listbox and Scrollbar are correctly bound
        self.save_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.save_list.yview)

        # Bind drag events to frame instead of scrollbar
        self.drag_frame.bind('<Button-1>', self.start_move)
        self.drag_frame.bind('<B1-Motion>', self.do_move)

        # Create preview window
        self.preview_window = PreviewWindow(self.root)
        self.scaling = self.preview_window.scaling

        # Add mouse event bindings for Listbox
        self.save_list.bind('<Motion>', self.on_motion)
        self.save_list.bind('<Leave>', self.on_leave)
        self.save_list.bind('<<ListboxSelect>>', self.on_select)
        self.save_list.bind('<Double-Button-1>', self.on_double_click)

        self.refresh_save_list()

    def format_save_name(self, name: str) -> str:
        try:
            date_part, time_part = name.split(' ')
            formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"
            return f"{date_part} {formatted_time}"
        except Exception:
            return name

    def refresh_save_list(self):
        self.save_list.delete(0, tk.END)
        self.saves = get_sorted_saves()
        for save in self.saves:
            formatted_name = self.format_save_name(save.name)
            self.save_list.insert(tk.END, formatted_name)

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

    def get_real_item_at(self, y_position):
        if self.item_height is None and self.save_list.size() > 0:
            bbox = self.save_list.bbox(0)
            if bbox:
                self.item_height = bbox[3]

        if self.item_height:
            first_visible = self.save_list.nearest(0)
            relative_y = y_position
            item_index = first_visible + int(relative_y / self.item_height)

            if 0 <= item_index < self.save_list.size():
                bbox = self.save_list.bbox(item_index)
                if bbox:
                    item_top = bbox[1]
                    item_bottom = item_top + bbox[3]
                    if item_top <= y_position <= item_bottom:
                        return item_index
        return None

    def on_motion(self, event):
        current_index = self.get_real_item_at(event.y)

        if current_index is None:
            if self.last_hover_index is not None:
                self.save_list.itemconfig(
                    self.last_hover_index,
                    background='',
                    foreground=''
                )
                self.last_hover_index = None
            self.preview_window.hide()
            return

        if self.last_hover_index != current_index:
            if self.last_hover_index is not None:
                self.save_list.itemconfig(
                    self.last_hover_index,
                    background='',
                    foreground=''
                )

            if current_index not in self.save_list.curselection():
                self.save_list.itemconfig(
                    current_index,
                    background='#2a3f52',
                    foreground='white'
                )

            self.last_hover_index = current_index

        if 0 <= current_index < len(self.saves):
            window_x = self.root.winfo_x()
            window_width = self.root.winfo_width()
            preview_width = int(400 * self.scaling)
            y = self.root.winfo_y() + event.y

            if window_x + window_width + preview_width + 10 > self.screen_width:
                x = window_x - preview_width - 10
            else:
                x = window_x + window_width + 10

            self.preview_window.show(self.saves[current_index], x, y)

    def on_leave(self, event):
        if self.last_hover_index is not None:
            self.save_list.itemconfig(
                self.last_hover_index,
                background='',
                foreground=''
            )
            self.last_hover_index = None

        self.preview_window.hide()

    def update_selection(self, index):
        if self.last_hover_index is not None:
            self.save_list.itemconfig(
                self.last_hover_index,
                background='',
                foreground=''
            )
            self.last_hover_index = None

        self.save_list.selection_clear(0, tk.END)
        if index >= 0:
            self.save_list.selection_set(index)
            self.save_list.see(index)

    def on_select(self, event):
        selection = self.save_list.curselection()
        if selection:
            index = selection[0]
            keyboard_handler = EventManager().keyboard_handler
            if keyboard_handler:
                keyboard_handler.current_index = index

    def on_double_click(self, event):
        selection = self.save_list.curselection()
        if selection:
            index = selection[0]
            keyboard_handler = EventManager().keyboard_handler
            if keyboard_handler:
                keyboard_handler.current_index = index
                keyboard_handler.saves = get_sorted_saves()
                if (keyboard_handler.saves and 0 <= keyboard_handler.current_index < len(keyboard_handler.saves)):
                    restore_save(
                        keyboard_handler.saves[keyboard_handler.current_index])
                    print(f"The Save: {
                          keyboard_handler.saves[keyboard_handler.current_index].name} has been restored.")

                    keyboard_handler.keyboard_controller.press('f')
                    time.sleep(0.8)
                    keyboard_handler.keyboard_controller.release('f')

    def start(self):
        self.root.mainloop()
