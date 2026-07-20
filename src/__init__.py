"""
AI CLI Kickstarter - Product Edition
开箱即用的 AI CLI 安装器

Cross-platform installer with TUI interface for:
- Qwen Code
- Kimi Code
- CodeBuddy CLI
"""

__version__ = "1.0.0"
__author__ = "xiaolai"

# Export main components
from .launcher import main
from .tui_core import InstallerStateMachine

__all__ = ["main", "InstallerStateMachine"]
