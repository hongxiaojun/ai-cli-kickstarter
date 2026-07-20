"""
CodeBuddy CLI Provider (腾讯)
"""

from typing import Literal
from ..utils import run_command, get_platform, ShellResult


class CodeBuddyProvider:
    """CodeBuddy CLI 安装器 (腾讯生态)"""

    NAME = "CodeBuddy CLI"
    COMMAND = "codebuddy"
    DESCRIPTION = {
        "zh": "腾讯 CodeBuddy，Beta 版本，原生安装器",
        "en": "Tencent CodeBuddy, Beta version, native installer"
    }

    # 官方安装 URL (通过 npm 安装)
    INSTALL_URLS = {
        "macos": "npm install -g @tencent-ai/codebuddy-code",
        "linux": "npm install -g @tencent-ai/codebuddy-code",
        "windows": "npm install -g @tencent-ai/codebuddy-code"
    }

    @classmethod
    def get_install_url(cls, platform: str = None) -> str:
        """获取安装 URL"""
        if platform is None:
            platform = get_platform()
        return cls.INSTALL_URLS.get(platform, cls.INSTALL_URLS["macos"])

    @classmethod
    def install(cls, mirror: Literal["official", "mirror_cn"] = "official") -> ShellResult:
        """
        执行安装

        Args:
            mirror: 是否使用镜像

        Returns:
            ShellResult
        """
        # 检查 npm 是否可用
        npm_check = run_command(["which", "npm"], timeout=5)
        if not npm_check.success:
            return ShellResult("", "npm 未安装，请先安装 Node.js 和 npm", 1)

        # macOS/Linux 需要 sudo 安装全局包
        if get_platform() in ["macos", "linux"]:
            return run_command([
                "sudo", "npm", "install", "-g",
                "@tencent-ai/codebuddy-code"
            ], timeout=180)
        else:
            # Windows
            return run_command([
                "npm", "install", "-g",
                "@tencent-ai/codebuddy-code"
            ], timeout=180)

    @classmethod
    def verify(cls) -> bool:
        """
        验证安装是否成功

        Returns:
            bool: 是否安装成功
        """
        result = run_command([cls.COMMAND, "--version"], timeout=10)
        return result.success

    @classmethod
    def get_command_name(cls) -> str:
        """获取命令名称"""
        return cls.COMMAND
