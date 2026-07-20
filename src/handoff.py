"""
安装后引导和测试模块
"""

import os
import subprocess
import sys
from typing import Literal, Optional


class HandoffGuide:
    """安装后引导指南"""

    # 基础使用规则（原项目的通用前置）
    BASIC_RULES = """
【通用前置规则 - 每次新会话先粘贴】
────────────────────────────────────
请把我当作计算机新手，始终用中文回复。
遇到我可能不懂的概念，先用通俗语言解释再继续。
动手改动之前：说明目标、说明风险、估计所需时间。
修改任何配置文件前先备份。
涉及管理员权限、删除、覆盖、付费或隐私的操作，先征得我的同意。
每完成一步都验证结果。
优先选择能解决问题的最简单方案；有多个好选项时只推荐最优的一个，并说明理由。
────────────────────────────────────
"""

    # 快速测试示例
    QUICK_TESTS = {
        "create_folder": {
            "name": "创建文件夹",
            "prompt": "帮我在桌面创建一个名为 '测试文件夹' 的文件夹",
            "expected": "桌面出现新文件夹"
        },
        "check_disk": {
            "name": "查看磁盘空间",
            "prompt": "帮我查看当前磁盘使用情况",
            "expected": "显示磁盘容量和使用率"
        },
        "list_files": {
            "name": "列出文件",
            "prompt": "帮我列出当前目录的文件",
            "expected": "显示文件列表"
        },
        "system_info": {
            "name": "查看系统信息",
            "prompt": "帮我查看电脑系统信息",
            "expected": "显示操作系统、CPU、内存等信息"
        }
    }

    # 原项目的 10 个任务 Prompt
    MISSION_PROMPTS = {
        "通用前置": BASIC_RULES,

        "起步": {
            "任务1_初始化电脑": """
【任务 1】初始化这台电脑
────────────────────────────────────
请帮我把这台电脑配置成适合现代 AI 开发的环境。
只安装必要的工具，例如：包管理器、终端增强、字体、Shell 提示符、常用命令行工具。
请根据我的操作系统选择最合适的工具。
────────────────────────────────────
""",
            "任务2_打造AI工作站": """
【任务 2】打造 AI 工作站
────────────────────────────────────
请把这台电脑打造成以 AI 为核心的工作站。
针对编程、写作、研究、终端、浏览器、AI Agent 分别推荐最合适的工具。
逐项征得我同意后再安装。
────────────────────────────────────
"""
        },

        "体检与治理": {
            "任务3_全面体检": """
【任务 3】全面体检
────────────────────────────────────
请对这台电脑做一次全面体检。
检查：硬件、操作系统、存储、内存、安全、备份、已安装软件、开发环境。
找出问题，先列出问题清单和修复方案，经我逐项确认后再修复。
────────────────────────────────────
""",
            "任务4_终端审计": """
【任务 4】终端环境审计
────────────────────────────────────
请检查我的终端环境。
优化：Shell、PATH、别名、提示符、字体、包管理器、开发工具。
清理过时的配置，保持整体简洁、易于维护。
────────────────────────────────────
""",
            "任务5_软件治理": """
【任务 5】软件治理
────────────────────────────────────
请审计这台电脑上安装的所有软件。
找出：重复的、过时的、不再需要的、相互冲突的软件。
告诉我哪些应该删除、更新或替换并说明理由，经我确认后执行。
────────────────────────────────────
""",
            "任务6_存储清理": """
【任务 6】存储清理
────────────────────────────────────
请分析这台电脑的存储使用情况。
找出：大文件、重复文件、不再需要的下载、临时文件。
给出清理方案。未经我确认不得删除任何文件；删除时优先使用可恢复的方式（如回收站）。
────────────────────────────────────
"""
        },

        "网络": {
            "任务7_局域网审计": """
【任务 7】局域网审计
────────────────────────────────────
请帮我检查这里的局域网。
识别网内设备：电脑、NAS、打印机、路由器、交换机、Wi-Fi。
只做只读探测，不要修改任何设备的配置。
找出性能、安全、易用性方面的问题，给出改进建议。
────────────────────────────────────
""",
            "任务8_搭建私有网络": """
【任务 8】搭建跨地点私有网络
────────────────────────────────────
请帮我把多个地点的设备连成一个私有网络。
推荐最简单、最安全的架构，并比较可选方案。
我选定方案后，一步一步带我完成搭建。
────────────────────────────────────
"""
        },

        "进阶": {
            "任务9_自动化": """
【任务 9】自动化
────────────────────────────────────
请帮我找出可以自动化的重复性工作。
先问我平时经常手动做哪些事，再判断哪些值得自动化、哪些不值得。
只实现我批准的自动化，并解释每个自动化是如何工作的。
────────────────────────────────────
""",
            "任务10_长期模式": """
【任务 10】长期模式：我的 IT 工程师
────────────────────────────────────
从现在起，请作为我的私人 IT 工程师。
我提出需求时，选最简单可靠的方案；如果存在明显更好的做法，先说明理由再推荐。
帮助我逐步变得更懂电脑，但不要一次教太多。
────────────────────────────────────
"""
        }
    }

    def __init__(self, provider_name: str, command_name: str):
        """
        初始化引导指南

        Args:
            provider_name: Provider 名称（如 Qwen Code）
            command_name: 命令名称（如 qwen）
        """
        self.provider_name = provider_name
        self.command_name = command_name
        self.platform = self._detect_platform()

    def _detect_platform(self) -> str:
        """检测平台"""
        if sys.platform == "darwin":
            return "macos"
        elif sys.platform.startswith("linux"):
            return "linux"
        elif sys.platform == "win32":
            return "windows"
        return "unknown"

    def get_launch_command(self) -> str:
        """获取启动命令"""
        if self.platform == "windows":
            return f"start {self.command_name}"
        else:
            return self.command_name

    def get_quick_test_prompt(self, test_name: str) -> Optional[str]:
        """获取快速测试 Prompt"""
        if test_name in self.QUICK_TESTS:
            return self.QUICK_TESTS[test_name]["prompt"]
        return None

    def get_mission_prompt(self, category: str, task_name: str) -> Optional[str]:
        """获取任务 Prompt"""
        if category in self.MISSION_PROMPTS:
            if isinstance(self.MISSION_PROMPTS[category], dict):
                return self.MISSION_PROMPTS[category].get(task_name)
            else:
                return self.MISSION_PROMPTS[category]
        return None

    def format_handoff_text(self) -> str:
        """格式化交接文本"""
        return f"""
═══════════════════════════════════════════════════════════════
  安装完成！/ Installation Complete!
═══════════════════════════════════════════════════════════════

【已安装 / Installed】
  AI CLI: {self.provider_name}
  启动命令: {self.command_name}

───────────────────────────────────────────────────────────────

【下一步 / Next Steps】

1️⃣  启动 AI CLI / Launch AI CLI
   在终端中输入：{self.get_launch_command()}

2️⃣  复制以下规则，在 AI CLI 中粘贴（每次新会话先粘贴）：

{self.BASIC_RULES}

3️⃣  尝试快速测试 / Quick Test

   示例命令 / Example Commands:
   ─────────────────────────────────────────────────────────
   • "帮我在桌面创建一个名为 '测试文件夹' 的文件夹"
   • "帮我查看当前磁盘使用情况"
   • "帮我列出当前目录的文件"
   • "帮我查看电脑系统信息"
   ─────────────────────────────────────────────────────────

4️⃣  探索更多任务 / Explore More Missions

   可用任务 / Available Missions:
   ─────────────────────────────────────────────────────────
   • 任务1: 初始化电脑环境
   • 任务2: 打造 AI 工作站
   • 任务3: 全面体检
   • 任务4: 终端环境审计
   • 任务5-10: 更多高级任务...
   ─────────────────────────────────────────────────────────

───────────────────────────────────────────────────────────────

【现在就开始 / Start Now】

打开新终端窗口，输入以下命令启动 AI CLI：

  {self.get_launch_command()}

然后将上述规则粘贴到 AI CLI 中，开始你的 AI 辅助之旅！

═══════════════════════════════════════════════════════════════
"""

    def save_to_file(self, filepath: str = None):
        """保存交接文本到文件"""
        if filepath is None:
            desktop = self._get_desktop_path()
            filepath = os.path.join(desktop, "AI_CLI_使用指南.txt")

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.format_handoff_text())
            return filepath
        except Exception as e:
            print(f"保存失败: {e}")
            return None

    def _get_desktop_path(self) -> str:
        """获取桌面路径"""
        if self.platform == "macos":
            return os.path.expanduser("~/Desktop")
        elif self.platform == "linux":
            return os.path.expanduser("~/Desktop")
        elif self.platform == "windows":
            return os.path.expanduser("~/Desktop")
        else:
            return os.path.expanduser("~")

    def create_quick_reference(self, filepath: str = None):
        """创建快速参考卡片"""
        if filepath is None:
            desktop = self._get_desktop_path()
            filepath = os.path.join(desktop, "AI_CLI_快速参考.txt")

        content = f"""
═══════════════════════════════════════════════════════════════
  AI CLI 快速参考 / Quick Reference
═══════════════════════════════════════════════════════════════

【启动 AI CLI】
  命令: {self.get_launch_command()}

【常用测试命令】
"""
        for test_key, test_info in self.QUICK_TESTS.items():
            content += f"\n  {test_info['name']}:\n"
            content += f"    {test_info['prompt']}\n"

        content += f"\n{self.BASIC_RULES}\n"
        content += "═══════════════════════════════════════════════════════════════\n"

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return filepath
        except Exception as e:
            print(f"保存失败: {e}")
            return None


