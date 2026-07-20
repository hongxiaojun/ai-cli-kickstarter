# macOS 使用说明

## 🚀 正确的使用方式

AI CLI Kickstarter 是一个**终端应用程序**，需要在终端中运行，**不是**双击打开的 GUI 应用。

---

## 📋 方法 1：直接运行可执行文件（推荐）

### 在终端中运行
```bash
# 进入项目目录
cd /Users/add/ai-cli-kickstarter-pro

# 直接运行
./dist/ai-cli-kickstarter
```

### 也可以从任何位置运行
```bash
/Users/add/ai-cli-kickstarter-pro/dist/ai-cli-kickstarter
```

---

## 📋 方法 2：使用启动脚本

双击 `ai-cli-kickstarter.command` 文件（在项目根目录），它会自动在终端中运行程序。

---

## 📋 方法 3：添加到 PATH（最方便）

### 临时添加
```bash
# 将可执行文件添加到 PATH
export PATH="/Users/add/ai-cli-kickstarter-pro/dist:$PATH"

# 然后可以在任何地方运行
ai-cli-kickstarter
```

### 永久添加
```bash
# 编辑 shell 配置文件
nano ~/.zshrc

# 添加以下行
export PATH="/Users/add/ai-cli-kickstarter-pro/dist:$PATH"

# 保存后重新加载配置
source ~/.zshrc
```

---

## 🎯 使用流程

1. **打开终端**
   - Spotlight 搜索 "Terminal" 或 "终端"
   - 或按 `Cmd + Space` 输入 "Terminal"

2. **运行安装器**
   ```bash
   /Users/add/ai-cli-kickstarter-pro/dist/ai-cli-kickstarter
   ```

3. **按界面提示操作**
   - 使用方向键 ↑↓ 选择
   - 按回车键确认
   - 按任意键继续

---

## 📁 文件位置

```
/Users/add/ai-cli-kickstarter-pro/
├── dist/
│   └── ai-cli-kickstarter          ← 单文件可执行程序 (8.1 MB)
├── ai-cli-kickstarter.command      ← 双击启动脚本
└── run.py                          ← Python 源码版本
```

---

## ⚠️ 注意事项

1. **不是 GUI 应用**
   - 不要双击 .app 文件（会无响应）
   - 必须在终端中运行

2. **需要终端权限**
   - 首次运行可能需要授权
   - 按提示输入密码（如果需要）

3. **Python 3.7+**
   - 可执行文件已内嵌 Python
   - 无需安装 Python

---

## 🔄 如果遇到问题

### 问题 1：权限被拒绝
```bash
chmod +x dist/ai-cli-kickstarter
```

### 问题 2：找不到命令
```bash
# 使用完整路径
/Users/add/ai-cli-kickstarter-pro/dist/ai-cli-kickstarter
```

### 问题 3：界面显示异常
```bash
# 尝试调整终端窗口大小
# 或使用不同的终端（如 iTerm2）
```

---

## 💡 推荐终端应用

- **Terminal**（macOS 自带）
- **iTerm2**（功能更强）
- **Warp**（现代化）

---

**记住：这是一个终端应用程序，不是 GUI 应用！** 🖥️
