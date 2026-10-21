"""
tools 包导出模块
================
统一导出所有工具函数，供 agent 层调用。
"""

from .search_tool import web_search
from .doc_reader import read_local_doc

__all__ = ["web_search", "read_local_doc"]
