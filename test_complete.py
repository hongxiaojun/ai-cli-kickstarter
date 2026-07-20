#!/usr/bin/env python3
"""
AI CLI Kickstarter - 完整测试脚本
测试从安装到使用 AI CLI 的完整流程
"""

import sys
import os
import subprocess
import time

# 添加 src 到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)


def print_header():
    """打印标题"""
    print("\n" + "=" * 60)
    print("AI CLI Kickstarter - 完整流程测试")
    print("=" * 60 + "\n")


def test_environment():
    """测试环境检测"""
    print("[1/6] 测试环境检测 / Testing Environment Check")

    # Python 版本
    print(f"  Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    # curses
    try:
        import curses
        print("  ✓ curses 可用 / curses available")
    except ImportError:
        print("  ✗ curses 不可用 / curses not available")
        return False

    # curl
    try:
        result = subprocess.run(
            ["which", "curl"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("  ✓ curl 可用 / curl available")
    except:
        print("  ✗ curl 不可用 / curl not available")

    return True


def test_tui_flow():
    """测试 TUI 流程（不实际启动 curses）"""
    print("\n[2/6] 测试 TUI 状态机 / Testing TUI State Machine")

    try:
        from src.tui_safe import InstallerStateMachine, State

        app = InstallerStateMachine()
        print("  ✓ 状态机创建成功")

        # 测试状态转移
        app.transition_to(State.MENU_LANGUAGE)
        print(f"  ✓ 状态转移: {app.state}")

        # 测试 Provider 选择
        from src.providers import QwenProvider, KimiProvider
        app.set_provider(KimiProvider)
        print(f"  ✓ Provider 设置: {app.selected_provider.NAME}")

        return True
    except Exception as e:
        print(f"  ✗ TUI 测试失败: {e}")
        return False


def test_handoff_guide():
    """测试交接指南生成"""
    print("\n[3/6] 测试交接指南 / Testing Handoff Guide")

    try:
        from src.handoff import HandoffGuide, AITester

        # 创建指南
        guide = HandoffGuide("Qwen Code", "qwen")
        print("  ✓ HandoffGuide 创建成功")

        # 测试快速参考生成
        ref_content = guide.format_handoff_text()
        print(f"  ✓ 指南内容生成: {len(ref_content)} 字符")

        # 保存到临时文件测试
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_file = f.name
            f.write(ref_content)

        print(f"  ✓ 临时文件保存: {temp_file}")
        os.unlink(temp_file)

        return True
    except Exception as e:
        print(f"  ✗ 交接指南测试失败: {e}")
        return False


def test_provider_verification():
    """测试 Provider 验证（模拟）"""
    print("\n[4/6] 测试 Provider 验证 / Testing Provider Verification")

    try:
        from src.providers import QwenProvider

        provider = QwenProvider()
        print(f"  ✓ Provider: {provider.NAME}")
        print(f"  ✓ 命令: {provider.get_command_name()}")
        print(f"  ✓ URL: {provider.get_install_url()[:50]}...")

        # 模拟验证（不实际安装）
        print("  ⚠ 实际安装验证需要用户交互")

        return True
    except Exception as e:
        print(f"  ✗ Provider 测试失败: {e}")
        return False


def test_mirror_config():
    """测试镜像配置"""
    print("\n[5/6] 测试镜像配置 / Testing Mirror Configuration")

    try:
        from src.mirrors import MirrorConfig, get_best_mirror

        # 测试 URL 获取
        url = MirrorConfig.get_install_url("qwen", "macos", "mirror_cn")
        print(f"  ✓ Qwen URL: {url[:50]}...")

        # 测试最佳镜像
        best = get_best_mirror(is_china=True)
        print(f"  ✓ 国内最佳镜像: {best}")

        best = get_best_mirror(is_china=False)
        print(f"  ✓ 海外最佳镜像: {best}")

        return True
    except Exception as e:
        print(f"  ✗ 镜像配置测试失败: {e}")
        return False


def test_complete_simulation():
    """模拟完整流程"""
    print("\n[6/6] 模拟完整流程 / Simulating Complete Flow")

    try:
        from src.tui_safe import InstallerStateMachine, State
        from src.handoff import HandoffGuide
        from src.providers import QwenProvider

        print("  1. 创建状态机...")
        app = InstallerStateMachine()

        print("  2. 设置网络环境（国内）...")
        app.network_info = {
            "location": "cn",
            "google": "unreachable",
            "baidu": "reachable",
            "recommended_mirror": "mirror_cn"
        }
        app.set_mirror("mirror_cn")

        print("  3. 选择 Provider...")
        app.set_provider(QwenProvider)
        app.transition_to(State.MENU_LANGUAGE)

        print("  4. 模拟安装成功...")
        app.install_success = True

        print("  5. 生成交接指南...")
        guide = HandoffGuide(
            app.selected_provider.NAME,
            app.selected_provider.get_command_name()
        )

        print("  6. 保存指南...")
        import tempfile
        temp_file = tempfile.mktemp(suffix='.txt')
        guide.save_to_file(temp_file)

        print("  7. 读取并显示关键内容...")
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            print("     指南行数:", len(lines))
            print("     包含 '下一步':", '下一步' in content)

        os.unlink(temp_file)

        print("  ✓ 完整流程模拟成功")
        return True

    except Exception as e:
        print(f"  ✗ 流程模拟失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print_header()

    tests = [
        test_environment,
        test_tui_flow,
        test_handoff_guide,
        test_provider_verification,
        test_mirror_config,
        test_complete_simulation
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ 测试异常: {e}")
            results.append(False)

    # 显示结果
    print("\n" + "=" * 60)
    print("测试结果 / Test Results")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"\n通过: {passed}/{total}")

    if passed == total:
        print("✓ 所有测试通过！/ All tests passed!")
        print("\n下一步 / Next Steps:")
        print("1. 运行实际安装: python3 run.py")
        print("2. 测试 AI CLI 功能")
        print("3. 验证创建文件夹等操作")
    else:
        print("✗ 部分测试失败，请检查错误信息")

    print("\n" + "=" * 60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
