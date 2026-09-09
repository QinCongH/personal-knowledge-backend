"""v1 健康检查 / 占位接口。

纯路由层：仅做协议处理，业务编排交由 services 层。
"""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from config import Settings
from deps import get_app_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: Settings = Depends(get_app_settings)) -> dict:
    """健康检查。"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }

