#!/usr/bin/env python3
"""
AI CLI 直接安装脚本
跳过 TUI，直接安装 Qwen Code
"""

import sys
import os

# 添加 src 到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

from src.providers import QwenProvider
from src.handoff import HandoffGuide


def main():
    """主安装函数"""

    print("\n" + "="*60)
    print("AI CLI Kickstarter - 直接安装")
    print("="*60 + "\n")

    provider = QwenProvider()

    print(f"准备安装: {provider.NAME}")
    print(f"Installing: {provider.NAME}\n")

    # 自动继续（非交互模式）
    # print("按回车键继续安装，或 Ctrl+C 取消")
    # print("Press Enter to continue, or Ctrl+C to cancel")
    # input()

    try:
        print(f"\n开始安装 {provider.NAME}...")
        print(f"Installing {provider.NAME}...\n")

        # 执行安装
        result = provider.install(mirror="mirror_cn")

        if result.success:
            print(f"\n✓ {provider.NAME} 安装成功！")
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
        else:
            print(f"\n✗ 安装失败:")
            print(f"   {result.stderr}")
            print(f"\n可能的原因:")
            print(f"  • 网络连接问题")
            print(f"  • 权限不足")
            print(f"  • 系统兼容性")

    except KeyboardInterrupt:
        print(f"\n\n安装已取消 / Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 安装异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "="*60)
    print("安装完成！")
    print("="*60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
