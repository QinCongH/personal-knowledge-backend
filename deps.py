"""依赖注入。

集中注册 FastAPI 可调用的依赖项，各层通过 Depends() 获取，
避免在路由/服务中直接引用全局单例，便于测试替换。
"""

from collections.abc import Generator

from fastapi import Depends, Request

from config import Settings, get_settings

# 请求级生命周期（如需数据库 Session、Redis 等，在此注册）


def get_request_id(request: Request) -> str:
    """返回请求 ID（可替换为链路追踪实现）。"""
    return request.headers.get("X-Request-ID", "")


def get_db() -> Generator[None, None, None]:
    """数据库会话占位实现（业务接入时替换为真实 Session）。"""
    yield None


# 导出公共依赖，供路由层使用
def get_app_settings(request: Request) -> Settings:
    """便捷获取配置的依赖。"""
    return get_settings()
