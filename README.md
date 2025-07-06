# TempCleaner - 智能文件清理专家

TempCleaner 是一个智能、可配置的自动化文件清理工具，旨在帮助您保持系统整洁，自动处理过期的下载、日志、构建产物和其他临时文件。

## ✨ 核心功能

- **高度可配置**: 通过简单易懂的 `config.yaml` 文件，灵活定义您的清理规则。
- **多种过滤器**: 支持按文件名模式 (`pattern`) 和文件年龄 (`age`) 精准筛选。
- **安全的操作**: 可选择将文件安全地移至回收站 (`trash`) 或进行永久删除 (`delete`)。
- **灵活的触发器**: 支持手动执行 (`manual`)，或设置为定时 (`schedule`)、开机 (`on-startup`) 和关机 (`on-shutdown`) 时自动运行。
- **跨平台与一键安装**: 完美支持 Windows, Linux, 和 macOS，并提供一键安装脚本，自动配置系统计划任务。
- **安全预览**: 提供 `--dry-run` 模式，在实际执行任何文件操作前，让您能预览清理任务将产生的影响，确保万无一失。

## ⚙️ 工作原理

TempCleaner 的核心是 **清理任务 (Job)**。每个任务都在 `config.yaml` 文件中定义，它告诉 TempCleaner：

1.  **`paths`**: 去哪些目录寻找文件。
2.  **`filters`**: 要清理符合哪些条件的文件。
3.  **`actions`**: 找到这些文件后，执行什么操作。

这个简单而强大的组合让您可以创建出满足各种需求的清理规则。

## 🚀 安装与设置

### 前提条件

- 确保您的系统已安装 **Python 3.6** 或更高版本。

### 一键安装 (推荐给普通用户)

这是最简单的安装方式，脚本会自动将 TempCleaner 配置为系统服务。

1.  从项目的 **[Releases](https://github.com/your-username/your-repo/releases)** 页面下载最新版本的预编译包 (`tempcleaner.exe` for Windows, `tempcleaner` for Linux/macOS)。
2.  将下载的可执行文件与 `config.yaml` 和对应的安装脚本 (`install.bat` 或 `install.sh`) 放在同一个文件夹中。

#### **Windows 用户**

1.  右键点击 `install.bat`。
2.  选择 **"以管理员身份运行"**。
3.  脚本会自动使用 Windows 任务计划程序 (Task Scheduler) 创建定时任务和开机启动任务。

#### **Linux / macOS 用户**

1.  打开您的终端。
2.  进入存放文件的目录。
3.  授予安装脚本执行权限: `chmod +x install.sh`。
4.  运行安装脚本: `sudo ./install.sh`。
5.  脚本会自动使用 `cron` 来配置定时任务和开机启动任务。

### 从源码打包 (适合开发者)

如果您想自行修改或打包，请按以下步骤操作：

```bash
# 1. 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 2. 使用 PyInstaller 打包成单文件可执行程序
pyinstaller --onefile temp_cleaner/run.py --name tempcleaner

# 3. 打包完成后，可执行文件会出现在 dist 目录中
```

## 🛠️ 配置指南

所有清理规则都在 `config.yaml` 文件中定义。您可以根据需要创建任意数量的任务。

以下是一个包含所有可用选项的配置示例：

```yaml
# config.yaml
jobs:
  # 任务一：清理超过30天的旧下载压缩包，并移入回收站
  cleanup_old_downloads:
    paths:
      - '~/Downloads'  # 支持用户主目录
      - 'D:/Temp'      # 支持绝对路径
    filters:
      - pattern: # pattern 现在可以接受单个字符串或字符串列表
          - '**/*.zip'
          - '**/*.rar'
          - '**/*.7z' # 新增示例
      - age:
          older_than: "30d"  # d=天, h=小时, m=分钟
    actions:
      - trash: {}  # 移至回收站（推荐）
    triggers:
      - schedule:
          every: "12h" # 每12小时检查一次

  # 任务二：清理开发项目中超过一周的构建产物，并直接删除
  cleanup_dev_builds:
    paths:
      - '~/Documents/Projects'
      - '/var/www/html' # Linux 路径示例
    filters:
      - pattern: # 多个 pattern 可以合并为一个列表
          - '**/target' # 匹配 Java/Rust 的 target 目录
          - '**/build'  # 匹配 a.js/C++ 的 build 目录
          - '**/node_modules'
      - age:
          older_than: "7d"
    actions:
      - delete: {} # 永久删除（请谨慎使用!）
    triggers:
      - on-startup # 每次开机时执行

  # 任务三：手动清理所有 .log 文件
  cleanup_log_files:
    paths:
      - '$APPDATA/MyLogDir' # 支持环境变量
    filters:
      - pattern: '**/*.log' # 单个 pattern 仍然支持
    actions:
      - trash: {}
    triggers:
      - manual # 此任务仅在手动运行时执行
```

### 配置项详解

- **`paths`**: 一个列表，定义了要扫描的文件夹。
    - 支持绝对路径 (e.g., `C:/Users/Test`)。
    - 支持 `~` 自动展开为用户主目录。
    - 支持环境变量 (e.g., `$TEMP`, `%APPDATA%`)。

- **`filters`**: 一个列表，定义了筛选文件的规则，文件必须 **同时满足所有** 过滤器才会被处理。
    - `pattern`: 使用 [glob](https://en.wikipedia.org/wiki/Glob_(programming)) 模式匹配文件名或路径。
        - 可以是单个字符串 (e.g., `pattern: '**/*.log'`)。
        - 也可以是字符串列表 (e.g., `pattern: ['**/*.tmp', '**/*.bak']`)，表示匹配其中任意一个模式。
        - `*.log`: 匹配当前目录下的所有 .log 文件。
        - `**/*.tmp`: 递归匹配所有子目录下的 .tmp 文件。
    - `age`: 根据文件的最后修改时间进行筛选。
        - `older_than`: 支持 `d` (天), `h` (小时), `m` (分钟)。例如 `"90d"`, `"24h"`。

- **`actions`**: 一个列表，定义了要对筛选出的文件执行的操作。
    - `trash: {}`: 将文件移至系统的回收站。这是推荐的默认选项，因为它更安全。
    - `delete: {}`: **永久删除文件**。此操作不可逆，请务必谨慎使用。

- **`triggers`**: 一个列表，定义了任务的触发时机。
    - `manual`: 任务只能通过命令行手动触发。
    - `schedule`: 定时触发。
        - `every`: 定义执行频率，例如 `"1h"`, `"30m"`, `"7d"`。安装脚本会读取此配置来设置系统计划任务。
    - `on-startup`: 在用户登录或系统启动时触发。
    - `on-shutdown`: 在系统关机时触发 (注意：此触发器在某些系统上可能需要额外的手动配置)。

## ⌨️ 使用方法

即使安装后 TempCleaner 会自动运行，您也可以通过命令行手动控制它。

- **立即运行所有适用任务**:
  ```bash
  tempcleaner run
  ```

- **安全地预览将要执行的操作（不会修改任何文件）**:
  ```bash
  tempcleaner run --dry-run
  ```

- **使用指定的配置文件运行**:
  ```bash
  tempcleaner run --config /path/to/my_special_config.yaml
  ```

## 📄 授权许可

本项目采用 [MIT License](LICENSE) 授权。