class AITester:
    """AI CLI 测试器"""

    def __init__(self, command_name: str):
        """
        初始化测试器

        Args:
            command_name: AI CLI 命令名称
        """
        self.command_name = command_name
        self.test_results = []

    def test_command_exists(self) -> bool:
        """测试命令是否存在"""
        try:
            result = subprocess.run(
                ["which" if sys.platform != "win32" else "where", self.command_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def test_command_version(self) -> bool:
        """测试命令版本"""
        try:
            result = subprocess.run(
                [self.command_name, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False

    def run_quick_test(self, test_prompt: str) -> dict:
        """
        运行快速测试

        Args:
            test_prompt: 测试 prompt

        Returns:
            测试结果 {"success": bool, "output": str, "error": str}
        """
        result = {
            "success": False,
            "output": "",
            "error": ""
        }

        try:
            # 注意：这里只是模拟测试，实际需要用户交互
            # 因为 AI CLI 需要用户手动输入 prompt
            result["output"] = "请手动测试：在 AI CLI 中输入以下命令：\n" + test_prompt
            result["success"] = True
        except Exception as e:
            result["error"] = str(e)

        return result

    def run_all_tests(self) -> dict:
        """运行所有测试"""
        tests = {
            "command_exists": self.test_command_exists(),
            "command_version": self.test_command_version()
        }

        return {
            "all_passed": all(tests.values()),
            "tests": tests
        }
