"""v1 路由：纯路由层。

只做协议处理（请求校验 + SSE 包装），不含业务逻辑。
"""

from fastapi import APIRouter

from api.v1 import health

router = APIRouter()
router.include_router(health.router)