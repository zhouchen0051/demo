"""
结构化日志工具
==============
统一日志格式，支持文件输出和控制台输出。
"""
import logging
import sys
from config import settings


def setup_logger(name: str = "multi-agent") -> logging.Logger:
    """
    创建并配置logger实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 控制台输出格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# 全局logger实例（这一行不能丢！！）
logger = setup_logger()
