"""
国内镜像配置模块
包含所有 AI CLI 的国内镜像地址
"""

from typing import Literal, Optional


# 镜像源类型
MirrorType = Literal["official", "mirror_cn", "ghproxy", "kgithub"]

# Provider 类型
ProviderType = Literal["qwen", "kimi", "codebuddy"]

# 平台类型
PlatformType = Literal["macos", "linux", "windows"]


class MirrorConfig:
    """镜像配置"""

    # ==================== Qwen Code 镜像 ====================
    # Qwen 官方服务器在国内，无需镜像
    QWEN_URLS = {
        "macos": "https://qwenplus.ai/static/files/release/dist/latest/qwen_cli_install_pkg.sh",
        "linux": "https://qwenplus.ai/static/files/release/dist/latest/qwen_cli_install_pkg.sh",
        "windows": "https://qwenplus.ai/static/files/release/dist/latest/qwen_cli_install.exe"
    }

    # ==================== Kimi Code 镜像 ====================
    # Kimi 官方服务器在国内，无需镜像
    KIMI_URLS = {
        "macos": "https://kimi.moonshot.cn/download/client/mac",
        "linux": "https://kimi.moonshot.cn/download/client/linux",
        "windows": "https://kimi.moonshot.cn/download/client/win"
    }

    # ==================== CodeBuddy 镜像 ====================
    # CodeBuddy (腾讯) 官方服务器在国内，无需镜像
    CODEBUDDY_URLS = {
        "macos": "https://codebuddy.qq.com/install/mac",
        "linux": "https://codebuddy.qq.com/install/linux",
        "windows": "https://codebuddy.qq.com/install/win"
    }

    # ==================== PyPI 镜像 ====================
    PYPI_MIRRORS = {
        "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
        "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple",
        "douban": "https://pypi.douban.com/simple",
        "tencent": "https://mirrors.cloud.tencent.com/pypi/simple"
    }

    # ==================== GitHub 镜像 ====================
    # 用于加速 GitHub 资源访问
    GITHUB_PROXIES = {
        "ghproxy": "https://mirror.ghproxy.com/",
        "kgithub": "https://kgithub.com/",
        "fastgit": "https://hub.fastgit.xyz/",
        "moeyy": "https://gh.moeyy.xyz/"
    }

    @classmethod
    def get_install_url(cls, provider: ProviderType, platform: PlatformType = "macos",
                        mirror: MirrorType = "mirror_cn") -> str:
        """
        获取指定 Provider 的安装 URL

        Args:
            provider: Provider 类型 (qwen, kimi, codebuddy)
            platform: 平台类型 (macos, linux, windows)
            mirror: 镜像类型 (official, mirror_cn, ghproxy, kgithub)

        Returns:
            安装 URL

        注意：
        - Qwen, Kimi, CodeBuddy 的官方服务器都在国内
        - 对于国内用户，mirror_cn 和 official 都指向同一个国内地址
        - ghproxy, kgithub 仅适用于需要从 GitHub 下载的情况
        """
        # 获取基础 URL
        urls = {
            "qwen": cls.QWEN_URLS,
            "kimi": cls.KIMI_URLS,
            "codebuddy": cls.CODEBUDDY_URLS
        }

        provider_urls = urls.get(provider, {})
        base_url = provider_urls.get(platform)

        if not base_url:
            # 回退到 macOS
            base_url = provider_urls.get("macos", "")

        # 对于国内服务，official 和 mirror_cn 相同
        # 因为这些服务的官方服务器就在国内
        return base_url

    @classmethod
    def get_pypi_mirror(cls, mirror_name: str = "tsinghua") -> str:
        """
        获取 PyPI 镜像地址

        Args:
            mirror_name: 镜像名称 (aliyun, tsinghua, douban, tencent)

        Returns:
            PyPI 镜像 URL
        """
        return cls.PYPI_MIRRORS.get(mirror_name, cls.PYPI_MIRRORS["tsinghua"])

    @classmethod
    def get_github_proxy(cls, proxy_name: str = "kgithub") -> str:
        """
        获取 GitHub 代理地址

        Args:
            proxy_name: 代理名称 (ghproxy, kgithub, fastgit, moeyy)

        Returns:
            GitHub 代理前缀
        """
        return cls.GITHUB_PROXIES.get(proxy_name, cls.GITHUB_PROXIES["kgithub"])

    @classmethod
    def proxy_github_url(cls, github_url: str, proxy: str = "kgithub") -> str:
        """
        将 GitHub URL 转换为代理 URL

        Args:
            github_url: 原始 GitHub URL
            proxy: 代理名称

        Returns:
            代理后的 URL
        """
        proxy_base = cls.get_github_proxy(proxy)

        # 移除 https://github.com 前缀
        if github_url.startswith("https://github.com/"):
            path = github_url[len("https://github.com/"):]
            return f"{proxy_base}{path}"

        # 移除 https://raw.githubusercontent.com 前缀
        if github_url.startswith("https://raw.githubusercontent.com/"):
            path = github_url[len("https://raw.githubusercontent.com/"):]
            return f"{proxy_base}https://raw.githubusercontent.com/{path}"

        return github_url

    @classmethod
    def get_all_pypi_mirrors(cls) -> dict:
        """获取所有可用的 PyPI 镜像"""
        return cls.PYPI_MIRRORS.copy()

    @classmethod
    def get_all_github_proxies(cls) -> dict:
        """获取所有可用的 GitHub 代理"""
        return cls.GITHUB_PROXIES.copy()


def get_best_mirror(is_china: bool = True) -> MirrorType:
    """
    根据网络环境获取最佳镜像类型

    Args:
        is_china: 是否在国内网络环境

    Returns:
        推荐的镜像类型

    注意：对于 Qwen/Kimi/CodeBuddy，由于官方服务器在国内，
    无论 is_china 如何，都推荐使用 mirror_cn (即官方国内地址)
    """
    if is_china:
        # 国内用户使用国内镜像（官方国内地址）
        return "mirror_cn"
    else:
        # 海外用户使用官方源
        return "official"


def get_recommended_pypi_mirror(is_china: bool = True) -> Optional[str]:
    """
    获取推荐的 PyPI 镜像

    Args:
        is_china: 是否在国内

    Returns:
        推荐的镜像 URL
    """
    if is_china:
        # 国内推荐清华镜像
        return MirrorConfig.get_pypi_mirror("tsinghua")
    return None  # 海外使用官方源


# 测试代码
if __name__ == "__main__":
    # 测试获取安装 URL
    print("Qwen (macos, 国内):", MirrorConfig.get_install_url("qwen", "macos", "mirror_cn"))
    print("Kimi (linux, 国内):", MirrorConfig.get_install_url("kimi", "linux", "mirror_cn"))
    print("CodeBuddy (windows, 国内):", MirrorConfig.get_install_url("codebuddy", "windows", "mirror_cn"))

    # 测试 PyPI 镜像
    print("\nPyPI 镜像:")
    for name, url in MirrorConfig.get_all_pypi_mirrors().items():
        print(f"  {name}: {url}")
