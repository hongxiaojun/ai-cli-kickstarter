#!/usr/bin/env python3
"""
AI CLI Kickstarter - 主入口
跨平台启动器，环境检测与 Python 运行时检查
"""

import sys
import os
import time


def print_header():
    """打印标题"""
    print("=" * 60)
    print("AI CLI Kickstarter - 产品版 / Product Edition")
    print("=" * 60)
    print()


def print_step(step: int, total: int, message: str):
    """打印进度步骤"""
    print(f"[{step}/{total}] {message}...")


def print_ok(message: str = "✓"):
    """打印成功消息"""
    print(f"  {message}")


def print_error(message: str):
    """打印错误消息"""
    print(f"  ✗ {message}")


def print_info(message: str):
    """打印信息"""
    print(f"  {message}")


def check_python_version():
    """检查 Python 版本"""
    print_step(1, 5, "检查 Python 版本 / Checking Python version")

    if sys.version_info < (3, 7):
        print_error(f"需要 Python 3.7+，当前: {sys.version}")
        return False

    print_ok(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_curses():
    """检查 curses 是否可用"""
    print_step(2, 5, "检查 curses 模块 / Checking curses module")

    try:
        import curses
        print_ok("curses 可用")
        return True
    except ImportError:
        print_error("curses 不可用")
        if sys.platform == "win32":
            print_info("Windows 用户请运行: pip install windows-curses")
            print_info("Windows users please run: pip install windows-curses")
        return False


def check_curl():
    """检查 curl 是否可用"""
    print_step(3, 5, "检查 curl / Checking curl")

    try:
        import subprocess
        result = subprocess.run(
            ["where" if sys.platform == "win32" else "which", "curl"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print_ok("curl 可用")
            return True
    except:
        pass

    print_error("curl 不可用")
    print_info("安装方法 / Install:")
    if sys.platform == "darwin":
        print_info("  brew install curl")
    elif sys.platform.startswith("linux"):
        print_info("  sudo apt-get install curl  # Debian/Ubuntu")
        print_info("  sudo yum install curl    # RHEL/CentOS")
    return False


def detect_network():
    """检测网络环境（已简化，所有 Provider 均为国内服务）"""
    print_step(4, 5, "配置国内环境 / Configuring CN environment")

    # 所有 Provider（Qwen、Kimi、CodeBuddy）均为国内服务
    print_ok("默认使用国内镜像 / Using CN mirror by default")
    return "cn"


def launch_tui(network_env: str):
    """启动 TUI 界面"""
    print_step(5, 5, "启动安装器 / Launching installer")
    print_ok()

    time.sleep(0.5)

    try:
        # 使用 src 前缀的绝对导入
        from src.tui_safe import InstallerStateMachine, State, run_tui
        from src.mirrors import get_best_mirror

        # 创建并运行状态机
        app = InstallerStateMachine()

        # 根据网络环境设置默认镜像
        if network_env == "cn":
            best_mirror = get_best_mirror(is_china=True)
            app.set_mirror(best_mirror)
            print_info(f"已配置国内镜像 / Using CN mirror: {best_mirror}")

        # 初始化为语言选择菜单
        app.transition_to(State.MENU_LANGUAGE)

        # 运行 TUI
        run_tui(network_env)

        return True

    except ImportError as e:
        print_error(f"导入错误: {e}")
        print_info("请确保在项目根目录运行此脚本")
        print_info("Please run this script from the project root directory")
        return False

    except KeyboardInterrupt:
        print()
        print_info("用户中断 / User interrupted")
        return False
    except Exception as e:
        print_error(f"运行时错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主入口"""
    print_header()

    # 检测平台
    platform = sys.platform
    if platform == "darwin":
        print_info(f"平台 / Platform: macOS")
    elif platform.startswith("linux"):
        print_info(f"平台 / Platform: Linux")
    elif platform == "win32":
        print_info(f"平台 / Platform: Windows")
    else:
        print_info(f"平台 / Platform: {platform}")
    print()

    # 环境检查
    checks = [
        check_python_version(),
        check_curses(),
        check_curl(),
    ]

    if not all(checks):
        print()
        print_error("环境检查未通过 / Environment check failed")
        print_info("请解决上述问题后重试")
        print_info("Please fix the issues above and retry")
        sys.exit(1)

    # 网络检测
    network_env = detect_network()

    # 启动 TUI
    print()
    success = launch_tui(network_env)

    if not success:
        sys.exit(1)

    print()
    print("感谢使用！/ Thank you for using!")


if __name__ == "__main__":
    # 确保项目根目录在 sys.path 中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    main()
