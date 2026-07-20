"""
网络检测与镜像切换模块
"""

import urllib.request
import socket
from typing import Literal, Optional
from .utils import get_platform


# 定义网络状态类型
NetworkStatus = Literal["reachable", "unreachable", "unknown"]
MirrorSource = Literal["official", "mirror_cn"]


class NetworkDetector:
    """网络环境检测器"""

    # 测试端点
    GOOGLE_ENDPOINT = "https://www.google.com/generate_204"
    BAIDU_ENDPOINT = "https://www.baidu.com"

    # 超时设置
    TIMEOUT_CONNECTION = 4  # 连接超时
    TIMEOUT_TOTAL = 7  # 总超时

    @classmethod
    def check_google(cls) -> NetworkStatus:
        """
        检查 Google 连通性

        Returns:
            "reachable", "unreachable", 或 "unknown"
        """
        try:
            response = urllib.request.urlopen(
                cls.GOOGLE_ENDPOINT,
                timeout=cls.TIMEOUT_TOTAL
            )
            if response.status == 204:
                return "reachable"
        except urllib.error.HTTPError:
            # 连接成功但返回非204状态
            return "reachable"
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                return "unreachable"
            return "unreachable"
        except Exception:
            return "unknown"

        return "unknown"

    @classmethod
    def check_baidu(cls) -> NetworkStatus:
        """
        检查百度连通性（用于判断是否在国内）

        Returns:
            "reachable", "unreachable", 或 "unknown"
        """
        try:
            response = urllib.request.urlopen(
                cls.BAIDU_ENDPOINT,
                timeout=cls.TIMEOUT_TOTAL
            )
            if response.status == 200:
                return "reachable"
        except:
            return "unreachable"

        return "unknown"

    @classmethod
    def detect_environment(cls) -> dict:
        """
        综合检测网络环境

        Returns:
            {
                "google": NetworkStatus,
                "baidu": NetworkStatus,
                "location": "cn" | "overseas" | "unknown",
                "recommended_mirror": MirrorSource
            }
        """
        google_status = cls.check_google()
        baidu_status = cls.check_baidu()

        # 判断地理位置
        if baidu_status == "reachable" and google_status != "reachable":
            location = "cn"
        elif google_status == "reachable":
            location = "overseas"
        else:
            location = "unknown"

        # 推荐镜像源
        recommended_mirror: MirrorSource = "mirror_cn" if location == "cn" else "official"

        return {
            "google": google_status,
            "baidu": baidu_status,
            "location": location,
            "recommended_mirror": recommended_mirror
        }


def get_install_url(provider: str, mirror: MirrorSource) -> str:
    """
    根据提供商和镜像类型获取安装 URL

    Args:
        provider: "qwen", "kimi", 或 "codebuddy"
        mirror: "official" 或 "mirror_cn"

    Returns:
        安装脚本 URL
    """
    urls = {
        "qwen": {
            "official": "https://qwenplus.ai/static/files/release/dist/20250125/qwen_client_darwin_x64/qwen_cli_install_pkg.sh",
            "mirror_cn": "https://qwenplus.ai/static/files/release/dist/20250125/qwen_client_darwin_x64/qwen_cli_install_pkg.sh"  # 例子，实际需确认
        },
        "kimi": {
            "official": "https://kimi.moonshot.cn/download/client",
            "mirror_cn": "https://kimi.moonshot.cn/download/client"
        },
        "codebuddy": {
            "official": "https://codebuddy.qq.com/install",
            "mirror_cn": "https://codebuddy.qq.com/install"
        }
    }

    return urls.get(provider, {}).get(mirror, urls[provider]["official"])


def format_network_status(status: NetworkStatus, lang: str = "zh") -> str:
    """
    格式化网络状态显示

    Args:
        status: 网络状态
        lang: 语言 ("zh" 或 "en")

    Returns:
        格式化的状态文本
    """
    if lang == "zh":
        return {
            "reachable": "✓ 可访问",
            "unreachable": "✗ 不可访问",
            "unknown": "? 未知"
        }.get(status, status)
    else:
        return {
            "reachable": "✓ Reachable",
            "unreachable": "✗ Unreachable",
            "unknown": "? Unknown"
        }.get(status, status)
