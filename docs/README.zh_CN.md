# BalatroSaveManager
[English](https://github.com/RiwiHow/BalatroSaveManager?tab=readme-ov-file#balatrosavemanager) | 简体中文

一个简单的工具来管理 Balatro 的存档。

## 使用方法
- 按 `[` 复制存档
- 按 `↑` 选择一个存档，然后按 `Enter` 加载选中的存档
- 要自动加载选中的存档，请使用 [BalatroQuickLoad](https://github.com/TsunamiinFantasy/BalatroQuickLoad)。

## 配置
`config.json` 文件包含以下设置：
- `screenshot_enable`: 在备份存档时的截屏功能
- `launch_balatro`: 运行 BalatroSaveManager 时自动启动 Balatro

## 已知问题及解决办法
- 截屏功能仅适用于 Windows。然而，在某些情况下，它可能会遇到问题，无法捕捉实时屏幕。如果您遇到这个问题，可以在 `选项 -> 设置 -> 视频` 中将 Balatro 的 `窗口模式（Windows Mode）` 更改为 `窗口模式（Windowed）`。

## 构建
1. 运行 `git clone https://github.com/RiwiHow/BalatroSaveManager.git`
2. 安装 [PDM](https://github.com/pdm-project/pdm)
3. 运行 `pdm install`
4. 运行 `pyinstaller --onefile --name BalatroSaveManager src/main.py`