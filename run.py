#!/usr/bin/env python3
"""
本地测试运行脚本
不需要打包即可测试 TUI 界面
"""

import sys
import os

# 添加 src 到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

if __name__ == "__main__":
    # 检查 Python 版本
    if sys.version_info < (3, 7):
        print("错误：需要 Python 3.7 或更高版本")
        sys.exit(1)

    # 运行启动器
    try:
        from src.launcher import main
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断 / User interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"错误 / Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
