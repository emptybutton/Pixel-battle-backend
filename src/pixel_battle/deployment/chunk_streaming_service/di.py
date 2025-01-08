from typing import Iterable

from dishka import Provider, Scope, make_async_container, provide
from fastapi import APIRouter

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    InfrastructureProvider,
    InteractorProvider,
    StreamingProvider,
)
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)


class ChunkStreamingServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> Iterable[APIRouter]:
        return [stream_chunk_router]


chunk_streaming_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    StreamingProvider(),
    ChunkStreamingServiceProvider(),
)
