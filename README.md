# BalatroSaveManager
English | [简体中文](https://github.com/RiwiHow/BalatroSaveManager/blob/master/docs/README.zh_CN.md)

A simple tool to manager Balatro saves.

## Usage
- Press `[` to copy saves
- Press `↑` to select a save and press `Enter` to load selected save
- Press `e` to delete all saves
- Configure `config.json` for custom key mapping
- To automatically load selected save, use [BalatroQuickLoad](https://github.com/TsunamiinFantasy/BalatroQuickLoad).

## Configuration
The `config.json` file contains the following settings:
- `screenshot_enable`: Enable/disable the screenshot feature when backing up saves
- `launch_balatro`: Whether to automatically launch Balatro when running BalatroSaveManager
- `key_mapping`: Use your favorite key to perform specific action
    - `backup`: Backup current save (default: `[`)
    - `delete`: Delete all saves (default: `e`)
    - `select`: Select previous save (default: `up`)
    - `load`: Load selected save (default: `enter`)
    - `exit`: Exit BalatroSaveManager (default: `esc`)

## Known Issues and Workarounds
- The screenshot feature is only for Windows. However, it may have issues that prevent it from capturing the real-time screen in some cases. If you encounter this problem, you can change Balatro's `Windows Mode` to `Windowed` in `OPTIONS -> Settings -> Video`

## Build
1. Run `git clone https://github.com/RiwiHow/BalatroSaveManager.git`
2. Install [PDM](https://github.com/pdm-project/pdm)
3. Run `pdm install`
4. Run `pyinstaller --onefile --name BalatroSaveManager src/main.py`
5. Copy the `config.json` file to `dist` folder which is created by pyinstaller