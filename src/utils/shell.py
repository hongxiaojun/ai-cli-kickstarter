"""
跨平台 shell 命令执行工具
"""

import subprocess
import sys
import os
from typing import Optional, Tuple


class ShellResult:
    """Shell 命令执行结果"""
    def __init__(self, stdout: str, stderr: str, returncode: int):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    @property
    def success(self) -> bool:
        return self.returncode == 0


def run_command(
    cmd: list,
    timeout: Optional[int] = None,
    capture: bool = True
) -> ShellResult:
    """
    执行 shell 命令（跨平台）

    Args:
        cmd: 命令列表，如 ['ls', '-la']
        timeout: 超时时间（秒）
        capture: 是否捕获输出

    Returns:
        ShellResult 对象
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            shell=sys.platform == "win32"
        )
        return ShellResult(
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            returncode=result.returncode
        )
    except subprocess.TimeoutExpired:
        return ShellResult("", "Command timeout", -1)
    except Exception as e:
        return ShellResult("", str(e), -1)


def run_shell_script(script: str) -> ShellResult:
    """
    执行 shell 脚本内容

    Args:
        script: 脚本内容

    Returns:
        ShellResult 对象
    """
    try:
        result = subprocess.run(
            script,
            shell=True,
            capture_output=True,
            text=True,
            executable='/bin/bash' if sys.platform != 'win32' else None
        )
        return ShellResult(
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            returncode=result.returncode
        )
    except Exception as e:
        return ShellResult("", str(e), -1)


def check_command_exists(command: str) -> bool:
    """
    检查命令是否存在

    Args:
        command: 命令名称

    Returns:
        bool: 命令是否存在
    """
    result = run_command(
        ["where" if sys.platform == "win32" else "which", command],
        timeout=5
    )
    return result.success and command.lower() in result.stdout.lower()


def get_platform() -> str:
    """
    获取当前平台标识

    Returns:
        'windows', 'macos', 或 'linux'
    """
    if sys.platform == "darwin":
        return "macos"
    elif sys.platform.startswith("linux"):
        return "linux"
    elif sys.platform == "win32" or sys.platform == "win64":
        return "windows"
    else:
        return "unknown"


def is_admin() -> bool:
    """
    检查是否有管理员权限

    Returns:
        bool: 是否有管理员权限
    """
    try:
        if sys.platform == "win32":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False
