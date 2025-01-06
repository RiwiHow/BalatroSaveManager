import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path


class PreviewWindow:
    def __init__(self, parent):
        self.preview = tk.Toplevel(parent)
        self.preview.withdraw()  # 初始隐藏
        self.preview.overrideredirect(True)  # 无边框
        self.preview.attributes('-topmost', True)  # 总在最前

        self.label = tk.Label(self.preview)
        self.label.pack()

        self.current_path = None

    def show(self, save_path: Path, x: int, y: int):
        screenshot_path = save_path / "screenshot.png"
        if not screenshot_path.exists():
            return

        if str(screenshot_path) != self.current_path:
            # 加载新图片
            image = Image.open(screenshot_path)
            # 设置预览图片大小
            image = image.resize((400, 225))  # 16:9 比例
            photo = ImageTk.PhotoImage(image)
            self.label.configure(image=photo)  # type: ignore
            self.label.image = photo  # type: ignore
            self.current_path = str(screenshot_path)

        # 设置窗口位置
        self.preview.geometry(f"+{x}+{y}")
        self.preview.deiconify()

    def hide(self):
        self.preview.withdraw()
