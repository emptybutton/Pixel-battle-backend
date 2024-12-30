from datetime import UTC, datetime
from typing import Any, AsyncIterator

from dishka import AsyncContainer, Provider, Scope, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from httpx import ASGITransport, AsyncClient
from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import (
    RecolorPixel,
)
from pixel_battle.application.interactors.view_chunk import (
    ViewChunk,
)
from pixel_battle.application.ports.broker import Broker
from pixel_battle.application.ports.chunk_view import DefaultChunkViewWhen
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.lock import Lock
from pixel_battle.application.ports.offsets import Offsets
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.space.time import Time
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultPNGImageChunkViewWhen,
    PNGImageChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_views import (
    InMemoryChunkViews,
)
from pixel_battle.infrastructure.adapters.clock import StoppedClock
from pixel_battle.infrastructure.adapters.lock import (
    FakeLock,
)
from pixel_battle.infrastructure.adapters.offsets import (
    InMemoryOffsets,
)
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.presentation.web.routes.recolor_pixel import router as router1
from pixel_battle.presentation.web.routes.stream_chunk import router as router2
from pixel_battle.presentation.web.routes.view_chunk import router as router3


@fixture
def routers() -> tuple[APIRouter, ...]:
    return router1, router2, router3


@fixture
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    provider.provide(
        lambda: Time(datetime=datetime(2006, 1, 1, tzinfo=UTC)),
        provides=Time,
    )
    provider.provide(
        lambda: UserDataSigningToHS256JWT(secret="super secret secret"),
        provides=UserDataSigning[str],
    )
    provider.provide(
        DefaultPNGImageChunkViewWhen,
        provides=DefaultChunkViewWhen[PNGImageChunkView],
    )
    provider.provide(
        lambda: InMemoryChunkViews(), provides=ChunkViews[PNGImageChunkView]
    )
    provider.provide(lambda: InMemoryOffsets(), provides=Offsets[int])
    provider.provide(lambda: InMemoryBroker(), provides=Broker)
    provider.provide(StoppedClock, provides=Clock)
    provider.provide(FakeLock, provides=Lock)
    provider.provide(RecolorPixel[str])
    provider.provide(
        ViewChunk[PNGImageChunkView, int],
        provides=ViewChunk[PNGImageChunkView, Any]
    )

    return make_async_container(provider)


@fixture
def app(container: AsyncContainer, routers: tuple[APIRouter, ...]) -> FastAPI:
    app = FastAPI()

    for router in routers:
        app.include_router(router)

    setup_dishka(container=container, app=app)

    return app


@fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    client_ = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    )

    async with client_:
        yield client_
