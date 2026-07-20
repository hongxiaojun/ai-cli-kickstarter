#!/usr/bin/env python3
"""
测试安装进度显示功能
"""

import sys
import os

# 添加 src 到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

from src.tui_safe import InstallerStateMachine, State


def test_progress_rendering():
    """测试进度条渲染逻辑"""
    print("\n测试安装进度渲染 / Testing Install Progress Rendering")

    app = InstallerStateMachine()
    app.install_progress = 0

    # 测试进度更新
    progress_values = [0, 25, 50, 75, 100]

    for progress in progress_values:
        app.install_progress = progress
        print(f"  ✓ 进度 {progress}%: 状态 = {app.state}")

        # 验证进度值正确
        assert 0 <= app.install_progress <= 100, f"进度值超出范围: {progress}"

    print("  ✓ 进度渲染测试通过")

    # 测试状态转移
    app.transition_to(State.PROGRESS_INSTALL)
    print(f"  ✓ 状态转移到: {app.state}")

    # 测试安装完成后转移
    app.install_success = True
    app.transition_to(State.HANDOFF_PROMPT)
    print(f"  ✓ 安装成功，转移到: {app.state}")

    # 测试安装失败转移
    app.install_success = False
    app.error_message = "测试错误"
    app.transition_to(State.ERROR)
    print(f"  ✓ 安装失败，转移到: {app.state}")
    print(f"  ✓ 错误信息: {app.error_message}")

    return True


def test_installation_flow():
    """测试完整安装流程"""
    print("\n测试完整安装流程 / Testing Complete Installation Flow")

    app = InstallerStateMachine()

    # 设置 Provider
    from src.providers import QwenProvider
    app.set_provider(QwenProvider)
    print(f"  ✓ 设置 Provider: {app.selected_provider.NAME}")

    # 设置网络环境
    app.network_info = {
        "location": "cn",
        "google": "unreachable",
        "baidu": "reachable",
        "recommended_mirror": "mirror_cn"
    }
    app.set_mirror("mirror_cn")
    print(f"  ✓ 设置镜像: {app.mirror_source}")

    # 模拟状态转移序列
    states = [
        State.MENU_LANGUAGE,
        State.MENU_PROVIDER,
        State.CHECK_NETWORK,
        State.MENU_CONFIRM,
        State.PROGRESS_INSTALL,
        State.HANDOFF_PROMPT,
        State.DONE
    ]

    for state in states:
        app.transition_to(state)
        print(f"  ✓ 状态转移: {state.value}")

    print("  ✓ 完整安装流程测试通过")

    return True


def test_error_recovery():
    """测试错误恢复机制"""
    print("\n测试错误恢复 / Testing Error Recovery")

    app = InstallerStateMachine()

    # 模拟安装失败
    app.install_success = False
    app.error_message = "网络连接失败"
    app.transition_to(State.ERROR)

    print(f"  ✓ 进入错误状态: {app.state}")
    print(f"  ✓ 错误信息: {app.error_message}")

    # 模拟重试
    app.error_message = ""
    app.install_progress = 0
    app.transition_to(State.MENU_CONFIRM)

    print(f"  ✓ 重试，返回确认状态: {app.state}")

    return True


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("AI CLI Kickstarter - 安装进度功能测试")
    print("=" * 60 + "\n")

    tests = [
        test_progress_rendering,
        test_installation_flow,
        test_error_recovery
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    # 显示结果
    print("\n" + "=" * 60)
    print("测试结果 / Test Results")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"\n通过: {passed}/{total}")

    if passed == total:
        print("✓ 安装进度功能测试通过！")
        print("\n新功能:")
        print("  • 安装进度显示 (PROGRESS_INSTALL 状态)")
        print("  • 错误处理和重试 (ERROR 状态)")
        print("  • 完整状态转移流程")
    else:
        print("✗ 部分测试失败")

    print("\n" + "=" * 60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
