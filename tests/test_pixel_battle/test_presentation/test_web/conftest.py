
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient
from httpx_ws.transport import ASGIWebSocketTransport
from pytest import fixture

from pixel_battle.presentation.web.routes.healthcheck import (
    router as healthcheck_router,
)
from pixel_battle.presentation.web.routes.recolor_pixel import (
    router as recolor_pixel_router,
)
from pixel_battle.presentation.web.routes.register_user import (
    router as register_user_router,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)
from pixel_battle.presentation.web.routes.view_chunk import (
    router as view_chunk_router,
)


@fixture
def routers() -> tuple[APIRouter, ...]:
    return (
        healthcheck_router,
        recolor_pixel_router,
        register_user_router,
        stream_chunk_router,
        view_chunk_router,
    )


@fixture
def app(container: AsyncContainer, routers: tuple[APIRouter, ...]) -> FastAPI:
    app = FastAPI()

    for router in routers:
        app.include_router(router)

    setup_dishka(container=container, app=app)

    return app


@fixture
def client(app: FastAPI) -> AsyncClient:
    transport = ASGIWebSocketTransport(app=app)

    return AsyncClient(transport=transport, base_url="http://localhost")
