"""
Qwen Code Provider
"""

from typing import Literal
from ..utils import run_command, get_platform, ShellResult


class QwenProvider:
    """通义千问 Qwen Code 安装器"""

    NAME = "Qwen Code"
    COMMAND = "qwen"
    DESCRIPTION = {
        "zh": "通义千问代码版，国内友好，独立安装器",
        "en": "Qwen Code, China-friendly, standalone installer"
    }

    # 官方安装 URL（使用阿里云 OSS 镜像，国内访问更稳定）
    INSTALL_URLS = {
        "macos": "https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.sh",
        "linux": "https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.sh",
        "windows": "https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.exe"
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
            # Windows: 下载并运行 .exe
            return run_command(["powershell", "-c",
                f"Invoke-WebRequest -Uri '{url}' -OutFile 'qwen-installer.exe'; "
                f"Start-Process -FilePath '.\\qwen-installer.exe' -Wait"
            ], timeout=120)
        else:
            # macOS/Linux: 下载并运行 shell 脚本
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
