# BalatroSaveManager
[English](https://github.com/RiwiHow/BalatroSaveManager?tab=readme-ov-file#balatrosavemanager) | 简体中文

一个简单的工具来管理 Balatro 的存档。

## 使用方法
- 按 `[` 复制存档
- 按 `↑` 选择一个存档，然后按 `Enter` 加载选中的存档
- 按 `e` 删除所有的存档
- 配置 `config.json` 自定义按键映射
- 要自动加载选中的存档，请使用 [BalatroQuickLoad](https://github.com/TsunamiinFantasy/BalatroQuickLoad)。

## 配置
`config.json` 文件包含以下设置：
- `screenshot_enable`: 开启或关闭备份存档时的截屏功能（默认：`true`）
- `launch_balatro`: 运行 BalatroSaveManager 时是否自动启动 Balatro（默认：`false`）
- `GUI`: 控制窗口的外观和行为
    - `window_opacity`: 控制窗口的透明度（范围：`0.0` 到 `1.0`）（默认值：`0.8`）
    - `always_on_top`: 是否始终置顶（默认值：`true`）
    - `window_size`: 设置窗口默认的宽度和高度（默认：`width = 400`, `height = 150`）
    - `window_position`: 设置窗口在屏幕上的位置。无需手动更改
- `key_mapping`: 自定义按键映射
    - `backup`: 备份当前存档（默认键：`[`）
    - `delete`: 删除所有存档（默认键：`e`）
    - `select`: 选择上一个存档（默认键：`up`）
    - `load`: 加载所选存档（默认键：`enter`）
    - `exit`: 退出 BalatroSaveManager（默认键：`esc`）

## 已知问题及解决办法
- 由于 DPI 的问题，按下保存存档按键后，窗口可能突然缩小，移动到另外一个位置。请右键这个程序，点击「属性」，前往 `兼容性 -> 更改高 DPI 设置 -> 高 DPI 缩放替代 -> 选择「应用程序」`
- 截屏功能仅适用于 Windows。然而，在某些情况下，它可能会遇到问题，无法捕捉实时屏幕。如果您遇到这个问题，可以在 `选项 -> 设置 -> 视频` 中将 Balatro 的 `窗口模式（Windows Mode）` 更改为 `窗口模式（Windowed）`
- GUI 的始终置顶功能在有多台显示器的电脑上的某些显示器不生效.请切换显示器，或者把 Balatro 的 `窗口模式（Windows Mode）` 更改为 `窗口模式（Windowed）`

## 构建
1. 运行 `git clone https://github.com/RiwiHow/BalatroSaveManager.git`
2. 安装 [PDM](https://github.com/pdm-project/pdm)
3. 运行 `pdm install`
4. 运行 `pyinstaller --onefile --noconsole --name BalatroSaveManager src\main.py`
5. 将 `config.json` 文件复制到由 pyinstaller 创建的 `dist` 文件夹中