"""
TUI 状态机核心模块
使用 Python curses 实现跨平台终端界面
"""

import curses
import sys
import os
from typing import Literal, Optional, Callable
from enum import Enum

from .network import NetworkDetector, MirrorSource, format_network_status
from .providers import QwenProvider, KimiProvider, CodeBuddyProvider
from .utils import get_platform


class State(Enum):
    """安装状态机"""
    LAUNCH = "launch"
    DETECT_ENV = "detect_env"
    MENU_LANGUAGE = "menu_language"
    MENU_PROVIDER = "menu_provider"
    CHECK_NETWORK = "check_network"
    MENU_CONFIRM = "menu_confirm"
    PROGRESS_INSTALL = "progress_install"
    VERIFY_SUCCESS = "verify_success"
    HANDOFF_PROMPT = "handoff_prompt"
    DONE = "done"
    ERROR = "error"


class InstallerStateMachine:
    """AI CLI 安装器状态机"""

    # 支持的语言
    LANGUAGES = {
        "zh": "中文",
        "en": "English"
    }

    # 支持的 Provider
    PROVIDERS = [QwenProvider, KimiProvider, CodeBuddyProvider]

    def __init__(self):
        self.state = State.LAUNCH
        self.language: Literal["zh", "en"] = "zh"
        self.selected_provider = QwenProvider
        self.network_info: dict = {}
        self.mirror_source: MirrorSource = "mirror_cn"
        self.install_success = False
        self.error_message = ""

        # curses 窗口
        self.stdscr: Optional[curses.window] = None

    def set_language(self, lang: Literal["zh", "en"]):
        """设置语言"""
        self.language = lang

    def set_provider(self, provider_class):
        """选择 Provider"""
        self.selected_provider = provider_class

    def set_mirror(self, mirror: MirrorSource):
        """设置镜像源"""
        self.mirror_source = mirror

    def transition_to(self, new_state: State):
        """状态转移"""
        self.state = new_state

    def get_text(self, key: str) -> str:
        """获取本地化文本"""
        texts = {
            "title": {
                "zh": "AI CLI 安装器",
                "en": "AI CLI Installer"
            },
            "subtitle": {
                "zh": "为完全不懂计算机的人设计的开箱即用安装程序",
                "en": "One-click installer designed for complete beginners"
            },
            "select_language": {
                "zh": "选择语言 / Select Language",
                "en": "Select Language"
            },
            "select_provider": {
                "zh": "选择 AI CLI / Select AI CLI",
                "en": "Select AI CLI"
            },
            "network_check": {
                "zh": "正在检测网络环境...",
                "en": "Checking network environment..."
            },
            "network_status": {
                "zh": "网络状态 / Network Status",
                "en": "Network Status"
            },
            "google": {
                "zh": "Google 访问",
                "en": "Google Access"
            },
            "confirm_install": {
                "zh": "确认安装 / Confirm Installation",
                "en": "Confirm Installation"
            },
            "installing": {
                "zh": "正在安装...",
                "en": "Installing..."
            },
            "install_success": {
                "zh": "安装成功！",
                "en": "Installation Successful!"
            },
            "install_failed": {
                "zh": "安装失败",
                "en": "Installation Failed"
            },
            "verify": {
                "zh": "正在验证...",
                "en": "Verifying..."
            },
            "handoff_title": {
                "zh": "安装完成！下一步...",
                "en": "Installation Complete! Next Steps..."
            },
            "retry": {
                "zh": "重试 / Retry",
                "en": "Retry"
            },
            "choose_another": {
                "zh": "选择其他 / Choose Another",
                "en": "Choose Another"
            },
            "exit": {
                "zh": "退出 / Exit",
                "en": "Exit"
            },
            "yes": {
                "zh": "是 / Yes",
                "en": "Yes"
            },
            "no": {
                "zh": "否 / No",
                "en": "No"
            },
            "back": {
                "zh": "返回 / Back",
                "en": "Back"
            },
            "next": {
                "zh": "继续 / Next",
                "en": "Next"
            }
        }
        return texts.get(key, {}).get(self.language, key)

    def run(self, stdscr: curses.window):
        """运行状态机"""
        self.stdscr = stdscr

        # 初始化 curses
        curses.curs_set(0)  # 隐藏光标
        curses.use_default_colors()

        while self.state != State.DONE:
            self._render_state()
            self._handle_input()

        curses.endwin()

    def _render_state(self):
        """渲染当前状态"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # 渲染标题栏
        title = self.get_text("title")
        subtitle = self.get_text("subtitle")
        self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.A_BOLD)
        self.stdscr.addstr(3, (width - len(subtitle)) // 2, subtitle)
        self.stdscr.addstr(4, 2, "─" * (width - 4))

        # 根据状态渲染不同内容
        if self.state == State.MENU_LANGUAGE:
            self._render_language_menu()
        elif self.state == State.MENU_PROVIDER:
            self._render_provider_menu()
        elif self.state == State.CHECK_NETWORK:
            self._render_network_check()
        elif self.state == State.MENU_CONFIRM:
            self._render_confirm_menu()
        elif self.state == State.PROGRESS_INSTALL:
            self._render_progress()
        elif self.state == State.VERIFY_SUCCESS:
            self._render_verify()
        elif self.state == State.HANDOFF_PROMPT:
            self._render_handoff()
        elif self.state == State.ERROR:
            self._render_error()

        self.stdscr.refresh()

    def _render_language_menu(self):
        """渲染语言选择菜单"""
        height, width = self.stdscr.getmaxyx()
        y = 8

        self.stdscr.addstr(y, (width - len(self.get_text("select_language"))) // 2,
                           self.get_text("select_language"), curses.A_BOLD)
        y += 3

        languages = list(self.LANGUAGES.items())
        for i, (code, name) in enumerate(languages):
            marker = "► " if code == self.language else "  "
            self.stdscr.addstr(y + i, width // 2 - 10, f"{marker}{i + 1}. {name}")

        # 底部提示
        hint = "使用 ↑↓ 选择，回车确认 / Use ↑↓ to select, Enter to confirm"
        self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)

    def _render_provider_menu(self):
        """渲染 Provider 选择菜单"""
        height, width = self.stdscr.getmaxyx()
        y = 8

        self.stdscr.addstr(y, (width - len(self.get_text("select_provider"))) // 2,
                           self.get_text("select_provider"), curses.A_BOLD)
        y += 3

        for i, provider in enumerate(self.PROVIDERS):
            marker = "► " if provider == self.selected_provider else "  "
            name = provider.NAME
            desc = provider.DESCRIPTION.get(self.language, "")
            self.stdscr.addstr(y + i * 2, width // 2 - 25, f"{marker}{i + 1}. {name}")
            self.stdscr.addstr(y + i * 2 + 1, width // 2 - 20, f"    {desc}")

        # 底部提示
        hint = "使用 ↑↓ 选择，回车确认 / Use ↑↓ to select, Enter to confirm"
        self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)

    def _render_network_check(self):
        """渲染网络检测"""
        height, width = self.stdscr.getmaxyx()

        # 执行网络检测
        if not self.network_info:
            self.network_info = NetworkDetector.detect_environment()

        y = 10
        self.stdscr.addstr(y, (width - len(self.get_text("network_status"))) // 2,
                           self.get_text("network_status"), curses.A_BOLD)
        y += 3

        # 显示检测结果
        google_status = self.network_info.get("google", "unknown")
        self.stdscr.addstr(y, width // 2 - 15,
                           f"{self.get_text('google')}: {format_network_status(google_status, self.language)}")

        y += 2
        location = self.network_info.get("location", "unknown")
        location_text = {
            "cn": "中国 / China",
            "overseas": "海外 / Overseas",
            "unknown": "未知 / Unknown"
        }.get(location, location)
        self.stdscr.addstr(y, width // 2 - 15, f"位置 / Location: {location_text}")

        y += 2
        mirror = self.network_info.get("recommended_mirror", "official")
        mirror_text = "国内镜像 / CN Mirror" if mirror == "mirror_cn" else "官方源 / Official"
        self.stdscr.addstr(y, width // 2 - 15, f"推荐源 / Recommended: {mirror_text}")

        # 底部提示
        hint = "按任意键继续 / Press any key to continue"
        self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)

    def _render_confirm_menu(self):
        """渲染确认菜单"""
        height, width = self.stdscr.getmaxyx()
        y = 8

        self.stdscr.addstr(y, (width - len(self.get_text("confirm_install"))) // 2,
                           self.get_text("confirm_install"), curses.A_BOLD)
        y += 3

        # 显示安装信息
        provider = self.selected_provider
        self.stdscr.addstr(y, width // 2 - 20, f"AI CLI: {provider.NAME}")
        y += 1
        self.stdscr.addstr(y, width // 2 - 20, f"安装源 / Source: {self.mirror_source}")
        y += 1
        url = provider.get_install_url()
        self.stdscr.addstr(y, width // 2 - 20, f"URL: {url[:50]}..." if len(url) > 50 else f"URL: {url}")

        y += 3
        self.stdscr.addstr(y, width // 2 - 10, "[Y] " + self.get_text("yes"))
        self.stdscr.addstr(y, width // 2 + 5, "[N] " + self.get_text("no"))

        # 底部提示
        hint = "按 Y 确认，N 取消 / Press Y to confirm, N to cancel"
        self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)

    def _render_progress(self):
        """渲染安装进度"""
        height, width = self.stdscr.getmaxyx()

        y = height // 2 - 2
        self.stdscr.addstr(y, (width - len(self.get_text("installing"))) // 2,
                           self.get_text("installing"), curses.A_BOLD)

        # 简单的加载动画
        import time
        for i in range(10):
            dots = "." * (i % 4)
            self.stdscr.addstr(y + 2, (width - 3) // 2, f"{' ' * 10}")
            self.stdscr.addstr(y + 2, (width - len(dots)) // 2, dots)
            self.stdscr.refresh()
            time.sleep(0.3)

    def _render_verify(self):
        """渲染验证界面"""
        height, width = self.stdscr.getmaxyx()
        y = height // 2

        if self.install_success:
            self.stdscr.addstr(y, (width - len(self.get_text("install_success"))) // 2,
                               self.get_text("install_success"), curses.A_BOLD | curses.color_pair(2))
        else:
            self.stdscr.addstr(y, (width - len(self.get_text("install_failed"))) // 2,
                               self.get_text("install_failed"), curses.A_BOLD | curses.color_pair(1))

        # 底部提示
        hint = "按任意键继续 / Press any key to continue"
        self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)

    def _render_handoff(self):
        """渲染交接提示"""
        height, width = self.stdscr.getmaxyx()
        y = 6

        self.stdscr.addstr(y, (width - len(self.get_text("handoff_title"))) // 2,
                           self.get_text("handoff_title"), curses.A_BOLD)
        y += 3

        # 通用前置规则
        rules = [
            "请把我当作计算机新手，始终用中文回复。",
            "遇到我可能不懂的概念，先用通俗语言解释再继续。",
            "动手改动之前：说明目标、说明风险、估计所需时间。",
            "修改任何配置文件前先备份。",
            "涉及管理员权限、删除、覆盖、付费或隐私的操作，先征得我的同意。",
            "每完成一步都验证结果。",
            "优先选择能解决问题的最简单方案。"
        ]

        for rule in rules:
            self.stdscr.addstr(y, 5, f"• {rule}")
            y += 1

        # 底部提示
        hint = "按任意键退出 / Press any key to exit"
        self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)

    def _render_error(self):
        """渲染错误界面"""
        height, width = self.stdscr.getmaxyx()
        y = height // 2 - 3

        self.stdscr.addstr(y, (width - len(self.get_text("install_failed"))) // 2,
                           self.get_text("install_failed"), curses.A_BOLD | curses.color_pair(1))
        y += 2

        if self.error_message:
            self.stdscr.addstr(y, (width - len(self.error_message)) // 2, self.error_message)
            y += 2

        # 错误处理选项
        options = [
            "[1] " + self.get_text("retry"),
            "[2] " + self.get_text("choose_another"),
            "[3] " + self.get_text("exit")
        ]
        for i, opt in enumerate(options):
            self.stdscr.addstr(y + i, width // 2 - 10, opt)

    def _handle_input(self):
        """处理输入"""
        if self.state == State.MENU_LANGUAGE:
            self._handle_language_input()
        elif self.state == State.MENU_PROVIDER:
            self._handle_provider_input()
        elif self.state in (State.CHECK_NETWORK, State.VERIFY_SUCCESS, State.HANDOFF_PROMPT):
            self._handle_continue_input()
        elif self.state == State.MENU_CONFIRM:
            self._handle_confirm_input()
        elif self.state == State.PROGRESS_INSTALL:
            self._handle_install()
        elif self.state == State.ERROR:
            self._handle_error_input()

    def _handle_language_input(self):
        """处理语言选择输入"""
        key = self.stdscr.getch()

        if key == curses.KEY_DOWN:
            if self.language == "zh":
                self.set_language("en")
        elif key == curses.KEY_UP:
            if self.language == "en":
                self.set_language("zh")
        elif key in (ord('\n'), ord(' ')):
            self.transition_to(State.MENU_PROVIDER)

    def _handle_provider_input(self):
        """处理 Provider 选择输入"""
        key = self.stdscr.getch()

        providers = self.PROVIDERS
        current_idx = providers.index(self.selected_provider) if self.selected_provider in providers else 0

        if key == curses.KEY_DOWN:
            current_idx = (current_idx + 1) % len(providers)
            self.set_provider(providers[current_idx])
        elif key == curses.KEY_UP:
            current_idx = (current_idx - 1) % len(providers)
            self.set_provider(providers[current_idx])
        elif key in (ord('\n'), ord(' ')):
            self.transition_to(State.CHECK_NETWORK)

    def _handle_continue_input(self):
        """处理继续输入"""
        self.stdscr.getch()

        if self.state == State.CHECK_NETWORK:
            # 设置推荐的镜像源
            recommended = self.network_info.get("recommended_mirror", "official")
            self.set_mirror(recommended)
            self.transition_to(State.MENU_CONFIRM)
        elif self.state == State.VERIFY_SUCCESS:
            self.transition_to(State.HANDOFF_PROMPT)
        elif self.state == State.HANDOFF_PROMPT:
            self.transition_to(State.DONE)

    def _handle_confirm_input(self):
        """处理确认输入"""
        key = self.stdscr.getch()

        if key in (ord('y'), ord('Y')):
            self.transition_to(State.PROGRESS_INSTALL)
        elif key in (ord('n'), ord('N'), 27):  # 27 is ESC
            self.transition_to(State.MENU_PROVIDER)

    def _handle_install(self):
        """执行安装"""
        try:
            result = self.selected_provider.install(mirror=self.mirror_source)
            self.install_success = result.success

            if not self.install_success:
                self.error_message = result.stderr or "Installation failed"

            # 验证安装
            self.install_success = self.selected_provider.verify()

            self.transition_to(State.VERIFY_SUCCESS)
        except Exception as e:
            self.error_message = str(e)
            self.install_success = False
            self.transition_to(State.VERIFY_SUCCESS)

    def _handle_error_input(self):
        """处理错误状态输入"""
        key = self.stdscr.getch()

        if key == ord('1'):
            # 重试
            self.transition_to(State.MENU_CONFIRM)
        elif key == ord('2'):
            # 选择其他
            self.transition_to(State.MENU_PROVIDER)
        elif key == ord('3'):
            # 退出
            self.transition_to(State.DONE)


def run_tui(network_env: str = "cn"):
    """运行 TUI 界面
    
    Args:
        network_env: 网络环境 ("cn", "international", "unknown")
    """
    app = InstallerStateMachine()
    
    # 预设网络检测结果，避免重复检测
    app.network_info = {
        "location": network_env,
        "google": "unreachable" if network_env == "cn" else "reachable",
        "baidu": "reachable" if network_env == "cn" else "unreachable",
        "recommended_mirror": "mirror_cn" if network_env == "cn" else "official"
    }
    
    # 初始化为语言选择菜单
    app.transition_to(State.MENU_LANGUAGE)
    curses.wrapper(app.run)
    return app
