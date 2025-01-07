import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk


class PreviewWindow:
    def __init__(self, parent):
        self.preview = tk.Toplevel(parent)
        self.preview.withdraw()  # Initially hidden
        self.preview.overrideredirect(True)
        self.preview.attributes('-topmost', True)

        # Get DPI scaling factor
        self.scaling = self.preview.winfo_fpixels('1i') / 72.0

        self.label = tk.Label(self.preview)
        self.label.pack()

        self.current_path = None

    def show(self, save_path: Path, x: int, y: int):
        screenshot_path = save_path / "screenshot.png"
        if not screenshot_path.exists():
            return

        # Scale preview size based on DPI
        preview_width = int(400 * self.scaling)
        preview_height = int(225 * self.scaling)

        image = Image.open(screenshot_path).resize(
            (preview_width, preview_height),
            Image.Resampling.LANCZOS  # 使用更高质量的重采样方法
        )
        photo = ImageTk.PhotoImage(image)
        self.label.configure(image=photo)  # type: ignore
        self.label.image = photo  # type: ignore
        self.current_path = str(screenshot_path)

        self.preview.geometry(f"+{x}+{y}")
        self.preview.deiconify()  # Show the hidden widgets

    def hide(self):
        self.preview.withdraw()
