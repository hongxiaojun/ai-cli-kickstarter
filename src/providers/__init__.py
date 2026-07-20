"""
AI CLI Provider 安装逻辑
"""

from .qwen import QwenProvider
from .kimi import KimiProvider
from .codebuddy import CodeBuddyProvider

__all__ = ["QwenProvider", "KimiProvider", "CodeBuddyProvider"]
