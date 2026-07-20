# AI CLI Kickstarter - 开发快照

**生成时间**: 2026-07-20
**项目路径**: `/Users/add/ai-cli-kickstarter-pro`
**开发状态**: 核心功能已完成，待测试验证

## 📋 项目概述

AI CLI Kickstarter 产品版 - 为完全不懂计算机的人设计的开箱即用 AI CLI 安装器。

### 核心功能

1. **TUI 界面** - 终端菜单界面，方向键操作
2. **默认国内用户** - 自动使用国内镜像
3. **环境依赖检测** - 启动时自动检测并提示
4. **网络环境检测** - 自动判断国内外网络
5. **安装后引导** - 生成使用指南保存到桌面
6. **完整测试流程** - 支持创建文件夹等操作验证

### 支持的 AI CLI

- Qwen Code (通义千问)
- Kimi Code (月之暗面)
- CodeBuddy CLI (腾讯)

## 🏗️ 项目架构

### 目录结构

```
ai-cli-kickstarter-pro/
├── src/
│   ├── __init__.py
│   ├── launcher.py          # 主入口，环境检测与启动
│   ├── tui_safe.py          # TUI 状态机（安全版本，带错误处理）
│   ├── network.py           # 网络检测模块
│   ├── mirrors.py           # 国内镜像配置
│   ├── handoff.py           # 交接指南生成 ⭐
│   ├── env_check.py         # 环境依赖检测模块
│   ├── providers/           # AI CLI 安装逻辑
│   │   ├── __init__.py
│   │   ├── qwen.py
│   │   ├── kimi.py
│   │   └── codebuddy.py
│   └── utils/              # 工具函数
│       ├── __init__.py
│       └── shell.py
├── build/                  # 打包脚本
│   ├── windows.bat
│   ├── macos.sh
│   └── linux.sh
├── vendors/               # 第三方依赖
├── run.py                 # 启动脚本
├── test_complete.py       # 完整测试脚本
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── USAGE.md              # 使用指南
└── TESTING.md            # 测试指南 ⭐
```

### 核心模块说明

#### 1. launcher.py - 主入口
- 环境检测（Python、curl、curses）
- 网络环境检测
- 启动 TUI 界面
- 错误处理和用户引导

#### 2. tui_safe.py - TUI 状态机
- 安全的 curses 包装（带错误处理）
- 状态机：MENU_LANGUAGE → MENU_PROVIDER → CHECK_NETWORK → MENU_CONFIRM → HANDOFF_PROMPT → DONE
- 备用文本模式（curses 失败时）
- 自动保存交接指南

#### 3. handoff.py - 交接指南 ⭐
- `HandoffGuide` 类：生成使用指南
- `AITester` 类：测试 AI CLI 功能
- 自动保存到桌面
- 包含 10 个任务 Prompt（原项目内容）

#### 4. mirrors.py - 镜像配置
- PyPI 国内镜像
- GitHub 加速代理
- Provider 安装 URL

#### 5. network.py - 网络检测
- 检测 Google 可达性
- 检测百度可达性
- 判断国内外网络环境
- 推荐最佳镜像

## 🔄 状态流程

```
启动 → 环境检测 → TUI菜单 → 选择Provider → 网络检测 → 确认安装 → 生成指南 → 完成
```

## ✅ 已完成功能

- [x] TUI 界面框架
- [x] 多语言支持（中英文）
- [x] Provider 选择
- [x] 网络环境检测
- [x] 镜像自动配置
- [x] 环境依赖检测
- [x] 交接指南生成
- [x] 快速参考卡片
- [x] 完整测试脚本

## ⚠️ 待完成功能

- [ ] 实际 AI CLI 安装执行
- [ ] 安装进度显示
- [ ] 错误恢复机制
- [ ] 打包脚本测试
- [ ] 跨平台测试
- [ ] 创建文件夹最终测试

## 🧪 测试状态

### 自动测试

- [ ] 环境检测测试
- [ ] TUI 界面测试
- [ ] 状态转移测试
- [ ] 指南生成测试

### 手动测试

- [ ] macOS 完整流程测试
- [ ] Windows 完整流程测试
- [ ] Linux 完整流程测试

### 最终验收测试

- [ ] 启动 AI CLI
- [ ] 粘贴使用规则
- [ ] 输入"创建文件夹"指令
- [ ] 验证文件夹创建成功

## 🎯 下一步开发

### 优先级 P0（必须完成）

1. **实际安装功能** - 实现真实的 AI CLI 安装
2. **错误处理** - 完善错误恢复机制
3. **最终测试** - 验证创建文件夹功能

### 优先级 P1（重要）

1. **进度显示** - 安装进度条
2. **打包测试** - 测试各平台打包
3. **文档完善** - 更新使用说明

### 优先级 P2（可选）

1. **配置保存** - 保存用户偏好
2. **自动测试** - 安装后自动运行测试
3. **多语言扩展** - 支持更多语言

## 📝 技术决策记录

### 为什么使用 TUI 而不是 GUI？

- 更轻量，无需额外依赖
- 跨平台兼容性好
- 符合开发者习惯
- 更容易实现和维护

### 为什么默认国内镜像？

- 目标用户主要是国内用户
- AI CLI 官方服务器都在国内
- 提升下载速度和成功率

### 为什么使用 Python？

- 跨平台支持
- 丰富的库支持
- 易于维护和扩展
- curses 内置支持

## 🔧 开发环境

- **Python**: 3.7+
- **主要依赖**: curses, urllib, subprocess
- **可选依赖**: windows-curses (Windows)
- **开发平台**: macOS

## 📦 打包方案

- **Windows**: PyInstaller → .exe
- **macOS**: PyInstaller → .app → .dmg
- **Linux**: PyInstaller → 可执行文件 → .deb/.rpm

## 🐛 已知问题

1. **curses 兼容性** - 某些终端环境可能有问题（已添加备用模式）
2. **Python 3.14** - curses.wrapper 可能有兼容性问题
3. **网络检测** - 可能因网络环境导致超时

## 💡 代码规范

- 使用中文注释
- 函数名使用英文
- 常量使用大写
- 类型提示使用 typing 模块

---

**继续开发指南**: 运行 `python3 run.py` 测试功能，参考 `TESTING.md` 进行完整测试。
