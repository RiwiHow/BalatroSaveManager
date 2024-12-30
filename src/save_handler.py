import os
import shutil
from pathlib import Path
from datetime import datetime

SOURCE_PATH = Path(os.environ["APPDATA"]) / "Balatro" / "1"
DESTINATION_PATH_ROOT = Path("saves")


def copy_saves() -> bool:
    try:
        src = Path(SOURCE_PATH)
        dst = Path(DESTINATION_PATH_ROOT) / datetime.now().strftime("%m.%d %H%M%S")

        if not src.exists():
            print("Please run Balatro once.")
            return False
        dst.mkdir(parents=True, exist_ok=True)

        shutil.copytree(src, dst, dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f"Error copying folder: {str(e)}")
        return False
