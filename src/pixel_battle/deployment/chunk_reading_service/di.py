from dishka import Provider, Scope, make_async_container, provide

from pixel_battle.deployment.common.di import (
    AdapterProvider,
    InfrastructureProvider,
    InteractorProvider,
)
from pixel_battle.presentation.web.app import AppCoroutines, AppRouters
from pixel_battle.presentation.web.routes.view_chunk import (
    router as view_chunk_router,
)


class ChunkReadingServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> AppRouters:
        return [view_chunk_router]

    @provide
    def provide_coroutines(self) -> AppCoroutines:
        return []


chunk_reading_service_container = make_async_container(
    InfrastructureProvider(),
    AdapterProvider(),
    InteractorProvider(),
    ChunkReadingServiceProvider(),
)
