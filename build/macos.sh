#!/bin/bash
# macOS 打包脚本

set -e

echo "======================================"
echo "AI CLI Kickstarter - macOS 打包脚本"
echo "======================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}PyInstaller 未安装，正在安装...${NC}"
    pip3 install pyinstaller
fi

# 清理旧的构建
echo -e "${GREEN}[1/5] 清理旧的构建文件${NC}"
rm -rf build dist
echo "  ✓ 清理完成"

# 安装依赖
echo -e "${GREEN}[2/5] 安装项目依赖${NC}"
pip3 install -r requirements.txt --quiet
echo "  ✓ 依赖安装完成"

# 使用 PyInstaller 打包
echo -e "${GREEN}[3/5] 使用 PyInstaller 打包${NC}"
cd "$(dirname "$0")/.."
pyinstaller build/ai-cli-kickstarter.spec --clean --noconfirm
echo "  ✓ 打包完成"

# 检查打包结果
if [ -d "dist/ai-cli-kickstarter.app" ]; then
    echo -e "${GREEN}[4/5] .app 创建成功${NC}"
else
    echo -e "${RED}[4/5] 打包失败${NC}"
    exit 1
fi

echo -e "${GREEN}[5/5] 打包完成${NC}"

echo ""
echo -e "${GREEN}======================================"
echo "macOS 打包完成！"
echo "======================================${NC}"
echo ""
echo "产物："
echo "  • dist/ai-cli-kickstarter.app"
echo ""
echo "使用方法："
echo "  • 双击 .app 文件即可运行"
echo ""
