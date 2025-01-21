from collections.abc import AsyncIterator
from datetime import UTC, datetime
from functools import partial

from dishka import AsyncContainer, Provider, Scope, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient
from httpx_ws.transport import ASGIWebSocketTransport
from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import (
    RecolorPixel,
)
from pixel_battle.application.interactors.register_user import (
    RegisterUser,
)
from pixel_battle.application.interactors.view_chunk import (
    ViewChunk,
)
from pixel_battle.application.interactors.view_chunk_stream import (
    ViewChunkStream,
)
from pixel_battle.application.ports.chunk_view import DefaultChunkViewWhen
from pixel_battle.application.ports.chunk_views import ChunkViews
from pixel_battle.application.ports.clock import Clock
from pixel_battle.application.ports.pixel_queue import PixelQueue
from pixel_battle.application.ports.user_data_signing import UserDataSigning
from pixel_battle.entities.space.time import Time
from pixel_battle.infrastructure.adapters.chunk_view import (
    DefaultPNGImageChunkViewWhen,
    PNGImageChunkView,
)
from pixel_battle.infrastructure.adapters.chunk_views import (
    InMemoryChunkViews,
)
from pixel_battle.infrastructure.adapters.clock import StoppedClock
from pixel_battle.infrastructure.adapters.pixel_queue import InMemoryPixelQueue
from pixel_battle.infrastructure.adapters.user_data_signing import (
    UserDataSigningToHS256JWT,
)
from pixel_battle.presentation.web.routes.healthchek import (
    router as healthchek_router,
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
from pixel_battle.presentation.web.streaming import Streaming


@fixture
def routers() -> tuple[APIRouter, ...]:
    return (
        healthchek_router,
        recolor_pixel_router,
        register_user_router,
        stream_chunk_router,
        view_chunk_router,
    )


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
    provider.provide(lambda: InMemoryPixelQueue(), provides=PixelQueue)
    provider.provide(StoppedClock, provides=Clock)
    provider.provide(RecolorPixel[str])
    provider.provide(ViewChunk[PNGImageChunkView])
    provider.provide(ViewChunkStream)
    provider.provide(RegisterUser[str])

    @partial(provider.provide, provides=Streaming)
    async def get_streaming(
        view_chunk_stream: ViewChunkStream
    ) -> AsyncIterator[Streaming]:
        async with Streaming(view_chunk_stream=view_chunk_stream) as streaming:
            yield streaming

    return make_async_container(provider)


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
