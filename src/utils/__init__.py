"""工具模块"""

from .shell import (
    run_command,
    run_shell_script,
    check_command_exists,
    get_platform,
    is_admin,
    ShellResult
)

__all__ = [
    "run_command",
    "run_shell_script",
    "check_command_exists",
    "get_platform",
    "is_admin",
    "ShellResult"
]
