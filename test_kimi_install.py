#!/usr/bin/env python3
"""
测试 Kimi Code 安装流程
"""

import sys
import os

# 确保项目根目录在 sys.path 中
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from src.providers.kimi import KimiProvider
from src.utils import get_platform

def main():
    print("=" * 60)
    print("Kimi Code 安装测试")
    print("=" * 60)
    print()

    # 检查平台
    platform = get_platform()
    print(f"当前平台 / Current platform: {platform}")

    # 获取安装 URL
    install_url = KimiProvider.get_install_url(platform)
    print(f"安装 URL / Install URL: {install_url}")

    # 检查是否已安装
    print()
    print("检查是否已安装 / Checking if already installed...")
    is_installed = KimiProvider.verify()
    if is_installed:
        print("  ✓ Kimi Code 已安装 / Already installed")
        return 0
    else:
        print("  ✗ Kimi Code 未安装 / Not installed")

    # 确认安装
    print()
    print("是否开始安装？ / Start installation?")
    print("测试模式 - 将显示安装命令但不执行 / Test mode - will show command without executing")
    print()
    choice = input("继续测试? / Continue test? [Y/n]: ")

    if choice.lower() in ('', 'y', 'yes'):
        print()
        print("=" * 60)
        print("模拟安装命令 / Simulated install command:")
        print("=" * 60)
        print()
        print(f"curl -fsSL '{install_url}' | bash")
        print()
        print("实际安装请运行 TUI 界面 / For actual install, run TUI")
        print("  python3 run.py")
        print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
