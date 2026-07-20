"""
Kimi Code Provider
"""

from typing import Literal
from ..utils import run_command, get_platform, ShellResult


class KimiProvider:
    """Kimi Code 安装器 (月之暗面)"""

    NAME = "Kimi Code"
    COMMAND = "kimi"
    DESCRIPTION = {
        "zh": "月之暗面 Kimi，国内友好，首次启动需 /login",
        "en": "Kimi Code, China-friendly, requires /login on first launch"
    }

    # 官方安装 URL (Kimi Code 新版安装器)
    INSTALL_URLS = {
        "macos": "https://code.kimi.com/kimi-code/install.sh",
        "linux": "https://code.kimi.com/kimi-code/install.sh",
        "windows": "https://code.kimi.com/kimi-code/install.sh"
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
            # Windows: Kimi 通常提供 GUI 安装包
            return run_command(["powershell", "-c",
                f"Invoke-WebRequest -Uri '{url}' -OutFile 'kimi-installer.exe'; "
                f"Start-Process -FilePath '.\\kimi-installer.exe' -Wait"
            ], timeout=120)
        else:
            # macOS/Linux: 使用官方安装脚本
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
