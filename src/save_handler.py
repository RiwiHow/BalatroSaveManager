import os
import shutil
from pathlib import Path
from datetime import datetime
from screenshot import screenshot

SOURCE_PATH = Path(os.environ["APPDATA"]) / "Balatro" / "1"
DESTINATION_PATH_ROOT = Path("saves")


def backup_saves() -> bool:
    try:
        src = Path(SOURCE_PATH)
        dst = Path(DESTINATION_PATH_ROOT) / datetime.now().strftime("%m.%d %H%M%S")

        if not src.exists():
            print("Please run Balatro once.")
            return False
        dst.mkdir(parents=True, exist_ok=True)

        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"{datetime.now().strftime("%m.%d %H%M%S")} save has been backed up.")
        screenshot("Balatro", dst)
        return True
    except Exception as e:
        print(f"Error copying folder: {str(e)}")
        return False


def restore_save(save_path: Path) -> bool:
    try:
        shutil.copytree(save_path, SOURCE_PATH, dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f"Error restoring save: {str(e)}")
        return False


def get_sorted_saves():
    dst = DESTINATION_PATH_ROOT
    if not dst.exists():
        return []
    saves = [(d, d.stat().st_birthtime)
             for d in dst.iterdir() if d.is_dir()]  # d for directory
    return [d[0] for d in sorted(saves, key=lambda x: x[1], reverse=True)]
