@echo off
REM Windows 打包脚本

echo ======================================
echo AI CLI Kickstarter - Windows 打包脚本
echo ======================================
echo.

REM 检查 PyInstaller
python -c "import PyInstaller" 2>/dev/null
if errorlevel 1 (
    echo [1/4] 安装 PyInstaller...
    pip install pyinstaller
) else (
    echo [1/4] PyInstaller 已安装
)

REM 清理旧的构建
echo [2/4] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo   清理完成

REM 安装依赖
echo [3/4] 安装项目依赖...
pip install -r requirements.txt --quiet
echo   依赖安装完成

REM 使用 PyInstaller 打包
echo [4/4] 使用 PyInstaller 打包...
cd /d %~dp0..
pyinstaller build/ai-cli-kickstarter.spec --clean --noconfirm
echo   打包完成

echo.
echo ======================================
echo Windows 打包完成！
echo ======================================
echo.
echo 产物：
echo   • dist\ai-cli-kickstarter.exe
echo.
echo 使用方法：
echo   • 双击 .exe 文件即可运行
echo.

pause
