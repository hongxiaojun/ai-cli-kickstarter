#!/bin/bash
# 一键打包脚本 - 自动检测平台并打包

echo "========================================"
echo "AI CLI Kickstarter - 一键打包"
echo "========================================"
echo ""

# 检测平台
PLATFORM=$(uname -s)

case "$PLATFORM" in
    Darwin*)
        echo "检测到 macOS 平台"
        exec bash build/macos.sh
        ;;
    Linux*)
        echo "检测到 Linux 平台"
        exec bash build/linux.sh
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "检测到 Windows 平台"
        exec cmd //c build\\windows.bat
        ;;
    *)
        echo "未知平台: $PLATFORM"
        echo "请手动运行对应平台的打包脚本"
        exit 1
        ;;
esac
