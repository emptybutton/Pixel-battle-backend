
from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    InfrastructureProvider,
    InteractorProvider,
    StreamingProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.stream_chunk import (
    router as stream_chunk_router,
)


class ChunkStreamingServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return [stream_chunk_router]

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


chunk_streaming_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    StreamingProvider(),
    ChunkStreamingServiceProvider(),
)
