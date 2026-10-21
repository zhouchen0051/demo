"""
全局配置管理
============
工业标准：所有配置从 .env 文件读取，代码里不硬编码任何敏感信息。
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Settings:
    """应用配置单例"""
    
    # LLM 配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # 搜索工具
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    
    # 应用配置
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    RECURSION_LIMIT: int = int(os.getenv("RECURSION_LIMIT", "50"))


# 全局配置实例
settings = Settings()
