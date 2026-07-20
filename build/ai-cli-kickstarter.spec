# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller 配置文件
用于打包 AI CLI Kickstarter 为独立可执行文件
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# 基础配置
block_cipher = None
name = 'ai-cli-kickstarter'

# 平台特定配置
if sys.platform == 'darwin':
    # macOS
    exe_extension = '.app'
    icon = 'assets/icon.icns' if True else None
elif sys.platform == 'win32':
    # Windows
    exe_extension = '.exe'
    icon = 'assets/icon.ico' if True else None
else:
    # Linux
    exe_extension = ''
    icon = None

# 收集所有数据文件
datas = []

# 收集源代码模块
datas += [('src', 'src')]

# 隐藏导入（可能需要动态导入的模块）
hiddenimports = [
    'curses',
    'urllib3',
    'requests',
]

# 分析配置
a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 过滤不需要的文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 可执行文件配置
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 保持控制台可见
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)

# 收集所有文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name,
)

# macOS .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name=name + '.app',
        icon=icon if icon else None,
        bundle_identifier='com.hongxiaojun.ai-cli-kickstarter',
        info_plist={
            'CFBundleName': 'AI CLI Kickstarter',
            'CFBundleDisplayName': 'AI CLI Kickstarter',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
        },
    )
