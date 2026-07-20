#!/usr/bin/env python3
"""
直接测试 Kimi Code 安装（绕过 TUI）
"""

import sys
import os
import subprocess

# 确保项目根目录在 sys.path 中
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from src.providers.kimi import KimiProvider
from src.utils import get_platform

def print_step(step: int, total: int, message: str):
    """打印进度步骤"""
    print(f"[{step}/{total}] {message}...")

def print_ok(message: str = "✓"):
    """打印成功消息"""
    print(f"  {message}")

def print_error(message: str):
    """打印错误消息"""
    print(f"  ✗ {message}")

def main():
    print("=" * 60)
    print("Kimi Code 直接安装测试")
    print("Direct Installation Test")
    print("=" * 60)
    print()

    # 1. 检查平台
    print_step(1, 5, "检查平台 / Checking platform")
    platform = get_platform()
    print_ok(f"Platform: {platform}")
    print()

    # 2. 获取安装 URL
    print_step(2, 5, "获取安装 URL / Getting install URL")
    install_url = KimiProvider.get_install_url(platform)
    print_ok(f"URL: {install_url}")
    print()

    # 3. 检查是否已安装
    print_step(3, 5, "检查是否已安装 / Checking if installed")
    is_installed = KimiProvider.verify()
    if is_installed:
        print_ok("Kimi Code 已安装 / Already installed")
        print()
        print("尝试验证版本 / Verifying version:")
        result = subprocess.run([KimiProvider.COMMAND, "--version"], capture_output=True, text=True, timeout=10)
        if result.success:
            print(f"  {result.stdout.strip()}")
        return 0
    else:
        print_error("Kimi Code 未安装 / Not installed")
    print()

    # 4. 确认安装
    print_step(4, 5, "准备安装 / Preparing installation")
    print()
    print("⚠️  警告 / Warning:")
    print("   将执行以下命令 / Will execute the following command:")
    print(f"   curl -fsSL '{install_url}' | bash")
    print()
    print("   这将下载并安装 Kimi Code 到您的系统")
    print("   This will download and install Kimi Code to your system")
    print()

    choice = input("继续安装? / Continue installation? [Y/n]: ")

    if choice.lower() not in ('', 'y', 'yes'):
        print()
        print_error("安装已取消 / Installation cancelled")
        return 1

    # 5. 执行安装
    print()
    print_step(5, 5, "正在安装 / Installing")
    print()
    print("=" * 60)
    print("开始安装 / Starting installation")
    print("=" * 60)
    print()

    try:
        result = KimiProvider.install(mirror="mirror_cn")

        if result.success:
            print()
            print("=" * 60)
            print_ok("安装成功！/ Installation successful!")
            print("=" * 60)
            print()

            # 验证安装
            if KimiProvider.verify():
                print_ok("安装验证通过 / Installation verified")
            else:
                print_error("安装可能未成功，请手动验证")
                print_error("Try running: kimi")

            print()
            print("下一步 / Next steps:")
            print("1. 在新终端输入: kimi")
            print("2. 首次使用需要登录: /login")
            print()

        else:
            print()
            print("=" * 60)
            print_error("安装失败 / Installation failed")
            print("=" * 60)
            print()
            print(f"错误 / Error: {result.stderr}")
            return 1

    except Exception as e:
        print()
        print_error(f"安装异常 / Installation error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print()
        print("用户中断 / User interrupted")
        sys.exit(1)
