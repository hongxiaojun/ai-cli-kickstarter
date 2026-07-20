#!/bin/bash
# Linux 打包脚本

set -e

echo "======================================"
echo "AI CLI Kickstarter - Linux 打包脚本"
echo "======================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}PyInstaller 未安装，正在安装...${NC}"
    pip3 install pyinstaller
fi

# 清理旧的构建
echo -e "${GREEN}[1/4] 清理旧的构建文件${NC}"
rm -rf build dist
echo "  ✓ 清理完成"

# 安装依赖
echo -e "${GREEN}[2/4] 安装项目依赖${NC}"
pip3 install -r requirements.txt --quiet
echo "  ✓ 依赖安装完成"

# 使用 PyInstaller 打包
echo -e "${GREEN}[3/4] 使用 PyInstaller 打包${NC}"
cd "$(dirname "$0")/.."
pyinstaller build/ai-cli-kickstarter.spec --clean --noconfirm
echo "  ✓ 打包完成"

# 检查打包结果
if [ -f "dist/ai-cli-kickstarter/ai-cli-kickstarter" ]; then
    echo -e "${GREEN}[4/4] 可执行文件创建成功${NC}"
else
    echo -e "${RED}[4/4] 打包失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}======================================"
echo "Linux 打包完成！"
echo "======================================${NC}"
echo ""
echo "产物："
echo "  • dist/ai-cli-kickstarter/ai-cli-kickstarter"
echo ""
echo "使用方法："
echo "  • chmod +x dist/ai-cli-kickstarter/ai-cli-kickstarter"
echo "  • ./dist/ai-cli-kickstarter/ai-cli-kickstarter"
echo ""

# 可选：创建 AppImage
echo -e "${YELLOW}是否创建 AppImage？(y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    if command -v appimagetool &> /dev/null; then
        echo "创建 AppImage..."
        # AppImage 创建逻辑
        echo "需要安装 appimagetool"
    else
        echo "appimagetool 未安装"
    fi
fi

echo ""
