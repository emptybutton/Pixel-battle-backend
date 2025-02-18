
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient
from httpx_ws.transport import ASGIWebSocketTransport
from pytest import fixture

from pixel_battle.presentation.web.routers import all_routers


@fixture
def routers() -> tuple[APIRouter, ...]:
    return all_routers


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
