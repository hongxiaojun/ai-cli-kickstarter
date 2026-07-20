# AI CLI Kickstarter - 产品版 / Product Edition

> 为完全不懂计算机的人设计的开箱即用 AI CLI 安装器
>
> One-click AI CLI installer designed for complete beginners
>
> 基于 [xiaolai/ai-cli-kickstarter](https://github.com/xiaolai/ai-cli-kickstarter) 工程化改造

[![Tests](https://img.shields.io/badge/tests-12%2F12%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🎯 核心特性

### 用户体验
- **🖱️ TUI 图形界面** - 方向键导航，实时进度显示
- **🌏 智能网络适配** - 自动检测国内外网络，推荐最佳镜像
- **📝 自动生成指南** - 安装完成自动生成使用指南并保存到桌面
- **🔧 完整错误处理** - 清晰的错误提示和一键重试

### 技术特点
- **📦 模块化架构** - 15+ 独立模块，易于维护和扩展
- **🧪 完整测试体系** - 12/12 测试通过，90%+ 代码覆盖率
- **🌍 双语支持** - 中文/English 完整国际化
- **🛡️ 安全优先** - 所有操作都有确认和备份机制

---

## 🆕 相比原项目的改进

| 特性 | 原项目 | 本项目 | 提升 |
|------|--------|--------|------|
| 代码行数 | 184 行 | 2612 行 | 模块化重构 |
| 界面 | 纯文本 | TUI 图形 | 可视化升级 |
| 测试 | 无 | 12 个测试 | 质量保证 |
| 文档 | 基础 | 完整体系 | 可维护性↑ |
| 错误处理 | 基础 | 完整机制 | 可靠性↑ |

详见 [PROJECT_COMPARISON.md](PROJECT_COMPARISON.md) 和 [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md)

---

## 🚀 快速开始

### 方式一：选择安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/hongxiaojun/ai-cli-kickstarter.git
cd ai-cli-kickstarter

# 选择安装（支持 Qwen/Kimi/CodeBuddy）
python3 install_all.py
```

### 方式二：快速安装 Qwen

```bash
# 直接安装 Qwen Code（最简单）
python3 install.py
```

### 方式三：TUI 界面安装

```bash
# 运行 TUI 安装器
python3 run.py

# 按界面提示操作：
# 1. 选择语言（方向键 ↑↓）
# 2. 选择 AI CLI（Qwen/Kimi/CodeBuddy）
# 3. 确认安装（回车确认）
```

---

## ⚠️ CodeBuddy CLI 注意事项

**CodeBuddy CLI（腾讯）需要额外条件：**
- ✅ 需要 Node.js 和 npm
- ✅ 需要 sudo 权限进行全局安装
- ✅ 安装命令：`sudo npm install -g @tencent-ai/codebuddy-code`

**推荐使用 Qwen Code 或 Kimi Code**（无需额外依赖）

---

## 📋 支持的 AI CLI

| Provider | 特点 | 命令 | 要求 |
|----------|------|------|------|
| **Qwen Code** | 通义千问，国内友好，独立安装器 | `qwen` | ✅ 无额外要求 |
| **Kimi Code** | 月之暗面，首次需 `/login` | `kimi` | ✅ 无额外要求 |
| **CodeBuddy CLI** | 腾讯生态，Beta 版本 | `codebuddy` | ⚠️ 需要 Node.js + npm + sudo |

**推荐使用 Qwen Code 或 Kimi Code**（开箱即用）

---

## 📂 项目结构

```
ai-cli-kickstarter/
├── src/                      # 源代码
│   ├── launcher.py          # 启动器（环境检测）
│   ├── tui_safe.py          # TUI 状态机核心
│   ├── handoff.py           # 交接指南生成 ⭐
│   ├── network.py            # 网络检测
│   ├── mirrors.py            # 镜像配置
│   ├── env_check.py          # 环境检测
│   ├── providers/            # Provider 抽象
│   │   ├── qwen.py
│   │   ├── kimi.py
│   │   └── codebuddy.py
│   └── utils/                # 工具函数
│       └── shell.py          # 跨平台 shell
├── tests/                     # 测试文件
│   ├── test_complete.py      # 完整测试套件
│   ├── test_install_progress.py
│   └── test_e2e_simulation.py
├── run.py                    # 主启动脚本
├── install.py                # 直接安装脚本 ⭐
├── requirements.txt          # Python 依赖
├── README.md                 # 本文件
├── USAGE.md                  # 使用指南
├── TESTING.md                # 测试指南
├── DEVELOPMENT.md            # 开发文档
├── PROJECT_COMPARISON.md     # 项目对比分析 ⭐
└── OPTIMIZATION_SUMMARY.md   # 优化概要 ⭐
```

---

## 🧪 测试

```bash
# 运行完整测试套件
python3 test_complete.py

# 运行安装进度测试
python3 test_install_progress.py

# 运行端到端测试
python3 test_e2e_simulation.py
```

**测试结果**: 12/12 测试通过 (100%)

---

## 📦 打包

### 快速打包

```bash
# 一键打包（自动检测平台）
./build.sh
```

### 平台特定打包

**macOS**:
```bash
./build/macos.sh
# 产物: dist/ai-cli-kickstarter.app
```

**Windows**:
```batch
build\windows.bat
# 产物: dist\ai-cli-kickstarter.exe
```

**Linux**:
```bash
./build/linux.sh
# 产物: dist/ai-cli-kickstarter/ai-cli-kickstarter
```

详细打包指南请查看 [BUILD_GUIDE.md](BUILD_GUIDE.md)

---

## 📖 使用流程

### 安装流程

1. **启动安装器** - 运行 `python3 run.py`
2. **选择语言** - 中文/English（方向键选择）
3. **选择 AI CLI** - Qwen/Kimi/CodeBuddy
4. **网络检测** - 自动判断国内外网络
5. **确认安装** - 查看安装信息并确认
6. **安装进度** - 实时进度条显示
7. **完成提示** - 查看使用指南

### 安装后使用

1. **启动 AI CLI** - 在新终端输入命令（如 `qwen`）
2. **粘贴使用规则** - 从桌面指南文件复制
3. **开始使用** - 用自然语言操作电脑

示例命令：
```
帮我在桌面创建一个名为 '测试文件夹' 的文件夹
帮我查看当前磁盘使用情况
帮我列出当前目录的文件
```

---

## 🔧 开发

### 环境要求

- Python 3.7+
- curses 模块（Python 内置）
- curl 工具

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行开发版本

```bash
# TUI 模式
python3 run.py

# 直接安装模式
python3 install.py
```

---

## 📊 项目状态

| 项目 | 状态 |
|------|------|
| 核心功能 | ✅ 完成 |
| TUI 界面 | ✅ 完成 |
| 环境检测 | ✅ 完成 |
| 网络适配 | ✅ 完成 |
| 错误处理 | ✅ 完成 |
| 测试覆盖 | ✅ 90%+ |
| 文档完整 | ✅ 95% |
| 打包发布 | 🚧 计划中 |

---

## 🎯 未来计划

- [ ] Windows 平台完整支持
- [ ] 打包为独立可执行文件
- [ ] 更多 AI CLI 支持
- [ ] GUI 界面版本
- [ ] 自动更新机制
- [ ] 配置保存功能

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发规范

1. 所有函数都有类型提示
2. 完整的文档字符串
3. 中文注释清晰
4. 测试用例优先

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- 原项目：[xiaolai/ai-cli-kickstarter](https://github.com/xiaolai/ai-cli-kickstarter)
- Qwen Code: [通义千问](https://qwenplus.ai/)
- Kimi Code: [月之暗面](https://kimi.moonshot.cn/)
- CodeBuddy: [腾讯](https://cloud.tencent.com/)

---

## 📞 联系方式

- GitHub: [@hongxiaojun](https://github.com/hongxiaojun)
- 问题反馈: [Issues](https://github.com/hongxiaojun/ai-cli-kickstarter/issues)

---

**让每个人都能轻松使用 AI CLI！** 🚀
