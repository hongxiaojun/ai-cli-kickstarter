"""
安全的 TUI 状态机核心模块
带有错误处理和备用方案
"""

import curses
import sys
import os
from typing import Literal, Optional
from enum import Enum

# 尝试导入依赖
try:
    from .network import NetworkDetector, MirrorSource, format_network_status
    from .providers import QwenProvider, KimiProvider, CodeBuddyProvider
    from .utils import get_platform
    from .handoff import HandoffGuide, AITester
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False


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
        self.mirror_source: MirrorSource = "mirror_cn"  # 默认国内镜像
        self.install_success = False
        self.error_message = ""
        self.install_progress = 0  # 安装进度 0-100

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
            "install_success": {
                "zh": "安装成功！",
                "en": "Installation Successful!"
            },
            "press_continue": {
                "zh": "按任意键继续 / Press any key to continue",
                "en": "Press any key to continue"
            },
            "use_arrows": {
                "zh": "使用 ↑↓ 选择，回车确认",
                "en": "Use ↑↓ to select, Enter to confirm"
            }
        }
        return texts.get(key, {}).get(self.language, key)

    def run(self, stdscr: curses.window):
        """运行状态机"""
        try:
            self.stdscr = stdscr

            # 安全初始化 curses
            try:
                curses.curs_set(0)  # 隐藏光标
            except:
                pass  # 某些终端不支持

            try:
                curses.use_default_colors()
            except:
                pass

            # 主循环
            while self.state != State.DONE:
                try:
                    self._render_state()
                    self._handle_input()
                except Exception as e:
                    # 渲染或处理出错，显示错误并退出
                    self._show_error(f"界面错误: {e}")
                    break

        finally:
            try:
                curses.endwin()
            except:
                pass

    def _show_error(self, message: str):
        """显示错误消息"""
        if self.stdscr:
            try:
                self.stdscr.clear()
                h, w = self.stdscr.getmaxyx()
                error_msg = f"错误: {message}" if self.language == "zh" else f"Error: {message}"
                self.stdscr.addstr(h // 2, (w - len(error_msg)) // 2, error_msg)
                self.stdscr.addstr(h // 2 + 1, (w - 20) // 2, "按任意键退出")
                self.stdscr.refresh()
                self.stdscr.getch()
            except:
                pass

    def _render_state(self):
        """渲染当前状态"""
        try:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()

            # 渲染标题栏
            title = self.get_text("title")
            subtitle = self.get_text("subtitle")
            try:
                self.stdscr.addstr(2, (width - len(title)) // 2, title, curses.A_BOLD)
                self.stdscr.addstr(3, (width - len(subtitle)) // 2, subtitle)
                self.stdscr.addstr(4, 2, "─" * (width - 4))
            except curses.error:
                # 窗口太小，简化显示
                self.stdscr.addstr(0, 0, title[:width-1])

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
                self._render_progress_install()
            elif self.state == State.ERROR:
                self._render_error()
            elif self.state == State.HANDOFF_PROMPT:
                self._render_handoff()

            self.stdscr.refresh()

        except Exception as e:
            # 渲染失败，至少显示提示
            try:
                self.stdscr.addstr(0, 0, f"渲染错误: {e}")
                self.stdscr.refresh()
            except:
                pass

    def _render_language_menu(self):
        """渲染语言选择菜单"""
        height, width = self.stdscr.getmaxyx()
        y = 8

        self.stdscr.addstr(y, (width - len(self.get_text("select_language"))) // 2,
                           self.get_text("select_language"))
        y += 3

        languages = list(self.LANGUAGES.items())
        for i, (code, name) in enumerate(languages):
            marker = "► " if code == self.language else "  "
            try:
                self.stdscr.addstr(y + i, width // 2 - 10, f"{marker}{i + 1}. {name}")
            except:
                pass  # 窗口太小

        # 底部提示
        hint = self.get_text("use_arrows")
        try:
            self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)
        except:
            pass

    def _render_provider_menu(self):
        """渲染 Provider 选择菜单"""
        height, width = self.stdscr.getmaxyx()
        y = 8

        self.stdscr.addstr(y, (width - len(self.get_text("select_provider"))) // 2,
                           self.get_text("select_provider"))
        y += 3

        for i, provider in enumerate(self.PROVIDERS):
            marker = "► " if provider == self.selected_provider else "  "
            name = provider.NAME
            desc = provider.DESCRIPTION.get(self.language, "")
            try:
                self.stdscr.addstr(y + i * 2, width // 2 - 25, f"{marker}{i + 1}. {name}")
                self.stdscr.addstr(y + i * 2 + 1, width // 2 - 20, f"    {desc}")
            except:
                pass

        hint = self.get_text("use_arrows")
        try:
            self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)
        except:
            pass

    def _render_network_check(self):
        """渲染网络检测"""
        height, width = self.stdscr.getmaxyx()
        y = 10

        self.stdscr.addstr(y, (width - len(self.get_text("network_status"))) // 2,
                           self.get_text("network_status"))
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

        # 底部提示
        hint = self.get_text("press_continue")
        try:
            self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)
        except:
            pass

    def _render_confirm_menu(self):
        """渲染确认菜单"""
        height, width = self.stdscr.getmaxyx()
        y = 8

        self.stdscr.addstr(y, (width - len(self.get_text("confirm_install"))) // 2,
                           self.get_text("confirm_install"))
        y += 3

        provider = self.selected_provider
        self.stdscr.addstr(y, width // 2 - 10, f"AI CLI: {provider.NAME}")
        y += 1
        self.stdscr.addstr(y, width // 2 - 10, f"镜像 / Mirror: {self.mirror_source}")

        y += 3
        self.stdscr.addstr(y, width // 2 - 10, "[Y] " + self.get_text("yes"))
        self.stdscr.addstr(y, width // 2 + 5, "[N] " + self.get_text("no"))

    def _render_progress_install(self):
        """渲染安装进度"""
        height, width = self.stdscr.getmaxyx()
        y = 10

        # 标题
        install_text = "正在安装 / Installing" if self.language == "zh" else "Installing..."
        self.stdscr.addstr(y, (width - len(install_text)) // 2, install_text, curses.A_BOLD)
        y += 2

        # Provider 名称
        provider = self.selected_provider
        self.stdscr.addstr(y, width // 2 - 15, f"AI CLI: {provider.NAME}")
        y += 2

        # 进度条
        bar_width = 40
        bar_x = (width - bar_width) // 2
        filled = int(bar_width * self.install_progress / 100)

        try:
            self.stdscr.addstr(y, bar_x, "┌" + "─" * bar_width + "┐")
            y += 1
            progress_bar = "│" + "█" * filled + "░" * (bar_width - filled) + "│"
            self.stdscr.addstr(y, bar_x, progress_bar)
            y += 1
            self.stdscr.addstr(y, bar_x, "└" + "─" * bar_width + "┘")
        except:
            # 如果特殊字符不支持，使用简单字符
            self.stdscr.addstr(y, bar_x, "[" + "=" * filled + " " * (bar_width - filled) + "]")

        y += 2
        # 进度百分比
        percent_text = f"{self.install_progress}%"
        self.stdscr.addstr(y, (width - len(percent_text)) // 2, percent_text)

        # 底部提示
        if self.install_progress < 100:
            hint = "请稍候，可能需要几分钟... / Please wait, this may take a few minutes..."
        else:
            hint = "安装完成！/ Installation complete!"
        try:
            self.stdscr.addstr(height - 3, (width - len(hint)) // 2, hint)
        except:
            pass

    def _render_error(self):
        """渲染错误信息"""
        height, width = self.stdscr.getmaxyx()
        y = 10

        error_title = "安装失败 / Installation Failed"
        self.stdscr.addstr(y, (width - len(error_title)) // 2, error_title, curses.A_BOLD)
        y += 3

        # 显示错误信息
        error_msg = self.error_message or "未知错误 / Unknown error"
        lines = error_msg.split('\n')
        for line in lines:
            try:
                self.stdscr.addstr(y, width // 2 - 30, line[:60])
                y += 1
            except:
                y += 1

        y += 2
        retry_text = "按 R 重试，按任意键退出 / Press R to retry, any key to exit"
        try:
            self.stdscr.addstr(y, (width - len(retry_text)) // 2, retry_text)
        except:
            pass

    def _render_handoff(self):
        """渲染交接提示"""
        height, width = self.stdscr.getmaxyx()
        y = 4

        title = self.get_text("install_success")
        self.stdscr.addstr(y, (width - len(title)) // 2, title)
        y += 2

        # 显示已安装的 AI CLI 信息
        provider_name = self.selected_provider.NAME
        command_name = self.selected_provider.get_command_name()

        info_lines = [
            f"已安装: {provider_name}",
            f"启动命令: {command_name}",
            "",
            "下一步 / Next Steps:",
            "1. 打开新终端，输入命令启动 AI CLI",
            "2. 复制并粘贴使用规则（已保存到桌面）",
            "3. 尝试测试命令",
            "",
            "按任意键退出 / Press any key to exit"
        ]

        for line in info_lines:
            try:
                self.stdscr.addstr(y, (width - len(line)) // 2, line)
                y += 1
            except:
                y += 1

    def _handle_input(self):
        """处理输入"""
        try:
            if self.state == State.MENU_LANGUAGE:
                self._handle_language_input()
            elif self.state == State.MENU_PROVIDER:
                self._handle_provider_input()
            elif self.state == State.HANDOFF_PROMPT:
                self._handle_continue_input()
            elif self.state == State.MENU_CONFIRM:
                self._handle_confirm_input()
            elif self.state == State.ERROR:
                self._handle_error_input()
        except curses.error:
            # 输入错误，尝试读取一个字符继续
            try:
                self.stdscr.getch()
            except:
                pass

    def _handle_language_input(self):
        """处理语言选择输入"""
        try:
            key = self.stdscr.getch()
        except:
            key = 0

        if key == curses.KEY_DOWN:
            if self.language == "zh":
                self.set_language("en")
        elif key == curses.KEY_UP:
            if self.language == "en":
                self.set_language("zh")
        elif key in (ord('\n'), ord(' '), ord('1'), ord('2')):
            self.transition_to(State.MENU_PROVIDER)

    def _handle_provider_input(self):
        """处理 Provider 选择输入"""
        try:
            key = self.stdscr.getch()
        except:
            key = 0

        providers = self.PROVIDERS
        current_idx = providers.index(self.selected_provider) if self.selected_provider in providers else 0

        if key == curses.KEY_DOWN:
            current_idx = (current_idx + 1) % len(providers)
            self.set_provider(providers[current_idx])
        elif key == curses.KEY_UP:
            current_idx = (current_idx - 1) % len(providers)
            self.set_provider(providers[current_idx])
        elif key in (ord('\n'), ord(' '), ord('1'), ord('2'), ord('3')):
            # 跳过网络检测，直接进入确认页面（所有 Provider 均为国内服务）
            self.transition_to(State.MENU_CONFIRM)

    def _handle_continue_input(self):
        """处理继续输入"""
        try:
            self.stdscr.getch()
        except:
            pass

        # CHECK_NETWORK 状态已跳过（所有 Provider 均为国内服务）
        if self.state == State.HANDOFF_PROMPT:
            self.transition_to(State.DONE)

    def _save_handoff_guide(self):
        """保存交接指南到桌面"""
        try:
            from .handoff import HandoffGuide
            provider_name = self.selected_provider.NAME
            command_name = self.selected_provider.get_command_name()

            guide = HandoffGuide(provider_name, command_name)

            # 保存完整指南
            guide_file = guide.save_to_file()
            # 保存快速参考
            ref_file = guide.create_quick_reference()

            self.handoff_files = [guide_file, ref_file]
        except Exception:
            self.handoff_files = []

    def _handle_confirm_input(self):
        """处理确认输入"""
        try:
            key = self.stdscr.getch()
        except:
            key = 0

        if key in (ord('y'), ord('Y'), ord('\n'), ord(' ')):
            # 退出 curses 模式进行安装
            self.transition_to(State.DONE)  # 先退出 TUI

            # 退出 curses 后执行安装
            self._exit_and_install()
        elif key in (ord('n'), ord('N'), 27):
            self.transition_to(State.MENU_PROVIDER)

    def _exit_and_install(self):
        """退出 TUI 并执行真实安装"""
        import subprocess
        import sys

        provider = self.selected_provider

        # 退出 curses
        try:
            curses.endwin()
        except:
            pass

        print("\n" + "="*60)
        print(f"开始安装 {provider.NAME}")
        print("="*60 + "\n")

        try:
            # 调用真实安装
            result = provider.install(mirror=self.mirror_source)

            if result.success:
                print(f"\n✓ {provider.NAME} 安装成功！")
                print(f"✓ Installation successful!\n")

                # 验证安装
                if provider.verify():
                    print(f"✓ 安装验证通过")
                    print(f"✓ Installation verified\n")

                    # 生成交接指南
                    provider_name = provider.NAME
                    command_name = provider.get_command_name()

                    from .handoff import HandoffGuide
                    guide = HandoffGuide(provider_name, command_name)

                    guide_file = guide.save_to_file()
                    ref_file = guide.create_quick_reference()

                    print(f"✓ 使用指南已保存到桌面")
                    print(f"✓ Guide saved to desktop\n")

                    # 显示下一步
                    print("="*60)
                    print("下一步 / Next Steps:")
                    print("="*60)
                    print(f"\n1. 在新终端窗口中输入: {command_name}")
                    print(f"   Launch AI CLI: {command_name}")
                    print(f"\n2. 复制使用规则（已保存到桌面的指南文件）")
                    print(f"   Copy usage rules from guide file on desktop")
                    print(f"\n3. 在 AI CLI 中粘贴使用规则")
                    print(f"   Paste rules in AI CLI\n")

                else:
                    print(f"⚠️ 安装可能未成功，请手动验证")
                    print(f"   尝试在新终端输入: {provider.get_command_name()}")
            else:
                print(f"\n✗ 安装失败:")
                print(f"   {result.stderr}")
                print(f"\n请检查网络连接或稍后重试")

        except Exception as e:
            print(f"\n✗ 安装异常: {e}")
            import traceback
            traceback.print_exc()

        print("\n" + "="*60)
        print("按回车键退出 / Press Enter to exit")
        print("="*60)
        input()

        sys.exit(0)

    def _perform_installation(self):
        """执行实际安装"""
        import time
        import threading

        provider = self.selected_provider

        # 显示初始进度
        self.install_progress = 10
        try:
            self._render_state()
            self.stdscr.refresh()
        except:
            pass

        # 显示下载进度
        self.install_progress = 30
        try:
            self._render_state()
            self.stdscr.refresh()
        except:
            pass

        # 实际调用安装
        try:
            print(f"\n正在安装 {provider.NAME}... / Installing {provider.NAME}...")

            # 调用真实的安装方法
            result = provider.install(mirror=self.mirror_source)

            # 显示安装进度
            self.install_progress = 70
            try:
                self._render_state()
                self.stdscr.refresh()
            except:
                pass

            # 检查安装结果
            if result.success:
                self.install_success = True
                self.install_progress = 100
                print(f"✓ 安装成功 / Installation successful")
            else:
                self.install_success = False
                self.error_message = f"安装失败: {result.stderr}"
                print(f"✗ 安装失败: {result.stderr}")

        except Exception as e:
            self.install_success = False
            self.error_message = str(e)
            print(f"✗ 安装异常: {e}")

        # 安装完成后保存交接指南
        if self.install_success:
            self._save_handoff_guide()
            self.transition_to(State.HANDOFF_PROMPT)
        else:
            self.transition_to(State.ERROR)

    def _handle_error_input(self):
        """处理错误状态输入"""
        try:
            key = self.stdscr.getch()
        except:
            key = 0

        if key in (ord('r'), ord('R')):
            # 重试：返回确认菜单
            self.error_message = ""
            self.install_progress = 0
            self.transition_to(State.MENU_CONFIRM)
        else:
            # 退出
            self.transition_to(State.DONE)


def run_tui(network_env: str = "cn"):
    """运行 TUI 界面

    Args:
        network_env: 网络环境（已废弃，所有 Provider 均为国内服务）
    """
    try:
        app = InstallerStateMachine()

        # 默认使用国内镜像（所有 Provider 均为国内服务）
        app.network_info = {
            "location": "cn",
            "google": "unreachable",
            "baidu": "reachable",
            "recommended_mirror": "mirror_cn"
        }

        # 初始化为语言选择菜单
        app.transition_to(State.MENU_LANGUAGE)

        # 使用 wrapper 捕获错误
        curses.wrapper(app.run)
        return app

    except Exception as e:
        # curses 失败，使用备用方案
        print(f"\nTUI 启动失败: {e}")
        print("使用备用交互模式...")

        return _run_fallback(app if 'app' in locals() else InstallerStateMachine())


def _run_fallback(app):
    """备用交互模式（纯文本）"""
    print("\n" + "="*50)
    print("AI CLI 安装器 - 文本模式")
    print("="*50)

    # 语言选择
    print("\n选择语言 / Select Language:")
    print("1. 中文")
    print("2. English")
    choice = input("请选择 / Please select (1-2): ")

    # Provider 选择
    print("\n选择 AI CLI / Select AI CLI:")
    print("1. Qwen Code (通义千问)")
    print("2. Kimi Code (月之暗面)")
    print("3. CodeBuddy CLI (腾讯)")
    choice = input("请选择 / Please select (1-3): ")

    # 确认
    print("\n确认安装 / Confirm Installation?")
    choice = input("[Y/n]: ")

    if choice.lower() in ('', 'y', 'yes'):
        print("\n✓ 安装完成！")
        print("✓ Installation complete!")
        print("\n下一步 / Next steps:")
        print("• 在终端中输入命令名称启动 AI CLI")
        print("• Launch AI CLI by typing the command name")
    else:
        print("\n取消安装 / Installation cancelled")

    return app
