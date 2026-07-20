#!/usr/bin/env python3
"""
AI CLI 直接安装脚本
支持选择安装 Qwen, Kimi, 或 CodeBuddy
"""

import sys
import os
import subprocess

# 添加 src 到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

from src.providers import QwenProvider, KimiProvider, CodeBuddyProvider
from src.handoff import HandoffGuide


def main():
    """主安装函数"""

    print("\n" + "="*60)
    print("AI CLI Kickstarter - 直接安装")
    print("="*60 + "\n")

    print("选择要安装的 AI CLI / Select AI CLI to install:")
    print("1. Qwen Code (通义千问) - 无需额外权限")
    print("2. Kimi Code (月之暗面) - 无需额外权限")
    print("3. CodeBuddy CLI (腾讯) - 需要 sudo 权限\n")

    choice = input("请选择 / Please select (1-3, 默认=1): ").strip() or "1"

    providers = {
        "1": (QwenProvider, "Qwen Code"),
        "2": (KimiProvider, "Kimi Code"),
        "3": (CodeBuddyProvider, "CodeBuddy CLI")
    }

    if choice not in providers:
        print("无效选择，默认安装 Qwen Code")
        choice = "1"

    provider_class, provider_name = providers[choice]
    provider = provider_class()

    print(f"\n准备安装: {provider_name}")
    print(f"Installing: {provider_name}\n")

    # CodeBuddy 需要 sudo 提示
    if choice == "3":
        print("⚠️ 注意: CodeBuddy CLI 需要 sudo 权限安装")
        print("   Attention: CodeBuddy CLI requires sudo for installation\n")

    try:
        print(f"开始安装 {provider_name}...")
        print(f"Installing {provider_name}...\n")

        # 执行安装
        result = provider.install(mirror="mirror_cn")

        if result.success:
            print(f"\n✓ {provider_name} 安装成功！")
            print(f"✓ Installation successful!\n")

            # 验证安装
            if provider.verify():
                print(f"✓ 安装验证通过 - 命令 '{provider.get_command_name()}' 可用")
                print(f"✓ Installation verified\n")

                # 生成交接指南
                guide = HandoffGuide(provider.NAME, provider.get_command_name())

                guide_file = guide.save_to_file()
                ref_file = guide.create_quick_reference()

                print(f"✓ 使用指南已保存到桌面")
                print(f"✓ Guide saved to desktop\n")

                # 显示使用规则
                print("="*60)
                print("使用规则 / Usage Rules")
                print("="*60)
                print(guide.BASIC_RULES)

                # 显示下一步
                print("="*60)
                print("下一步 / Next Steps:")
                print("="*60)
                print(f"\n1. 在新终端窗口中输入: {provider.get_command_name()}")
                print(f"   Launch AI CLI: {provider.get_command_name()}")
                print(f"\n2. 复制上述使用规则，在 AI CLI 中粘贴")
                print(f"   Copy the rules above and paste in AI CLI")
                print(f"\n3. 尝试测试命令: '帮我在桌面创建一个测试文件夹'")
                print(f"   Try test: '帮我在桌面创建一个测试文件夹'\n")

            else:
                print(f"⚠️ 安装可能未成功，请手动验证")
                print(f"   请在新终端输入: {provider.get_command_name()}")
                print(f"   If using CodeBuddy, try: sudo npm install -g @tencent-ai/codebuddy-code")
        else:
            print(f"\n✗ 安装失败:")
            print(f"   {result.stderr}")
            print(f"\n可能的原因:")
            print(f"  • 网络连接问题")
            print(f"  • CodeBuddy 需要 Node.js 和 npm")
            print(f"  • CodeBuddy 需要 sudo 权限")

    except KeyboardInterrupt:
        print(f"\n\n安装已取消 / Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 安装异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "="*60)
    print("按回车键退出 / Press Enter to exit")
    print("="*60)
    input()

    return 0


if __name__ == "__main__":
    sys.exit(main())
