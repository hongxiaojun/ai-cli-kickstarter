# AI CLI Kickstarter - 打包指南

## 📦 打包说明

本项目使用 PyInstaller 将 Python 项目打包为独立可执行文件。

---

## 🔧 前置要求

### 通用要求
- Python 3.7+
- pip

### macOS
- Xcode Command Line Tools
- PyInstaller

### Windows
- Microsoft Visual C++ Redistributable
- PyInstaller

### Linux
- 开发工具 (build-essential)
- PyInstaller

---

## 🚀 快速打包

### macOS 打包

```bash
# 进入项目目录
cd ai-cli-kickstarter

# 运行打包脚本
./build/macos.sh

# 或使用 PyInstaller 直接打包
pyinstaller build/ai-cli-kickstarter.spec
```

**产物**: `dist/ai-cli-kickstarter.app`

### Windows 打包

```batch
REM 进入项目目录
cd ai-cli-kickstarter

REM 运行打包脚本
build\windows.bat

REM 或使用 PyInstaller 直接打包
pyinstaller build/ai-cli-kickstarter.spec
```

**产物**: `dist\ai-cli-kickstarter.exe`

### Linux 打包

```bash
# 进入项目目录
cd ai-cli-kickstarter

# 运行打包脚本
./build/linux.sh

# 或使用 PyInstaller 直接打包
pyinstaller build/ai-cli-kickstarter.spec
```

**产物**: `dist/ai-cli-kickstarter/ai-cli-kickstarter`

---

## 📋 详细步骤

### 步骤 1：安装依赖

```bash
# 安装 PyInstaller
pip install pyinstaller>=5.0.0

# 安装项目依赖
pip install -r requirements.txt
```

### 步骤 2：清理旧构建（可选）

```bash
# macOS/Linux
rm -rf build dist

# Windows
rmdir /s /q build
rmdir /s /q dist
```

### 步骤 3：执行打包

```bash
# 使用 spec 文件打包（推荐）
pyinstaller build/ai-cli-kickstarter.spec --clean --noconfirm
```

### 步骤 4：测试打包结果

```bash
# macOS
open dist/ai-cli-kickstarter.app

# Windows
dist\ai-cli-kickstarter.exe

# Linux
chmod +x dist/ai-cli-kickstarter/ai-cli-kickstarter
./dist/ai-cli-kickstarter/ai-cli-kickstarter
```

---

## 🎨 高级配置

### 自定义图标

将图标文件放置在 `assets/` 目录：
- macOS: `icon.icns`
- Windows: `icon.ico`
- Linux: `icon.png` (可选)

### 单文件模式

修改 `ai-cli-kickstarter.spec`，添加：
```python
exe = EXE(
    ...
    exclude_binaries=False,  # 改为 False
    ...
)

# 删除 COLLECT 和 BUNDLE 部分
```

### 启用 UPX 压缩

```bash
pyinstaller build/ai-cli-kickstarter.spec --upx
```

### 添加数字签名（Windows）

```batch
signtool sign /f certificate.pfx /p password dist\ai-cli-kickstarter.exe
```

---

## 🐛 常见问题

### Q: PyInstaller 找不到模块

**A**: 在 `spec` 文件的 `hiddenimports` 中添加：
```python
hiddenimports = ['缺失的模块名']
```

### Q: curses 显示异常

**A**: Windows 用户安装 `windows-curses`：
```bash
pip install windows-curses
```

### Q: 打包后文件过大

**A**: 使用 UPX 压缩或单文件模式：
```bash
pyinstaller --onefile --upx run.py
```

### Q: macOS 提示"已损坏"

**A**: 移除隔离标志：
```bash
xattr -cr dist/ai-cli-kickstarter.app
```

---

## 📦 发布流程

### 1. 版本号更新

更新 `src/__init__.py` 中的版本号：
```python
__version__ = "1.0.0"
```

### 2. 打包所有平台

```bash
# macOS
./build/macos.sh

# Windows (在 Windows 机器上)
build\windows.bat

# Linux (在 Linux 机器上)
./build/linux.sh
```

### 3. 创建发布包

```bash
# macOS - 创建 DMG
hdiutil create -volname "AI CLI Kickstarter" \
              -srcfolder dist/ai-cli-kickstarter.app \
              -ov -format UDZO \
              AI-CLI-Kickstarter-1.0.0-macOS.dmg

# Windows - 创建 ZIP
powershell Compress-Archive -Path dist\ai-cli-kickstarter.exe -DestinationPath AI-CLI-Kickstarter-1.0.0-Windows.zip

# Linux - 创建 tar.gz
tar -czf AI-CLI-Kickstarter-1.0.0-Linux.tar.gz -C dist ai-cli-kickstarter
```

### 4. GitHub Release

1. 在 GitHub 创建新 Release
2. 上传各平台的安装包
3. 发布 Release Notes

---

## 📊 文件大小参考

| 平台 | 预期大小 | UPX 压缩后 |
|------|----------|------------|
| macOS .app | ~50 MB | ~30 MB |
| Windows .exe | ~45 MB | ~25 MB |
| Linux | ~40 MB | ~20 MB |

---

## 🔗 相关资源

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [PyInstaller Spec 文件指南](https://pyinstaller.org/en/stable/spec-files.html)
- [macOS .app 打包最佳实践](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/HowToBuildASoftwareProduct/)
- [Windows 数字签名](https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)

---

**打包完成后，请先测试可执行文件是否正常运行。**
