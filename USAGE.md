# AI CLI Kickstarter - 使用指南

## 项目已创建完成！/ Project Created!

你的 AI CLI 安装器项目已经准备就绪，位于：

```
/Users/add/ai-cli-kickstarter-pro/
```

## 快速测试 / Quick Test

### 方法 1：直接运行（开发模式）

```bash
cd /Users/add/ai-cli-kickstarter-pro
python3 run.py
```

### 方法 2：安装依赖后运行

```bash
cd /Users/add/ai-cli-kickstarter-pro
pip3 install -r requirements.txt
python3 src/launcher.py
```

## 打包发布 / Build for Distribution

### macOS

```bash
cd /Users/add/ai-cli-kickstarter-pro/build
./macos.sh
```

输出：`dist/ai-cli-kickstarter.app` 和 `dist/ai-cli-kickstarter.dmg`

### Linux

```bash
cd /Users/add/ai-cli-kickstarter-pro/build
./linux.sh

# 如需创建 .deb 包
./linux.sh --deb
```

输出：`dist/ai-cli-kickstarter` 可执行文件

### Windows

在 Windows 系统上运行：

```batch
cd build
windows.bat
```

输出：`dist/ai-cli-kickstarter.exe`

## 用户使用流程 / User Flow

1. **双击**运行对应平台的安装包
2. 使用 **方向键** 选择语言（中文/English）
3. 使用 **方向键** 选择 AI CLI（Qwen/Kimi/CodeBuddy）
4. 查看 **网络检测结果**（自动检测是否在国内）
5. **确认安装**信息
6. 等待 **安装完成**
7. 查看 **后续使用提示**

## 功能特性 / Features

| 特性 | 说明 |
|------|------|
| **零门槛** | 双击即用，无需命令行知识 |
| **TUI 界面** | 终端菜单界面，方向键操作 |
| **双语** | 中文/English 界面 |
| **网络检测** | 自动检测并切换镜像源 |
| **跨平台** | Windows/macOS/Linux |

## 支持的 AI CLI

| 名称 | 命令 | 特点 |
|------|------|------|
| Qwen Code | `qwen` | 通义千问，国内友好 |
| Kimi Code | `kimi` | 月之暗面，首次需 /login |
| CodeBuddy | `codebuddy` | 腾讯，Beta 版 |

## 下一步 / Next Steps

- [ ] 添加应用图标（`assets/icon.ico`, `assets/icon.icns`）
- [ ] 测试各平台打包流程
- [ ] 验证网络检测逻辑
- [ ] 测试实际 AI CLI 安装流程
- [ ] 考虑代码签名（避免 SmartScreen/Guard 警告）

## 问题排查 / Troubleshooting

### Windows: "curses 模块不可用"

```bash
pip install windows-curses
```

### macOS: "无法打开，因为无法验证开发者"

右键点击应用 → 选择"打开" → 点击"打开"

### Linux: 缺少依赖

```bash
sudo apt-get install python3-curses  # Debian/Ubuntu
sudo yum install python3-curses      # RHEL/CentOS
```

---

**项目基于** [xiaolai/ai-cli-kickstarter](https://github.com/xiaolai/ai-cli-kickstarter)
