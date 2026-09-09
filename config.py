"""应用配置。

通过环境变量 / .env 文件加载，所有配置项集中在 Settings 上，
供 deps.py 及各层通过依赖注入获取。
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 应用基础信息
    app_name: str = "personal-knowledge-backend"
    app_version: str = "0.1.0"
    debug: bool = False

    # 服务监听
    host: str = "0.0.0.0"
    port: int = 8000

    # 数据库
    database_url: str = "sqlite:///./personal_knowledge.db"


@lru_cache
def get_settings() -> Settings:
    """返回单例配置（供 FastAPI 依赖注入使用）。"""
    return Settings()


settings = get_settings()
