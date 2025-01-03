import os
import shutil
from gui import GUI
from pathlib import Path
from datetime import datetime
from screenshot import screenshot
from read_config import ConfigReader


SOURCE_PATH = Path(os.environ["APPDATA"]) / "Balatro" / "1"
DESTINATION_PATH_ROOT = Path("saves")


def backup_saves() -> bool:
    try:
        src = Path(SOURCE_PATH)
        dst = Path(DESTINATION_PATH_ROOT) / datetime.now().strftime("%m.%d %H%M%S")

        if not src.exists():
            GUI().show_message("Please run Balatro once.")
            return False
        dst.mkdir(parents=True, exist_ok=True)

        shutil.copytree(src, dst, dirs_exist_ok=True)
        GUI().show_message(f"{datetime.now().strftime('%m.%d %H%M%S')} save has been backed up.")
        if ConfigReader().read_config().get("screenshot_enable", True):
            screenshot(dst)

        return True
    except Exception as e:
        GUI().show_message(f"Error copying folder: {str(e)}")
        return False


def restore_save(save_path: Path) -> bool:
    try:
        shutil.copytree(save_path, SOURCE_PATH, dirs_exist_ok=True)
        return True
    except Exception as e:
        GUI().show_message(f"Error restoring save: {str(e)}")
        return False


def delete_saves() -> bool:
    try:
        for item in DESTINATION_PATH_ROOT.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        GUI().show_message("All saves have been deleted.")
        return True
    except Exception as e:
        GUI().show_message(f"Error deleting saves: {str(e)}")
        return False


def get_sorted_saves() -> list:
    dst = DESTINATION_PATH_ROOT
    if not dst.exists():
        return []
    saves = [(d, d.stat().st_birthtime)
             for d in dst.iterdir() if d.is_dir()]  # d for directory
    return [d[0] for d in sorted(saves, key=lambda x: x[1], reverse=True)]


def refresh_saves() -> bool:
    saves = get_sorted_saves()
    return len(saves) > 0
