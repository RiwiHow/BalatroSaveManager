import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk


class PreviewWindow:
    def __init__(self, parent):
        self.preview = tk.Toplevel(parent)
        self.preview.withdraw()  # Initially hidden
        self.preview.overrideredirect(True)
        self.preview.attributes('-topmost', True)

        self.label = tk.Label(self.preview)
        self.label.pack()

        self.current_path = None

    def show(self, save_path: Path, x: int, y: int):
        screenshot_path = save_path / "screenshot.png"
        if not screenshot_path.exists():
            return

        # if str(screenshot_path) != self.current_path:
        image = Image.open(screenshot_path).resize((400, 225))
        photo = ImageTk.PhotoImage(image)
        self.label.configure(image=photo)  # type: ignore
        self.label.image = photo  # type: ignore
        self.current_path = str(screenshot_path)

        self.preview.geometry(f"+{x}+{y}")
        self.preview.deiconify()  # Show the hidden widgets

    def hide(self):
        self.preview.withdraw()
