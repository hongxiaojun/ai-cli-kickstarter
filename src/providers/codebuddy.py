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

    # 官方安装 URL (当前标注 Beta)
    INSTALL_URLS = {
        "macos": "https://codebuddy.qq.com/install/mac",
        "linux": "https://codebuddy.qq.com/install/linux",
        "windows": "https://codebuddy.qq.com/install/win"
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
        url = cls.get_install_url()
        platform = get_platform()

        if platform == "windows":
            return run_command(["powershell", "-c",
                f"Invoke-WebRequest -Uri '{url}' -OutFile 'codebuddy-installer.exe'; "
                f"Start-Process -FilePath '.\\codebuddy-installer.exe' -Wait"
            ], timeout=120)
        else:
            return run_command([
                "bash", "-c",
                f"curl -fsSL '{url}' | bash"
            ], timeout=120)

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
